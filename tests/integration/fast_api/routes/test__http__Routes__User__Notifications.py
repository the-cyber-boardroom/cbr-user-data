import pytest
import requests
from unittest                                           import TestCase
from fastapi                                            import FastAPI
from cbr_shared.cbr_backend.users.Temp_User_Request     import Temp_User_Request
from cbr_user_data.fast_api.User_Data__Fast_API         import User_Data__Fast_API
from cbr_user_data.utils.Version                        import version__cbr_user_data
from osbot_fast_api.utils.Fast_API_Server               import Fast_API_Server
from osbot_fast_api.utils.Version                       import version__osbot_fast_api
from osbot_utils.context_managers.print_duration        import print_duration
from osbot_utils.utils.Objects                          import dict_to_obj, __
from tests.integration.user_data__objs_for_tests        import user_data__assert_local_stack, fast_api__user_data__app, \
    fast_api__user_data

class test__http__Routes__User__Notifications(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with print_duration(action_name='setUpClass'):
            user_data__assert_local_stack()
            cls.fast_api__user_data = fast_api__user_data
            cls.fast_api_server     = Fast_API_Server(app=fast_api__user_data__app)
            cls.fast_api_server.start()

            cls.temp_user_request = Temp_User_Request().create()
            cls.temp_user         = cls.temp_user_request.temp_user
            cls.db_session        = cls.temp_user_request.temp_db_session
            cls.request           = cls.temp_user_request.request

            assert cls.fast_api_server.is_port_open() is True

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fast_api_server.stop()
        cls.temp_user_request.delete()
        assert cls.fast_api_server.is_port_open() is False
        assert cls.temp_user      .exists      () is False
        assert cls.db_session     .exists      () is False

    def setUp(self):
        with print_duration(action_name='setUp'):
            all_notifications = self.request_with_user__get('notifications/all')                                # Clean up notifications before each test
            for notification in all_notifications.notifications:
                delete_path = f'notifications/delete?notification_id={notification.notification_id}'
                self.request_with_user__delete(delete_path)

    def test__setUpClass(self):
        assert type(fast_api__user_data     )     is User_Data__Fast_API
        assert type(fast_api__user_data__app)     is FastAPI
        assert type(self.fast_api_server    )     is Fast_API_Server

        assert '/notifications/all'               in fast_api__user_data.routes_paths()
        assert self.temp_user.exists()            is True
        assert self.db_session.exists()           is True
        assert self.request.headers.get('cookie') == f'CBR__SESSION_ID__ACTIVE={self.db_session.session_id}'

    def test_version(self):
        assert self.fast_api_server.requests_get('/config/version').json() == {'version': version__osbot_fast_api }
        assert self.fast_api_server.requests_get('/info/version'  ).json() == {'version': version__cbr_user_data  }

    def test__http___with_invalid_cookie_values(self):
        path           = 'notifications/all'
        url            = self.fast_api_server.url() + path
        expected_error = { 'data'  : None                                              ,
                           'error' : None                                              ,
                           'message': 'Session not found from the current request data',
                           'status' : 'error'
                           }
        cookies    = {'NOT_THE_SESSION_ID_NAME': self.db_session.session_id}
        response_1 = requests.get(url)                                          # Send the request without cookies
        response_2 = requests.get(url, cookies=cookies)                         # Send the request with an invalid cookie name

        assert response_1.status_code == 200                                    # BUG: this should be 401
        assert response_2.status_code == 200                                    # BUG: this should be 401
        assert response_1.json() == expected_error
        assert response_2.json() == expected_error
        assert response_1.json() == expected_error

    # Requests helper methods

    def request_with_user__get(self, path):
        url     = self.fast_api_server.url() + path
        cookies = {'CBR__SESSION_ID__ACTIVE': self.db_session.session_id}
        response = requests.get(url, cookies=cookies)                   # Send the request with the cookie
        assert response.status_code == 200
        return dict_to_obj(response.json())

    def request_with_user__post(self, path):
        url         = self.fast_api_server.url() + path
        cookies     = {'CBR__SESSION_ID__ACTIVE': self.db_session.session_id}
        response    = requests.post(url, cookies=cookies)
        assert response.status_code == 200
        return dict_to_obj(response.json())

    def request_with_user__delete(self, path, expected_status_code=200):
        url = self.fast_api_server.url() + path
        cookies = {'CBR__SESSION_ID__ACTIVE': self.db_session.session_id}
        response = requests.delete(url, cookies=cookies)
        assert response.status_code == expected_status_code
        return dict_to_obj(response.json())

    # API methods

    def test__http__notifications__all(self):
        path    = 'notifications/all'
        assert self.request_with_user__get(path)  == __(notifications=[])

    def test__http__notifications__create(self):
        path     = f'notifications/create?message=test-notification'                    # Test creating a notification with valid message
        response = self.request_with_user__post(path)
        assert response.status                    == 'ok'
        assert response.message                   == 'Notification created'
        assert response.data.notification.message == 'test-notification'


        all_notifications = self.request_with_user__get('notifications/all')            # Verify the notification was created by fetching all notifications
        assert len(all_notifications.notifications)      == 1
        assert all_notifications.notifications[0].message == 'test-notification'

    def test__http__notifications__create__edge_cases(self):
        path                     = f'notifications/create?message='                     # Test empty message
        response                 = self.request_with_user__post(path)
        assert response.status  == 'ok'
        assert response.message == 'Notification created'

        long_message             = 'a' * 1000                                            # Test long message
        path                     = f'notifications/create?message={long_message}'
        response                 = self.request_with_user__post(path)
        assert response.status                    == 'ok'
        assert response.message                   == 'Notification created'
        assert response.data.notification.message == long_message

    def test__http__notifications__delete(self):
        create_path     = f'notifications/create?message=to-delete'                     # First create a notification
        create_response = self.request_with_user__post(create_path)
        notification_id = create_response.data.notification.notification_id

        delete_path     = f'notifications/delete?notification_id={notification_id}'     # Now delete it
        delete_response = self.request_with_user__delete(delete_path)
        assert delete_response.status == 'ok'
        assert delete_response.message == 'Notification deleted'

        all_notifications = self.request_with_user__get('notifications/all')            # Verify it was deleted
        assert len(all_notifications.notifications) == 0

    def test__http__notifications__delete_invalid(self):
        path        = f'notifications/delete?notification_id=non-existent'                     # Try to delete non-existent notification
        response    = self.request_with_user__delete(path, expected_status_code=404)
        assert response == __(detail='Notification not found')

    def test__http__notifications__current(self):
        messages = ['current-msg-1', 'current-msg-2']                                   # Create two notifications
        for message in messages:
            create_path = f'notifications/create?message={message}'
            self.request_with_user__post(create_path)

        current_notifications = self.request_with_user__get('notifications/current')    # Get current notifications
        assert len(current_notifications.notifications) == 2
        received_messages = {n.message for n in current_notifications.notifications}
        assert received_messages == set(messages)

    def test__http__notifications__live_stream(self):
        url     = self.fast_api_server.url() + 'notifications/live-stream?wait_count=2&wait_time=0.1'
        cookies = {'CBR__SESSION_ID__ACTIVE': self.db_session.session_id}
        response = requests.get(url, cookies=cookies, stream=True)
        assert response.status_code == 200
        print()
        streamed_data = []
        for chunk in response.iter_content(chunk_size=1024):  # Process in 1KB chunks
            if chunk:  # Only process non-empty chunks
                streamed_data.append(chunk)

        assert len(streamed_data) == 2

    # @pytest.mark.skip("needs aiohttp")
    # def test__http__notifications__live_stream(self):
    #     import asyncio
    #     import aiohttp
    #
    #     async def get_stream_data():
    #         url = self.fast_api_server.url() + 'notifications/live-stream'
    #         cookies = {'CBR__SESSION_ID__ACTIVE': self.db_session.session_id}
    #
    #         async with aiohttp.ClientSession(cookies=cookies) as session:
    #             async with session.get(url) as response:
    #                 assert response.status == 200
    #                 data = await response.content.read(200)  # Read first chunk
    #                 return data.decode()
    #
    #     # Create a notification
    #     message = 'stream-test-message'
    #     create_path = f'notifications/create?message={message}'
    #     create_response = self.request_with_user__post(create_path)
    #
    #     # Get stream data
    #     stream_data = asyncio.run(get_stream_data())
    #
    #     # Verify we received SSE data
    #     assert 'event: notifications' in stream_data
    #     assert message in stream_data




