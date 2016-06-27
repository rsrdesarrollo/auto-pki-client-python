
def fingerprint(cert_path):
    from OpenSSL.crypto import load_certificate, FILETYPE_PEM

    cert_file_string = open(cert_path, "rb").read()
    cert = load_certificate(FILETYPE_PEM, cert_file_string)

    return cert.digest("sha1").decode()
