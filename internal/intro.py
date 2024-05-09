import streamlit as st

#MARK: - Home
def get_intro():
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