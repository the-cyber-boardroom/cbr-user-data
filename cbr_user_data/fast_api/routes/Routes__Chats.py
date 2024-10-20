from fastapi                                                import Request
from cbr_shared.cbr_backend.session.CBR__Session_Auth       import cbr_session_auth
from cbr_shared.cbr_backend.users.DB_Users                  import DB_Users
from osbot_fast_api.api.Fast_API_Routes                     import Fast_API_Routes


def user_profile(self, db_user):
    return db_user.user_profile()

class Routes__Chats(Fast_API_Routes):
    tag      : str = 'chats'
    db_users : DB_Users

    def db_user(self, request: Request):
        user_details = self.user_details(request)
        if user_details:
            user_id = user_details.get('data', {}).get('sub')
            db_user = self.db_users.db_user(user_id)
            return db_user

    # def user_details(self, request: Request):
    #     return cbr_session_auth.session_data__from_cookie(request)

    def user_profile(self, request: Request):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_profile()
        return {}

    def chats(self, request: Request):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats()
        return {}

    def chats_table(self, request: Request):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats__in_table()
        return {}

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
        #self.add_route_get(self.user_details)
        self.add_route_get(self.user_profile)
        self.add_route_get(self.chat_add    )
        self.add_route_get(self.chats       )
        self.add_route_get(self.chats_table )
        self.add_route_get(self.chats_clear )

