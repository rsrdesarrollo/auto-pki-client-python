import yaml
import os
import logging
import string
import random

def password_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

log = logging.getLogger('auto_pki_client')

class Config(dict):
    config_file = None

    def __init__(self, config_file):
        self.config_file = config_file
        conf_dirname = os.path.dirname(config_file)
        try:
            with open(self.config_file, 'r') as f:
                dict.__init__(self, yaml.load(f))
        except (IOError, OSError) as ex:
            try:
                os.makedirs(conf_dirname)
                log.info("Configuration directory created on %s", conf_dirname)
            except (IOError, OSError) as e:
                pass

            with open(self.config_file, 'w'):
                pass
            dict.__init__(self, {
                'client':{
                    'certs_dir':'./certs/',
                    'password': 'bootstrap',
                    'username': 'bootstrap',
                    'export_key': password_generator(size=20)
                },
                'server': {
                    'cacert': 'cacert.pem'
                }
            })

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.config_file, 'w') as outfile:
            outfile.write(yaml.dump(dict(self), default_flow_style=False))