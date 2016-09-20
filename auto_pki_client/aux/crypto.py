from OpenSSL import crypto
from OpenSSL.crypto import X509Req, X509
import hashlib

def get_cert_info(cert_path):
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert_path, "r").read())
    return cert

def get_csr_info(csr_path):
    csr_obj = crypto.load_certificate_request(crypto.FILETYPE_PEM, open(csr_path, "r").read())
    return csr_obj

def fingerprint(cert):
    if isinstance(cert, X509):
        return cert.digest("sha1").decode()
    elif isinstance(cert, X509Req):
        req = cert
        pub_key = req.get_pubkey()
        data = "".join(crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key).split("\n")[1:-2])
        digest = hashlib.sha1(data).hexdigest()

        return ':'.join(a+b for a,b in zip(digest[::2], digest[1::2]))


def export_to_pkcs12(cert_path,priv_key_path,cacert_path, passphrase):
    pkcs12 = crypto.PKCS12()

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert_path, 'r').read())
    cacert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cacert_path, 'r').read())
    priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(priv_key_path, 'r').read())

    pkcs12.set_ca_certificates([cacert])
    pkcs12.set_certificate(cert)
    pkcs12.set_privatekey(priv_key)

    return pkcs12.export(passphrase=passphrase)