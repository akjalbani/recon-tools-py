#!/usr/bin/env python3

import argparse
import dns.resolver
import requests
import subprocess
from bs4 import BeautifulSoup

def dns_enumeration(domain):
    records = ['A', 'AAAA', 'MX', 'NS', 'SOA', 'TXT']
    dns_info = {}
    for record in records:
        try:
            answers = dns.resolver.resolve(domain, record)
            dns_info[record] = [answer.to_text() for answer in answers]
        except Exception:
            dns_info[record] = []
    return dns_info

def subdomain_enumeration(domain, wordlist):
    subdomains = []
    with open(wordlist, 'r') as file:
        for line in file:
            subdomain = line.strip() + '.' + domain
            url = 'http://' + subdomain
            try:
                response = requests.get(url, timeout=3)
                if response.status_code < 400:
                    subdomains.append(subdomain)
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.RequestException:
                pass
    return subdomains

def run_theHarvester(domain):
    command = ['theHarvester', '-d', domain, '-l', '500', '-b', 'bing']
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.stdout.decode()

def parse_theHarvester_output(output):
    lines = output.split('\n')
    hosts = []
    for i, line in enumerate(lines):
        if 'Hosts found:' in line:
            index = i + 1
            while index < len(lines) and lines[index].strip() != '':
                hosts.append(lines[index].strip())
                index += 1
            break
    return hosts

def save_results(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(item + '\n')

def vulnerability_checks(subdomains):
    vulnerabilities = {}
    for subdomain in subdomains:
        url = 'http://' + subdomain
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else ''
            if 'Index of /' in title:
                vulnerabilities[subdomain] = 'Directory Listing Enabled'
            elif 'Test Page for' in title or 'Welcome to' in title:
                vulnerabilities[subdomain] = 'Default Page Detected'
        except requests.exceptions.RequestException:
            pass
    return vulnerabilities

def main():
    parser = argparse.ArgumentParser(description='Automate Reconnaissance Tasks')
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('-w', '--wordlist', default='subdomains.txt', help='Subdomain wordlist')
    args = parser.parse_args()

    domain = args.domain
    wordlist = args.wordlist

    print(f"[*] Starting DNS Enumeration for {domain}")
    dns_info = dns_enumeration(domain)
    save_results('dns_info.txt', [f"{key}: {', '.join(value)}" for key, value in dns_info.items()])
    print("[+] DNS information saved to dns_info.txt")

    print(f"[*] Starting Subdomain Enumeration for {domain}")
    subdomains = subdomain_enumeration(domain, wordlist)
    save_results('subdomains_found.txt', subdomains)
    print(f"[+] Found {len(subdomains)} subdomains. Results saved to subdomains_found.txt")

    print(f"[*] Running theHarvester for {domain}")
    harvester_output = run_theHarvester(domain)
    harvester_hosts = parse_theHarvester_output(harvester_output)
    save_results('theHarvester_hosts.txt', harvester_hosts)
    print("[+] theHarvester results saved to theHarvester_hosts.txt")

    print("[*] Performing Vulnerability Checks")
    vulnerabilities = vulnerability_checks(subdomains)
    save_results('vulnerabilities.txt', [f"{k}: {v}" for k, v in vulnerabilities.items()])
    print("[+] Vulnerability scan results saved to vulnerabilities.txt")

if __name__ == "__main__":
    main()
