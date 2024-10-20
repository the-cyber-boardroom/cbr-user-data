from starlette.requests import Request

from cbr_user_data.user_data.decorators.with_db_user import with_db_user
from osbot_fast_api.api.Fast_API_Routes              import Fast_API_Routes


class Routes__User(Fast_API_Routes):
    tag: str = 'user'

    @with_db_user
    def user_profile(self, request: Request):
        return "here"
        db_user = request.state.db_user
        return db_user.user_profile()

    def setup_routes(self):
        self.add_route_get(self.user_profile)
        return self