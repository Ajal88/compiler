PB = []  # program block
ss = []  # semantic stack
all_sym = []  # all of the classes and methods

# changes added : for classes when we have var declarations we should add a dict to contain[] :{int|boolean : identifier}


class NameSpace:
    def __init__(self):
        self.contain = []
        self.type = None
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

    elif action == 'Class_Find_Set':

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
