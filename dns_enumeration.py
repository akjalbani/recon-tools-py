import requests

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
    return subdomains
