from unittest import TestCase

from cbr_user_data.fast_api.routes.Routes__User__Files import Routes__User__Files
from tests.integration.user_data__objs_for_tests import user_data__assert_local_stack


class test__int__Routes__User_Data(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user_data__assert_local_stack()
        cls.routes_user_files = Routes__User__Files()

    def test_tree_view(self):
        with self.routes_user_files as _:
            assert _.tree_view() == 'will go here'
            #print(_.tree_view())