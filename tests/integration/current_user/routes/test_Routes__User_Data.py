from unittest                                                         import TestCase

import pytest
from fastapi                                                          import Request
from cbr_athena.athena__fastapi.current_user.routes.Routes__User_Data import Routes__User_Data
from osbot_aws.aws.s3.S3 import S3


class test_Routes__User_Data(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.local_stack      = cbr_athena_local_stack
        cls.routes_user_data = Routes__User_Data()

    def find_valid_session(self):
        with S3() as _:
            s3_bucket = 'cyber-boardroom-470426667096-server-data'
            folder    = 'users_sessions'
            sessions = _.folder_list(s3_bucket=s3_bucket, parent_folder=folder)
            if len(sessions) >0:
                return sessions[0]


    def test_user_details(self):
        user_session = self.find_valid_session()
        if user_session:
            cbr_token    = user_session
            cookie_value = f'CBR_TOKEN={cbr_token}'.encode('utf-8')
            scope        = dict(type='http', method='GET', headers=[ (b'cookie', cookie_value)])
            request      = Request(scope)
            result       = self.routes_user_data.user_details(request)