from starlette.requests import Request

from cbr_shared.cbr_backend.session.CBR__Session_Auth   import cbr_session_auth
from cbr_shared.cbr_backend.users.DB_User               import DB_User
from cbr_shared.cbr_backend.users.DB_Users              import DB_Users
from cbr_user_data.user_data.decorators.with_db_user    import with_db_user
from osbot_fast_api.api.Fast_API_Routes                 import Fast_API_Routes


class Routes__Session(Fast_API_Routes):
    tag     : str = 'session'
    db_users: DB_Users

    @with_db_user
    def user_profile(self, request: Request):
        db_user = request.state.db_user
        return db_user.user_profile()

    def logged_in(self, request: Request):
        return request.session.get('logged_in')

    def setup_routes(self):
        self.add_route_get(self.logged_in   )
        self.add_route_get(self.user_profile)
        return self