# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: tool/components/wheel
@brief: wheel component
@requires: tool.components.component
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
reload(maya_math)


class Wheel(component.Component):
    """Simple atom component"""

    def __init__(self, mod, side, description):
        """Initialize Atom class component subclassing from Base Component"""
        super(Wheel, self).__init__(mod, side, description)

    def guide(self):
        """Implement the wheel guides using locators and various shapes.

        This guide consists of the following base elements:
        wheel rotation
        wheel bank in
        wheel bank out
        wheel rod in
        wheel rod out

        additional advanced elements:
        wheel steer base
        wheel steer tip
        tire ground deform
        """

        square = [[1, 0, 1], [-1, 0, 1], [-1, 0, -1], [1, 0, -1], [1, 0, 1]]
        self.guide_srt = pm.curve(d=1, point=square, n='%s_guide_srt' % self.name)
        self.guide_rotation = pm.circle(n='%s_rotation_guide_srt' % self.name, nr=[1, 0, 0])[0]
        self.guide_bank_in = pm.spaceLocator(n='%s_bankIn_guide_srt' % self.name)
        self.guide_bank_out = pm.spaceLocator(n='%s_bankOut_guide_srt' % self.name)
        self.guide_rod_in = pm.spaceLocator(n='%s_rodIn_guide_srt' % self.name)
        self.guide_rod_out = pm.spaceLocator(n='%s_rodOut_guide_srt' % self.name)

        # fixed position values
        self.guide_rotation.t.set(0, 4, 0)
        self.guide_bank_in.t.set(-1, 0, 0)
        self.guide_bank_out.t.set(1, 0, 0)
        self.guide_rod_in.t.set(-3, 4, 0)
        self.guide_rod_out.t.set(-1, 4, 0)

        # set scaling
        scale = maya_math.get_bb_size(cmds.ls(type='mesh')) * 0.3
        maya_math.scale_shape(self.guide_rotation, scale + scale)
        maya_math.scale_shape(self.guide_srt, scale + scale)
        self.guide_bank_in.getShape().localScale.set(scale, scale, scale)
        self.guide_bank_out.getShape().localScale.set(scale, scale, scale)
        self.guide_rod_in.getShape().localScale.set(scale, scale, scale)
        self.guide_rod_out.getShape().localScale.set(scale, scale, scale)

        # parent guides
        self.guide_srt.setParent(self.guide_grp)
        pm.parent(self.guide_rotation, self.guide_bank_in, self.guide_bank_out,
                  self.guide_rod_in, self.guide_rod_out, self.guide_srt)

    def puppet(self):
        """Implement rig method"""
        self.guide_grp.v.set(0)
        self.ctrl_rotation = control.Control(self, self.guide_rotation, 0)
        self.ctrl_bank_in = control.Control(self, self.guide_bank_in, 1, 1)
        self.ctrl_bank_out = control.Control(self, self.guide_bank_out, 1, 1)
        self.ctrl_rod_in = control.Control(self, self.guide_rod_in, 0)
        self.ctrl_rod_out = control.Control(self, self.guide_rod_out, 0)

        self.setup_bank()
        # self.setup_rod()
        self.plug()

    def setup_bank(self):
        """Using the existing bank controls create an attribute driven setup"""
        if not pm.objExists('%s.bankInOut' % self.ctrl_rotation):
            self.ctrl_rotation.srt.addAttr('bankInOut', at='float', dv=0, k=True,
                                       min=-25.0, max=25.0)
        cnd_in = pm.createNode('condition', n='%s_bankIn_dg' % self.name)
        cnd_out = pm.createNode('condition', n='%s_bankOut_dg' % self.name)
        self.ctrl_rotation.srt.bankInOut.connect(cnd_in.firstTerm)
        self.ctrl_rotation.srt.bankInOut.connect(cnd_in.colorIfTrueR)
        cnd_in.outColorR.connect(self.ctrl_bank_in.buffers[0].rz)
        cnd_in.operation.set(2)
        self.ctrl_rotation.srt.bankInOut.connect(cnd_out.firstTerm)
        self.ctrl_rotation.srt.bankInOut.connect(cnd_out.colorIfTrueR)
        cnd_out.outColorR.connect(self.ctrl_bank_out.buffers[0].rz)
        cnd_out.operation.set(4)

    def setup_rod(self):
        """Setup a a rod ik rig"""
        self.jnt_rod_in = pm.createNode('joint', n=self.guide_rotation)

    def plug(self):
        """Setup the plug and socket connection"""
        self.ctrl_rotation.hrc.setParent(self.ctrl_bank_in.srt)
        self.ctrl_bank_in.hrc.setParent(self.ctrl_bank_out.srt)

    def deform(self):
        """Implement deform method"""
