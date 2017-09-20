# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: utils/attribute
@brief: list of attribute related functions
@requires: math
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'


# python
import math

# maya
from maya import cmds
import pymel.core as pm


def connect_construction_history(connector=None, nodes=[]):
    """Retrieve and connect construction history of specified nodes or all.

    :param connector: Control which switches ihi attr of connected node
    :type connector: str

    :param nodes: Nodes to connect their isHistoricallyInteresting attr
    :type nodes: list of maya dg and dag nodes

    :return pyNode of the connector storing the showHistory attribute
    """

    if not nodes:
        nodes = pm.ls()
    else:
        nodes = [pm.PyNode(node) for node in nodes]

    if not connector:
        if not pm.objExists('ConstructionHistory'):
            connector = pm.createNode('transform', n='ConstructionHistory')
        else:
            connector = pm.PyNode('ConstructionHistory')
    else:
        connector = pm.PyNode(connector)

    if not pm.objExists('%s.showHistory' % connector):
        connector.addAttr('showHistory', at='short', min=0, max=1)
        connector.showHistory.set(e=True, cb=True)

    print nodes
    for node in nodes:
        if not pm.isConnected(connector.showHistory, node.ihi):
            connector.showHistory >> node.ihi
    return connector
