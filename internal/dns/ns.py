import streamlit as st
from internal.dns.dns import get_dns_record, DNS_SERVERS

#MARK: - DNS Functions - NS Record
def get_ns_record():
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
