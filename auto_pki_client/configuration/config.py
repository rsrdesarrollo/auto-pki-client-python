import yaml


class Config(dict):
    config_file = None

    def __init__(self, config_file):
        self.config_file = config_file

        try:
            with open(self.config_file, 'r') as f:
                dict.__init__(self, yaml.load(f))
        except (OSError) as ex:
            with open(self.config_file, 'w'):
                pass
            dict.__init__(self, {
                'client':{
                    'certs_dir':'./certs/',
                    'password': 'bootstrap',
                    'username': 'bootstrap'
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