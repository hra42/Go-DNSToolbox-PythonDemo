import app as st

#MARK: - Home
def intro():
    import app as st

    st.write("# Welcome to the Demo of DNS-Toolbox")

    st.markdown(
    """
    This is a simple web application that demonstrates the use of DNS-Toolbox.
    The App is designed to allow for DNS queries to be made like MXToolbox.com.
    It can help you solve DNS problems, find out about your DNS records, and more.
    Another Demo will focus around the check of SSL certificates.

    You can find a desktop version of this application on my GitHub page:
    [DNS-Toolbox](https://github.com/hra42/Go-DNS)
    """
)

#MARK: - DNS Functions - A Record
def a_record():
    import app as st

    st.write("# A Record")
    st.markdown(
    """
    An A record maps a domain name to the IP address (Version 4) of the computer hosting the domain.
    With this demo you can check the A record of a (sub-)domain.
    """
)

#MARK: - DNS Functions - AAAA Record
def aaaa_record():
    import app as st

    st.write("# AAAA Record")
    st.markdown(
    """
    An AAAA record maps a domain name to the IP address (Version 6) of the computer hosting the domain.
    With this demo you can check the AAAA record of a (sub-)domain.
    """
)

#MARK: - DNS Functions - CNAME Record
def cname_record():
    import app as st

    st.write("# CNAME Record")
    st.markdown(
    """
    A CNAME record maps a domain name to another domain name.
    With this demo you can check the CNAME record of a (sub-)domain.
    """
)

#MARK: - DNS Functions - MX Record
def mx_record():
    import app as st

    st.write("# MX Record")
    st.markdown(
    """
    An MX record maps a domain name to a list of mail exchange servers for that domain.
    With this demo you can check the MX record of a (sub-)domain.
    """
)

#MARK: - DNS Functions - NS Record
def ns_record():
    import app as st

    st.write("# NS Record")
    st.markdown(
    """
    An NS record maps a domain name to a list of name servers for that domain.
    With this demo you can check the NS record of a (sub-)domain.
    """
)

#MARK: - DNS Functions - TXT Record
def txt_record():
    import app as st

    st.write("# TXT Record")
    st.markdown(
    """
    A TXT record maps a domain name to a list of text records.
    With this demo you can check the TXT record of a (sub-)domain.
    """
)

#MARK: - SSL Function
def ssl_check():
    import app as st

    st.write("# SSL Check")
    st.markdown(
    """
    An SSL check is a test that checks the validity of the SSL certificate of a domain.
    With this demo you can check the SSL certificate of a domain.
    """
)

#MARK: - M365 Function
def m365_check():
    import app as st
    
    st.write("# M365 Check")
    st.markdown(
    """
    An M365 check is a test that checks the validity of the M365 configuration of a domain.
    With this demo you can check the M365 configuration of a domain.
    """
)

#MARK: - Pages List
page_names_to_funcs = {
    "-": intro,
    "A Record": a_record,
    "AAAA Record": aaaa_record,
    "CNAME Record": cname_record,
    "MX Record": mx_record,
    "NS Record": ns_record,
    "TXT Record": txt_record,
    "SSL Check": ssl_check,
    "M365 Check": m365_check
}


#MARK: - Sidebar
go_dnstoolbox = st.sidebar.selectbox("Choose a function", list(page_names_to_funcs.keys()))
page_names_to_funcs[go_dnstoolbox]()