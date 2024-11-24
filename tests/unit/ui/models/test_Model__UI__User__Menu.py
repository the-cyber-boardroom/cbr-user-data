from unittest                                           import TestCase
from cbr_user_data.ui.models.Model__UI__User__Menu      import Model__UI__User__Menu
from cbr_user_data.ui.models.Model__UI__User__Menu_Item import Model__UI__User__Menu_Item
from osbot_utils.utils.Objects                          import __


class test_Model__UI__User__Menu(TestCase):

    def setUp(self):
        self.user_menu = Model__UI__User__Menu()

    def test__init__(self):
        assert self.user_menu.obj()  == __(menu_items=__())

    def test__add_menu_item__empty(self):
        menu_item                              = Model__UI__User__Menu_Item()
        self.user_menu.menu_items['menu_item'] = menu_item

        assert self.user_menu.obj () == __(menu_items=__(menu_item=__(icon='', label='', web_component='', web_component_path= '',  path='')))
        assert self.user_menu.json() == {'menu_items': {'menu_item': {'icon': '', 'label': '', 'path': '', 'web_component': '', 'web_component_path': ''}}}

    def test__add_menu_item__with_values(self):
        kwargs                                 =  dict (icon               = 'an icon'              ,
                                                        label              = 'an label'             ,
                                                        web_component      = 'an web_component'     ,
                                                        web_component_path = 'an web_component_path',
                                                        path               = 'an path'              )
        menu_item                              = Model__UI__User__Menu_Item(**kwargs)
        self.user_menu.menu_items['menu_item'] = menu_item

        assert self.user_menu.obj () == __(menu_items=__(menu_item=__(icon               = 'an icon'              ,
                                                                      label              = 'an label'             ,
                                                                      web_component      = 'an web_component'     ,
                                                                      web_component_path = 'an web_component_path',
                                                                      path               = 'an path'              )))

        assert self.user_menu.json() == {'menu_items': {'menu_item': {'icon'              : 'an icon'               ,
                                                                      'label'             : 'an label'              ,
                                                                      'path'              : 'an path'               ,
                                                                      'web_component'     : 'an web_component'      ,
                                                                      'web_component_path': 'an web_component_path' }}}