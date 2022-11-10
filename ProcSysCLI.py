import cmd
import System as System
import Users
import CLIParser
from Permissions import FunctionTypes as perm

##################################################################################################
# Class: ProcSysCLI
# @members: ProcurementSystem sys
#
# @methods: do_exit() - Exits System
#           do_user() - CMD line feature that allows listing and generation of user accounts (for authorized users). 
#                       Features the following:
#                       user_list() - lists all users in database
#                       user_make() - Creates a user account
#           do_login() - CMD line feature that allows a user to login to their account
#           
# This class instantiates and CMD line interface for system users to interaxct with the system. 
#
#################################################################################################


class ProcSysCLI(cmd.Cmd):
    intro = "----Procurement System Prototype CLI----"
    sys = System.ProcurementSystem() #Initialize system
    name, userID, pwd, userType = sys.GetUserValues(sys.active_user)
    prompt = f"({userType}) "
    #prompt = f"({sys.active_user.GetType().name}) "


    def do_exit(self, arg):
        '''
        Exits the system
        '''
        return True
    

    def do_test(self, arg):
        '''Test function, used for development purposes'''
        print(">:)")


    def do_user(self, arg):
        '''
        Usage: user [option]
            [option]:
            -l: Lists users
            -m: Make user
                user -m <user-type> <user-name> <password>
                <user-type>:
                    -c: Client
                    -m: Manager
                    -s: Supplier
                <password>:
                    defaults to 'password' if not specifies
        '''
        try:
            commandType = CLIParser.do_user_parse(self, arg)
            if (commandType == "list"):
                print(self.sys.GetListOfUsers())
            elif (commandType == "make"):
                # Check for permissions
                if (not self.sys.CheckPermissions(perm.MAKE_USER)):
                    print("Permission Denied")
                    return
                type, name, pwd = CLIParser.do_user_make_parse(self, arg)
                userID = self.sys.CreateNewUser(type, name, pwd)
                print(f"User of type {type.name} created with ID: {userID}")
        except Exception as e:
            print(f"ERROR: {str(e)}")


    def do_assign(self, arg):
        '''
        Usage: assign <client-id> <manager-id>
            <manager-id>
                -s: uses active user's ID
        '''
        # Check for permissions
        if(not(self.sys.CheckPermissions(perm.ASSIGN_CLI_TO_MANA))):
            print("Permission Denied")
            return
        # Attempt to assign client to manager
        try:
            clientID, managerID = CLIParser.do_assign_parse(self, arg)
            self.sys.AssignManager(clientID, managerID)
            print(f"Client {clientID} successfully assigned to manager {managerID}")
        except Exception as e:
            print(f"ERROR: {str(e)}")
    

    def do_login(self, arg):
        '''
        Usage: login <user-name> <user-password>
        '''
        if (not self.sys.CheckPermissions(perm.LOGIN)):
            print(f"Permission denied")
            return
        try:
            userID, pwd = CLIParser.do_login_parse(self, arg)
            userType = self.sys.SwitchActiveUser(userID, pwd)
            self.prompt = f"({userType}) "
        except Exception as e:
            print(f"ERROR: {str(e)}")


#Main program loop
if __name__ == '__main__':
    ProcSysCLI().cmdloop()