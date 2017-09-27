# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: component/basic
@brief: basic rig component
@requires: core.component; utils.control
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# maya
from maya import cmds
import pymel.core as pm

# third party modules
from rigging.core import component
from rigging.utils import control, maya_math
reload(component)
reload(control)


class Chain(component.Component):
    """Simple chain component"""

    def __init__(self, mod, side, description):
        """Initialize Chain class component subclassing from Base Component"""
        super(Chain, self).__init__(mod, side, description)

    def guide(self):
        """Implement guide method"""
        self.guide_base = pm.spaceLocator(n='%s_base_guide_srt' % self.name)
        self.guide_tip = pm.spaceLocator(n='%s_tip_guide_srt' % self.name)
        self.guide_tip.ty.set(1)
        pm.parent(self.guide_base, self.guide_tip, self.guide_grp)
        scale = maya_math.get_bb_size(cmds.ls(type='mesh')) * 0.5
        self.guide_base.getShape().localScale.set(scale, scale, scale)
        self.guide_tip.getShape().localScale.set(scale, scale, scale)


    def puppet(self):
        """Implement rig method"""
        self.guide_grp.v.set(0)
        self.ctrl_base = control.Control(self, self.guide_base, 1, 1)
        self.ctrl_tip = control.Control(self, self.guide_tip, 1, 1)

        self.setup_ik_chain()
        self.deform()

    def setup_ik_chain(self):
        """Create a simple ikSCsolver chain rig setup"""
        self.jnt_base = pm.createNode('joint', p=self.guide_base,
                                      n=self.guide_base.replace('guide', 'ik'))
        self.jnt_tip = pm.createNode('joint', p=self.guide_tip,
                                     n=self.guide_tip.replace('guide', 'ik'))
        self.jnt_tip.setParent(self.jnt_base)
        self.jnt_base.setParent(self.deform_grp)
        pm.parentConstraint(self.ctrl_base.srt, self.jnt_base, mo=True)
        self.ik_rod = pm.ikHandle(sj=self.jnt_base, ee=self.jnt_tip,
                                  n=self.jnt_base.replace('ik_srt', 'ikh'),
                                  solver='ikSCsolver')
        self.ik_rod[0].v.set(0)
        self.ik_rod[0].setParent(self.deform_grp)
        pm.pointConstraint(self.ctrl_tip.srt, self.ik_rod[0], mo=True)

    def deform(self):
        """Implement deform method"""
        self.deform_grp.v.set(0)
