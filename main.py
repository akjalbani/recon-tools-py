#!/usr/bin/env python3

import argparse
import dns.resolver
import requests
import subprocess
from bs4 import BeautifulSoup

# Functions from previous sections go here...

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
    save_results('subdomains.txt', subdomains)
    print(f"[+] Found {len(subdomains)} subdomains. Results saved to subdomains.txt")

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
