# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: assets/lamborghini
@brief: build file for the lamborghini
@requires: utility.node; tool.component
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# python
import inspect
import json
import os

# maya
from maya import cmds

# third party modules
from utility import menu_commands
from tool.components import atom, wheel
reload(menu_commands)
reload(atom)
reload(wheel)


class Lamborghini(object):
    """Build class for the transformer"""

    def __init__(self):
        """Initialize Transformer build file"""
        self.asset_name = None

    def run(self, stage=0):
        """Build the transformer"""
        self.load_asset()
        self.register()
        self.guides()
        self.load_guides()
        self.puppet()

    def load_asset(self):
        """Load the latest model version of the asset into a new scene file"""
        project_path = cmds.workspace(q=True, fn=True)
        current_file = os.path.abspath(inspect.getsourcefile(lambda: 0))
        scene_path = os.path.abspath(os.path.join(project_path, 'scenes'))
        asset_name = os.path.splitext(os.path.basename(current_file))[0]
        asset_path = os.path.abspath(os.path.join(scene_path, asset_name))
        model_path = os.path.abspath(os.path.join(asset_path, 'modeling'))
        latest_version = ''
        for f in os.listdir(model_path):
            if f.startswith(asset_name):
                latest_version = os.path.abspath(os.path.join(model_path, f))
        if not latest_version:
            raise ImportError('Could not find model version -> %s' % asset_name)
        cmds.file(new=True, f=True)
        cmds.file(latest_version, i=True, f=True)
        self.asset_name = asset_name
        # create a geo display attribute
        if not cmds.objExists('%s.geoDisplay' % self.asset_name):
            cmds.addAttr(self.asset_name, ln='geoDisplay', at='enum', dv=2,
                         enumName='normal:template:reference', k=True)
            cmds.setAttr('geo.overrideEnabled', 1)
            cmds.connectAttr('%s.geoDisplay' % self.asset_name,
                             'geo.overrideDisplayType')

    def register(self):
        """Register components"""
        # components
        self.god = atom.Atom('god', 'C', 'main')
        self.body = atom.Atom('vehicle', 'C', 'body')

        self.chassy_front = atom.Atom('chassy', 'C', 'front')
        self.chassy_mid = atom.Atom('chassy', 'C', 'mid')
        self.chassy_rear = atom.Atom('chassy', 'C', 'rear')
        self.chassy_left = atom.Atom('chassy', 'L', 'bank')
        self.chassy_right = atom.Atom('chassy', 'R', 'bank')

        self.wheel_lf = wheel.Wheel('wheel', 'L', 'front')
        self.wheel_rf = wheel.Wheel('wheel', 'R', 'front')
        self.wheel_lr = wheel.Wheel('wheel', 'L', 'rear')
        self.wheel_rr = wheel.Wheel('wheel', 'R', 'rear')

    def guides(self):
        """Create the guides for the asset"""
        self.god.guide()
        self.body.guide()

        self.chassy_front.guide()
        self.chassy_mid.guide()
        self.chassy_rear.guide()
        self.chassy_left.guide()
        self.chassy_right.guide()

        self.wheel_lf.guide()
        self.wheel_rf.guide()
        self.wheel_lr.guide()
        self.wheel_rr.guide()

    def load_guides(self):
        """Build and load guides which are joints"""
        path = os.path.abspath(os.path.join(inspect.getsourcefile(lambda: 0),
                                            os.path.pardir, 'data', 'guides.json'))
        menu_commands.load_guides(path)

    def puppet(self):
        """Puppet method"""
        self.wheel_lr.puppet()
        self.wheel_rr.puppet()

asset = Lamborghini()
asset.run()
