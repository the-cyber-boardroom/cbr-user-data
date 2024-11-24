from unittest                                       import TestCase
from cbr_user_data.fast_api.routes.Routes__User__UI import Routes__User__UI


class test_Routes__User__UI(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.routes_user_ui = Routes__User__UI()

    def test_left_menu(self):
        with self.routes_user_ui as _:
            assert _.left_menu() == self.routes_user_ui.ui_user_menu.json__cached()