from starlette.requests                                     import Request
from cbr_shared.cbr_backend.users.S3_DB__Users              import S3_DB__Users
from cbr_shared.cbr_backend.users.decorators.with_db_user   import with_db_user
from osbot_fast_api.api.Fast_API_Routes                     import Fast_API_Routes

class Routes__Session(Fast_API_Routes):
    tag     : str = 'session'
    db_users: S3_DB__Users

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