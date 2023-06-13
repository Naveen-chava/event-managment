from enum import IntEnum
from typing import List, Tuple, Optional


class BaseIntEnum(IntEnum):
    @classmethod
    def get_choices(cls) -> List[Tuple]:
        return [(item.value, item.name) for item in cls]

    @classmethod
    def get_string_for_obj(cls, value: int) -> Optional[str]:
        """
        This class method returns the string representation of an enum integer value if it exists in the enum.

        Eg:
        UserStatusType.get_string_for_type(1) returns UserStatusType.ONLINE
        UserGenderType.get_string_for_type(99) returns DO_NOT_WANT_TO_DISCOLSE

        """
        for item in cls:
            if item.value == value:
                return item.name
        return None

    @classmethod
    def get_obj_for_string(cls, type: str) -> "BaseIntEnum":
        """
        This method returns the enum object for the given string representation.

        Eg:
        UserStatusType.get_obj_for_string("ONLINE") returns UserStatusType.ONLINE
        UserGenderType.get_obj_for_string("MALE") returns UserGenderType.MALE

        Throws KeyError if the input string is invalid
        """
        return cls.__members__[type]


class Length:
    EVENT_NAME = 64
    CATEGORY_NAME = 64
    LOCATION_NAME = 64
    ADDRESS = 255
    CITY = 64
    STATE = 64


class EventType(BaseIntEnum):
    ONLINE = 1
    OFFLINE = 2


class EventStatusType(BaseIntEnum):
    CREATED = 1
    COMPLETED = 2
    CANCELLED = 3


class EventPriceType(BaseIntEnum):
    ECONOMY = 1
    PREMIUM = 2

    SAME = 99  # same prices for all the tickets


class EventCategoryType(BaseIntEnum):
    # all the categories should be added here
    DANCE = 1
    SINGING = 2
    MOVIE = 3
    SPORTS = 4
    MAGIC_SHOW = 5
    EXHIBITION = 6

    OTHERS = 999
