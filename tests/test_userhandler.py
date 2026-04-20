# Tests for userhandler.py
# PullA Vibes
# Tests cover User dataclass field storage for visitors and staff,
# and UserManager authentication — valid credentials, wrong password,
# unknown user, empty input, and overwriting an existing user.

import sys
import pytest

sys.path.insert(0, "..")

from userhandler import User, UserManager


class TestUser:
    def test_visitor_user_fields(self):
        # User should store all fields correctly for a visitor
        user = User("alice", "pass123", "visitor", room_type="basic", room_id=101)
        assert user.username == "alice"
        assert user.password == "pass123"
        assert user.role == "visitor"
        assert user.room_type == "basic"
        assert user.room_id == 101

    def test_staff_user_no_room(self):
        # A staff user created without room info should have None for room_id and room_type
        user = User("staff", "staffpass", "staff")
        assert user.room_id is None
        assert user.room_type is None

    def test_suite_visitor(self):
        # A visitor assigned to a suite should store suite room_type and correct room_id
        user = User("visitor301", "pass", "visitor", room_type="suite", room_id=301)
        assert user.room_type == "suite"
        assert user.room_id == 301


class TestUserManager:
    def setup_method(self):
        self.manager = UserManager()
        self.manager.add_user(User("visitor101", "visitor123", "visitor", room_id=101, room_type="basic"))
        self.manager.add_user(User("staff", "staff123", "staff"))

    def test_authenticate_valid_visitor(self):
        # Correct visitor credentials should return the visitor User object
        user = self.manager.authenticate("visitor101", "visitor123")
        assert user is not None
        assert user.role == "visitor"

    def test_authenticate_valid_staff(self):
        # Correct staff credentials should return the staff User object
        user = self.manager.authenticate("staff", "staff123")
        assert user is not None
        assert user.role == "staff"

    def test_authenticate_wrong_password(self):
        # Wrong password should return None
        assert self.manager.authenticate("visitor101", "wrongpass") is None

    def test_authenticate_unknown_user(self):
        # A username that does not exist should return None
        assert self.manager.authenticate("ghost", "anything") is None

    def test_authenticate_empty_credentials(self):
        # Empty username and password should return None
        assert self.manager.authenticate("", "") is None

    def test_add_user_overwrite(self):
        # Adding a user with an existing username should replace the old user
        self.manager.add_user(User("visitor101", "newpass", "visitor", room_id=102))
        user = self.manager.authenticate("visitor101", "newpass")
        assert user is not None
        assert user.room_id == 102

    def test_old_password_invalid_after_overwrite(self):
        # The old password should no longer work after a user is overwritten
        self.manager.add_user(User("visitor101", "newpass", "visitor", room_id=102))
        assert self.manager.authenticate("visitor101", "visitor123") is None