# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: rigging/core/interface
@brief: interface for the build file
@requires: rigging.core.io; rigging.utils.attribute; rigging.utils.menu_commands
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'


# python
from abc import abstractmethod
import os

# maya
from maya import cmds
import pymel.core as pm

# third party modules
from rigging.core import io
from rigging.utils import attribute
from rigging.utils import menu_commands
reload(attribute)
reload(io)
reload(menu_commands)

# CONSTANTS
ASSET = 0
GUIDE = 4
PUPPET = 7
EXTRAS = 8
FINAL = 9


class RigInterface(object):
    """Base interface for all the rigging build file subclasses"""

    def __init__(self, current_file=None, project=None):
        """Initialize RigInterface class"""
        self.current_file = current_file
        self.asset_name = os.path.basename(self.current_file).split('.')[0]
        # tmp solution for now
        self.project = project

    def run(self, stage=0):
        """build function to construct the rig setup"""
        self.load_asset()
        if stage > 0:
            self.set_asset_attributes()
        if stage > 1:
            self.register()
        if stage > 2:
            self.guide()
        if stage > 3:
            self.load_guides()
        if stage > 4:
            self.puppet()
        if stage > 5:
            self.load_control_shapes()
        if stage > 6:
            self.load_constraints()
        if stage > 7:
            self.extras()
        if stage > 8:
            self.finalize()

    def load_asset(self):
        """Load the latest model version of the asset into a new scene file"""
        workspace_path = cmds.workspace(q=True, fn=True)
        project_path = io.join_path(workspace_path, 'scenes', self.project)
        model_path = io.join_path(project_path, self.asset_name, 'modeling')
        latest_version = ''
        for f in os.listdir(model_path):
            latest_version = io.join_path(model_path, f)
        if not latest_version:
            raise ImportError('Could not find any scenes under %s' % model_path)
        cmds.file(new=True, f=True)
        cmds.file(latest_version, i=True, f=True)
        # create a geo display attribute
        if not cmds.objExists('%s.geoDisplay' % self.asset_name):
            cmds.addAttr(self.asset_name, ln='geoDisplay', at='enum', dv=2,
                         enumName='normal:template:reference', k=True)
            cmds.setAttr('geo.overrideEnabled', 1)
            cmds.connectAttr('%s.geoDisplay' % self.asset_name,
                             'geo.overrideDisplayType')

    def set_asset_attributes(self):
        """Setup asset attributes"""
        top_grp = pm.ls(type='mesh')
        if not top_grp:
            cmds.warning('RigInterface: Model scene is missing!')
            return
        top_grp = top_grp[0].getParent(-1)
        data = os.path.abspath(os.path.join(self.current_file,
                                            os.path.pardir, 'data'))
        if not pm.objExists('%s.data_path' % top_grp):
            top_grp.addAttr('data_path', dt='string')
            top_grp.data_path.set(data, l=True)

    @abstractmethod
    def register(self):
        """Implement function to register components"""

    @abstractmethod
    def guide(self):
        """Implement function to cretae guides of the component"""

    def load_guides(self):
        """Build and load guides which are joints"""
        menu_commands.load_guides()

    @abstractmethod
    def puppet(self):
        """Implement function to create puppet of the components"""

    def load_control_shapes(self):
        """Build and load control shapes"""
        menu_commands.load_control_shapes()

    def load_constraints(self):
        """Load the constraints"""
        menu_commands.load_constraints()

    @abstractmethod
    def extras(self):
        """Implement function to deal with extra functions for the rig setup"""

    def finalize(self):
        """prepare the rig to be ready for a publish"""
        attribute.connect_construction_history(self.asset_name)
