#!/usr/bin/env python3
from requests import request
from bs4 import BeautifulSoup
import unittest
import os
import argparse

DOMAIN = "qgis.demo"
SERVER_PATH = "qgisserver"
PROJECT_PATH = f"{os.getcwd()}/test.qgz"


class CapabilityTest(unittest.TestCase):
    def setUp(self):
        self.req = request(
            "GET",
            f"http://{DOMAIN}/{SERVER_PATH}?SERVICE=WMS&MAP={PROJECT_PATH}&REQUEST=GetCapabilities",
        )
        self.capability = BeautifulSoup(self.req.content, "xml").find("Capability")

    def test_capability(self):
        self.assertEqual(self.req.status_code, 200)
        self.assertIsNotNone(self.capability)
        self.assertIsNotNone(self.capability.find("GetMap"))
        self.assertIsNotNone(self.capability.find("GetFeatureInfo"))

        layer = self.capability.find("Layer")
        self.assertIsNotNone(layer)

        crs = layer.find_all("CRS")
        self.assertIsNotNone(crs)

        layer = layer.find("Layer")
        self.assertIsNotNone(layer.find("EX_GeographicBoundingBox"))
        self.assertIsNotNone(layer.find("BoundingBox"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("EcoGis Tests")
    parser.add_argument("--DOMAIN", type=str, default=DOMAIN)
    parser.add_argument("--SERVERPATH", type=str, default=SERVER_PATH)
    parser.add_argument("--PROJECTPATH", type=str, default=PROJECT_PATH)

    args = parser.parse_args()

    DOMAIN = args.DOMAIN
    SERVER_PATH = args.SERVERPATH
    PROJECT_PATH = args.PROJECTPATH

    unittest.main()
