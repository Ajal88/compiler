PB = []  # program block
ss = []  # semantic stack


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
    elif action == 'Assign_Table_Class':
        name = ss.pop()
        package = ss.pop()
        cls = NameSpace()
        cls.name = name
        cls.type = 'class'
        cls.parent.append(package)
        package.contain.append(cls)
        ss.append(cls)
    elif action == 'Class_Extend':
        name_extend = ss.pop()
        name = ss.pop()
        # TODO extender class read from symbol table and update it
        name.parent.append(name_extend)
        name_extend.contain.append(name)
        ss.append(name)
    elif action == 'Main':
        package = ss.pop()
        main = NameSpace()
        main.type = 'void'
        main.parent.append(package)
        package.children.append(main)
