from unittest                                                       import TestCase
from cbr_shared.cbr_backend.files.User__File__System                import User__File__System
from cbr_shared.cbr_backend.folders.Temp_Folders_Structure          import Temp_Folders_Structure
from cbr_shared.cbr_backend.users.Temp_User_Request                 import Temp_User_Request
from cbr_user_data.fast_api.routes.Routes__User__File_To_LLMs       import Routes__User__File_To_LLMs
from tests.integration.user_data__objs_for_tests                    import user_data__assert_local_stack


class test__int__Routes__User__File_To_LLMs(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        user_data__assert_local_stack()
        cls.routes_user_file_to_llms = Routes__User__File_To_LLMs()
        cls.temp_folders_structure   = Temp_Folders_Structure().create()
        cls.temp_user                = cls.temp_folders_structure.temp_user
        cls.temp_user_request        = Temp_User_Request(temp_user=cls.temp_user).create()
        cls.file_system              = User__File__System(db_user=cls.temp_user).setup()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_user_request     .delete()
        cls.temp_folders_structure.delete()
        assert cls.temp_user                                    .exists() is False
        assert cls.temp_folders_structure.user_folders_structure.exists() is False

    def temp_file(self, file_name='file.txt', file_bytes=b'hello world'):
        user_file = self.file_system.add_file(file_name=file_name, file_bytes=file_bytes)
        return user_file.file_id

    def test_setUpClass(self):
        assert self.temp_user                                          .exists() is True
        assert self.temp_folders_structure.user_folders_structure      .exists() is True
        assert self.file_system.user_folders().user_folders_structure().exists() is True

    # this needs an LLM Cache
    # def test_file__summary(self):
    #     file_id = self.temp_file(file_bytes=b"This is a document about Cyber Security")
    #     result = self.routes_user_file_to_llms.file_summary(request=self.temp_user_request.request, file_id=file_id)
    #     from osbot_utils.utils.Dev import pprint
    #     pprint(result)

