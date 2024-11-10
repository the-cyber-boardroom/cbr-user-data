import pytest
from unittest                                                               import TestCase
from cbr_shared.cbr_backend.folders.Temp_Folders_Structure                  import Temp_Folders_Structure
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from cbr_shared.cbr_backend.users.Temp_User_Request                         import Temp_User_Request
from cbr_user_data.fast_api.routes.Routes__User__File_System                import Routes__User__File_System
from osbot_utils.utils.Env                                                  import not_in_github_action
from osbot_utils.utils.Misc                                                 import is_guid
from osbot_utils.utils.Status                                               import status_ok
from tests.integration.user_data__objs_for_tests                            import user_data__assert_local_stack

class test__int__Routes__User__File_System(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user_data__assert_local_stack()
        cls.routes_user_files      = Routes__User__File_System()
        cls.temp_folders_structure = Temp_Folders_Structure().create()
        cls.temp_user              = cls.temp_folders_structure.temp_user
        cls.temp_user_request      = Temp_User_Request().create()
        cls.request                = cls.temp_user_request.request

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_user_request     .delete()
        cls.temp_folders_structure.delete()

    def test_setUpClass(self):
        assert self.temp_user                                    .exists() is True
        assert self.temp_folders_structure.user_folders_structure.exists() is True

    def test_delete_file_system(self):
        if not_in_github_action():
            pytest.skip("Don't execute locally since it takes about 200ms to run")
        with self.routes_user_files as _:
            assert self.temp_user_request.temp_user.user_config().file_system == False
            assert _.tree_view(self.request)                                  == '🏠root'
            assert self.temp_user_request.temp_user.user_config().file_system == True
            assert _.delete_file_system(self.request) == status_ok(message="File System deleted")
            assert self.temp_user_request.temp_user.user_config().file_system == False
            assert _.tree_view(self.request) == '🏠root'
            assert self.temp_user_request.temp_user.user_config().file_system == True

    def test_folder_structure(self):
        with self.routes_user_files as _:
            folder_structure_data = _.folder_structure(self.request)
            folder_structure      = Model__User__Folders__Structure.from_json(folder_structure_data)
            root_id               = folder_structure.root_id

            assert is_guid(root_id)                            is True
            assert folder_structure.folders[root_id].folder_id == root_id

    def test_tree_view(self):
        with self.routes_user_files as _:
            print()
            assert _.tree_view(self.request) == '🏠root'