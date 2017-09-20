# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@brief: Custom menu library called in userSetup.py
@requires: Nothing
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# python
import os

# maya
from maya import cmds
import pymel.core as pm


def digital_epics():
    """Run this function to create a custom menu for digital epics"""
    menu_name = 'Digital_Epics'
    # name of the global variable for the Maya window
    maya_window = pm.language.melGlobals['gMainWindow']

    if cmds.menu(menu_name, ex=True, p=maya_window):
        cmds.deleteUI(cmds.menu(menu_name, e=1, dai=1, vis=1))

    # build a menu and parent under the Maya Window
    custom_menu = pm.menu(menu_name, parent=maya_window)

    # modeling menu item
    pm.menuItem(d=True, dl='Modeling')
    pm.menuItem(label='save model', parent=custom_menu,
                command="from utility import menu_commands;"
                        "reload(menu_commands);menu_commands.save_model();")
    pm.menuItem(label='load model', parent=custom_menu,
                command="print 'Open model scene folder'")

    # rigging menu item
    pm.menuItem(d=True, dl='Rigging')
    pm.menuItem(label='save guides', parent=custom_menu,
                command="from rigging.utils import menu_commands;"
                        "reload(menu_commands);menu_commands.save_guides();")
    pm.menuItem(label='load guides', parent=custom_menu,
                command="print 'load guides'")
    pm.menuItem(label='mirror guides', parent=custom_menu,
                command="from rigging.utils import menu_commands;"
                        "reload(menu_commands);menu_commands.mirror_guides();")
    pm.menuItem(label='save control shapes', parent=custom_menu,
                command="from rigging.utils import menu_commands;"
                        "reload(menu_commands);menu_commands.save_control_shapes();")
    pm.menuItem(label='load control shapes', parent=custom_menu,
                command="from rigging.utils import menu_commands;"
                        "reload(menu_commands);menu_commands.load_control_shapes();")
    pm.menuItem(label='mirror control shapes', parent=custom_menu,
                command="from rigging.utils import menu_commands;"
                        "reload(menu_commands);menu_commands.mirror_control_shapes();")
    pm.menuItem(label='save constraints', parent=custom_menu,
                command="from rigging.utils import menu_commands;"
                        "reload(menu_commands);menu_commands.save_constraints();")
    pm.menuItem(label='load constraints', parent=custom_menu,
                command="from rigging.utils import menu_commands;"
                        "reload(menu_commands);menu_commands.load_constraints();")

    # animation menu item
    pm.menuItem(d=True, dl='Animation')
    pm.menuItem(label='save animation', parent=custom_menu,
                command="print 'Publish animation scene'")
    pm.menuItem(label='load animation', parent=custom_menu,
                command="print 'Open animation scene folder'")
