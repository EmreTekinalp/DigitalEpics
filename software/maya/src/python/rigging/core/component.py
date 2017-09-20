# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: core/component
@brief: base rig component interface
@requires: Nothing
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# python
from abc import abstractmethod

# maya
from maya import cmds
import pymel.core as pm


class Component(object):
    """Base rig component class providing the foundation for rig modules"""

    def __init__(self, mod, side, description):
        """Initialize Component class.

        :param mod: mod of the component
        :type mod: str

        :param side: side of the component
        :type side: str

        :param description: descriptive part of the component
        :type description: str
        """
        # args
        self.mod = mod
        self.side = side
        self.description = description
        # vars
        self.asset = pm.ls(type='transform')[0].getParent(-1)
        self.rig_grp = 'rig'
        self.name = '%s_%s_%s' % (self.mod, self.side, self.description)
        self.comp_grp = '%s_comp' % self.name
        self.input_grp = 'input'
        self.output_grp = 'output'
        self.guide_grp = 'guide'
        self.deform_grp = 'deform'
        self.control_grp = 'control'
        # methods
        self.setup_structure()

    def setup_structure(self):
        """Setup the rig structure hierarchy"""
        if not cmds.objExists(self.rig_grp):
            self.rig_grp = pm.createNode('transform', n=self.rig_grp, p=self.asset)
        if not cmds.objExists(self.comp_grp):
            self.comp_grp = pm.createNode('transform', n=self.comp_grp, p=self.rig_grp)
            self.input_grp = pm.createNode('transform', n=self.input_grp, p=self.comp_grp)
            self.output_grp = pm.createNode('transform', n=self.output_grp, p=self.comp_grp)
            self.guide_grp = pm.createNode('transform', n=self.guide_grp, p=self.comp_grp)
            self.deform_grp = pm.createNode('transform', n=self.deform_grp, p=self.comp_grp)
            self.control_grp = pm.createNode('transform', n=self.control_grp, p=self.comp_grp)

    @abstractmethod
    def guide(self):
        """guide method which needs to be implemented for subclasses"""

    @abstractmethod
    def puppet(self):
        """rig method which needs to be implemented for subclasses"""

    @abstractmethod
    def deform(self):
        """deform method which needs to be implemented for subclasses"""

    def socket(self, plug, mode='parentConstraint'):
        """given a transform node, constraint to this objects comp_grp
        
        :param mode: define which constraint type is desired
        :type mode: str
        """
        if mode == 'parentConstraint':
            pm.parentConstraint(plug, self.comp_grp, mo=True)
        elif mode == 'pointConstraint':
            pm.pointConstraint(plug, self.comp_grp, mo=True)
        elif mode == 'orientConstraint':
            pm.orientConstraint(plug, self.comp_grp, mo=True)
        pm.scaleConstraint(plug, self.comp_grp, mo=True)
