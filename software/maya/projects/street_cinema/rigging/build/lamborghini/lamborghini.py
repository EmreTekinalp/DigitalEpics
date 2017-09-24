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
@requires: utils.menu_command; component.basic; component.wheel; core.interface
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# python
import inspect

# maya
from maya import cmds

# third party modules
from rigging.utils import menu_commands
from rigging.component import basic, chain, wheel
from rigging.core import interface
reload(basic)
reload(chain)
reload(interface)
reload(menu_commands)
reload(wheel)


class Lamborghini(interface.RigInterface):
    """Build class for the transformer"""

    def __init__(self):
        """Initialize Transformer build file"""
        super(Lamborghini, self).__init__(inspect.getsourcefile(lambda: 0),
                                          'street_cinema_intro')

    def register(self):
        """Register components"""
        self.god = basic.Basic('god', 'C', 'main')
        self.body = basic.Basic('vehicle', 'C', 'body')

        self.chassy_front = basic.Basic('chassy', 'C', 'front')
        self.chassy_mid = basic.Basic('chassy', 'C', 'mid')
        self.chassy_rear = basic.Basic('chassy', 'C', 'rear')
        self.chassy_left = basic.Basic('chassy', 'L', 'bank')
        self.chassy_right = basic.Basic('chassy', 'R', 'bank')

        self.wheel_lf = wheel.Wheel('wheel', 'L', 'front')
        self.wheel_rf = wheel.Wheel('wheel', 'R', 'front')
        self.wheel_lr = wheel.Wheel('wheel', 'L', 'rear')
        self.wheel_rr = wheel.Wheel('wheel', 'R', 'rear')

        self.rod_lf = chain.Chain('rod', 'L', 'front')
        self.rod_rf = chain.Chain('rod', 'R', 'front')
        self.rod_lr = chain.Chain('rod', 'L', 'rear')
        self.rod_rr = chain.Chain('rod', 'R', 'rear')

    def guide(self):
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

        self.rod_lf.guide()
        self.rod_rf.guide()
        self.rod_lr.guide()
        self.rod_rr.guide()

    def puppet(self):
        """Puppet method"""
        self.god.puppet()
        self.body.puppet()

        self.chassy_front.puppet()
        self.chassy_mid.puppet()
        self.chassy_rear.puppet()
        self.chassy_left.puppet()
        self.chassy_right.puppet()

        self.wheel_lf.puppet()
        self.wheel_rf.puppet()
        self.wheel_lr.puppet()
        self.wheel_rr.puppet()

        self.rod_lf.puppet()
        self.rod_rf.puppet()
        self.rod_lr.puppet()
        self.rod_rr.puppet()

        self.plug()

    def plug(self):
        """plug the controls to their sockets"""
        self.body.socket(self.god.ctrl.srt)
        self.chassy_front.socket(self.body.ctrl.srt)
        self.chassy_rear.socket(self.chassy_front.ctrl.srt)
        self.chassy_left.socket(self.chassy_rear.ctrl.srt)
        self.chassy_right.socket(self.chassy_left.ctrl.srt)
        self.chassy_mid.socket(self.chassy_right.ctrl.srt)
        self.wheel_lf.socket(self.chassy_rear.ctrl.srt)
        self.wheel_rf.socket(self.chassy_rear.ctrl.srt)
        self.wheel_lr.socket(self.chassy_rear.ctrl.srt)
        self.wheel_rr.socket(self.chassy_rear.ctrl.srt)
        self.rod_lf.socket(self.chassy_rear.ctrl.srt)
        self.rod_rf.socket(self.chassy_rear.ctrl.srt)
        self.rod_lr.socket(self.chassy_rear.ctrl.srt)
        self.rod_rr.socket(self.chassy_rear.ctrl.srt)

asset = Lamborghini()
asset.run(interface.FINAL)
