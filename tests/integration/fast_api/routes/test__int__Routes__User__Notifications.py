from unittest                                                               import TestCase
from starlette.requests                                                     import Request
from fastapi                                                                import HTTPException
from cbr_shared.cbr_backend.user_notifications.Model__User__Notification    import Model__User__Notification
from cbr_shared.cbr_backend.user_notifications.User__Notifications          import User__Notifications
from cbr_shared.cbr_backend.users.Temp_User_Request                         import Temp_User_Request
from cbr_shared.cbr_backend.users.decorators.with_db_user                   import with_db_user
from cbr_user_data.fast_api.routes.Routes__User__Notifications              import Routes__User__Notifications
from osbot_utils.utils.Json                                                 import str_to_json
from osbot_utils.utils.Misc                                                 import random_text
from osbot_utils.utils.Threads                                              import invoke_async
from tests.integration.user_data__objs_for_tests                            import user_data__assert_local_stack


class test__int__Routes__User__Notifications(TestCase):
    @classmethod
    def setUpClass(cls):
        user_data__assert_local_stack()
        cls.temp_user_request         = Temp_User_Request().create()
        cls.temp_user                 = cls.temp_user_request.temp_user
        cls.db_session                = cls.temp_user_request.temp_db_session
        cls.request                   = cls.temp_user_request.request
        cls.routes_user_notifications = Routes__User__Notifications()
        cls.user_notifications        = User__Notifications(db_user=cls.temp_user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_user_request.delete()
        assert cls.temp_user .exists() is False
        assert cls.db_session.exists() is False

    def setUp(self):
        assert self.user_notifications.delete_all() is True


    def test_setUpClass(self):
        assert self.temp_user .exists() is True
        assert self.db_session.exists() is True
        assert self.request.headers.get('cookie') == f'CBR__SESSION_ID__ACTIVE={self.db_session.session_id}'

        @with_db_user
        def get_user(_, request:Request):
            return request.state.db_user

        db_user = get_user(None, request=self.request)

        assert db_user.json()  == self.temp_user.json()
        assert db_user.user_id == self.temp_user.user_id
        assert db_user.user_id == self.db_session.session_config__user_id()



    def test_create_notification(self):
        message = random_text("test-message")
        result  = self.routes_user_notifications.create(self.request, message=message)


        user_notifications = self.routes_user_notifications.user_notifications(self.request)
        notifications     = user_notifications.all()
        notification      = notifications[0]
        assert len(notifications)       == 1
        assert notification.message == message

        assert result == {"status": "ok", "message": "Notification created", 'data': {'notification': notification.json()}}

    def test_delete_notification(self):
        message = random_text("to-delete")                                                                  # First create a notification
        self.routes_user_notifications.create(self.request, message=message)

        user_notifications = self.routes_user_notifications.user_notifications(self.request)
        notification_id = user_notifications.all()[0].notification_id

        result = self.routes_user_notifications.delete(self.request, notification_id=notification_id)       # Now delete it
        assert result == {"status": "ok", "message": "Notification deleted"}
        assert len(user_notifications.all()) == 0

    def test_current_notifications(self):
        messages = [random_text("msg-1"), random_text("msg-2")]
        for message in messages:
            self.routes_user_notifications.create(self.request, message=message)

        result = self.routes_user_notifications.current(self.request)
        assert len(result["notifications"]) == 2
        assert {n["message"] for n in result["notifications"]} == set(messages)

    def test_all_notifications(self):
        messages = [random_text("msg-1"), random_text("msg-2")]
        for message in messages:
            self.routes_user_notifications.create(self.request, message=message)

        result = self.routes_user_notifications.all(self.request)
        assert len(result["notifications"]) == 2
        assert {n["message"] for n in result["notifications"]} == set(messages)


    def test_live_stream(self):
        wait_count = 2                                                                          # Reduced count for testing
        wait_time  = 0.1                                                                        # Faster wait time for testing
        message    = random_text("stream-test")                                                 # Random message to send
        response   = self.routes_user_notifications.create(self.request, message=message)       # Create a notification first

        assert response.get('status') == 'ok'

        notification      = response.get('data').get('notification')                            # Get notification from response
        user_notification = Model__User__Notification.from_json(notification)

        stream = self.routes_user_notifications.live_stream(self.request,                       # Start the stream with test parameters
                                                          wait_count=wait_count,
                                                          wait_time=wait_time)

        def get_notifications_from_stream():
            notifications_received = []
            async def process_stream():
                async for data in stream.body_iterator:
                    notifications_received.append(str_to_json(data))
                return notifications_received
            return invoke_async(process_stream())

        events = get_notifications_from_stream()                                                # Get all events from stream

        assert len(events) == 3                                                                 # Verify we got all expected events

        heartbeat_1, notification_event, heartbeat_2 = events                                   # Unpack events for clarity

        # Verify first heartbeat
        assert heartbeat_1['event'] == 'heartbeat'
        assert heartbeat_1['count'] == 2
        assert isinstance(heartbeat_1['data']['timestamp'], float)

        # Verify notification event
        assert notification_event['event'] == 'notification'
        assert notification_event['count'] == 2
        assert notification_event['data']['message'] == message
        assert notification_event['data']['notification_id'] == user_notification.notification_id
        assert notification_event['data']['user_delivered'] is False
        assert notification_event['data']['user_acknowledged'] is False

        # Verify second heartbeat
        assert heartbeat_2['event'] == 'heartbeat'
        assert heartbeat_2['count'] == 1
        assert isinstance(heartbeat_2['data']['timestamp'], float)

        # Verify notification was marked as delivered after stream
        current_notifications = self.routes_user_notifications.current(self.request)

        assert len(current_notifications["notifications"]) == 1                                                 # Should be empty as notification was delivered
        assert current_notifications["notifications"][0]["user_delivered"] is True

    def test_invalid_operations(self):
        with self.assertRaises(HTTPException) as context:                                                       # Delete non-existent notification
            self.routes_user_notifications.delete(self.request, notification_id="non-existent")
        assert context.exception.status_code == 404


        result = self.routes_user_notifications.create(self.request, message="")                                # Create with empty message
        assert result["status"] == "ok"                                                                         # Empty messages are allowed

        long_message = "a" * 1000                                                                               # Create with very long message
        result = self.routes_user_notifications.create(self.request, message=long_message)
        assert result["status"] == "ok"

