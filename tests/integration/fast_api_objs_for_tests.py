from osbot_aws.testing.Temp__Random__AWS_Credentials import Temp_AWS_Credentials

from osbot_utils.utils.Dev import pprint

from osbot_serverless_flows.Serverless_Flows__Server_Config import DEFAULT__SERVERLESS_FLOWS__AWS_ACCOUNT_ID, \
    ENV_NAME__SERVERLESS_FLOWS__USE_LOCAL_STACK, serverless_flows__server_config
from osbot_utils.utils.Env import set_env, in_github_action

from osbot_local_stack.local_stack.Local_Stack                  import Local_Stack
from osbot_serverless_flows.fast_api.Fast_API__Serverless_Flows import Fast_API__Serverless_Flows
from osbot_utils.context_managers.capture_duration              import capture_duration
                                      # todo : see side effects of putting this here

TEST__AWS_ACCOUNT_ID        = '000011110000'

def setup_env_vars():
    Temp_AWS_Credentials().set_vars()
    set_env('AWS_ACCOUNT_ID'                      , TEST__AWS_ACCOUNT_ID)

with capture_duration() as duration:
    setup_env_vars()
    fast_api__local_stack      = Local_Stack().activate()
    fast_api__user_data =  Fast_API__User_Data()
    fast_api__serverless_flows.setup()                                               # setup_server
    client__serverless_flows = fast_api__serverless_flows.client()
    assert fast_api__local_stack.is_local_stack_configured_and_available() is True

print(f"************* DURATION ***********")
print(f"****    {duration.seconds}" )
if in_github_action():
    assert duration.seconds < 5         # give it more time when running in github actions
else:
    assert duration.seconds < 1         # make sure the setup time is less than 1 second


def ensure_browser_is_installed():
    from osbot_serverless_flows.playwright.Playwright__Serverless import Playwright__Serverless
    playwright_browser = Playwright__Serverless()
    playwright_browser.browser__install()