# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: component/basic
@brief: basic atom component
@requires: core.component; utils.control
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# maya
import pymel.core as pm

# third party modules
from rigging.core import component
from rigging.utils import control
reload(component)
reload(control)


class Basic(component.Component):
    """Simple atom component"""

    def __init__(self, mod, side, description):
        """Initialize Basic class component subclassing from Base Component"""
        super(Basic, self).__init__(mod, side, description)

    def guide(self):
        """Implement guide method"""
        self.guide_srt = pm.spaceLocator(n='%s_guide_srt' % self.name)
        self.guide_srt.setParent(self.guide_grp)

    def puppet(self):
        """Implement rig method"""
        self.ctrl = control.Control(self, self.guide_srt, 1)
        self.guide_grp.v.set(0)

    def deform(self):
        """Implement deform method"""
