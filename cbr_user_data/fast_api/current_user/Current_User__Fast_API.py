from cbr_athena.athena__fastapi.current_user.routes.Routes__User_Data import Routes__User_Data
from osbot_fast_api.api.Fast_API import Fast_API


class Current_User__Fast_API(Fast_API):
    base_path     : str  = '/current-user'
    default_routes: bool = False

    def setup_routes(self):
        self.add_routes(Routes__User_Data)