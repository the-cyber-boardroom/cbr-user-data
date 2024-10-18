from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

from tests.unit.utils.test_Version import version__cbr_user_data


class Routes__Info(Fast_API_Routes):
    tag : str = 'info'

    def version(self):
        return {"version" : version__cbr_user_data }

    def setup_routes(self):
        self.add_route_get(self.version)