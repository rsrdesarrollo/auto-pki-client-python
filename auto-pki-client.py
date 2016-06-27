import os
import argparse
import sys
import logging
import socket
from time import sleep

from est.client import Client
from est.errors import TryLater, RequestError

from auto_pki.configuration.config import Config
from auto_pki.aux.crypto import fingerprint
from auto_pki.aux.discovery import get_est_services

parser = argparse.ArgumentParser(
    description="Start Auto-PKI client"
)
parser.add_argument(
    '--config', '-c',
    help="Path to config file YAML.",
    default="./config/config.yaml",
    type=str
)
parser.add_argument(
    '--re-discovery',
    help="Force to rediscover all services.",
    action='store_true'
)
parser.add_argument(
    '--wait-for-cert',
    help="Wait for EST server to get the certificate",
    action='store_true'
)
parser.add_argument(
    '--verbose', '-v',
    default= 0,
    action='count'
)
parser.add_argument(
    '--quiet', '-q',
    action='store_true'
)
args = parser.parse_args(sys.argv[1:])

args.verbose += (0,1)[not args.quiet]
if args.verbose > 3:
    args.verbose = 3

log_level = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)[args.verbose]
logging.basicConfig(level=log_level)
logging.getLogger('zeroconf').setLevel(log_level)
logging.getLogger('request').setLevel(log_level)

log = logging.getLogger('auto-pki-client')
log.setLevel(log_level)
log.addHandler(logging.StreamHandler(sys.stdout))


def discovery_est(conf):
    services = get_est_services()
    for service in services:
        log.info("Found EST Service %s on %s:%d ", service.server, service.address, service.port)

    if len(services) == 0:
        log.error("No EST Service found in .local domain")
        sys.exit(1)

    service = services[0]

    log.info("Configuring EST Service %s:%d", service.server, service.port)
    srv_cfg['host'] = service.server
    srv_cfg['port'] = service.port


with Config(args.config) as conf:
    common_name = socket.getfqdn()

    cli_cfg = conf['client']
    srv_cfg = conf['server']

    csr_path = os.path.join(cli_cfg['certs_dir'], common_name+'.csr')
    cert_path = os.path.join(cli_cfg['certs_dir'], common_name+'.pem')
    priv_path = os.path.join(cli_cfg['certs_dir'], common_name+'.key.pem')

    if os.path.isfile(cert_path) and os.path.isfile(priv_path):
        log.error("Skip generate Client Cert. Certificate already present in %s", cert_path)
        sys.exit()

    try:
        os.mkdir(cli_cfg['certs_dir'])
        log.info("Certificate's directory created on %s", cli_cfg['certs_dir'])
    except (OSError) as e:
        pass

    cacert_path = os.path.join(cli_cfg['certs_dir'], srv_cfg['cacert'])
    cacert = (False, cacert_path)[os.path.isfile(cacert_path)]

    if args.re_discovery:
        discovery_est(conf)

    try:
        host = srv_cfg['host']
        port = srv_cfg['port']
    except (KeyError) as ex:
        discovery_est(conf)
        host = srv_cfg['host']
        port = srv_cfg['port']

    client = Client(host, port, cacert)

    if not cacert:
        log.debug("Cacert is not present. Initial bootstraping.")
        cacert_str = client.cacerts()
        log.debug("Received cacert %s", cacert_str)
        with open(cacert_path, 'w') as cacert_file:
            cacert_file.write(cacert_str)
            log.debug("cacert writed to file %s", cacert_path)

        log.warn("Adding CA. Fingerprint: %s", fingerprint(cacert_path))

        client = Client(host, port, cacert)

    username = cli_cfg['username']
    password = cli_cfg['password']

    client.set_basic_auth(username, password)

    if os.path.isfile(csr_path):
        log.info("Found previous CSR in %s", csr_path)
        try:
            with open(csr_path, 'r') as cert_file:
                csr = cert_file.read()
        except (OSError) as ex:
            log.error("Failed to read CSR file from %s. ERROR: %s", csr_path, ex.message)
            sys.exit(1)
    else:
        # Create CSR and get private key used to sign the CSR.
        common_name = socket.getfqdn()
        priv, csr = client.create_csr(common_name, subject_alt_name=b"DNS:serialnumber._serial.vendor.com")

        try:
            with open(csr_path, 'w') as cert_file:
                cert_file.write(csr)
        except (OSError) as ex:
            log.error("Failed to write CSR file to %s. ERROR: %s", csr_path, ex.message)
            sys.exit(2)

        try:
            with open(priv_path, 'w') as cert_file:
                cert_file.write(priv)
        except (OSError) as ex:
            log.error("Failed to write Private Key file to %s. ERROR: %s", priv_path, ex.message)
            sys.exit(3)


    done = False
    while not done:
        try:
            client_cert = client.simpleenroll(csr)
            done = True

            with open(cert_path, 'w') as cert_file:
                cert_file.write(client_cert)
        except (TryLater) as ex:
            if not args.wait_for_cert:
                break

            log.info("Waiting for cert %d seconds.", ex.seconds)
            sleep(ex.seconds)
        except (RequestError) as ex:
            log.error("Request error to EST simple enroll service. ERROR: %s", ex.message)
        except (OSError) as ex:
            log.error("Failed to write Certificate file to %s. ERROR: %s", cert_path, ex.message)
            sys.exit(4)
