import cmd
import System as System
import Users

class ProcSysCLI(cmd.Cmd):
    intro = "----Procurement System Prototype CLI----"
    sys = System.ProcurementSystem() #Initialize system
    prompt = f"({sys.active_user.type}) "


    def do_exit(self, arg):
        '''Exits the system'''
        return True
    

    def do_test(self, arg):
        '''Test function, used for development purposes'''
        print("Hello World!")
        print(type(arg))
        print(arg)


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


    '''Helper function: prints the list of current users in the system'''
    def user_list(self):
        if (self.sys.userDB.GetNumberOfUsers() == 0):
            print("No users in system\n")
            return
        print(self.sys.GetListOfUsers())
    

    '''Helper function: makes a new user and adds it to the system'''
    def user_make(self, type, name):
        if (type == 'c'):
            self.sys.userDB.AddUser(Users.Client(name))
        if (type == 'm'):
            self.sys.userDB.AddUser(Users.Manager(name))
        if (type == 's'):
            self.sys.userDB.AddUser(Users.Supplier(name))
    
    def do_login(self, arg):
        '''
        Usage: login <user-name>
        '''
        if (self.sys.SwitchActiveUser(arg)):
            print(f"Switched to user '{self.sys.active_user.name}'\n")
            self.prompt = f"({self.sys.active_user.type}) "
        else:
            print(f"Unable to find user '{arg}' in system\n")


#Main program loop
if __name__ == '__main__':
    ProcSysCLI().cmdloop()