import streamlit as st
import ssl
import socket
from datetime import datetime
import certifi

#MARK: - SSL Function
def ssl_check():    
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
                context = ssl.create_default_context()
                context.load_verify_locations(certifi.where())
                with socket.create_connection((domain, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
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
                        with st.expander("Certificate Details", expanded=False):
                            if 'subject' in cert and cert['subject'] is not None:
                                for k, v in cert['subject'][0]:
                                    st.write(f"Subject: {v}")
                            if 'issuer' in cert and cert['issuer'] is not None:
                                for k, v in cert['issuer'][0]:
                                    st.write(f"Issuer: {v}")
                            if 'version' in cert:
                                st.write(f"Version: {cert['version']}")
                            if 'serialNumber' in cert:
                                st.write("Serial Number: ", cert['serialNumber'])
                            if 'notBefore' in cert:
                                st.write("Valid From: ", cert['notBefore'])
                            if 'notAfter' in cert:
                                st.write("Valid To: ", cert['notAfter'])
                            if 'subjectAltName' in cert and cert['subjectAltName'] is not None:
                                for item in cert['subjectAltName']:
                                    st.write(f"Subject Alt Name: {item[1]}")
                            if 'OCSP' in cert:
                                st.write(f"OCSP: ", cert['OCSP'])
                            if 'caIssuers' in cert:
                                st.write(f"CA Issuers: ", cert['caIssuers'])
            except Exception as e:
                    st.error(f"Error: {str(e)}")