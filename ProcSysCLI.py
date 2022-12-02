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
    intro = "\n\n----Procurement System Prototype CLI----"
    sys = System.ProcurementSystem() #Initialize system
    name, userID, pwd, userType = sys.GetUserValues(sys.active_user)
    prompt = f"({userType}) "

    def do_exit(self, arg):
        '''
        Exits the system
        '''
        return True
    

    def do_test(self, arg):
        '''testin' stuff'''
   
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
                    defaults to 'password' if not specified
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


    def do_reset(self,arg):
        ''' Usage: reset <user-id> <new_password>
                <new_password>: defaults to 'password' if not specified
        '''
        # Check for permissions
        if(not(self.sys.CheckPermissions(perm.RESET_PASSWORD))):
            print("Permission Denied")
            return
        #Attempt to reset password
        try:
            user_ID,password =CLIParser.do_reset_parse(self,arg)
            print(user_ID)
            self.sys.ResetPassword(user_ID,password)
            print(f"User {user_ID} password successfully reset.")
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
            self.prompt = f"({userType.name}) "
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def do_request(self,arg):
        '''
        Usage: request <item-name> <quantity>
        '''
        #check for permissions
        if(not(self.sys.CheckPermissions(perm.CREATE_REQUEST))): 
            print("Permission Denied")
            return
        try: 
            item, quant = CLIParser.do_request_parse(self,arg)
            reqID = self.sys.CreateRequest(self.sys.active_user, item,quant)
            print(f"Request created with ID {reqID}")
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def do_displayRequests(self):
        '''
        Usage: display requests
        '''
        #check for permissions
        if (not(self.sys.CheckPermissions(perm.CREATE_REQUEST))):
            print("Permission Denied")
            return
        try:
            self.sys.displayAllRequests(self.sys.active_user)
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def do_display(self,arg):
        '''
        Usage: display <request-id>
        '''

        #check for permissions
        if (not(self.sys.CheckPermissions(perm.CREATE_REQUEST))):
            print("Permission Denied")
            return
        try:
            request_id = CLIParser.do_display_parse(self,arg)
            requestNumber, itemName, quantity, clientName, assignedManager, status, acceptedQuoteID = self.sys.displayRequest(request_id)
            if (status==0):
                statusStr = "REQUEST BEING PROCESSED: SENT TO SUPPLIER"
            elif (status==1):
                statusStr =  "REQUEST COMPLETE: ACCEPTED BY DEFAULT"
            elif (status==2):
                statusStr =  "REQUEST BEING PROCESSED: UNDER SUPERVISOR REVIEW"
            elif (status==3):
                statusStr =  "REQUEST COMPLETE: ACCEPTED BY SUPERVISOR"
            elif (status==4):
                statusStr = "REQUEST COMPELTE: DENIED BY SUPERVISOR"
            print(f"REQUEST  {requestNumber}: \n NAME: {itemName}\n QUANTITY: {quantity}\n ORDERED BY: {clientName}\n ASSIGNED MANAGER: {assignedManager}\n STATUS: {statusStr}\n ACCEPTED QUOTE ID: {acceptedQuoteID}\n")
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def do_status(self,arg):
        '''
        Usage: status <request-id>
        '''
        #check for permissions
        if (not(self.sys.CheckPermissions(perm.CREATE_REQUEST))):
            print("Permission Denied")
            return
        try:
            request_id = CLIParser.do_display_parse(self,arg)
            status = self.sys.displayStatus(request_id)
            if (status==0):
                statusStr = "REQUEST BEING PROCESSED: SENT TO SUPPLIER"
            elif (status==1):
                statusStr =  "REQUEST COMPLETE: ACCEPTED BY DEFAULT"
            elif (status==2):
                statusStr =  "REQUEST BEING PROCESSED: UNDER SUPERVISOR REVIEW"
            elif (status==3):
                statusStr =  "REQUEST COMPLETE: ACCEPTED BY SUPERVISOR"
            elif (status==4):
                statusStr = "REQUEST COMPELTE: DENIED BY SUPERVISOR"
            else:
                statusStr = "ERROR: REQUEST STATUS UNAVAILABLE"
            print(f"REQUEST {request_id} STATUS: {statusStr}")
        except Exception as e:
            print(f"ERROR: {str(e)}")


    def do_quote(self,arg):
        '''
        Usage: quote <price> <request-id>
        '''
        if (not(self.sys.CheckPermissions(perm.CREATE_QUOTE))):
            print("Permission Denied")
            return
        try:
            unitPrice, requestID = CLIParser.do_display_parse(self,arg)
            self.sys.CreateQuote(unitPrice,requestID)

        except Exception as e:
            print(f"ERROR: {str(e)}")
        

#Main program loop
if __name__ == '__main__':
    ProcSysCLI().cmdloop()