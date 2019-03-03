import json
import logging
import os
import requests
import subprocess
import tempfile
import time
import unittest
import uuid

from service_discovery.discovery_constants import DISCOVERY_TYPES
from service_discovery.discover import discover_services


class Test_1_POST_song_data_creates_playlist_with_posted_data(unittest.TestCase):

    def setUp(self):
        # First we start up a speaker server
        discovery_network = str(uuid.uuid4())
        _, self.config_filename = tempfile.mkstemp()
        with open(self.config_filename, "w") as f:
            f.write(json.dumps({
                "discovery_network": discovery_network,
                "network_interface": "lo",
            }))
        server_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "speaker_server.py")
        self.subprocess = subprocess.Popen(["python", server_file, self.config_filename])

        # The discovery network stuff uses the logging module, so we'll configure it
        logging.basicConfig(
            format="%(asctime)s %(levelname)s: %(message)s",
            level=logging.INFO
        )

        # Now wait until something appears on our naned discovery network and says it's a speaker
        for retry in range(5):
            time.sleep(1)
            services = discover_services(discovery_network)
            if DISCOVERY_TYPES.SPEAKER in services and len(services[DISCOVERY_TYPES.SPEAKER]) == 1:
                self.service_descriptor = services[DISCOVERY_TYPES.SPEAKER][0]
                break
        else:
            self.fail("Could not find a speaker server after starting one")


    def tearDown(self):
        self.subprocess.kill()
        self.subprocess.wait()
        os.remove(self.config_filename)


    def test_functionality(self):
        response = requests.get(self.service_descriptor["web_url"])
        assert response.status_code == 200

        data = response.json()

