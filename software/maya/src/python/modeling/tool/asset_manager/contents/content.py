'''
@author:  etekinalp
@date:    Sep 7, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module contains the ui content
'''

import os
import shutil
import json

from PySide2 import QtGui, QtCore, QtWidgets
from shiboken2 import wrapInstance

from maya import cmds, OpenMayaUI
from utility import generator
reload(generator)


def get_project_info(projectPath):
    result = list()

    #--- check if project path exists
    assert os.path.exists(projectPath), ("Path does not exist: " + `projectPath`)

    #--- get the projects
    projects = list()
    pro_path = os.listdir(projectPath)
    for pro in pro_path:
        projects.append(pro)

    #--- get the types and assets
    for pro in projects:
        assets = dict()
        info = dict()
        #--- list asset types
        typ_path = os.listdir(os.path.join(projectPath, pro))
        for typ in typ_path:
            if not typ:
                continue
            #--- list asset names
            asset_path = os.listdir(os.path.join(projectPath, pro, typ))
            asset = list()
            for ass in asset_path:
                if not ass:
                    continue
                asset.append(ass)
            assets[typ] = asset
        info[pro] = assets
        result.append(info)
    return result
#END get_project_info()


def get_env_info(projectPath):
    result = list()

    #--- check if goe_builds path exists in PandorasBox
    build_path = os.path.join(projectPath, 'goe_builds')
    if not os.path.exists(build_path):
        raise Exception("Path does not exist: " + `build_path`)

    #--- get the projects
    projects = list()
    pro_path = os.listdir(build_path)
    for pro in pro_path:
        if os.path.isdir(os.path.join(build_path, pro)):
            projects.append(pro)

    #--- get the types and assets
    for pro in projects:
        assets = dict()
        info = dict()
        #--- list asset types
        typ_path = os.listdir(os.path.join(build_path, pro))
        for typ in typ_path:
            if not typ:
                continue
            if not os.path.isdir(os.path.join(build_path, pro, typ)):
                continue
            #--- list asset names
            asset_path = os.listdir(os.path.join(build_path, pro, typ))
            asset = list()
            for ass in asset_path:
                if not ass:
                    continue
                if not os.path.isdir(os.path.join(build_path, pro, typ, ass)):
                    continue
                asset.append(ass)
            assets[typ] = asset
        info[pro] = assets
        result.append(info)
    return result
#END get_env_info()


def set_asset_structure(path=None,
                        project=None,
                        assetType=None,
                        assetName=None,
                        resolution=None,
                        department=None):
    #--- check if goe_builds path exists in PandorasBox
    assert os.path.exists(path), ("Path does not exist: " + `path`)

    #--- define paths
    project_path = os.path.join(path, project)
    asset_type_path = os.path.join(project_path, assetType)
    asset_name_path = os.path.join(asset_type_path, assetName)
    asset_res_path = os.path.join(asset_name_path, resolution)
    asset_dpt_path = os.path.join(asset_res_path, department)
    asset_release_path = os.path.join(asset_dpt_path, 'release')
    asset_work_path = os.path.join(asset_dpt_path, 'work')

    #--- check and create paths
    #--- project path
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    #--- assetType path
    if not os.path.exists(asset_type_path):
        os.makedirs(asset_type_path)
    #--- assetName path
    if not os.path.exists(asset_name_path):
        os.makedirs(asset_name_path)
    #--- assetRes path
    if not os.path.exists(asset_res_path):
        os.makedirs(asset_res_path)
    #--- assetDpt path
    if not os.path.exists(asset_dpt_path):
        os.makedirs(asset_dpt_path)
    #--- assetRelease path
    if not os.path.exists(asset_release_path):
        os.makedirs(asset_release_path)
    #--- assetWork path
    if not os.path.exists(asset_work_path):
        os.makedirs(asset_work_path)
    else:
        cmds.warning("Specified asset structure already exists: " + `asset_dpt_path`)
        return
#END set_asset_structure()


