# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: component/motionpath
@brief: motionpath along a surface
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
from rigging.utils import control
reload(component)
reload(control)


class MotionPath(component.Component):
    """Create a MotionPath along a given surface"""

    def __init__(self, mod, side, description, surface):
        """Initialize MotionPath class"""
        super(MotionPath,  self).__init__(mod, side, description)

        # args
        self.surface = surface

        # vars
        self.guide_srt = '%s_guide_srt' % self.name
        self.surface_loc = '%s_onSurface_srt' % self.name
        self.posi = '%s_surfaceSlide_dg' % self.name

    def guide(self):
        """Define the amount and position of the on surface controls"""
        if not pm.objExists(self.surface):
            pm.warning('MotionPath: surface does not exist - %s' % self.surface)
            return
        self.surface = pm.PyNode(self.surface)
        self.guide_srt = pm.spaceLocator(n=self.guide_srt)
        self.guide_srt.setParent(self.guide_grp)
        pos = pm.createNode('pointOnSurfaceInfo', n=self.posi)
        rot = pm.createNode('rotateHelper', n='%s_calcOrientation_dg' % self.name)
        dcm = pm.createNode('decomposeMatrix', n='%s_rotateMatrix_dg' % self.name)
        self.surface.getShape().worldSpace.connect(pos.inputSurface)
        pos.position.connect(self.guide_srt.t)
        pos.normal.connect(rot.forward)
        pos.tangentU.connect(rot.up)
        rot.rotateMatrix.connect(dcm.inputMatrix)
        dcm.outputRotate.connect(self.guide_srt.r)
        self.posi = pos

    def puppet(self, multislider=None):
        """Using the guide locator create a control setup on top
        
        :param multislider: several slider controls to add on top of parameters
        :type multislider: list of pyNodes with paramU and paramV attributes
        """
        self.ctrl = control.Control(self, self.guide_srt, 1)
        pm.parentConstraint(self.guide_srt, self.ctrl.hrc, mo=False)
        # add param slider attributes
        self.ctrl.srt.addAttr('paramU', at='float', k=True, min=0, max=100)
        self.ctrl.srt.addAttr('paramV', at='float', k=True, min=0, max=100)
        pma = pm.createNode('plusMinusAverage', n='%s_addMultiSlider_dg' % self.name)
        rmv_u = pm.createNode('remapValue', n='%s_limitFromZeroToOneU_dg' % self.name)
        rmv_v = pm.createNode('remapValue', n='%s_limitFromZeroToOneV_dg' % self.name)

        self.ctrl.srt.paramU.connect(pma.input2D[0].input2Dx)
        self.ctrl.srt.paramV.connect(pma.input2D[0].input2Dy)

        if multislider:
            for i, slider in enumerate(multislider):
                slider.paramU.connect(pma.input2D[i + 1].input2Dx)
                slider.paramV.connect(pma.input2D[i + 1].input2Dy)

        pma.output2Dx.connect(rmv_u.inputValue)
        pma.output2Dy.connect(rmv_v.inputValue)

        rmv_u.inputMax.set(100)
        rmv_v.inputMax.set(100)

        rmv_u.outValue.connect(self.posi.parameterU)
        rmv_v.outValue.connect(self.posi.parameterV)
        self.guide_grp.v.set(0)
        self.deform()

    def deform(self):
        """Deform method"""
        self.deform_grp.v.set(0)
