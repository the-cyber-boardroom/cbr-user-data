from unittest import TestCase

from cbr_shared.cbr_backend.users.S3_DB__User import S3_DB__User
from cbr_shared.cbr_backend.users.S3_DB__Users import S3_DB__Users
from cbr_shared.cbr_backend.users.Temp_User_Request import Temp_User_Request
from cbr_shared.schemas.data_models.Model__Chat__Saved import Model__Chat__Saved
from cbr_user_data.fast_api.routes.Routes__User__Chats import Routes__User__Chats
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import is_guid
from tests.integration.user_data__objs_for_tests import user_data__assert_local_stack


class test__int__Routes__User__Chats(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        user_data__assert_local_stack()
        cls.temp_user_request       = Temp_User_Request().create()
        cls.request                 = cls.temp_user_request.request
        cls.routes_user_chats       = Routes__User__Chats()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_user_request     .delete()

    def test_db_user(self):
        with self.routes_user_chats as _:
            db_user = _.db_user(self.request)
            assert type(db_user) == S3_DB__User

    def test_chats(self):
        with self.routes_user_chats  as _:
            chat_path  = 'abc/123'
            chat_saved = _.chat_add(self.request, chat_path)
            chat_id    =  chat_saved.chat_id
            assert type(chat_saved)         is Model__Chat__Saved
            assert chat_saved.chat_path     == chat_path
            response = _.chats(self.request)
            assert response == {'saved_chats': {chat_id : chat_saved.json()} }