def set_rig_structure(path=None,
                      project=None,
                      assetType=None,
                      assetName=None,
                      resolution=None):
    #--- check if goe_builds path exists in PandorasBox
    build_path = os.path.join(path, 'goe_builds')
    if not os.path.exists(build_path):
        raise Exception("Path does not exist: " + `build_path`)

    #--- define paths
    project_path = os.path.join(build_path, project)
    asset_type_path = os.path.join(project_path, assetType)
    asset_name_path = os.path.join(asset_type_path, assetName)
    asset_build_path = os.path.join(asset_name_path, 'build_' + resolution)
    asset_file_path = os.path.join(asset_build_path, assetName + '.py')
    asset_data_path = os.path.join(asset_build_path, 'data')
    data_obj_path = os.path.join(asset_data_path, 'obj.py')
    asset_misc_path = os.path.join(asset_data_path, 'misc')
    asset_weights_path = os.path.join(asset_data_path, 'weights')

    #--- check and create paths
    #--- project path
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        init = os.path.join(project_path, '__init__.py')
        if not os.path.exists(init):
            open(init, 'w')
    #--- assetType path
    if not os.path.exists(asset_type_path):
        os.makedirs(asset_type_path)
        init = os.path.join(asset_type_path, '__init__.py')
        if not os.path.exists(init):
            open(init, 'w')
    #--- assetName path
    if not os.path.exists(asset_name_path):
        os.makedirs(asset_name_path)
        init = os.path.join(asset_name_path, '__init__.py')
        if not os.path.exists(init):
            open(init, 'w')
    #--- assetBuild path
    if not os.path.exists(asset_build_path):
        os.makedirs(asset_build_path)
        init = os.path.join(asset_build_path, '__init__.py')
        if not os.path.exists(init):
            open(init, 'w')
    #--- assetData path
    if not os.path.exists(asset_data_path):
        os.makedirs(asset_data_path)
        init = os.path.join(asset_data_path, '__init__.py')
        if not os.path.exists(init):
            open(init, 'w')
    #--- dataObj path
    if not os.path.exists(data_obj_path):
        open(data_obj_path, 'w')
    #--- assetMisc path
    if not os.path.exists(asset_misc_path):
        os.makedirs(asset_misc_path)
    #--- assetWeights path
    if not os.path.exists(asset_weights_path):
        os.makedirs(asset_weights_path)
    #--- assetFile path
    if not os.path.exists(asset_file_path):
        open(asset_file_path, 'w')
        generator.base_build_code(asset_file_path, asset_data_path)
        print "Successfully created new asset structure: " + `asset_file_path`
    else:
        cmds.warning("Specified asset structure already exists: " + `asset_file_path`)
        return
#END set_rig_structure()


def remove_structure(path=None,
                     project=None,
                     assetType=None,
                     assetName=None,
                     resolution=None,
                     element=2):
    #--- check if goe_builds path exists in PandorasBox
    build_path = os.path.join(path, 'goe_builds')
    if not os.path.exists(build_path):
        raise Exception("Path does not exist: " + `build_path`)

    #--- define paths
    project_path = os.path.join(build_path, project)
    asset_type_path = os.path.join(project_path, assetType)
    asset_name_path = os.path.join(asset_type_path, assetName)
    asset_build_path = os.path.join(asset_name_path, 'build_' + resolution)

    if not element:
        if not os.path.exists(project_path):
            return
        remove_confirm_dialog('Remove Project ' + project, project_path)
        return True
    elif element == 1:
        if not os.path.exists(asset_type_path):
            return
        remove_confirm_dialog('Remove ' + assetType, asset_type_path)
        return True
    elif element == 2:
        if os.path.exists(asset_build_path):
            check = 1
            folders = os.listdir(asset_name_path)
            if len(folders) > 2:
                for i in folders:
                    if not i == '__init__.py':
                        if not i:
                            check = 0
            else:
                check = 0
            if not check:
                remove_confirm_dialog('Remove ' + assetName, asset_name_path)
                return True
            else:
                remove_confirm_dialog('Remove ' + assetName + '_' + resolution,
                                      asset_build_path)
                return False
        else:
            check = 1
            folders = os.listdir(asset_name_path)
            if len(folders) > 1:
                for i in folders:
                    if not i == '__init__.py':
                        if not i:
                            check = 0
            else:
                check = 0
            if not check:
                remove_confirm_dialog('Remove ' + assetName, asset_name_path)
                return True
#END remove_structure()


def remove_confirm_dialog(titleName, pathToDelete):
    result = cmds.confirmDialog(title=titleName,
                                message='Are you sure you wanna do this?',
                                button=['Yes', 'No'],
                                defaultButton='Yes',
                                cancelButton='No',
                                dismissString='No')
    if result == 'Yes':
        shutil.rmtree(pathToDelete)
#END remove_confirm_dialog()


def get_version(path=None,
                project=None,
                assetType=None,
                assetName=None,
                resolution=None,
                department=None,
                status=None):
    #--- define paths
    project_path = os.path.join(path, project)
    asset_type_path = os.path.join(project_path, assetType)
    asset_name_path = os.path.join(asset_type_path, assetName)
    asset_res_path = os.path.join(asset_name_path, resolution)
    asset_dpt_path = os.path.join(asset_res_path, department)
    asset_status_path = os.path.join(asset_dpt_path, status)
    #--- check and create paths
    #--- project path
    if not os.path.exists(project_path):
        return
    #--- assetType path
    if not os.path.exists(asset_type_path):
        return
    #--- assetName path
    if not os.path.exists(asset_name_path):
        return
    #--- assetRes path
    if not os.path.exists(asset_res_path):
        return
    #--- assetDpt path
    if not os.path.exists(asset_dpt_path):
        return
    #--- assetRelease path
    if not os.path.exists(asset_status_path):
        return
    result = os.listdir(asset_status_path)
    result.reverse()
    return result
