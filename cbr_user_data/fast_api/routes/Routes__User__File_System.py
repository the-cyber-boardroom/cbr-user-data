from fastapi                                                    import Body
from starlette.requests                                         import Request
from starlette.responses                                        import PlainTextResponse
from cbr_shared.cbr_backend.files.User__File__System            import User__File__System
from cbr_shared.cbr_backend.users.decorators.with_db_user       import with_db_user
from cbr_user_data.fast_api.models.Model__API__User__Add_File   import Model__API__User__Add_File, SWAGGER_EXAMPLE__Model__API__User__Add_File
from osbot_fast_api.api.Fast_API_Routes                         import Fast_API_Routes
from osbot_utils.utils.Status                                   import status_ok, status_error


class Routes__User__File_System(Fast_API_Routes):
    tag: str = 'files'

    def file_system(self, request: Request):
        db_user = request.state.db_user
        return User__File__System(db_user=db_user).setup()

    @with_db_user
    def add_file(self, request: Request, model_add_file: Model__API__User__Add_File = SWAGGER_EXAMPLE__Model__API__User__Add_File):
        file_system = self.file_system(request)
        kwargs      = dict(file_name      =  model_add_file.file_name ,
                           file_bytes     =  model_add_file.file_bytes,
                           user_folder_id =  model_add_file.folder_id )
        user_file = file_system.add_file(**kwargs)
        return status_ok(message='File added', data = dict(file_id=user_file.file_id))

    @with_db_user
    def add_folder(self, request: Request, folder_name: str, parent_folder_id: str = None):
        file_system = self.file_system(request)
        folder      = file_system.add_folder(parent_folder_id=parent_folder_id, folder_name=folder_name)
        return status_ok(message='folder created', data=dict(folder_id=folder.folder_id))

    @with_db_user
    def delete_file(self, request: Request, file_id:str):
        file_system = self.file_system(request)
        if file_system.delete_file(file_id):
            return status_ok(message="File deleted")
        return status_error(message="File not found")

    @with_db_user
    def delete_folder(self, request: Request, folder_id: str):
        file_system = self.file_system(request)
        try:
            if file_system.delete_folder(folder_id):
                return status_ok(message="Folder deleted")
            return status_error(message="Folder not found")
        except Exception as error:
            return status_error(message=str(error))

    @with_db_user
    def file_contents(self, request: Request, file_id: str):
        file_system = self.file_system(request)
        file_contents = file_system.file__contents(file_id=file_id)
        if file_contents:
            return status_ok(data=file_contents)
        return status_error(message='file not found')

    @with_db_user
    def files(self, request: Request):
        file_system = self.file_system(request)
        return file_system.folder_structure__files()

    @with_db_user
    def folder(self, request: Request, folder_id: str = None):
        file_system = self.file_system(request)
        folder = file_system.folder(user_folder_id=folder_id)
        if folder:
            return status_ok(data=folder.json())
        return status_error(message='Folder not found')

    @with_db_user
    def folder_structure(self, request: Request):
        file_system = self.file_system(request)
        return file_system.folder_structure().json()

    @with_db_user
    def json_view(self, request: Request):
        file_system = self.file_system(request)
        return file_system.json_view()

    @with_db_user
    def tree_view(self, request: Request):
        file_system = self.file_system(request)
        tree_view   = file_system.tree_view()
        return PlainTextResponse(content=tree_view)


    def setup_routes(self):
        self.add_route_post  (self.add_file          )
        self.add_route_post  (self.add_folder        )
        self.add_route_delete(self.delete_file       )
        self.add_route_delete(self.delete_folder     )
        #self.add_route_delete(self.delete_file_system)
        self.add_route_get   (self.files             )
        self.add_route_get   (self.file_contents     )
        self.add_route_get   (self.folder            )
        self.add_route_get   (self.folder_structure  )
        self.add_route_get   (self.json_view         )
        self.add_route_get   (self.tree_view         )

    # @with_db_user                                                        # todo: find better place to put this, since this feels quite dangerous to have like this
    # def delete_file_system(self, request: Request):                      # todo: we really should add an 'are you sure?" check there :)
    #     file_system = self.file_system(request)
    #     file_system.delete()
    #     return status_ok(message="File System deleted")
