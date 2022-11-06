import enum


class Permissions(enum.Enum):
    All = "all"
    All_value = 1
    User = "user"
    User_value = 2
    Subscriber = "subscriber"
    Subscriber_value = 3

    @classmethod
    def get_permission_value(cls, permission: str):
        permission = permission.lower()
        if permission == cls.All.value:
            return 1
        if permission == cls.User.value:
            return 2
        if permission == cls.Subscriber.value:
            return 3
