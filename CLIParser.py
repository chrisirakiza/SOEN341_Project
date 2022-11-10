import Users

def do_assign_parse(cli_sys, arg):
    params = arg.split()
    if (len(params) != 2):
        raise Exception(f"Command expects 2 passed arguments")
    clientID = params[0]
    managerID = params[1]
    if (managerID == "-s"):
        managerID = cli_sys.sys.active_user.GetID()
    print(managerID)
    return clientID, managerID

def do_login_parse(cli_sys, arg):
    params = arg.split()
    if (len(params) != 2):
        raise Exception(f"Command expects 2 passed arguments")
    userID = params[0]
    pwd = params[1]
    return userID, pwd

def do_user_parse(cli_sys, arg):
    params = arg.split()
    if (len(params) == 0):
        raise Exception(f"Command expects arguments")
    if (params[0] == "-l" or params[0] == "list"):
        return "list"
    elif (params[0] == "-m" or params[0] == "make"):
        return "make"
    else:
        raise Exception(f"Unknown argument '{params[0]}'")

def do_user_make_parse(cli_sys, arg):
    params = arg.split()
    if (len(params) < 3):
        raise Exception(f"Make user command requires a minimum of 2 arguments: <type> <name>")
    if (params[1] == "client" or params[1] == "-c"):
        type = Users.UserType.CLIENT
    elif (params[1] == "manager" or params[1] == "-m"):
        type = Users.UserType.MANAGER
    elif (params[1] == "supplier" or params[1] == "-s"):
        type = Users.UserType.SUPPLIER
    elif (params[1] == "admin" or params[1] == "-a"):
        type = Users.UserType.ADMIN
    else:
        raise Exception(f"Unknown user type '{params[1]}'")
    name = params[2]
    if (len(params) == 3):
        pwd = "password"
    else:
        pwd = params[3]
    return type, name, pwd