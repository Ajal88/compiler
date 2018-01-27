PB = dict()  # program block  memory : 1-99
ss = []  # semantic stack
all_sym = []  # all of the classes and methods
pb_index = 0  # for pb[]
temp = dict()
adr = 100  # data memory : 100-499
tmp_adr = 500  # temp data memor/.y : 500 -


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_temp():
    global temp, tmp_adr
    temp[tmp_adr] = None
    tmp_adr += 4
    return temp, tmp_adr


class NameSpace:
    def __init__(self):
        self.contain = []
        self.type = None
        self.return_type = None
        self.return_address = None
        self.parent = []
        self.name = None
        self.address = None


def code_gen(action, symbole_table, last_token):
    global pb_index, PB, ss, all_sym, temp, adr, tmp_adr
    print(ss)
    print('===========')
    if action == 'Create_Package':
        package = NameSpace()
        package.name = 'Package'
        ss.append(package)
        all_sym.append(package)
        pb_index += 1

    elif action == 'Assign_Table_Class':
        name = ss.pop()  # must be a token ['type', addr]
        package = ss.pop()
        cls = NameSpace()
        # print(symbole_table)
        cls.name = symbole_table[name[1]]['name']
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
        find = False
        for s in all_sym:
            if s.name == symbole_table[name_extend[1]]['name']:
                name_extend = s
                find = True
        if not find:
            print(Color.FAIL + 'Class ' + str(symbole_table[name_extend[1]]['name']) + ' does not exist!' + Color.ENDC)
        name.parent.append(name_extend)
        name_extend.contain.append(name)
        ss.append(name)

    elif action == 'Main':
        PB[0] = '(JP , ' + str(pb_index) + ', , )'
        pb_index += 1
        package = ss.pop()
        main = NameSpace()
        main.return_type = 'void'
        main.type = 'method'
        main.return_address = get_temp()
        main.parent.append(package)
        main.address = pb_index
        package.contain.append(main)
        all_sym.append(main)

    elif action == 'Assign_Table_Field':
        var_name = ss.pop()
        var_type = ss.pop()[0]
        parent = ss.pop()
        static_var = NameSpace()
        static_var.name = var_name[0]
        static_var.address = var_name[1]
        static_var.type = var_type
        static_var.parent.append(parent)
        parent.contain.append(static_var)
        ss.append(parent)
        symbole_table[static_var.address]['type'] = var_type

    elif action == 'Var_Dec':
        var_name = ss.pop()
        var_type = ss.pop()[0]
        parent = ss.pop()
        var = NameSpace()
        var.name = symbole_table[var_name[1]]['name']
        var.type = var_type
        var.address = var_name[1]
        var.parent.append(parent)
        parent.contain.append(var)
        ss.append(parent)
        symbole_table[var.address]['type'] = var_type

    elif action == 'Assign_Table_Method':
        param_num = ss.pop()
        params = []
        for i in range(param_num):
            params.append(ss.pop())
        m_name = ss.pop()
        m_type = ss.pop()[0]
        m_parent = ss.pop()
        method = NameSpace()
        method.name = symbole_table[m_name[1]]['name']
        method.type = 'method'
        method.return_type = m_type
        method.parent.append(m_parent)
        method.address = pb_index
        t = get_temp()
        method.return_address = t[1]
        all_sym.append(method)
        for i in range(param_num):
            method.contain.append(params[i])
            params[i].parent = method
            all_sym.append(params[i])

    elif action == 'Assign_Table_Param_First':
        name = ss.pop()
        typ = ss.pop()
        param = NameSpace()
        param.name = name[0]
        param.address = name[1]
        param.type = typ
        ss.append(param)
        symbole_table[param.address]['type'] = typ
        ss.append(1)

    elif action == 'Zero_Param':
        ss.append(0)

    elif action == 'Assign_Table_Param_Count':
        name = ss.pop()
        typ = ss.pop()
        param_count = ss.pop()
        param = NameSpace()
        param.name = name[0]
        param.address = name[1]
        param.type = typ
        ss.append(param)
        ss.append(param_count + 1)

    elif action == 'Type' or action == 'Pid' or action == 'Int':
        ss.append(last_token)

    elif action == 'Save':
        ss.append(pb_index)
        pb_index += 1

    elif action == 'Jpf_Save':
        index = ss.pop()
        address = ss.pop()[1]
        PB[index] = '(JPF , ' + str(address) + ',' + str(pb_index + 1) + ', )'
        ss.append(pb_index)
        pb_index += 1

    elif action == 'Jp':
        index = ss.pop()
        PB[index] = '(JP , ' + str(pb_index) + ', , )'

    elif action == 'Label':
        ss.append(pb_index)

    elif action == 'While':
        index = ss.pop()
        content = ss.pop()
        jp_content = ss.pop()
        PB[index] = '(JPF , ' + str(content) + ',' + str(pb_index + 1)
        ', )'
        PB[pb_index] = '(JP , ' + str(jp_content) + ', , )'
        pb_index += 1

    elif action == 'Assign':
        source = ss.pop()
        dest = ss.pop()
        PB[pb_index] = '(ASSIGN , ' + str(source) + ',' + str(dest) + ', )'
        pb_index += 1

    elif action == 'Cmp_Save':
        t = get_temp()
        var1 = ss.pop()
        var2 = ss.pop()
        PB[pb_index] = '(LT , ' + str(var2) + ',' + str(var1) + ',' + t[1] + ')'
        pb_index += 1
        ss.append(var2)
        ss.append(t[1])
        ss.append(pb_index)
        pb_index += 1

    elif action == 'For':
        var1 = ss.pop()
        var2 = ss.pop()
        var3 = ss.pop()
        var4 = ss.pop()
        var5 = var2 - 1
        PB[pb_index] = '(ADD , ' + str(var1) + ',' + str(var4) + ',' + str(var4) + ')'
        pb_index += 1
        PB[pb_index] = '(JP , ' + str(var5) + ', , )'
        pb_index += 1
        PB[var2] = '(JPF , ' + str(var3) + ',' + str(pb_index) + ', )'

    elif action == 'Step':
        var = ss.pop()
        intgr = ss.pop()
        PB[pb_index] = '(ADD , #' + str(intgr) + ',' + str(var[1]) + ', ' + str(var[1]) + ' )'
        pb_index += 1
        ss.append(var[1])

    elif action == 'Mult':
        t = get_temp()
        var1 = ss.pop()
        var2 = ss.pop()
        PB[pb_index] = '(MULT , ' + str(var1) + ',' + str(var2) + ',' + str(t[1]) + ')'
        pb_index += 1
        ss.append(t[1])

    elif action == 'Add':
        t = get_temp()
        var1 = ss.pop()
        var2 = ss.pop()
        PB[pb_index] = '(ADD , ' + str(var1) + ',' + str(var2) + ',' + str(t[1]) + ')'
        pb_index += 1
        ss.append(t[1])

    elif action == 'Sub':
        t = get_temp()
        var1 = ss.pop()
        var2 = ss.pop()
        PB[pb_index] = '(SUB , ' + str(var1) + ',' + str(var2) + ',' + str(t[1]) + ')'
        pb_index += 1
        ss.append(t[1])

    elif action == 'Check_Equality':
        t = get_temp()
        var1 = ss.pop()
        var2 = ss.pop()
        PB[pb_index] = '(EQ , ' + str(var1) + ',' + str(var2) + ',' + str(t[1]) + ')'
        pb_index += 1
        ss.append(t[1])

    elif action == 'Less_Than':
        t = get_temp()
        var1 = ss.pop()
        var2 = ss.pop()
        PB[pb_index] = '(LT , ' + str(var1) + ',' + str(var2) + ',' + str(t[1]) + ')'
        pb_index += 1
        ss.append(t[1])

    elif action == 'And':
        t = get_temp()
        var1 = ss.pop()
        var2 = ss.pop()
        PB[pb_index] = '(AND , ' + str(var1) + ',' + str(var2) + ',' + str(t[1]) + ')'
        pb_index += 1
        ss.append(t[1])

    elif action == 'Print':
        printable = ss.pop()
        output = symbole_table[printable]['value']
        PB[pb_index] = '(PRINT , ' + output + ' )'

    elif action == 'Var_Call':
        var = ss.pop()
        cls = ss.pop()
        for a in all_sym:
            if symbole_table(var[1])['name'] == a.name:
                for c in a.parent:
                    if c.name == symbole_table(cls[1])['name']:
                        var = a
                        ss.append(var.address)
                        break

    elif action == 'First_Arg':
        ss.append(1)

    elif action == 'Zero_Arg':
        ss.append(0)

    elif action == 'Arg_Cont':
        res = ss.pop()
        cnt = ss.pop()
        ss.append(res)
        ss.append(cnt + 1)
    elif action == 'Last_Arg':
        arg_count = ss.pop()
        ar = []
        for i in range(arg_count):
            res = ss.pop()
            ar[i] = res
        mtd = ss.pop()
        cls = ss.pop()
        if mtd in cls.contain and mtd.type == 'method':
            for i in range(arg_count):
                PB[pb_index] = '(ASSIGN , ' + str(ar.pop().address) + ',' + str(mtd.contain[i].address) + ', )'
                pb_index += 1
            PB[pb_index] = '(JP , ' + str(mtd.address) + ', , )'
            pb_index += 1
            ss.append(cls)
            ss.append(mtd)
            ss.append(pb_index)
    elif 'Jp_Return':
        r_val = ss.pop()
        j_address = ss.pop()
        mtd = ss.pop()
        cls = ss.pop()
        PB[pb_index] = '(ASSIGN , ' + str(mtd.return_address) + ', #' + str(j_address) + ', )'
        pb_index += 1
        PB[pb_index] = '(JP , @' + str(mtd.return_address) + ' )'
        pb_index += 1
        ss.append(r_val)


print(PB)


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
