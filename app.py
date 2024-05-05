import streamlit as st
import dns.resolver

#MARK: - DNS Servers
DNS_SERVERS = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "Quad9": "9.9.9.9"
}

st.set_page_config(page_title="DNS-Toolbox", page_icon="🤖", layout="wide")

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

#MARK: - Home
def intro():
    st.write("# Welcome to the Demo of DNS-Toolbox")

    st.warning("This is a demo version of DNS-Toolbox. This is subject to change. The real application is not yet ready for prime time and will be delivered instead of this one in a few months time.")
    
    st.markdown(
    """
    This is a simple web application that demonstrates the use of DNS-Toolbox.
    The App is designed to allow for DNS queries to be made like MXToolbox.com.
    It can help you solve DNS problems, find out about your DNS records, and more.
    Another Demo will focus around the check of SSL certificates.
    
    For an broad overview use the M365 Check, if you are using Microsoft 365.
    
    The SSL Check will help you to check the SSL certificate of a webpage.
    
    Explanation of the DNS Records:
    - A and AAAA Records point you to an IP Address (mostly used for web pages)
    - CNAME Records point you to another domain (mostly used for web pages hosted by another service like GitHub Pages)
    - MX Records point you to a mail exchange server (used for mail servers)
    - NS Records point you to a nameserver (mostly used for mail servers, here you can find out who to ask for changes in the domain configuration, i.e. for DKIM configuration)
    - TXT Records point you to a text record (used for SPF and other authentication purposes)
    """
)

#MARK: - DNS Functions - A Record
def a_record():
    st.write("# A Record")
    st.markdown(
    """
    An A record maps a domain name to the IP address (Version 4) of the computer hosting the domain.
    With this demo you can check the A record of a (sub-)domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="a_record_domain")
    dns_server = st.selectbox("DNS Server", list(DNS_SERVERS.keys()), key="a_record_dns_server", ) or DNS_SERVERS["Cloudflare"]
    if st.button("Check", key="a_record_check"):
        with st.spinner("Checking..."):
            result = get_dns_record(domain or "", DNS_SERVERS.get(dns_server), "A")
            if len(result) == 1 and result[0].startswith("Error:"):
                st.error(result[0])
            else:
                for i, record in enumerate(result):
                    st.info(f"Record {i+1}: {record}")

#MARK: - DNS Functions - AAAA Record
def aaaa_record():
    st.write("# AAAA Record")
    st.markdown(
    """
    An AAAA record maps a domain name to the IP address (Version 6) of the computer hosting the domain.
    With this demo you can check the AAAA record of a (sub-)domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="a_record_domain")
    dns_server = st.selectbox("DNS Server", list(DNS_SERVERS.keys()), key="a_record_dns_server", ) or DNS_SERVERS["Cloudflare"]
    if st.button("Check", key="a_record_check"):
        with st.spinner("Checking..."):
            result = get_dns_record(domain or "", DNS_SERVERS.get(dns_server), "AAAA")
            if len(result) == 1 and result[0].startswith("Error:"):
                st.error(result[0])
            else:
                for i, record in enumerate(result):
                    st.info(f"Record {i+1}: {record}")

#MARK: - DNS Functions - CNAME Record
def cname_record():
    st.write("# CNAME Record")
    st.markdown(
    """
    A CNAME record maps a domain name to another domain name.
    With this demo you can check the CNAME record of a (sub-)domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="a_record_domain")
    dns_server = st.selectbox("DNS Server", list(DNS_SERVERS.keys()), key="a_record_dns_server", ) or DNS_SERVERS["Cloudflare"]
    if st.button("Check", key="a_record_check"):
        with st.spinner("Checking..."):
            result = get_dns_record(domain or "", DNS_SERVERS.get(dns_server), "CNAME")
            if len(result) == 1 and result[0].startswith("Error:"):
                st.error(result[0])
            else:
                for i, record in enumerate(result):
                    st.info(f"Record {i+1}: {record}")

#MARK: - DNS Functions - MX Record
def mx_record():
    st.write("# MX Record")
    st.markdown(
    """
    An MX record maps a domain name to a list of mail exchange servers for that domain.
    With this demo you can check the MX record of a (sub-)domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="a_record_domain")
    dns_server = st.selectbox("DNS Server", list(DNS_SERVERS.keys()), key="a_record_dns_server", ) or DNS_SERVERS["Cloudflare"]
    if st.button("Check", key="a_record_check"):
        with st.spinner("Checking..."):
            result = get_dns_record(domain or "", DNS_SERVERS.get(dns_server), "MX")
            if len(result) == 1 and result[0].startswith("Error:"):
                st.error(result[0])
            else:
                for i, record in enumerate(result):
                    st.info(f"Record {i+1}: {record}")

