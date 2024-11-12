from starlette.requests                                     import Request
from cbr_shared.cbr_backend.files.User__File__System        import User__File__System
from cbr_shared.cbr_backend.llms.LLM__Content__Actions      import LLM__Content__Actions
from cbr_shared.cbr_backend.users.decorators.with_db_user   import with_db_user
from osbot_fast_api.api.Fast_API_Routes                     import Fast_API_Routes
from osbot_utils.utils.Status                               import status_ok


class Routes__User__File_To_LLMs(Fast_API_Routes):
    tag                 : str                    = 'file-to-llms'
    llm_content_actions : LLM__Content__Actions

    def file_system(self, request: Request):
        db_user = request.state.db_user
        return User__File__System(db_user=db_user).setup()

    @with_db_user
    def file_summary(self, request: Request, file_id: str):
        file_system   = self.file_system(request)
        user_file     = file_system.file(file_id)
        file_summary  = user_file.summary()
        if not file_summary:
            file_contents = user_file.contents().decode()
            file_summary  = self.llm_content_actions.create_summary(user_prompt=file_contents)
            user_file.summary__update(file_summary)
        return status_ok(data=file_summary)

    def setup_routes(self):
        self.add_route_post  (self.file_summary)

