import pytest
from unittest                                                               import TestCase
from cbr_shared.cbr_backend.folders.Temp_Folders_Structure                  import Temp_Folders_Structure
from cbr_shared.cbr_backend.folders.models.Model__User__Folders__Structure  import Model__User__Folders__Structure
from cbr_shared.cbr_backend.users.Temp_User_Request                         import Temp_User_Request
from cbr_user_data.fast_api.models.Model__API__User__Add_File               import Model__API__User__Add_File
from cbr_user_data.fast_api.routes.Routes__User__File_System                import Routes__User__File_System
from osbot_utils.utils.Env                                                  import not_in_github_action
from osbot_utils.utils.Misc                                                 import is_guid
from osbot_utils.utils.Objects                                              import dict_to_obj, __
from osbot_utils.utils.Status                                               import status_ok
from tests.integration.user_data__objs_for_tests                            import user_data__assert_local_stack

class test__int__Routes__User__File_System(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user_data__assert_local_stack()
        cls.routes_user_files       = Routes__User__File_System()
        cls.temp_folders_structure  = Temp_Folders_Structure().create()
        cls.temp_user               = cls.temp_folders_structure.temp_user
        cls.user_folders_structure  = cls.temp_folders_structure.user_folders_structure
        cls.folders_operations      = cls.user_folders_structure.folders_operations()
        cls.temp_user_request       = Temp_User_Request(temp_user=cls.temp_user).create()
        cls.request                 = cls.temp_user_request.request

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_user_request     .delete()
        cls.temp_folders_structure.delete()

    def test_setUpClass(self):
        assert self.temp_user                                    .exists() is True
        assert self.temp_folders_structure.user_folders_structure.exists() is True

    def test_add_file(self):
        model_api_user_add_file = Model__API__User__Add_File(file_name='file.txt', file_bytes=b'hello world')
        response = dict_to_obj(self.routes_user_files.add_file(request=self.request, model_add_file=model_api_user_add_file))
        file_id  = response.data.file_id
        assert response         == __(data=__(file_id=file_id), error=None, message='File added', status='ok')
        assert is_guid(file_id) is True
        assert self.routes_user_files.tree_view(self.request).body.decode('utf-8')  == ('🏠root\n'
                                                                                        '│  📄file_txt')
        assert self.user_folders_structure.load().tree_view()                       == ('🏠root\n'
                                                                                        '│  📄file_txt')

    def test_add_folder(self):
        assert self.user_folders_structure.tree_view() == ('🏠root\n'
                                                           '│  📄file_txt')
        folder_1_id = self.routes_user_files.add_folder(self.request, folder_name='folder_1').get('data').get('folder_id')
        assert self.user_folders_structure.load().tree_view() == ('🏠root\n'
                                                                  '└─ 📁folder_1\n'
                                                                  '│  📄file_txt')
        folder_2_id = self.routes_user_files.add_folder(self.request, folder_name='folder_2', parent_folder_id=folder_1_id).get('data').get('folder_id')

        assert self.user_folders_structure.load().tree_view() == ('🏠root\n'
                                                                  '└─ 📁folder_1\n'
                                                                  '│  └─ 📁folder_2\n'
                                                                  '│  📄file_txt')

        assert is_guid(folder_1_id) is True
        assert is_guid(folder_2_id) is True

        model_api_user_add_file = Model__API__User__Add_File(file_name='file.txt', file_bytes=b'hello world', folder_id=folder_2_id)
        self.routes_user_files.add_file(request=self.request, model_add_file=model_api_user_add_file)
        assert self.user_folders_structure.load().tree_view() == ('🏠root\n'
                                                                  '└─ 📁folder_1\n'
                                                                  '│  └─ 📁folder_2\n'
                                                                  '│  │  │  📄file_txt\n'
                                                                  '│  📄file_txt')
        #pprint(self.user_folders_structure.load().json_view())

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
            assert _.tree_view(self.request).body.decode() == ('🏠root\n'
                                                               '└─ 📁folder_1\n'
                                                               '│  └─ 📁folder_2\n'
                                                               '│  │  │  📄file_txt\n'
                                                               '│  📄file_txt')