# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: tool/components/atom
@brief: basic atom component
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
from tool.components import component
reload(component)
from utility import control


class Atom(component.Component):
    """Simple atom component"""

    def __init__(self, mod, side, description):
        """Initialize Atom class component subclassing from Base Component"""
        super(Atom, self).__init__(mod, side, description)

        # vars
        self.guide_srt = None
        self.control_srt = None

    def guide(self):
        """Implement guide method"""
        self.guide_srt = pm.spaceLocator(n='%s_guide_srt' % self.name)
        self.guide_srt.setParent(self.guide_grp)

    def puppet(self):
        """Implement rig method"""
        self.ctrl = control.Control(self)
        pm.xform(self.ctrl.hrc, t=self.guide_srt.t, ws=True)
        pm.xform(self.ctrl.hrc, r=self.guide_srt.r, ws=True)

    def deform(self):
        """Implement deform method"""
