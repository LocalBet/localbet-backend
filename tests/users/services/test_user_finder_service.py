"""
Test user finder domain service.
"""

from pytest import mark, raises as assert_raises

from backend.users.errors import UserNotFoundError
from backend.users.services import UserFinderService
from tests.shared.models.mothers import ConditionMother
from tests.users.actions import MockUserActions
from tests.users.models.mothers import UserMother


@mark.unit_testing
def test_user_finder() -> None:
    """
    Test user finder happy path.
    """
    user_actions = MockUserActions()
    user_finder_service = UserFinderService(action=user_actions)

    expected_user = UserMother.create()
    user_actions.prepare_return_search(user=expected_user)

    find_conditions = [ConditionMother.create()]

    assert [expected_user] == user_finder_service.find(conditions=find_conditions)
    user_actions.assert_search_method_called(conditions=find_conditions)


@mark.unit_testing
def test_user_finder_with_no_user_found() -> None:
    """
    Test user finder with no user found and raises UserNotFoundError.
    """
    user_actions = MockUserActions()
    user_finder_service = UserFinderService(action=user_actions)

    user_actions.prepare_return_search(user=None)
    find_conditions = [ConditionMother.create()]

    with assert_raises(expected_exception=UserNotFoundError):
        user_finder_service.find(conditions=find_conditions)

    user_actions.assert_search_method_called(conditions=find_conditions)
