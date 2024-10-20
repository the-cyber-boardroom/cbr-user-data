from functools                                          import wraps
from fastapi                                            import Request
from cbr_shared.cbr_backend.session.CBR__Session_Auth   import cbr_session_auth


def with_db_user(func):
    @wraps(func)
    def wrapper(self, request: Request, *args, **kwargs):
        user_details = cbr_session_auth.session_data__from_cookie(request)
        if user_details:
            user_id = user_details.get('data', {}).get('sub')
            db_user = self.db_users.db_user(user_id)
            if db_user:
                request.state.db_user = db_user                                 # Attach db_user to request.state
                return func(self, request, *args, **kwargs)
        return {"error": "User not authenticated"}                              # Handle the case where db_user is not found
    return wrapper
