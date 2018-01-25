PB = []  # program block
ss = []  # semantic stack
all_sym = []  # all of the classes and methods
last_token = None  # for id and types


class NameSpace:
    def __init__(self):
        self.contain = []
        self.type = None
        self.return_type = None
        self.parent = []
        self.name = None


def code_gen(action):
    if action == 'Create_Package':
        package = NameSpace()
        package.name = 'Package'
        ss.append(package)
        all_sym.append(package)

    elif action == 'Assign_Table_Class':
        name = ss.pop()
        package = ss.pop()
        cls = NameSpace()
        cls.name = name
        cls.type = 'class'
        cls.parent.append(package)
        package.contain.append(cls)
        ss.append(package)
        ss.append(cls)
        all_sym.append(cls)
        all_sym.append(package)

    elif action == 'Class_Extend':
        name_extend = ss.pop()
        name = ss.pop()
        for s in all_sym:
            if s.name == name_extend:
                name_extend = s
        name.parent.append(name_extend)
        name_extend.contain.append(name)
        ss.append(name)

    elif action == 'Main':
        package = ss.pop()
        main = NameSpace()
        main.type = 'void'
        main.parent.append(package)
        package.children.append(main)
        all_sym.append(main)

    elif action == 'Assign_Table_Field':
        var_name = ss.pop()
        var_type = ss.pop()
        parent = ss.pop()
        # TODO search symbole table to update for static var
        static_var = NameSpace()
        static_var.name = var_name
        static_var.type = var_type
        static_var.parent.append(parent)
        parent.contain.append(static_var)
        ss.append(parent)

    elif action == 'Var_Dec':
        var_name = ss.pop()
        var_type = ss.pop()
        parent = ss.pop()
        # TODO search symbole table to update for var
        var = NameSpace()
        var.name = var_name
        var.type = var_type
        var.parent.append(parent)
        parent.contain.append(var)
        ss.append(parent)

    elif action == 'Assign_Table_Method':
        param_num = ss.pop()
        params = []
        for i in range(param_num):
            params[i] = ss.pop()
        m_name = ss.pop()
        m_type = ss.pop()
        m_parent = ss.pop()
        method = NameSpace()
        method.name = m_name
        method.type = 'method'
        method.return_type = m_type
        method.parent.append(m_parent)
        all_sym.append(method)
        for i in range(param_num):
            method.contain.append(params[i])
            params[i].parent = method
            all_sym.append(params[i])

    elif action == 'Assign_Table_Param_First':
        name = ss.pop()
        type = ss.pop()
        param = NameSpace()
        param.name = name
        param.type = type
        ss.append(param)
        ss.append(1)

    elif action == 'Zero_Param':
        ss.append(0)

    elif action == 'Assign_Table_Param_Count':
        name = ss.pop()
        type = ss.pop()
        param_count = ss.pop()
        param = NameSpace()
        param.name = name
        param.type = type
        ss.append(param)
        ss.append(param_count + 1)

    elif action == 'Type' or action == 'Id' or action == 'Int':
        ss.append(last_token)


def find_var(var_name, var_parents):
    # find a var in parents recursively
    if var_parents is None:
        return False
    for p in var_parents:
        for c in p.contain:
            if c.name == var_name:
                return True
    for p in var_parents:
        find_var(var_name, p.parents)
    pass
