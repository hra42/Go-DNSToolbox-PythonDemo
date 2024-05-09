import streamlit as st
from internal.dns.dns import get_dns_record, DNS_SERVERS

#MARK: - M365 Function
def invoke_m365_check():
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
