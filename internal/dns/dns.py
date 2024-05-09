import dns.resolver

#MARK: - DNS Servers
DNS_SERVERS = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "Quad9": "9.9.9.9"
}

#MARK: - DNS Function
def get_dns_record(domain, dns_server, type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    try:
        answers = resolver.resolve(domain, type)
        return [str(rdata) for rset in answers.response.answer for rdata in rset]
    except dns.resolver.NoAnswer:
        return ["Error: No answer from the DNS server for the requested domain and record type."]
    except dns.resolver.NXDOMAIN:
        return ["Error: The requested domain does not exist."]
    except dns.resolver.NoNameservers:
        return ["Error: No nameservers are available to fulfill the request."]
    except dns.resolver.Timeout:
        return ["Error: The DNS request timed out."]