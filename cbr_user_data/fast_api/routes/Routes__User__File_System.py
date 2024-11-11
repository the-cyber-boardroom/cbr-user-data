from dataclasses                                            import dataclass
from typing                                                 import Dict, Any, Union
from fastapi                                                import Body
from starlette.requests                                     import Request
from starlette.responses                                    import PlainTextResponse
from cbr_shared.cbr_backend.files.User__File__System        import User__File__System
from cbr_shared.cbr_backend.users.decorators.with_db_user   import with_db_user
from cbr_user_data.fast_api.models.Model__API__User__Add_File import Model__API__User__Add_File
from osbot_fast_api.api.Fast_API_Routes                     import Fast_API_Routes
from osbot_utils.base_classes.Type_Safe                     import Type_Safe
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from osbot_utils.utils.Status                               import status_ok

SWAGGER_EXAMPLE__Model__API__User__Add_File  = Body(..., example=dict(file_name  ='an_file.txt'    ,
                                                                             file_bytes = b'file_contents',
                                                                             folder_id  = ''              ))
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
    def delete_file_system(self,request: Request):                      # todo: we really should add an 'are you sure?" check there :)
        file_system = self.file_system(request)
        file_system.delete()
        return status_ok(message="File System deleted")

    @with_db_user
    def files(self, request: Request):
        file_system = self.file_system(request)
        return file_system.folder_structure__files()

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
        self.add_route_delete(self.delete_file_system)
        self.add_route_get   (self.files             )
        self.add_route_get   (self.folder_structure  )
        self.add_route_get   (self.json_view         )
        self.add_route_get   (self.tree_view         )
