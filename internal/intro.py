import streamlit as st

#MARK: - Home
def get_intro():
    st.write("# Welcome to the Demo of DNS-Toolbox")

    st.warning("This is a demo version of DNS-Toolbox. This is subject to change. The real application is not yet ready for prime time and will be delivered instead of this one in a few months time.")
    
    st.markdown(
    """
    This is a simple web application that demonstrates the use of DNS-Toolbox. The app is designed to allow for DNS queries similar to MXToolbox.com. It can help you solve DNS problems, find out about your DNS records, and more. Another demo will focus on checking SSL certificates.

    ### Features

    - **M365 Check**: For a broad overview if you are using Microsoft 365.
    - **SSL Check**: Helps you check the SSL certificate of a webpage.

    ### Explanation of DNS Records

    - **A and AAAA Records**: Point to an IP address (mostly used for web pages).
    - **CNAME Records**: Point to another domain (mostly used for web pages hosted by another service like GitHub Pages).
    - **MX Records**: Point to a mail exchange server (used for mail servers).
    - **NS Records**: Point to a nameserver (mostly used for mail servers, useful for finding out who to ask for changes in the domain configuration, e.g., for DKIM configuration).
    - **TXT Records**: Point to a text record (used for SPF and other authentication purposes).
    """
)