"""
test_userhandler.py
# PullA Vibes

Tests for userhandler.py — User, UserManager

Run with: pytest test_userhandler.py -v
"""

import sys
import pytest

from userhandler import User, UserManager


class TestUser:
    def test_visitor_user_fields(self):
        user = User("alice", "pass123", "visitor", room_type="basic", room_id=101)
        assert user.username == "alice"
        assert user.password == "pass123"
        assert user.role == "visitor"
        assert user.room_type == "basic"
        assert user.room_id == 101

    def test_staff_user_no_room(self):
        user = User("staff", "staffpass", "staff")
        assert user.room_id is None
        assert user.room_type is None

    def test_suite_visitor(self):
        user = User("visitor301", "pass", "visitor", room_type="suite", room_id=301)
        assert user.room_type == "suite"
        assert user.room_id == 301


class TestUserManager:
    def setup_method(self):
        self.manager = UserManager()
        self.manager.add_user(User("visitor101", "visitor123", "visitor", room_id=101, room_type="basic"))
        self.manager.add_user(User("staff", "staff123", "staff"))

    def test_authenticate_valid_visitor(self):
        user = self.manager.authenticate("visitor101", "visitor123")
        assert user is not None
        assert user.role == "visitor"

    def test_authenticate_valid_staff(self):
        user = self.manager.authenticate("staff", "staff123")
        assert user is not None
        assert user.role == "staff"

    def test_authenticate_wrong_password(self):
        assert self.manager.authenticate("visitor101", "wrongpass") is None

    def test_authenticate_unknown_user(self):
        assert self.manager.authenticate("ghost", "anything") is None

    def test_authenticate_empty_credentials(self):
        assert self.manager.authenticate("", "") is None

    def test_add_user_overwrite(self):
        self.manager.add_user(User("visitor101", "newpass", "visitor", room_id=102))
        user = self.manager.authenticate("visitor101", "newpass")
        assert user is not None
        assert user.room_id == 102

    def test_old_password_invalid_after_overwrite(self):
        self.manager.add_user(User("visitor101", "newpass", "visitor", room_id=102))
        assert self.manager.authenticate("visitor101", "visitor123") is None