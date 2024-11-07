from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes


class Routes__User__Files(Fast_API_Routes):
    tag: str = 'files'

    def tree_view(self):
        return 'will go here'

    def setup_routes(self):
        self.add_route_get(self.tree_view)