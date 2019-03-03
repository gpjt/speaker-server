import logging

import hypercorn.asyncio
import hypercorn.config
from quart import Quart
from quart.json import jsonify


app = Quart(__name__)

@app.route('/')
async def playlist():
    return jsonify([])


def start_webserver(loop, ip_address):
    bind_address = "{}:9943".format(ip_address)
    logging.info("Binding to {}".format(bind_address))
    config = hypercorn.config.Config.from_mapping({
        "bind": [bind_address]
    })
    loop.create_task(hypercorn.asyncio.serve(app, config))

    return "http://{}".format(bind_address)
