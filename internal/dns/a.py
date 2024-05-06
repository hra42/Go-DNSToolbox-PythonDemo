import streamlit as st
from internal.dns.dns import get_dns_record, DNS_SERVERS

#MARK: - DNS Functions - A Record
def get_a_record():
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