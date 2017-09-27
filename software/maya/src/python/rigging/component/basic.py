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
from rigging.utils import control, rsCameraUI, maya_math
reload(component)
reload(control)
reload(rsCameraUI)


class Basic(component.Component):
    """Simple basic component"""

    def __init__(self, mod, side, description):
        """Initialize Basic class component subclassing from Base Component"""
        super(Basic, self).__init__(mod, side, description)

        self.guide_srt = '%s_guide_srt' % self.name

    def guide(self):
        """Implement guide method"""
        self.guide_srt = pm.spaceLocator(n=self.guide_srt)
        self.guide_srt.setParent(self.guide_grp)
        scale = maya_math.get_bb_size(cmds.ls(type='mesh')) * 0.5
        self.guide_srt.getShape().localScale.set(scale, scale, scale)

    def puppet(self, with_joint=False, with_shake=False):
        """Implement rig method
        
        :param with_joint: create a joint and constraint the control properly
        :type with_joint: bool
        """
        self.guide_grp.v.set(0)
        self.ctrl = control.Control(self, self.guide_srt, 1, 1)
        if with_joint:
            jnt = pm.createNode('joint', n=self.guide_srt.replace('guide', 'jnt'),
                                p=self.ctrl.srt)
            jnt.setParent(self.deform_grp)
            pm.parentConstraint(self.ctrl.srt, jnt, mo=False)
        if with_shake:
            self.create_shake(self.ctrl)

    def create_shake(self, target):
        """Create the shake rig based on algorithms from rsCameraUI

        :param target: Specify the target object to add the shake to
        :type target: Control
        """
        ctrl_buffer = str(target.buffers[0])
        shaker = pm.PyNode(rsCameraUI.rsCameraUIShakeAdd(ctrl_buffer))
        shaker.getShape().v.set(0)
        for i in pm.listAttr(shaker, ud=True):
            if i == 'CameraShake':
                target.srt.addAttr('shake', at='short', min=0, max=0)
                target.srt.shake.set(cb=True, l=True)
                continue
            target.srt.addAttr(i, at='double', k=True)
            target.srt.attr(i).connect(shaker.attr(i))
            shaker.attr(i).set(l=True, k=False)

    def deform(self):
        """Implement deform method"""
