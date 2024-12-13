from fastapi import Request, HTTPException

from cbr_shared.cbr_backend.users.S3_DB__User import S3_DB__User
from cbr_shared.cbr_backend.users.S3_DB__Users            import S3_DB__Users
from cbr_shared.cbr_backend.users.decorators.with_db_user import with_db_user
from cbr_shared.cbr_sites.CBR__Shared_Objects import cbr_shared_objects
from osbot_fast_api.api.Fast_API_Routes                   import Fast_API_Routes
from osbot_utils.utils.Status import status_ok, status_error


class Routes__User__Chats(Fast_API_Routes):
    tag      : str = 'chats'
    db_users : S3_DB__Users

    @with_db_user
    def db_user(self, request: Request):
        db_user = request.state.db_user
        if type(db_user) is not S3_DB__User:
            raise HTTPException(401, "User not found")
        return db_user

    def chats(self, request: Request):
        db_user = self.db_user(request)
        return db_user.user_past_chats()

    def chats_table(self, request: Request):                # todo: legacy, this logic needs to be moved to the WebC
        db_user = self.db_user(request)
        return db_user.user_past_chats__in_table()

    def chat_data_legacy(self, chat_path:str, request: Request):
        self.db_user(request)                                   # make sure user is valid
        chat_data = cbr_shared_objects.s3_db_chat_threads().chat_completion_data(chat_path)
        if chat_data:
            return status_ok(data=chat_data)
        return status_error(message= "Chat not found")

    def chat_add(self, request: Request, chat_path):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats__add_chat(chat_path)
        return False

    def chats_clear(self,request: Request):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats__clear()



    def setup_routes(self):
        self.add_route_get   (self.chat_data_legacy)
        self.add_route_post  (self.chat_add    )
        self.add_route_get   (self.chats       )
        self.add_route_get   (self.chats_table )
        self.add_route_delete(self.chats_clear )