#END get_version()


def open_asset(path=None,
               project=None,
               assetType=None,
               assetName=None,
               resolution=None,
               department=None,
               status=None,
               version=None):
    #--- define paths
    project_path = os.path.join(path, project)
    asset_type_path = os.path.join(project_path, assetType)
    asset_name_path = os.path.join(asset_type_path, assetName)
    asset_res_path = os.path.join(asset_name_path, resolution)
    asset_dpt_path = os.path.join(asset_res_path, department)
    asset_status_path = os.path.join(asset_dpt_path, status)
    asset_version_path = os.path.join(asset_status_path, version)
    #--- project path
    if not os.path.exists(project_path):
        return
    #--- assetType path
    if not os.path.exists(asset_type_path):
        return
    #--- assetName path
    if not os.path.exists(asset_name_path):
        return
    #--- assetRes path
    if not os.path.exists(asset_res_path):
        return
    #--- assetDpt path
    if not os.path.exists(asset_dpt_path):
        return
    #--- assetStatus path
    if not os.path.exists(asset_status_path):
        return
    #--- assetVersion path
    if not os.path.exists(asset_version_path):
        return
    return asset_version_path
#END open_asset()


def save_asset(path=None,
               project=None,
               assetType=None,
               assetName=None,
               resolution=None,
               department=None,
               status=None):
    #--- define paths
    project_path = os.path.join(path, project)
    asset_type_path = os.path.join(project_path, assetType)
    asset_name_path = os.path.join(asset_type_path, assetName)
    asset_res_path = os.path.join(asset_name_path, resolution)
    asset_dpt_path = os.path.join(asset_res_path, department)
    asset_status_path = os.path.join(asset_dpt_path, status)
    #--- project path
    if not os.path.exists(project_path):
        return
    #--- assetType path
    if not os.path.exists(asset_type_path):
        return
    #--- assetName path
    if not os.path.exists(asset_name_path):
        return
    #--- assetRes path
    if not os.path.exists(asset_res_path):
        return
    #--- assetDpt path
    if not os.path.exists(asset_dpt_path):
        return
    #--- assetStatus path
    if not os.path.exists(asset_status_path):
        return
    versions = os.listdir(asset_status_path)
    if not versions:
        versions = []
    asset_version_path = os.path.join(asset_status_path, assetName + str((len(versions) + 1)))
    return asset_version_path
#END save_asset()


def create_config_file(envpath, projectpath):
    assert envpath, 'Please set MAYA_PLUGIN_PATH to PandorasBox in your Maya.env'
    if not projectpath:
        return
    config = dict()
    config['projectpath'] = projectpath
    config_path = os.path.join(envpath, 'ASSET_DATA_PATH.config')
    if not os.path.exists(config_path):
        with open(config_path, 'w') as json_file:
            json.dump(config, json_file, sort_keys=True, indent=2, ensure_ascii=False)
#END create_config_file()


def get_config_file(envpath):
    assert envpath, 'Please set MAYA_PLUGIN_PATH to PandorasBox in your Maya.env'
    config_path = os.path.join(envpath, 'ASSET_DATA_PATH.config')
    if os.path.exists(config_path):
        with open(config_path) as json_file:
            json_data = json.load(json_file)
            return json_data.values()[0]
#END get_config_file()


class ExtendedQLabel(QtWidgets.QLabel):
    def __init__(self,
                 parent=None,
                 onPressPix=None,
                 onReleasePix=None,
                 initLabels=[],
                 switchLabels=[]):
        QtWidgets.QLabel.__init__(self, parent)
        self.setMouseTracking(True)

        #--- args
        self.on_press_pix = onPressPix
        self.on_release_pix = onReleasePix
        self.init_labels = initLabels
        self.switch_labels = switchLabels

    def mousePressEvent(self, event):
        self.setPixmap(self.on_press_pix)

    def mouseReleaseEvent(self, event):
        self.emit(QtCore.SIGNAL('clicked()'))
        self.setPixmap(self.on_release_pix)
        if not self.init_labels:
            return
        if not self.switch_labels:
            return
        if not len(self.init_labels) == len(self.switch_labels):
            return
        for i, j in zip(self.init_labels, self.switch_labels):
            if j.isHidden():
                i.setHidden(True)
                j.setHidden(False)
            else:
                i.setHidden(False)
                j.setHidden(True)
