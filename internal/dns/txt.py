import streamlit as st
from internal.dns.dns import get_dns_record, DNS_SERVERS

#MARK: - DNS Functions - TXT Record
def get_txt_record():
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