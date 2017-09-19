# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 17, 2017
@contact: e.tekinalp@icloud.com
@package: utility/control
@brief: foundation for control rigs
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'


# maya
import pymel.core as pm


class Control(object):
    """Rig control objects based on nurbsCurves"""

    def __init__(self, component=None, guide=None, shape=0, name=None, offset=0):
        """Initialize Control class

        :param component: Component object if accessible
        :type component: Component

        :param guide: guide object to extract all name and location information
        :type guide: PyNode

        :param shape: Each number represents a specific shape
        :type shape: int

        :param name: additional name if no guide is given
        :type name: str

        :param offset: amount of buffer nodes
        :type offset: int
        """

        # private args
        self._component = component
        self._guide = guide
        self._shape = shape
        self._name = name
        self._offset = offset

        # vars
        self.hrc = None
        self.srt = None
        self.buffers = list()

        # methods
        self._parent_groups()

        if shape == 0:
            self.circle()
        elif shape == 1:
            self.square()

    def _parent_groups(self):
        """Add additional buffers under the hrc"""
        if self._guide:
            self.hrc = pm.createNode('transform', n=self._guide.replace('guide_srt', 'ctrl_hrc'),
                                     p=self._component.control_grp)
        else:
            self.hrc = pm.createNode('transform', n='%s_ctrl_hrc' % self._component.name,
                                     p=self._component.control_grp)
        for i in range(self._offset):
            if self._guide:
                off = pm.createNode('transform',
                                    n=self._guide.replace('guide_srt', 'buffer%s_hrc' % i))
            else:
                off = pm.createNode('transform', n='%s_buffer%s_hrc' %
                                                   (self._component.name, i))
            if self.buffers:
                off.setParent(self.buffers[-1])
            else:
                off.setParent(self.hrc)
            self.buffers.append(off)

    def _set_default_colors(self):
        """Set default control colors, left=blue, right=red, center=yellow"""
        self.srt.getShape().overrideEnabled.set(1)
        if '_C_' in self.srt:
            self.srt.getShape().overrideColor.set(17)
        elif '_L_' in self.srt:
            self.srt.getShape().overrideColor.set(6)
        elif '_R_' in self.srt:
            self.srt.getShape().overrideColor.set(13)

    def circle(self):
        """Create a nurbsCurve circle"""
        if self._guide:
            self.srt = pm.circle(n=self._guide.replace('guide', 'ctrl'))[0]
        else:
            self.srt = pm.circle(n='%s_ctrl_srt' % self._component.name)[0]
        if self.buffers:
            self.srt.setParent(self.buffers[-1])
        else:
            self.srt.setParent(self.hrc)
        if self._guide:
            self.hrc.t.set(pm.xform(self._guide, q=True, t=True, ws=True))
            self.hrc.r.set(pm.xform(self._guide, q=True, ro=True, ws=True))
        self._set_default_colors()

    def square(self):
        """Create a nurbsCurve square"""
        points = [[1, 0, 1], [-1, 0, 1], [-1, 0, -1], [1, 0, -1], [1, 0, 1]]
        if self._guide:
            self.srt = pm.curve(d=1, n=self._guide.replace('guide', 'ctrl'), point=points)
        else:
            self.srt = pm.curve(d=1, n='%s_ctrl_srt' % self._component.name, point=points)
        if self.buffers:
            self.srt.setParent(self.buffers[-1])
        else:
            self.srt.setParent(self.hrc)
        if self._guide:
            self.hrc.t.set(pm.xform(self._guide, q=True, t=True, ws=True))
            self.hrc.r.set(pm.xform(self._guide, q=True, ro=True, ws=True))
        self._set_default_colors()
