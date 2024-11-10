from starlette.requests                                     import Request
from cbr_shared.cbr_backend.files.User__File__System        import User__File__System
from cbr_shared.cbr_backend.users.decorators.with_db_user   import with_db_user
from osbot_fast_api.api.Fast_API_Routes                     import Fast_API_Routes
from osbot_utils.utils.Status                               import status_ok


class Routes__User__File_System(Fast_API_Routes):
    tag: str = 'files'

    def file_system(self, request: Request):
        db_user = request.state.db_user
        return User__File__System(db_user=db_user).setup()

    @with_db_user
    def delete_file_system(self,request: Request):                      # todo: we really should add an 'are you sure?" check there :)
        file_system = self.file_system(request)
        file_system.delete()
        return status_ok(message="File System deleted")

    @with_db_user
    def folder_structure(self, request: Request):
        file_system = self.file_system(request)
        # with file_system.user_folders():
        #     file_system.user_folders().setup()
        return file_system.folder_structure().json()

    @with_db_user
    def tree_view(self, request: Request):
        file_system = self.file_system(request)
        return file_system.tree_view()


    def setup_routes(self):
        self.add_route_delete(self.delete_file_system)
        self.add_route_get   (self.tree_view         )
        self.add_route_get   (self.folder_structure  )
