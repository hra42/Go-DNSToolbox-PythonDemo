import streamlit as st
from internal.intro import intro
from internal.dns.a import get_a_record
from internal.dns.aaaa import get_aaaa_record
from internal.dns.cname import cname_record
from internal.dns.mx import mx_record
from internal.dns.ns import ns_record
from internal.dns.txt import txt_record
from internal.ssl.check import ssl_check
from internal.m365.check import m365_check

st.set_page_config(page_title="DNS-Toolbox", page_icon="🤖", layout="wide")

#MARK: - Pages List
page_names_to_funcs = {
    "-": intro,
    "M365 Check": m365_check,
    "A Record": get_a_record,
    "AAAA Record": get_aaaa_record,
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