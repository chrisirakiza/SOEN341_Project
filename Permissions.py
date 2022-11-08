from enum import Enum
import Users

#################################################################################################
# Class: FunctionTypes
# @members: N/A
# @methods: N/A
# 
# This class instantiates a enumeration for the different functionalities of the system.
# Additional functionalities can be added and given an enumeration
# The ENUM values are used to verify user permission to perform a given function/action
#
#################################################################################################

class FunctionTypes(Enum):
    MAKE_USER = 0 
    LOGIN = 1
    ASSIGN_CLI_TO_MANA = 2


#################################################################################################
# Class: Permissions
# @members: user_permission
# @methods: N/A
# 
# This class instantiates a dictionary containing the permissions for a given user type for a given FunctionType ENUM
# To add/remove/modify permissions, add the UserType ENUM in the dictionary of a given FunctionType ENUM (or remove a
# given UserType ENUM)
# The dictionary for a given FunctionType specifies which users are allowed to carry out the given function. The default
# value of FALSE is returned if a given UserType does not appear in the dictionarry of a given FunctionType
#
#################################################################################################

class Permissions:
    user_permissions = { # Make dictionary
        FunctionTypes.MAKE_USER: {Users.UserType.ADMIN: True},
        FunctionTypes.LOGIN: {Users.UserType.ADMIN: True, Users.UserType.CLIENT: True, Users.UserType.SUPPLIER: True, Users.UserType.MANAGER: True},
        FunctionTypes.ASSIGN_CLI_TO_MANA: {Users.UserType.ADMIN: True,Users.UserType.MANAGER: True}
    }