import streamlit as st

def intro():
    import streamlit as st
    
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
    
page_names_to_funcs = {
    "-": intro
}

demo_name = st.sidebar.selectbox("Choose a function", list(page_names_to_funcs.keys()))
page_names_to_funcs[demo_name]()