#MARK: - DNS Functions - NS Record
def ns_record():
    st.write("# NS Record")
    st.markdown(
    """
    An NS record maps a domain name to a list of name servers for that domain.
    With this demo you can check the NS record of a (sub-)domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="a_record_domain")
    dns_server = st.selectbox("DNS Server", list(DNS_SERVERS.keys()), key="a_record_dns_server", ) or DNS_SERVERS["Cloudflare"]
    if st.button("Check", key="a_record_check"):
        with st.spinner("Checking..."):
            result = get_dns_record(domain or "", DNS_SERVERS.get(dns_server), "NS")
            if len(result) == 1 and result[0].startswith("Error:"):
                st.error(result[0])
            else:
                for i, record in enumerate(result):
                    st.info(f"Record {i+1}: {record}")

#MARK: - DNS Functions - TXT Record
def txt_record():
    st.write("# TXT Record")
    st.markdown(
    """
    A TXT record maps a domain name to a list of text records.
    With this demo you can check the TXT record of a (sub-)domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="a_record_domain")
    dns_server = st.selectbox("DNS Server", list(DNS_SERVERS.keys()), key="a_record_dns_server", ) or DNS_SERVERS["Cloudflare"]
    if st.button("Check", key="a_record_check"):
        with st.spinner("Checking..."):
            result = get_dns_record(domain or "", DNS_SERVERS.get(dns_server), "TXT")
            if len(result) == 1 and result[0].startswith("Error:"):
                st.error(result[0])
            else:
                for i, record in enumerate(result):
                    st.info(f"Record {i+1}: {record}")


