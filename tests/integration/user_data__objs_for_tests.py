from osbot_aws.testing.Temp__Random__AWS_Credentials import Temp_AWS_Credentials
from osbot_utils.utils.Env                           import set_env, in_github_action
from osbot_local_stack.local_stack.Local_Stack       import Local_Stack
from osbot_utils.context_managers.capture_duration   import capture_duration
from cbr_user_data.fast_api.User_Data__Fast_API      import User_Data__Fast_API

TEST__AWS_ACCOUNT_ID        = '000011110000'

def setup_env_vars():
    Temp_AWS_Credentials().set_vars()
    set_env('AWS_ACCOUNT_ID'  , TEST__AWS_ACCOUNT_ID) # todo: move this to the Temp_AWS_Credentials class

with capture_duration() as duration:
    setup_env_vars()
    fast_api__local_stack       = Local_Stack().activate()
    fast_api__user_data         = User_Data__Fast_API().setup()
    fast_api__user_data__app    = fast_api__user_data.app()
    fast_api__user_data__client = fast_api__user_data.client()
    assert fast_api__local_stack.is_local_stack_configured_and_available() is True

print(f"************* DURATION ***********")
print(f"****    {duration.seconds}" )
if in_github_action():
    assert duration.seconds < 5         # give it more time when running in github actions
else:
    assert duration.seconds < 1         # make sure the setup time is less than 1 second
