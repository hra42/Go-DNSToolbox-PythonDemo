import streamlit as st
from internal.intro import get_intro
from internal.dns.a import get_a_record
from internal.dns.aaaa import get_aaaa_record
from internal.dns.cname import get_cname_record
from internal.dns.mx import get_mx_record
from internal.dns.ns import get_ns_record
from internal.dns.txt import get_txt_record
from internal.ssl.check import invoke_ssl_check
from internal.m365.check import invoke_m365_check

st.set_page_config(page_title="DNS-Toolbox", page_icon="🤖", layout="wide")

#MARK: - Pages List
page_names_to_funcs = {
    "-": get_intro,
    "M365 Check": invoke_m365_check,
    "A Record": get_a_record,
    "AAAA Record": get_aaaa_record,
    "CNAME Record": get_cname_record,
    "MX Record": get_mx_record,
    "NS Record": get_ns_record,
    "TXT Record": get_txt_record,
    "SSL Check": invoke_ssl_check,
}


#MARK: - Sidebar
go_dnstoolbox = st.sidebar.selectbox("Choose a function", list(page_names_to_funcs.keys()))
go_dnstoolbox = go_dnstoolbox or "-"  # Assign a default value if go_dnstoolbox is None
page_names_to_funcs[go_dnstoolbox]()