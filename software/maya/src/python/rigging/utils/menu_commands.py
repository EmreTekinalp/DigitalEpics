# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 17, 2017
@contact: e.tekinalp@icloud.com
@package: utils/menu_command
@brief: include menu commands to call
@requires: rigging.core.io
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# python
import json
import os
import sys

# maya
from maya import cmds
import pymel.core as pm

# third party modules
from rigging.core import io
reload(io)


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


def data_path():
    """Return the data directory of the rig build asset"""
    asset = pm.ls(type='mesh')[0].getParent(-1)
    return asset.data_path.get()


def save_guides():
    """Save the guide locators"""
    gd = list()
    for g in cmds.ls('guide'):
        if g:
            for i in cmds.listRelatives(g, ad=True, type='transform'):
                if i:
                    gd.append(i)
    if not gd:
        cmds.warning('Saving Guides: No guides in the scene!')
        return
    data = dict()
    for i in gd:
        data[i] = [cmds.xform(i, q=True, t=True, ws=False),
                   cmds.xform(i, q=True, ro=True, ws=False)]
    path = os.path.abspath(os.path.join(data_path(), 'guides.json'))
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print 'Saved guides under: %s' % path


def load_guides(path=None):
    """Load the guide locators"""
    if not path:
        path = io.join_path(data_path(), 'guides.json')
    with open(path) as json_file:
        data = json.load(json_file)
    for key, value in data.items():
        if not cmds.objExists(key):
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


def save_control_shapes():
    """Save the control shapes"""
    gd = [i.getParent() for g in pm.ls('control')
          for i in pm.listRelatives(g, ad=True, type='nurbsCurve')]
    if not gd:
        pm.warning('Saving Guides: No guides in the scene!')
        return
    data = dict()
    for i in gd:
        data[str(i)] = {str(cv): pm.xform(cv, q=True, t=True, ws=True)
                        for cv in pm.ls('%s.cv[*]' % i, fl=True)}
    path = os.path.abspath(os.path.join(data_path(), 'control.json'))
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print 'Saved control shapes under: %s' % path


def load_control_shapes(path=None):
    """Load the control shapes"""
    if not path:
        path = os.path.abspath(os.path.join(data_path(), 'control.json'))
    with open(path) as json_file:
        data = json.load(json_file)
    for d in data.values():
        for key, value in d.items():
            if not cmds.objExists(key):
                continue
            cmds.xform(key, t=value, ws=True)
    print 'Loaded control shapes from: %s' % path


def mirror_control_shapes():
    """Simple function to mirror all left/right control shapes"""
    sel = cmds.ls(sl=True)
    if not sel:
        sel = [i for g in cmds.ls('control') for i in cmds.listRelatives(g, c=True)]
    for i in sel:
        for cv in cmds.ls('%s.cv[*]' % i, fl=True):
            mirror = ''
            if '_L_' in cv:
                mirror = cv.replace('_L_', '_R_')
            elif '_R_' in cv:
                mirror = cv.replace('_R_', '_L_')
            else:
                continue
            pos = cmds.xform(cv, q=True, t=True, ws=True)
            cmds.xform(mirror, t=[pos[0] * -1.0, pos[1], pos[2]], ws=True)


def save_constraints():
    """Save all the constraints"""
    data = list()
    for i in pm.listRelatives('geo', ad=True, type='constraint'):
        nodes = list(set(k for k in i.listConnections()))
        constraint = [n for n in nodes if not n.type() == 'transform']
        data.append([str(nodes[1]), str(nodes[0]), str(nodes[-1].type())])
    path = os.path.abspath(os.path.join(data_path(), 'constraints.json'))
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print 'Saved constraints under: %s' % path


def load_constraints(path=None):
    """Load constraints files"""
    if not path:
        path = os.path.abspath(os.path.join(data_path(), 'constraints.json'))
    with open(path) as json_file:
        data = json.load(json_file)
    for d in data:
        if not cmds.objExists(d[0]) or not cmds.objExists(d[1]):
            continue
        if d[-1] == 'parentConstraint':
            cmds.parentConstraint(d[0], d[1], mo=True)
        elif d[-1] == 'pointConstraint':
            cmds.pointConstraint(d[0], d[1], mo=True)
        elif d[-1] == 'orientConstraint':
            cmds.orientConstraint(d[0], d[1], mo=True)
        elif d[-1] == 'scaleConstraint':
            cmds.scaleConstraint(d[0], d[1], mo=True)
    print 'Loaded constraints from: %s' % path


def asset_manager():
    """Open the asset manager from the modeling section"""
    from modeling.tool.asset_manager import main
    reload(main)
    main.main()


def rig_build_menu():
    """Generate a rig build menu"""
