"""
SQL Operations allowed enum.
"""

from enum import StrEnum, unique


@unique
class SQLOperation(StrEnum):
    """
    SQL Operations.
    """

    EQUAL = "="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LIKE = "LIKE"
    ILIKE = "ILIKE"
    NOT_LIKE = "NOT LIKE"
    IN = "IN"
    NOT_IN = "NOT IN"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
