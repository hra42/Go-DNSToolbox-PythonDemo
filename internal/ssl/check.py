import streamlit as st
import ssl
import socket
from datetime import datetime
import certifi
import pandas as pd

def check_ssl_certificate(domain):
    """
    Check the SSL certificate of a given domain.
    
    Args:
        domain (str): The domain to check the SSL certificate for.
        
    Returns:
        dict: A dictionary containing the SSL certificate details if the certificate is valid, otherwise None.
    """
    try:
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.load_verify_locations(certifi.where())
        
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
        if cert is not None:
            return cert
        else:
            return None
        
    except ssl.SSLError as e:
        if "unknown protocol" in str(e) or "unsupported protocol" in str(e):
            raise Exception("The server does not support TLS 1.2 or TLS 1.3.")
        else:
            raise e
    except Exception as e:
        raise e

import pandas as pd
from datetime import datetime

def display_ssl_certificate_details(cert):
    """
    Display SSL certificate details in a prettier format using Streamlit.
    
    Args:
        cert (dict): A dictionary containing the SSL certificate details.
    """
    cert_details = []
    
    if 'subject' in cert and cert['subject'] is not None:
        subject = ", ".join([f"{v}" for k, v in cert['subject'][0]])
        cert_details.append(["Subject", subject])
        
    if 'issuer' in cert and cert['issuer'] is not None:
        issuer = ", ".join([f"{v}" for k, v in cert['issuer'][0]])
        cert_details.append(["Issuer", issuer])
        
    if 'version' in cert:
        cert_details.append(["Version", str(cert['version'])])
        
    if 'serialNumber' in cert:
        cert_details.append(["Serial Number", str(cert['serialNumber'])])
        
    if 'notBefore' in cert:
        not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        cert_details.append(["Valid From", not_before.strftime('%Y-%m-%d %H:%M:%S %Z')])
        
    if 'notAfter' in cert:
        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        cert_details.append(["Valid To", not_after.strftime('%Y-%m-%d %H:%M:%S %Z')])
        
    if 'subjectAltName' in cert and cert['subjectAltName'] is not None:
        subject_alt_names = ", ".join([item[1] for item in cert['subjectAltName']])
        cert_details.append(["Subject Alt Names", subject_alt_names])
        
    if 'OCSP' in cert:
        cert_details.append(["OCSP", cert['OCSP'][0]])
        
    if 'caIssuers' in cert:
        cert_details.append(["CA Issuers", cert['caIssuers'][0]])
        
    # Convert all values to strings
    cert_details = [[str(field), str(value)] for field, value in cert_details]
    
    # Convert the list to a DataFrame
    df = pd.DataFrame(cert_details, columns=['Field', 'Value'])
    # Display the DataFrame without the index using st.write
    st.write(df.set_index('Field'))

def invoke_ssl_check():
    st.write("# SSL Check")
    st.markdown(
    """
    An SSL check is a test that checks the validity of the SSL certificate of a domain.
    With this demo you can check the SSL certificate of a domain.
    """
    )
    domain = st.text_input("Domain", "example.com", key="ssl_check_domain")
    if st.button("Check", key="ssl_check_check"):
        with st.spinner("Checking..."):
            try:
                cert = check_ssl_certificate(domain)
                if cert is not None:
                    if 'notAfter' in cert:
                        not_after = cert['notAfter']
                        if isinstance(not_after, str):
                            expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                            remaining = expiry_date - datetime.now()
                            if remaining.days < 0:
                                st.error("The certificate has expired.")
                            else:
                                st.success(f"The certificate is valid for {remaining.days} days.")
                            st.info(f"Valid to: {not_after}")
                    
                    st.divider()
                    # Display the certificate details with a click on the button
                    with st.expander("Show Certificate Details"):
                        display_ssl_certificate_details(cert)
                else:
                    st.error("No SSL certificate found.")
            except Exception as e:
                st.error(f"Error: {str(e)}")