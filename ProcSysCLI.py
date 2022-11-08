import cmd
import System as System
import Users
import Permissions as perm

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
    prompt = f"({sys.active_user.GetType().name}) "


    def do_exit(self, arg):
        '''Exits the system'''
        return True
    

    def do_test(self, arg):
        '''Test function, used for development purposes'''
        print(self.sys.CheckPermissions(perm.FunctionTypes.MAKE_USER))

    def do_user(self, arg):
        '''
        Usage: user [option]
            [option]:
            -l: Lists users
            -m: Make user
                user -m <user-type> <user-name>
                <user-type>:
                    -c: Client
                    -m: Manager
                    -s: Supplier
        '''
        params = arg.split()
        if (params[0] == "list" or params[0] == "-l"):
            self.user_list()
        elif (params[0] == "make" or params[0] == "-m"):
            if (params[1] == "client" or params[1] == "-c"):
                self.user_make('c', params[2])
            elif (params[1] == "manager" or params[1] == "-m"):
                self.user_make('m', params[2])
            elif (params[1] == "supplier" or params[1] == "-s"):
                self.user_make('s', params[2])
            else:
                print(f"Invalid user type '{params[1]}'")
        else:
            print(f"Unknown argument '{params[0]}'\n")

    #def do_assign(self, arg)
        #to be implemented

    '''Helper function: prints the list of current users in the system'''
    def user_list(self):
        if (self.sys.userDB.GetNumberOfUsers() == 0):
            print("No users in system\n")
            return
        print(self.sys.GetListOfUsers())

    '''Helper function: makes a new user and adds it to the system'''
    def user_make(self, type, name):
        if(not(self.sys.CheckPermissions(perm.FunctionTypes.MAKE_USER))):
            print("Permission Denied")
            return
        if (type == 'c'):
            self.sys.userDB.AddUser(Users.Client(name, 'password'))
        if (type == 'm'):
            self.sys.userDB.AddUser(Users.Manager(name, 'password'))
        if (type == 's'):
            self.sys.userDB.AddUser(Users.Supplier(name, 'password'))
    
    def do_login(self, arg):
        '''
        Usage: login <user-name> <user-password>
        '''
        params = arg.split()
        if (self.sys.SwitchActiveUser(params[0], params[1])):
            print(f"Switched to user '{self.sys.active_user.name}'\n")
            self.prompt = f"({self.sys.active_user.GetType().name}) "
        else:
            print(f"Invalid username or password\n")


#Main program loop
if __name__ == '__main__':
    ProcSysCLI().cmdloop()