'''
Created on Oct 9, 2014

@author: Emre
'''

import shiboken2
from maya import OpenMayaUI
from PySide2 import QtWidgets
import pyside2uic
import xml.etree.ElementTree as xml
from cStringIO import StringIO


# def wrapinstance(ptr, base=None):
#     """Utility to convert a pointer to a Qt class instance.
#     @param ptr: Pointer to QObject in memory
#     @param base: (Optional) Base class to wrap with (Defaults to QObject,
#                  which should handle anything)
#     @type ptr: long or Swig instance
#     @type base: QtGui.QWidget
#     @return: QWidget or subclass instance
#     """
#     if ptr is None:
#         return None
#     ptr = long(ptr)
#     if base is None:
#         qObj = shiboken2.wrapInstance(long(ptr), QtCore.QObject)
#         metaObj = qObj.metaObject()
#         cls = metaObj.className()
#         superCls = metaObj.superClass().className()
#         if hasattr(QtGui, cls):
#             base = getattr(QtGui, cls)
#         elif hasattr(QtGui, superCls):
#             base = getattr(QtGui, superCls)
#         else:
#             base = QtWidgets.QWidget
#     return shiboken2.wrapInstance(long(ptr), base)
# # END def wrapinstance
#
#
# def load_ui_type(ui_file):
#     """Pyside lacks the "loadUiType" command, so we have to convert the ui
#     file to py code in-memory first and then execute it in a special frame to
#     retrieve the form_class.
#     @param ui_file: the ui file
#     @type ui_file: String
#     @return: the classes
#     """
#     parsed = xml.parse(ui_file)
#     widget_class = parsed.find('widget').get('class')
#     form_class = parsed.find('class').text
#     with open(ui_file, 'r') as f:
#         o = StringIO()
#         frame = dict()
#         pyside2uic.compileUi(f, o, indent=0)
#         pyc = compile(o.getvalue(), '<string>', 'exec')
#         exec pyc in frame
#         # Fetch the base_class and form class based on their type in the
#         # xml from designer
#         form_class = frame['Ui_%s' % form_class]
#         base_class = eval('QtGui.%s' % widget_class)
#     # END with open(ui_file, 'r') as f
#     return form_class, base_class
# # END def load_ui_type
#
#
# def get_maya_window():
#     """Get the maya main window as a QMainWindow instance.
#     @return: the maya main window
#     """
#     ptr = OpenMayaUI.MQtUtil.mainWindow()
#     return wrapinstance(long(ptr), QtWidgets.QWidget)
# # END def get_maya_window


def get_maya_window():

    ptr = OpenMayaUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)

def load_ui_type(ui_file):

    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    with open(ui_file,'r') as f:
        o = StringIO()
        frame = {}

        pyside2uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from design
        form_class = frame['Ui_{0}'.format(form_class)]
        base_class = eval('QtWidgets.{0}'.format(widget_class))

    return form_class, base_class
