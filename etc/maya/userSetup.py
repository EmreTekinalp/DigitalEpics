# python
import sys

# maya
import maya.cmds as cmds
if not cmds.commandPort(':4434', q=True):
    cmds.commandPort(n=':4434') 

# add the project path to the system path
sys.path.append('/Users/emretekinalp/PycharmProjects/DigitalEpics/software/maya/src/python')
sys.path.append('/Users/emretekinalp/PycharmProjects/DigitalEpics/software/maya')
