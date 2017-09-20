'''
@author:  etekinalp
@date:    Oct 24, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates and setups the asset manager ui
'''


import os
from asset_manager.contents import utils, content
reload(utils)
reload(content)

from PySide2 import QtGui, QtCore
from maya import cmds

basepath = os.path.join(os.path.dirname(content.__file__).split('contents')[0])
uipath = os.path.join(basepath, 'ui', 'asset_manager.ui')
assert os.path.exists(os.path.normpath(uipath)), 'Path does not exist!'

form_class, base_class = utils.load_ui_type(uipath)


class AssetManagerUI(form_class, base_class):
    """
    @DONE save file to another location
    @todo asset info box
    @DONE change position of env path and project path
    @todo confirm dialogs by saving etc
    """
    def __init__(self):
        super(AssetManagerUI, self).__init__()
        self.setupUi(self)
        self.setGeometry(600, 300, 100, 100)

        #--- methods
        self.__create()
    #END __init__()

    def __create_labels(self):
        icons_path = os.path.join(basepath, 'icons')
        if not os.path.exists(icons_path):
            raise Exception("Path does not exist: " + `icons_path`)
        #--- header image
        header_pic = QtGui.QPixmap(os.path.join(icons_path, "goe_header_large_de.jpg"))
        self.header_lab.setPixmap(header_pic)

        #--- plus project image
        release_pic = QtGui.QPixmap(os.path.join(icons_path, "plus.png"))
        pressed_pic = QtGui.QPixmap(os.path.join(icons_path, "plusPress.png"))
        self.plus_project_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.plus_project_pic.setPixmap(release_pic)

        #--- plus type image
        self.plus_type_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.plus_type_pic.setPixmap(release_pic)

        #--- plus asset image
        self.plus_asset_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.plus_asset_pic.setPixmap(release_pic)
    #END __create_labels()

    def __setup_label_layout(self):
        #--- add widgets to layouts
        self.project_name_lay.addWidget(self.plus_project_pic)
        self.asset_type_lay.addWidget(self.plus_type_pic)
        self.asset_name_lay.addWidget(self.plus_asset_pic)
    #END __setup_label_layout()

    def __check_env_path(self):
        path = os.getenv('MAYA_PLUG_IN_PATH')
        envs = path.split(':')
        for i in envs:
            print i
            if 'PandorasBox' in i:
                self.env_path = i
        self.env_path = '/Users/emretekinalp/PycharmProjects/Public/src/python/tool/autorigger_v02_obsolete/__obsolete_rig_system'
        self.env_led.setText(self.env_path)

        #--- get env info
        self.env_info = content.get_env_info(self.env_path)
    #END __check_env_path()

    def __check_asset_data_path(self):
        path = content.get_config_file(self.env_path)
        if path:
            self.set_led.setText(path)
            self.__check_project_path()
    #END __check_asset_data_path()

    def __open_file_browser(self):
        self.env_path = '/Users/emretekinalp/PycharmProjects/Public/src/python/tool/autorigger_v02_obsolete/__obsolete_rig_system'
        path = content.get_config_file(self.env_path)
        if path:
            self.set_led.setText(path)
            self.__check_project_path()
            return
        path = cmds.fileDialog2(fileMode=3, dialogStyle=1)
        if path:
            path = path[0]
            self.set_led.setText(path)
            content.create_config_file(self.env_path, path)
            self.__check_project_path()
    #END __open_file_browser()

    def __check_project_path(self):
        self.project_path = self.set_led.text()
        self.project_path = '/Users/emretekinalp/PycharmProjects/Public/src/python/tool/autorigger_v02_obsolete/__obsolete_rig_system'

        #--- get project info
        self.project_info = content.get_project_info(self.project_path)

        #--- set project info
        self.__set_project_info()
    #END __check_project_path()

    def __set_project_info(self):
        #--- set project info
        if not self.project_info:
            return
        self.projects = [i.keys()[0] for i in self.project_info]
        self.project_name_cb.clear()
        if self.projects:
            self.projects.sort()
            self.projects.insert(0, '...')
            self.project_name_cb.addItems(self.projects)
        else:
            self.project_name_cb.addItem('...')
    #END __set_project_info()

    def __update_project_info(self):
        self.current_project = self.project_name_cb.currentText()
        self.asset_type_cb.clear()
        for d in self.project_info:
            for i in d.items():
                if not self.current_project == i[0]:
                    continue
                self.types = i[1].keys()
                if self.types:
                    self.types.sort()
                    self.asset_type_cb.addItems(self.types)
    #END __update_project_info()

    def __update_type_info(self):
        if not self.types:
            return
        self.current_project = self.project_name_cb.currentText()
        self.current_type = self.asset_type_cb.currentText()
        self.asset_name_cb.clear()
        for d in self.project_info:
            for i in d.items():
                if not self.current_project == i[0]:
                    continue
                for t in i[1].items():
                    if not self.current_type == t[0]:
                        continue
                    self.assets = t[1]
                    if self.assets:
                        self.assets.sort()
                        self.asset_name_cb.addItems(self.assets)
    #END __update_type_info()

    def __add_project(self):
        result = self.__add_prompt_dialog()
        if result:
            count = self.project_name_cb.count()
            self.project_name_cb.addItem(result)
            self.project_name_cb.setCurrentIndex(count)
    #END __add_project()

    def __add_type(self):
        if self.project_name_cb.currentIndex():
            result = self.__add_prompt_dialog()
            if result:
                count = self.asset_type_cb.count()
                self.asset_type_cb.addItem(result)
                self.asset_type_cb.setCurrentIndex(count)
    #END __add_type()

    def __add_asset(self):
        if self.asset_type_cb.currentText():
            result = self.__add_prompt_dialog()
            if result:
                count = self.asset_name_cb.count()
                self.asset_name_cb.addItem(result)
                self.asset_name_cb.setCurrentIndex(count)
    #END __add_asset()

    def __add_prompt_dialog(self):
        text = None
        result = cmds.promptDialog(title='Create new...',
                                   message='Enter Name:',
                                   button=['OK', 'Cancel'],
                                   defaultButton='OK',
                                   cancelButton='Cancel',
                                   dismissString='Cancel')
        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
        return text
    #END __add_prompt_dialog()

    def __add_asset_structure(self):
        self.current_project = self.project_name_cb.currentText()
        self.current_type = self.asset_type_cb.currentText()
        self.current_asset = self.asset_name_cb.currentText()
        self.current_res = self.asset_res_cb.currentText()
        self.current_dpt = self.asset_dpt_cb.currentText()
        if self.current_project == '...':
            if not self.current_type:
                return
            else:
                if not self.current_asset:
                    return
        if self.current_project:
            if not self.current_type:
                return
            else:
                if not self.current_asset:
                    return

        #--- create new ui structure
        self.__create_ui_structure()

        #--- create rig structure
        if self.current_dpt == 'rigging':
            content.set_rig_structure(self.env_path,
                                      self.current_project,
                                      self.current_type,
                                      self.current_asset,
                                      self.current_res)
    #END __add_asset_structure()

    def __create_ui_structure(self):
        #--- create new structure
        content.set_asset_structure(self.project_path,
                                    self.current_project,
                                    self.current_type,
                                    self.current_asset,
                                    self.current_res,
                                    self.current_dpt)
        #--- store the previous current states
        project = self.project_name_cb.currentIndex()
        types = self.asset_type_cb.currentIndex()
        asset = self.asset_name_cb.currentIndex()
        res = self.asset_res_cb.currentIndex()
        #--- update setup manager
        self.__check_project_path()
        #--- set the previous states
        self.project_name_cb.setCurrentIndex(project)
        self.asset_type_cb.setCurrentIndex(types)
        self.asset_name_cb.setCurrentIndex(asset)
        self.asset_res_cb.setCurrentIndex(res)
    #END __create_ui_structure()

    def __add_version(self):
        self.asset_version_cb.clear()

        self.project_path = self.set_led.text()
        self.current_project = self.project_name_cb.currentText()
        self.current_type = self.asset_type_cb.currentText()
        self.current_asset = self.asset_name_cb.currentText()
        self.current_res = self.asset_res_cb.currentText()
        self.current_dpt = self.asset_dpt_cb.currentText()
        self.current_status = self.asset_status_cb.currentText()
        if not self.current_project:
            return
        if not self.current_type:
            return
        if not self.current_asset:
            return
        if not self.current_res:
            return
        if not self.current_dpt:
            return
        if not self.current_status:
            return
        versions = content.get_version(self.project_path,
                                       self.current_project,
                                       self.current_type,
                                       self.current_asset,
                                       self.current_res,
                                       self.current_dpt,
                                       self.current_status)
        if versions:
            self.asset_version_cb.addItems(versions)
    #END __add_version()

    def __open_asset(self):
        self.project_path = self.set_led.text()
        self.current_project = self.project_name_cb.currentText()
        self.current_type = self.asset_type_cb.currentText()
        self.current_asset = self.asset_name_cb.currentText()
        self.current_res = self.asset_res_cb.currentText()
        self.current_dpt = self.asset_dpt_cb.currentText()
        self.current_status = self.asset_status_cb.currentText()
        self.current_version = self.asset_version_cb.currentText()
        if not self.current_project:
            return
        if not self.current_type:
            return
        if not self.current_asset:
            return
        if not self.current_res:
            return
        if not self.current_dpt:
            return
        if not self.current_status:
            return
        if not self.current_version:
            return
        result = content.open_asset(self.project_path,
                                    self.current_project,
                                    self.current_type,
                                    self.current_asset,
                                    self.current_res,
                                    self.current_dpt,
                                    self.current_status,
                                    self.current_version)
        cmds.file(result, force=True, typ="mayaAscii", open=True)
    #END __open_asset()

    def __save_asset(self):
        self.project_path = self.set_led.text()
        self.current_project = self.project_name_cb.currentText()
        self.current_type = self.asset_type_cb.currentText()
        self.current_asset = self.asset_name_cb.currentText()
        self.current_res = self.asset_res_cb.currentText()
        self.current_dpt = self.asset_dpt_cb.currentText()
        self.current_status = self.asset_status_cb.currentText()
        self.current_version = self.asset_version_cb.currentText()
        if not self.current_project:
            return
        if not self.current_type:
            return
        if not self.current_asset:
            return
        if not self.current_res:
            return
        if not self.current_dpt:
            return
        if not self.current_status:
            return
        result = content.save_asset(self.project_path,
                                    self.current_project,
                                    self.current_type,
                                    self.current_asset,
                                    self.current_res,
                                    self.current_dpt,
                                    self.current_status)
        cmds.file(rename=result)
        cmds.file(save=True, type='mayaAscii')
        self.__add_version()
    #END __save_asset()

    def __connect_signals(self):
        self.set_btn.clicked.connect(self.__open_file_browser)

        self.project_name_cb.currentIndexChanged['QString'].connect(self.__update_project_info)
        self.asset_type_cb.currentIndexChanged['QString'].connect(self.__update_type_info)
        self.asset_name_cb.currentIndexChanged['QString'].connect(self.__add_version)
        self.asset_res_cb.currentIndexChanged['QString'].connect(self.__add_version)
        self.asset_dpt_cb.currentIndexChanged['QString'].connect(self.__add_version)
        self.asset_status_cb.currentIndexChanged['QString'].connect(self.__add_version)

        self.connect(self.plus_project_pic, QtCore.SIGNAL('clicked()'), self.__add_project)
        self.connect(self.plus_type_pic, QtCore.SIGNAL('clicked()'), self.__add_type)
        self.connect(self.plus_asset_pic, QtCore.SIGNAL('clicked()'), self.__add_asset)

        self.open_btn.clicked.connect(self.__open_asset)
        self.save_btn.clicked.connect(self.__save_asset)
        self.create_btn.clicked.connect(self.__add_asset_structure)
    #END __connect_signals()

    def __create(self):
        #--- create labels
        self.__create_labels()

        #--- setup label layout
        self.__setup_label_layout()

        #--- check env path
#         self.__check_env_path()

        #--- check asset data path
#         self.__check_asset_data_path()

        #--- connect signals
        self.__connect_signals()
    #END __create()
#END AssetManagerUI()


def main(*args, **kwargs):
    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass

    win = AssetManagerUI()
    win.show()
#END main()

# main()
