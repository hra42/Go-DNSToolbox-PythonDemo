import streamlit as st
from collections import defaultdict
from internal.dns.dns import get_dns_record, DNS_SERVERS

DESCRIPTION = """
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

def check_mx_record(domain, dns_server):
    """Check if the MX record for the domain is valid on the given DNS server."""
    return get_dns_record(domain, dns_server, "MX")

def check_spf_record(domain, dns_server):
    """Check if the SPF record for the domain exists on the given DNS server."""
    return next((record for record in get_dns_record(domain, dns_server, "TXT") if "spf.protection.outlook.com" in record), None)

def check_verify_domain_record(domain, dns_server):
    """Check if the Microsoft Domain Verification record for the domain exists on the given DNS server."""
    return next((record for record in get_dns_record(domain, dns_server, "TXT") if "v=verifydomain MS=" in record), None)

def check_cname_record(record_name, domain, dns_server):
    """Check if the CNAME record for the given record name exists on the given DNS server."""
    return get_dns_record(f"{record_name}.{domain}", dns_server, "CNAME")

def display_detailed_results(dns_results, domain):
    """Display detailed results for each DNS server."""
    for dns_server_name, dns_server_results in dns_results.items():
        st.subheader(f"DNS Server: {dns_server_name}")

        mx_records = dns_server_results["MX"]
        if mx_records:
            valid_mx_records = [record.split()[-1] for record in mx_records if record.split()[-1].endswith("mail.protection.outlook.com.")]
            st.success(f"MX Record: {', '.join(valid_mx_records)}") if valid_mx_records else st.error("MX Record: No valid records found")
        else:
            st.error("MX Record: No records found")

        spf_record = dns_server_results["SPF"]
        st.success(f"SPF TXT Record: {spf_record}") if spf_record else st.error("SPF TXT Record: Not found")

        verify_domain_record = dns_server_results["VerifyDomain"]
        st.success(f"Microsoft Domain verification TXT Record: {verify_domain_record}") if verify_domain_record else st.warning("Microsoft Domain verification TXT Record: Not found")

        for record_name in ["autodiscover", "lyncdiscover", "selector1._domainkey", "selector2._domainkey"]:
            record_value = dns_server_results[record_name]
            st.success(f"{record_name} CNAME Record: {', '.join(record_value)}") if record_value else st.error(f"{record_name} CNAME Record: No records found")

def check_record_status(dns_results, record_type):
    """Check the status of a specific DNS record type across all DNS servers."""
    record_status = [dns_results[dns_server_name][record_type] for dns_server_name in DNS_SERVERS.keys()]
    
    if all(record_status):
        st.success(f"{record_type} record verified.")
    elif any(record_status):
        st.warning(f"{record_type} record doesn't seem to be available worldwide.")
    else:
        st.error(f"{record_type} record not found on any DNS server.")

def check_discrepancies(dns_results, record_checks):
    """Check for discrepancies in DNS records across all DNS servers."""
    discrepancies = {}
    
    for record_type in record_checks.keys():
        record_values = {}
        unique_values = set()

        for dns_server_name in DNS_SERVERS.keys():
            record_value = dns_results[dns_server_name][record_type]
            # Handle None values by converting them to an empty tuple
            if record_value is None:
                record_value = ()
            elif isinstance(record_value, list):
                # Convert lists to tuples
                record_value = tuple(record_value)
            elif isinstance(record_value, str):
                # Keep strings as single-element tuples
                record_value = (record_value,)

            if record_value not in record_values:
                record_values[record_value] = [dns_server_name]
            else:
                record_values[record_value].append(dns_server_name)
            unique_values.add(record_value)
        
        # Collect discrepancies only if there are multiple unique values
        if len(unique_values) > 1:
            for value, servers in record_values.items():
                discrepancies.setdefault(record_type, {})[value] = servers
    
    # Report discrepancies
    if discrepancies:
        st.error("Discrepancies found in DNS records across servers:")
        for record_type, values in discrepancies.items():
            st.write(f"- {record_type}:")
            for value, servers in values.items():
                st.write(f"  - Value: {value}, Servers: {', '.join(servers)}")
    else:
        st.success("All DNS records are consistent across all DNS servers.")

def invoke_m365_check():
    """Perform an M365 check on a domain."""
    st.write("# M365 Check")
    st.markdown(DESCRIPTION)
    
    domain = st.text_input("Domain", "example.com", key="m365_check_domain")
    if st.button("Check", key="m365_check_check"):
        with st.spinner("Checking..."):
            st.divider()
            st.header("Status for DNS Configuration")
            
            record_checks = {
                "MX": check_mx_record,
                "SPF": check_spf_record,
                "VerifyDomain": check_verify_domain_record,
                "autodiscover": lambda domain, dns_server: check_cname_record("autodiscover", domain, dns_server),
                "lyncdiscover": lambda domain, dns_server: check_cname_record("lyncdiscover", domain, dns_server),
                "selector1._domainkey": lambda domain, dns_server: check_cname_record("selector1._domainkey", domain, dns_server),
                "selector2._domainkey": lambda domain, dns_server: check_cname_record("selector2._domainkey", domain, dns_server)
            }
            
            dns_results = defaultdict(dict)
            for dns_server_name, dns_server in DNS_SERVERS.items():
                for record_type, check_func in record_checks.items():
                    dns_results[dns_server_name][record_type] = check_func(domain, dns_server)
            
            for record_type in record_checks.keys():
                check_record_status(dns_results, record_type)
            
            check_discrepancies(dns_results, record_checks)
            
            st.divider()
            
            st.header("Details:")
            
            with st.expander("Show all details:"):
                display_detailed_results(dns_results, domain)
