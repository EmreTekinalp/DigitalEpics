# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: utils/maya_math
@brief: math functions used in maya
@requires: math
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# python
import math

# maya
from maya import cmds
import pymel.core as pm


def get_bb_size(meshes):
    """Based on the meshes calculate the boundingBox to return a float number"""
    bbox = cmds.exactWorldBoundingBox(meshes)
    mult = 0.5
    center = [(bbox[3] + bbox[0]) * mult,
              (bbox[4] + bbox[1]) * mult,
              (bbox[5] + bbox[2]) * mult]
    vec = [bbox[3] - center[0], bbox[4] - center[1], bbox[5] - center[2]]
    mag = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
    return mag * 0.25


def scale_shape(shape, size):
    """Scale the cvs of a nurbsCurve away from the center of the transform"""
    cvs = pm.ls('%s.cv[*]' % shape, fl=True)
    for cv in cvs:
        cv_pos = pm.xform(cv, q=True, t=True, ws=True)
        center = pm.xform(shape, q=True, t=True, ws=True)
        scaled_diff = [(cv_pos[0] - center[0]) * size,
                       (cv_pos[1] - center[1]) * size,
                       (cv_pos[2] - center[2]) * size]
        pm.xform(cv, t=[scaled_diff[0] + cv_pos[0],
                        scaled_diff[1] + cv_pos[1],
                        scaled_diff[2] + cv_pos[2]], ws=True)
