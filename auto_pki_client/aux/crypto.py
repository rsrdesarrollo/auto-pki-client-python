from OpenSSL import crypto

def get_cert_info(cert_path):
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert_path, "r").read())
    return cert

def fingerprint(cert):
    return cert.digest("sha256").decode()


def export_to_pkcs12(cert_path,priv_key_path,cacert_path, passphrase):
    pkcs12 = crypto.PKCS12()

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert_path, 'r').read())
    cacert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cacert_path, 'r').read())
    priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(priv_key_path, 'r').read())

    pkcs12.set_ca_certificates([cacert])
    pkcs12.set_certificate(cert)
    pkcs12.set_privatekey(priv_key)

    return pkcs12.export(passphrase=passphrase)