#MARK: - SSL Function
def ssl_check():
    import ssl
    import socket
    from datetime import datetime
    import certifi
    
    st.write("# SSL Check")
    st.markdown(
    """
    An SSL check is a test that checks the validity of the SSL certificate of a domain.
    With this demo you can check the SSL certificate of a domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="ssl_check_domain")
    if st.button("Check", key="ssl_check_check"):
        with st.spinner("Checking..."):
            try:
                context = ssl.create_default_context()
                context.load_verify_locations(certifi.where())
                with socket.create_connection((domain, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                    if cert is not None:
                        if 'notAfter' in cert:
                            not_after = cert['notAfter']
                            if isinstance(not_after, str):
                                expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                                remaining = expiry_date - datetime.now()
                                if remaining.days < 0:
                                    st.error("The certificate has expired.")
                                else:
                                    st.success(f"The certificate is valid for {remaining.days} days.")
                                st.info(f"Valid to: {not_after}")
                        st.divider()
                        with st.expander("Certificate Details", expanded=False):
                            if 'subject' in cert and cert['subject'] is not None:
                                for k, v in cert['subject'][0]:
                                    st.write(f"Subject: {v}")
                            if 'issuer' in cert and cert['issuer'] is not None:
                                for k, v in cert['issuer'][0]:
                                    st.write(f"Issuer: {v}")
                            if 'version' in cert:
                                st.write(f"Version: {cert['version']}")
                            if 'serialNumber' in cert:
                                st.write("Serial Number: ", cert['serialNumber'])
                            if 'notBefore' in cert:
                                st.write("Valid From: ", cert['notBefore'])
                            if 'notAfter' in cert:
                                st.write("Valid To: ", cert['notAfter'])
                            if 'subjectAltName' in cert and cert['subjectAltName'] is not None:
                                for item in cert['subjectAltName']:
                                    st.write(f"Subject Alt Name: {item[1]}")
                            if 'OCSP' in cert:
                                st.write(f"OCSP: ", cert['OCSP'])
                            if 'caIssuers' in cert:
                                st.write(f"CA Issuers: ", cert['caIssuers'])
            except Exception as e:
                    st.error(f"Error: {str(e)}")

#MARK: - M365 Function
def m365_check():
    st.write("# M365 Check")
    st.markdown(
    """
    An M365 check is a test that checks the validity of the M365 configuration of a domain.
    With this demo you can check the M365 configuration of a domain.
    This will check the following DNS-Records on all 3 DNS-Servers (Google, Cloudflare, Quad9):
    - MX Record for *.mail.protection.outlook.com
    - TXT Record containing spf.protection.outlook.com
    - TXT Record containing v=verifydomain MS=*
    - CNAME Records for:
        - autodiscover
        - lyncdiscover
        - selector1._domainkey
        - selector2._domainkey
    """
    )
    
    domain = st.text_input("Domain", "example.com", key="m365_check_domain")
    if st.button("Check", key="m365_check_check"):
        with st.spinner("Checking..."):
            st.divider()
            st.header("Status for DNS Configuration")
            dns_results = {}
            for dns_server_name, dns_server in DNS_SERVERS.items():
                dns_results[dns_server_name] = {
                    "MX": get_dns_record(domain, dns_server, "MX"),
                    "SPF": next((record for record in get_dns_record(domain, dns_server, "TXT") if "spf.protection.outlook.com" in record), None),
                    "VerifyDomain": next((record for record in get_dns_record(domain, dns_server, "TXT") if "v=verifydomain MS=" in record), None),
                    "autodiscover": get_dns_record(f"autodiscover.{domain}", dns_server, "CNAME"),
                    "lyncdiscover": get_dns_record(f"lyncdiscover.{domain}", dns_server, "CNAME"),
                    "selector1._domainkey": get_dns_record(f"selector1._domainkey.{domain}", dns_server, "CNAME"),
                    "selector2._domainkey": get_dns_record(f"selector2._domainkey.{domain}", dns_server, "CNAME")
                }
                
            # Check MX record status
            mx_status = []
            for dns_server_name in DNS_SERVERS.keys():
                mx_records = dns_results[dns_server_name]["MX"]
                if mx_records and not mx_records[0].startswith("Error:"):
                    mx_status.append(True)
                else:
                    mx_status.append(False)

            if all(mx_status):
                st.success("MX record verified.")
            elif any(mx_status):
                st.warning("MX record don't seem to be available worldwide.")
            else:
                st.error("MX record not found on any DNS server.")
                
            # Check SPF record status
            spf_status = []
            for dns_server_name in DNS_SERVERS.keys():
                spf_record = dns_results[dns_server_name]["SPF"]
                if spf_record:
                    spf_status.append(True)
                else:
                    spf_status.append(False)

            if all(spf_status):
                st.success("SPF record verified.")
            elif any(spf_status):
                st.warning("SPF records don't seem to be available worldwide.")
            else:
                st.error("SPF records not found on any DNS server.")

            # Check MS Domain verification record status
            ms_domain_verification_status = []
            for dns_server_name in DNS_SERVERS.keys():
                ms_domain_verification_record = dns_results[dns_server_name]["VerifyDomain"]
                if ms_domain_verification_record:
                    ms_domain_verification_status.append(True)
                else:
                    ms_domain_verification_status.append(False)

            if all(ms_domain_verification_status):
                st.success("Microsoft Domain verification record verified.")
            else:
                st.warning("Microsoft Domain verification record not verified. Check details down below!")

            # Check autodiscover CNAME record status
            autodiscover_status = []
            for dns_server_name in DNS_SERVERS.keys():
                autodiscover_record = dns_results[dns_server_name]["autodiscover"]
                if autodiscover_record and not autodiscover_record[0].startswith("Error:"):
                    autodiscover_status.append(True)
                else:
                    autodiscover_status.append(False)

            if all(autodiscover_status):
                st.success("autodiscover CNAME record verified.")
            elif any(autodiscover_status):
                st.warning("autodiscover CNAME record doesn't seem to be available worldwide.")
            else:
                st.error("autodiscover CNAME record not verified on any DNS server.")

            # Check lyncdiscover CNAME record status
            lyncdiscover_status = []
            for dns_server_name in DNS_SERVERS.keys():
                lyncdiscover_record = dns_results[dns_server_name]["lyncdiscover"]
                if lyncdiscover_record and not lyncdiscover_record[0].startswith("Error:"):
                    lyncdiscover_status.append(True)
                else:
                    lyncdiscover_status.append(False)

            if all(lyncdiscover_status):
                st.success("lyncdiscover CNAME record verified.")
            elif any(lyncdiscover_status):
                st.warning("lyncdiscover CNAME record doesn't seem to be available worldwide.")
            else:
                st.error("lyncdiscover CNAME record not verified on any DNS server.")
                
            # Check selector1._domainkey CNAME record status
            selector1_status = []
            for dns_server_name in DNS_SERVERS.keys():
                selector1_record = dns_results[dns_server_name]["selector1._domainkey"]
                if selector1_record and not selector1_record[0].startswith("Error:"):
                    selector1_status.append(True)
                else:
                    selector1_status.append(False)

            # Check selector2._domainkey CNAME record status
            selector2_status = []
            for dns_server_name in DNS_SERVERS.keys():
                selector2_record = dns_results[dns_server_name]["selector2._domainkey"]
                if selector2_record and not selector2_record[0].startswith("Error:"):
                    selector2_status.append(True)
                else:
                    selector2_status.append(False)

            if all(selector1_status) and all(selector2_status):
                st.success("DKIM is enabled.")
            elif any(selector1_status) and any(selector2_status):
                st.warning("DKIM CNAME records don't seem to be available worldwide.")
            else:
                st.error("DKIM is not enabled. Expect problems with email delivery.")

            # Check for discrepancies
            discrepancies = {}
            for record_type in ["MX", "SPF", "VerifyDomain", "autodiscover", "lyncdiscover", "selector1._domainkey", "selector2._domainkey"]:
                values = [dns_results[dns_server_name][record_type] for dns_server_name in DNS_SERVERS.keys()]
                if len(set(tuple(value) for value in values if value is not None)) > 1:
                    discrepancies[record_type] = values

            if discrepancies:
                st.error("Discrepancies found in DNS records across servers:")
                for record_type, values in discrepancies.items():
                    st.write(f"- {record_type}:")
                    for i, value in enumerate(values):
                        st.write(f"  - {list(DNS_SERVERS.keys())[i]}: {value}")
            else:
                st.success("All DNS records are consistent across all DNS servers.")

            st.divider()
            
            st.header("Details:")
            
            with st.expander("Show all details:"):
                for dns_server_name, dns_server_results in dns_results.items():
                    st.subheader(f"DNS Server: {dns_server_name}")

                    mx_records = dns_server_results["MX"]
                    if mx_records and not mx_records[0].startswith("Error:"):
                        valid_mx_records = [record.split()[-1] for record in mx_records if record.split()[-1].endswith("mail.protection.outlook.com.")]
                        if valid_mx_records:
                            st.success(f"MX Record: {', '.join(valid_mx_records)}")
                        else:
                            st.error("MX Record: No valid records found")
                    else:
                        st.error(f"MX Record: {mx_records[0] if mx_records else 'No records found'}")

                    spf_record = dns_server_results["SPF"]
                    if spf_record:
                        st.success(f"SPF TXT Record: {spf_record}")
                    else:
                        st.error("SPF TXT Record: Not found")

                    verify_domain_record = dns_server_results["VerifyDomain"]
                    if verify_domain_record:
                        st.success(f"Microsoft Domain verification TXT Record: {verify_domain_record}")
                    else:
                        st.warning("Microsoft Domain verification TXT Record: Not found")

                    for record_name in ["autodiscover", "lyncdiscover", "selector1._domainkey", "selector2._domainkey"]:
                        record_value = dns_server_results[record_name]
                        if record_value and not record_value[0].startswith("Error:"):
                            st.success(f"{record_name} CNAME Record: {', '.join(record_value)}")
                        else:
                            st.error(f"{record_name} CNAME Record: {record_value[0] if record_value else 'No records found'}")

#MARK: - Pages List
page_names_to_funcs = {
    "-": intro,
    "M365 Check": m365_check,
    "A Record": a_record,
    "AAAA Record": aaaa_record,
    "CNAME Record": cname_record,
    "MX Record": mx_record,
    "NS Record": ns_record,
    "TXT Record": txt_record,
    "SSL Check": ssl_check,
}


#MARK: - Sidebar
go_dnstoolbox = st.sidebar.selectbox("Choose a function", list(page_names_to_funcs.keys()))
go_dnstoolbox = go_dnstoolbox or "-"  # Assign a default value if go_dnstoolbox is None
page_names_to_funcs[go_dnstoolbox]()