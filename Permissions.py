from enum import Enum
from Users import UserType as UT

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
    CREATE_REQUEST = 3
    RESET_PASSWORD = 4
    CREATE_QUOTE = 5


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
    user_permissions = {
        FunctionTypes.MAKE_USER: {UT.ADMIN: True},
        FunctionTypes.LOGIN: {UT.ADMIN: True, UT.CLIENT: True, UT.SUPPLIER: True, UT.MANAGER: True},
        FunctionTypes.ASSIGN_CLI_TO_MANA: {UT.ADMIN: True,UT.MANAGER: True},
        FunctionTypes.CREATE_REQUEST: {UT.CLIENT: True},
        FunctionTypes.RESET_PASSWORD: {UT.ADMIN: True},
        FunctionTypes.CREATE_REQUEST: {UT.SUPPLIER:True}
    }