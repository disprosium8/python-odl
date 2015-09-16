#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#          - Beraldo Leal <beraldo AT ncc DOT unesp DOT br>
#
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import json
import sys
import requests

from odl.flow import ODLFlow
from odl.node import ODLNode
from odl.table import ODLTable

class ODLInstance(object):
    def __init__(self, server, credentials):
        self.server = server
        self.credentials = credentials
        self.headers = { 'Content-type' : 'application/json' }

    def get_inventory_nodes(self):
        endpoint = "/restconf/operational/opendaylight-inventory:nodes/"

        try:
            response = requests.get(self.server + endpoint,
                                    headers=self.headers,
                                    auth=self.credentials)
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

        # Consider any status other than 2xx an error
        if not response.status_code // 100 == 2:
            print "Error: Unexpected response", format(response)
            sys.exit(2)

        return json.loads(response.text)

    def get_nodes(self):
        inventory = self.get_inventory_nodes()
        nodes = inventory['nodes']['node']
        result = {}
        for node in nodes:
            obj = ODLNode(node, self)
            result[obj.id] = obj
        return result

    def get_node_by_id(self, id):
        nodes = self.get_nodes()
        try:
            return nodes[id]
        except KeyError:
            return None

    def get_connector_by_id(self, id):
        nodes = self.get_nodes()
        for node in nodes.values():
            connector = node.get_connector_by_id(id)
            if connector and connector.id == id:
                return connector
        return None