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
import pymel.core as pm
from maya import cmds

# third party modules
from rigging.utils import menu_commands
from rigging.component import basic, chain, motionpath, wheel
from rigging.core import interface
reload(basic)
reload(chain)
reload(interface)
reload(menu_commands)
reload(motionpath)
reload(wheel)


class Train(interface.RigInterface):
    """Build class for the transformer"""

    def __init__(self):
        """Initialize Transformer build file"""
        super(Train, self).__init__(inspect.getsourcefile(lambda: 0), 'infra_surf')

    def register(self):
        """Register components"""
        self.god = basic.Basic('god', 'C', 'main')

        self.front = chain.Chain('chain', 'C', 'frontWagon')
        self.mid = chain.Chain('chain', 'C', 'midWagon')
        self.back = chain.Chain('chain', 'C', 'backWagon')

        self.wheelBack = basic.Basic('wheel', 'C', 'back')
        self.wheelMidBack = basic.Basic('wheel', 'C', 'midBack')
        self.wheelMid = basic.Basic('wheel', 'C', 'mid')
        self.wheelFront = basic.Basic('wheel', 'C', 'front')

        self.wagonFront = motionpath.MotionPath('wagon', 'C', 'front', 'track_C_srf')
        self.wagonFrontMid = motionpath.MotionPath('wagon', 'C', 'frontMid', 'track_C_srf')
        self.wagonMid = motionpath.MotionPath('wagon', 'C', 'mid', 'track_C_srf')
        self.wagonBackMid = motionpath.MotionPath('wagon', 'C', 'backMid', 'track_C_srf')
        self.wagonBack = motionpath.MotionPath('wagon', 'C', 'back', 'track_C_srf')

    def guide(self):
        """Create the guides for the asset"""
        self.god.guide()
        self.front.guide()
        self.mid.guide()
        self.back.guide()

        self.wheelFront.guide()
        self.wheelMid.guide()
        self.wheelMidBack.guide()
        self.wheelBack.guide()

        self.wagonFront.guide()
        self.wagonFrontMid.guide()
        self.wagonMid.guide()
        self.wagonBackMid.guide()
        self.wagonBack.guide()

    def puppet(self):
        """Puppet method"""
        self.god.puppet()
        self.front.puppet()
        self.mid.puppet()
        self.back.puppet()

        # add paramU and paramV attrs to mid control
        if not pm.objExists('%s.paramU' % self.god.ctrl.srt):
            self.god.ctrl.srt.addAttr('paramU', at='float', k=True, min=0, max=100)
        if not pm.objExists('%s.paramV' % self.god.ctrl.srt):
            self.god.ctrl.srt.addAttr('paramV', at='float', k=True, min=0, max=100)

        self.wagonFront.puppet([self.god.ctrl.srt])
        self.wagonFrontMid.puppet([self.god.ctrl.srt])
        self.wagonMid.puppet([self.god.ctrl.srt])
        self.wagonBackMid.puppet([self.god.ctrl.srt])
        self.wagonBack.puppet([self.god.ctrl.srt])
        self.wheelFront.puppet()
        self.wheelMid.puppet()
        self.wheelMidBack.puppet()
        self.wheelBack.puppet()
        self.plug()
        self.extras()

    def plug(self):
        """plug the controls to their sockets"""
        self.mid.socket(self.god.ctrl.srt)
        self.front.socket(self.god.ctrl.srt)
        self.back.socket(self.god.ctrl.srt)
        self.wheelMid.socket(self.mid.ctrl_base.srt)
        self.wheelMidBack.socket(self.mid.ctrl_tip.srt)
        self.wheelFront.socket(self.front.ctrl_tip.srt)
        self.wheelBack.socket(self.back.ctrl_tip.srt)
        # constraint the basis of the ik chains to the mid ctrl
        pm.parentConstraint(self.back.ctrl_base.srt, self.mid.ctrl_tip.hrc, mo=True)
        pm.parentConstraint(self.front.ctrl_base.srt, self.mid.ctrl_base.hrc, mo=True)

    def extras(self):
        """Add additional features or functionality"""
        self.wagonFront.ctrl.srt.paramU.set(24)
        self.wagonFrontMid.ctrl.srt.paramU.set(16.6)
        self.wagonMid.ctrl.srt.paramU.set(12)
        self.wagonBackMid.ctrl.srt.paramU.set(7.4)
        self.wagonBack.ctrl.srt.paramU.set(0)

        self.wagonFront.ctrl.srt.paramV.set(50)
        self.wagonFrontMid.ctrl.srt.paramV.set(50)
        self.wagonMid.ctrl.srt.paramV.set(50)
        self.wagonBackMid.ctrl.srt.paramV.set(50)
        self.wagonBack.ctrl.srt.paramV.set(50)

        # setup skinweights
        if not cmds.objExists('balgenSkincluster'):
            pm.skinCluster(self.back.jnt_base, self.mid.jnt_base, 'Lint_41_Wagen1_Teile_Balgen', tsb=True, n='balgenSkincluster')
            pm.setAttr('Lint_41_Wagen1_Teile_Balgen.inheritsTransform', 0)
        if not cmds.objExists('balgenSkincluster2'):
            pm.skinCluster(self.mid.jnt_base, self.front.jnt_base, 'Lint_41_Wagen1_Teile_Balgen_geo', tsb=True, n='balgenSkincluster2')
            pm.setAttr('Lint_41_Wagen1_Teile_Balgen_geo.inheritsTransform', 0)

    def add_on_in_maya(self):
        from maya import cmds

        cmds.parentConstraint('wagon_C_mid_guide_srt', 'god_C_main_ctrl_hrc',
                              mo=False)
        cmds.setAttr('god_C_main_buffer0_hrc.r', -90, 0, 180)
        cmds.parentConstraint('wagon_C_back_guide_srt',
                              'chain_C_backWagon_tip_buffer0_hrc', mo=True)
        cmds.parentConstraint('wagon_C_backMid_guide_srt',
                              'chain_C_backWagon_base_buffer0_hrc', mo=True)
        cmds.parentConstraint('wagon_C_frontMid_guide_srt',
                              'chain_C_frontWagon_base_buffer0_hrc', mo=True)
        cmds.parentConstraint('wagon_C_front_guide_srt',
                              'chain_C_frontWagon_tip_buffer0_hrc', mo=True)


asset = Train()
asset.run(interface.FINAL)
