from enum import Enum
import Users

class FunctionTypes(Enum):
    MAKE_USER = 0 
    LOGIN = 1

# class Permissions:
#     user_permissions = { # Make dictionary
#         FunctionTypes.MAKE_USER: [False, False, False, False, True],
#         FunctionTypes.LOGIN: [True, True, True, True, True]
#     }

class Permissions:
    user_permissions = { # Make dictionary
        FunctionTypes.MAKE_USER: {Users.UserType.ADMIN: True},
        FunctionTypes.LOGIN: {Users.UserType.ADMIN: True, Users.UserType.CLIENT: True, Users.UserType.SUPPLIER: True, Users.UserType.MANAGER: True}
    }