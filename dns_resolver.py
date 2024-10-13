import dns.resolver

def dns_enumeration(domain):
    records = ['A', 'AAAA', 'MX', 'NS', 'SOA', 'TXT']
    dns_info = {}
    for record in records:
        try:
            answers = dns.resolver.resolve(domain, record)
            dns_info[record] = [answer.to_text() for answer in answers]
        except Exception as e:
            dns_info[record] = []
    return dns_info
