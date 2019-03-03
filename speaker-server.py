#!/usr/bin/env python
"""Starts the media server

Usage:
  speaker-server.py <config_file>
"""

import asyncio
import json
import logging
import sys

from docopt import docopt
import hypercorn.asyncio
import hypercorn.config
import netifaces
from quart import Quart

from service_discovery.discovery_constants import DISCOVERY_TYPES
from service_discovery.discovery_server import start_discovery_server


def start_webserver(loop, ip_address):
    app = Quart(__name__)

    @app.route('/')
    async def hello():
        return 'hello'

    bind_address = "{}:9943".format(ip_address)
    print("Binding to {}".format(bind_address))
    config = hypercorn.config.Config.from_mapping({
        "bind": [bind_address]
    })
    loop.create_task(hypercorn.asyncio.serve(app, config))

    return "http://{}".format(bind_address)


def start_servers(loop, ip_address, discovery_network):
    web_url = start_webserver(loop, ip_address)
    start_discovery_server(
        loop, ip_address, discovery_network,
        DISCOVERY_TYPES.SPEAKER, web_url
    )


def main(ip_address, discovery_network):
    loop = asyncio.get_event_loop()
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO
    )

    start_servers(loop, ip_address, discovery_network)

    loop.run_forever()
    loop.close()


def get_discovery_info(configfile):
    with open(configfile, "r") as f:
        config = json.loads(f.read())

    if config["network_interface"] not in netifaces.interfaces():
        print("Unknown interface {}.  Pick one of {}".format(config["network_interface"], netifaces.interfaces()))
        sys.exit(-1)
    ip_address = netifaces.ifaddresses(config["network_interface"])[netifaces.AF_INET][0]["addr"]
    discovery_network = config["discovery_network"]
    return ip_address, discovery_network


if __name__ == "__main__":
    print("a")
    arguments = docopt(__doc__)
    config_file = arguments["<config_file>"]
    ip_address, discovery_network = get_discovery_info(config_file)
    main(ip_address, discovery_network)
