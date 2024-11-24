from unittest                        import TestCase
from cbr_user_data.ui.UI__User__Menu import UI__User__Menu, FILE__CBR__USER__SITE_MENU_CONFIG
from osbot_utils.utils.Files         import file_exists, file_extension
from osbot_utils.utils.Objects       import __


class test_UI__User__Menu(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ui_user_menu = UI__User__Menu()


    def test__init__(self):
        with self.ui_user_menu as _:
            assert _.obj()  == __(user_menu=__(menu_items=__()))
            assert _.json() == {'user_menu': {'menu_items': {}}} != {}

    def test_load_cbr_user_menu(self):
        with self.ui_user_menu as _:
            _.load_cbr_user_menu()
            assert _.user_menu.obj().menu_items.home.icon == 'home'

    def test_path__cbr_user_menu(self):
        with self.ui_user_menu as _:
            path_toml_menu_file = _.path__cbr_user_menu()
            assert (FILE__CBR__USER__SITE_MENU_CONFIG in path_toml_menu_file) is True
            assert file_exists   (path_toml_menu_file)                        is True
            assert file_extension(path_toml_menu_file)                        == '.toml'
