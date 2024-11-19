import json
from unittest                                                               import TestCase
from starlette.requests                                                     import Request
from fastapi                                                                import HTTPException
from cbr_shared.cbr_backend.user_notifications.Model__User__Notification    import Model__User__Notification
from cbr_shared.cbr_backend.user_notifications.User__Notifications          import User__Notifications
from cbr_shared.cbr_backend.users.Temp_User_Request                         import Temp_User_Request
from cbr_shared.cbr_backend.users.decorators.with_db_user                   import with_db_user
from cbr_user_data.fast_api.routes.Routes__User__Notifications              import Routes__User__Notifications
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

    # todo: use osbot_utils async invoke methods
    def test_live_stream(self):
        # Helper to consume stream for testing
        async def get_next_event(stream):
            async for data in stream.body_iterator:

                if "event: notifications" in data:
                    return json.loads(data.split("data: ")[1])
            return None


        message           = random_text("stream-test")                                            # Create a notification
        response          = self.routes_user_notifications.create(self.request, message=message)
        notification      = response.get('data').get('notification')
        user_notification = Model__User__Notification.from_json(notification)
        stream            = invoke_async(self.routes_user_notifications.live_stream(self.request))  # Start the stream
        notifications     = invoke_async(get_next_event(stream))  # Get the first notification event

        assert response.get('status')      == 'ok'
        assert user_notification.message   == message                       # confirm message is correct
        assert notifications               == [user_notification.json()]
        assert notifications[0]["message"] == message                       # confirm message is correct

        # todo: find way to do this, since is a bit harder to test here, since the event loop that was executed in get_next_event(stream) is not running anymore
        # Verify notifications are marked as delivered
        #user_notifications = self.routes_user_notifications.user_notifications(self.request)
        #all_notifications = user_notifications.all()
        #assert all(n.user_delivered for n in all_notifications)

    def test_invalid_operations(self):
        with self.assertRaises(HTTPException) as context:                                                       # Delete non-existent notification
            self.routes_user_notifications.delete(self.request, notification_id="non-existent")
        assert context.exception.status_code == 404


        result = self.routes_user_notifications.create(self.request, message="")                                # Create with empty message
        assert result["status"] == "ok"                                                                         # Empty messages are allowed

        long_message = "a" * 1000                                                                               # Create with very long message
        result = self.routes_user_notifications.create(self.request, message=long_message)
        assert result["status"] == "ok"

