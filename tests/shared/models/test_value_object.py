"""
Test value object module.
"""

from typing_extensions import override

from pytest import mark, raises as assert_raises

from backend.shared.models import ValueObject


class SimpleValueObject(ValueObject[int]):
    """
    SimpleValueObject value object class.
    """

    @override
    def _validate(self, value: int) -> None:
        """
        Validate the value object value.

        Args:
            value (int): Value object value.
        """
        pass


@mark.unit_testing
def test_value_object_slots() -> None:
    """
    Test the slots of a value object.
    """
    assert SimpleValueObject.__slots__ == ('_value',)


@mark.unit_testing
def test_value_object_detailed_string_representation() -> None:
    """
    Test the detailed string representation of a value object.
    """
    value_object = SimpleValueObject(value=1)

    assert repr(value_object) == f'{value_object.__class__.__name__}(value=1)'


@mark.unit_testing
def test_value_object_string_representation() -> None:
    """
    Test the string representation of a value object.
    """
    assert str(object=SimpleValueObject(value=1)) == '1'


@mark.unit_testing
def test_value_object_hash() -> None:
    """
    Test the hash of a value object.
    """
    assert hash(SimpleValueObject(value=1)) == hash(1)


@mark.unit_testing
def test_value_object_equality_comparison() -> None:
    """
    Test that two value objects are equal if their values are equal.
    """
    value_object_1 = SimpleValueObject(value=1)
    value_object_2 = SimpleValueObject(value=1)
    value_object_3 = SimpleValueObject(value=2)

    assert value_object_1 == value_object_2
    assert value_object_1 != value_object_3


@mark.unit_testing
def test_value_object_equality_comparison_different_types() -> None:
    """
    Test that a value object is not equal to an object of a different type.
    """
    assert SimpleValueObject(value=1).__eq__(1) == NotImplemented


@mark.unit_testing
def test_value_object_cannot_modify_value() -> None:
    """
    Test that a value object value cannot be modified after initialization.
    """
    value_object = SimpleValueObject(value=1)

    with assert_raises(
        expected_exception=AttributeError,
        match='Cannot modify attribute "value" of immutable instance',
    ):
        value_object.value = 2  # type: ignore[misc]


@mark.unit_testing
def test_value_object_cannot_modify_protected_value() -> None:
    """
    Test that a value object protected value cannot be modified after initialization.
    """
    value_object = SimpleValueObject(value=1)

    with assert_raises(
        expected_exception=AttributeError,
        match='Cannot modify attribute "_value" of immutable instance',
    ):
        value_object._value = 2 # pyright: ignore[reportPrivateUsage]


@mark.unit_testing
def test_value_object_cannot_add_new_attribute() -> None:
    """
    Test that cannot add a new attribute to a value object after initialization.
    """
    value_object = SimpleValueObject(value=1)

    with assert_raises(
        expected_exception=AttributeError,
        match=f'{value_object.__class__.__name__} object has no attribute "new_attribute"',
    ):
        value_object.new_attribute = 2
