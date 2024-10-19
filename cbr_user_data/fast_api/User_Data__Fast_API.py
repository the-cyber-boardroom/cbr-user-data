from osbot_fast_api.api.Fast_API                        import Fast_API
from cbr_user_data.fast_api.routes.Routes__Info         import Routes__Info
from cbr_user_data.fast_api.routes.Routes__Chats        import Routes__Chats


class User_Data__Fast_API(Fast_API):
    base_path  : str  = '/user-data'
    enable_cors: bool = True

    def setup_routes(self):
        self.add_routes(Routes__Info )
        self.add_routes(Routes__Chats)