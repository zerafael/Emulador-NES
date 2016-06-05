def Zero(cpu):
    address = cpu.memory[cpu.registers['PC']+1]

    return address

def Zero_X(cpu):
    address = cpu.memory[cpu.registers['PC']+1]
    address = (address + cpu.registers['X']) & 0xFF

    return address

def Zero_Y(cpu):
    address = cpu.memory[cpu.registers['PC']+1]
    address = (address + cpu.registers['Y']) & 0xFF

    return address

def Absolute(cpu):
    addr1 = cpu.memory[cpu.registers['PC']+1]
    addr2 = cpu.memory[cpu.registers['PC']+2]
    address = ((addr2 << 8) | addr1) & 0xFFFF

    return address

def Absolute_X(cpu):
    addr1 = cpu.memory[cpu.registers['PC']+1]
    addr2 = cpu.memory[cpu.registers['PC']+2]
    address = (((addr2 << 8) | addr1) + cpu.registers['X']) & 0xFFFF

    return address

def Absolute_Y(cpu):
    addr1 = cpu.memory[cpu.registers['PC']+1]
    addr2 = cpu.memory[cpu.registers['PC']+2]
    address = (((addr2 << 8) | addr1) + cpu.registers['Y']) & 0xFFFF

    return address

def Indirect(cpu):
    addr1 = cpu.memory[cpu.registers['PC']+1]
    addr2 = cpu.memory[cpu.registers['PC']+2]
    addressTmp = addr2 << 8
    addressTmp += addr1

    address = cpu.memory[addressTmp] | (cpu.memory[(addressTmp & 0xFF00) | ((addressTmp + 1) & 0x00FF)] << 8)

    return address

def Indirect_X(cpu):
    value = (cpu.memory[cpu.registers['PC']+1])
    addr1 = (cpu.memory[(value + cpu.registers['X']) & 0xFF])
    addr2 = (cpu.memory[(value + cpu.registers['X']+1) & 0xFF])
    address = ((addr2 << 8) | addr1) & 0xFFFF

    return address

def Indirect_Y(cpu):
    value = (cpu.memory[cpu.registers['PC']+1])
    addr1 = (cpu.memory[value])
    addr2 = (cpu.memory[(value+1) & 0xFF])
    address = (((addr2 << 8) | addr1) + cpu.registers['Y']) & 0xFFFF

    return address