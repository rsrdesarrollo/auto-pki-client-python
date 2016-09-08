## auto-pki-client
### About
auto-pki-client is the python client for [auto-pki-server](https://github.com/rsrdesarrollo/auto-pki-server) project.
This project aims to find a simple way to manage automatic certificate enrollments for all your devices in a LAN.

### Install
```bash
sudo apt install python-setuptools python-pip python-dev libyaml-dev libffi-dev build-essential libssl-dev

```

### Status
This project is a PoC for a master thesis at _'Universidad Carlos III de Madrid'_.

### Help

```
usage: auto-pki-client [-h] [--serial-number SERIAL_NUMBER] [--config CONFIG]
                       [--re-discovery] [--wait-for-cert] [--verbose]
                       [--quiet] [--force]

Start Auto-PKI client

optional arguments:
  -h, --help            show this help message and exit
  --serial-number SERIAL_NUMBER, -s SERIAL_NUMBER
                        Serial number of device.
  --config CONFIG, -c CONFIG
                        Path to config file YAML.
  --re-discovery        Force to rediscover all services.
  --wait-for-cert       Wait for EST server to get the certificate
  --verbose, -v
  --quiet, -q
  --force, -f           Force to do any action
```
