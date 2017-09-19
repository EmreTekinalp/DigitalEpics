# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 17, 2017
@contact: e.tekinalp@icloud.com
@package: utility/menu_command
@brief: include menu commands to call
@requires: utility.node
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'


# python
import os
import json

# maya
from maya import cmds


def scene_path():
    """Return the modeling path based on the project settings"""
    project_path = cmds.workspace(q=True, fn=True)
    return os.path.abspath(os.path.join(project_path, 'scenes'))


def save_model():
    """Save the asset model"""
    f = cmds.fileDialog2(dir=scene_path(), ds=2, fm=0)
    if f:
        cmds.file(rn=f[0])
        cmds.file(save=True)


def save_guides():
    """Save the guide locators"""
    gd = [i for g in cmds.ls('guide') for i in cmds.listRelatives(g, ad=True, type='transform')]
    if not gd:
        cmds.warning('Saving Guides: No guides in the scene!')
        return
    tmp_path = '/Users/emretekinalp/PycharmProjects/Public/src/python/assets/lamborghini/data/guides.json'
    data = dict()
    for i in gd:
        data[i] = [cmds.xform(i, q=True, t=True, ws=False),
                   cmds.xform(i, q=True, ro=True, ws=False)]
    with open(tmp_path, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print 'Saved guides under: %s' % tmp_path


def load_guides(path=None):
    """Load the guide locators"""
    if not path:
        path = '/Users/emretekinalp/PycharmProjects/Public/src/python/assets/lamborghini/data/guides.json'
    with open(path) as json_file:
        data = json.load(json_file)
    for key, value in data.items():
        if not cmds.objExists(key):
            cmds.warning('Loading Guides: %s does not exist! Skip...' % key)
            continue
        cmds.xform(key, t=value[0], ws=False)
        cmds.xform(key, ro=value[1], ws=False)
    print 'Loaded guides from: %s' % path


def mirror_guides():
    """Simple function to mirror all left/right guides + based on selection"""
    sel = cmds.ls(sl=True)
    if not sel:
        sel = [i for g in cmds.ls('guide') for i in cmds.listRelatives(g, c=True)]
    for i in sel:
        mirror = ''
        if '_L_' in i:
            mirror = i.replace('_L_', '_R_')
        elif '_R_' in i:
            mirror = i.replace('_R_', '_L_')
        else:
            continue
        pos = cmds.xform(i, q=True, t=True, ws=True)
        rot = cmds.xform(i, q=True, ro=True, ws=True)
        cmds.xform(mirror, t=[pos[0] * -1.0, pos[1], pos[2]], ws=True)
        cmds.xform(mirror, ro=[rot[0] * -1.0, rot[1] * -1.0, rot[2] * -1.0], ws=True)
