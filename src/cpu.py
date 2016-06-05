import instructions
import pygame
from ppu import ppu
import joypad

class cpu:

    def __init__(self, cartridge):
        self.ppu = ppu(self, cartridge)

        self.registers = {  'PC': 0,            #Program Counter
                            'SP': 0xFF,            #Stack Pointer
                            'A': 0,             #Accumulator
                            'X': 0,             #Register X
                            'Y': 0,             #Register Y
                            'P': 0b00100000}    #Processor Status

        self.statusFlags = {'c': 0,      #Carry Flag
                            'z': 1,      #Zero Flag
                            'i': 2,      #Interrupt Disable
                            'd': 3,      #Decimal Mode
                            'b': 4,      #Break Command
                            'v': 6,      #Overflow Flag
                            'n': 7 }     #Negative Flag

        self.memory = [0] * 0x10000
        self.scanline = 0
        self.cart = cartridge
        self.initMemory()
        self.registers['PC'] = self.memory[0xFFFC] | (self.memory[0xFFFD] << 8)
        self.count = 0
        self.z = 0

        self.instructions = {   0x00: instructions.BRK_Implied,
                                0x01: instructions.ORA_Indirect_X,
                                0x05: instructions.ORA_Zero,
                                0x06: instructions.ASL_Zero,
                                0x08: instructions.PHP_Implied,
                                0x09: instructions.ORA_Immediate,
                                0x0A: instructions.ASL_Accumulator,
                                0x0D: instructions.ORA_Absolute,
                                0x0E: instructions.ASL_Absolute,
                                0x10: instructions.BPL_Relative,
                                0x11: instructions.ORA_Indirect_Y,
                                0x15: instructions.ORA_Zero_X,
                                0x16: instructions.ASL_Zero_X,
                                0x18: instructions.CLC_Implied,
                                0x19: instructions.ORA_Absolute_Y,
                                0x1D: instructions.ORA_Absolute_X,
                                0x1E: instructions.ASL_Absolute_X,
                                0x20: instructions.JSR_Absolute,
                                0x21: instructions.AND_Indirect_X,
                                0x24: instructions.BIT_Zero,
                                0x25: instructions.AND_Zero,
                                0x26: instructions.ROL_Zero,
                                0x28: instructions.PLP_Implied,
                                0x29: instructions.AND_Immediate,
                                0x2A: instructions.ROL_Accumulator,
                                0x2C: instructions.BIT_Absolute,
                                0x2D: instructions.AND_Absolute,
                                0x2E: instructions.ROL_Absolute,
                                0x30: instructions.BMI_Relative,
                                0x31: instructions.AND_Indirect_Y,
                                0x35: instructions.AND_Zero_X,
                                0x36: instructions.ROL_Zero_X,
                                0x38: instructions.SEC_Implied,
                                0x39: instructions.AND_Absolute_Y,
                                0x3D: instructions.AND_Absolute_X,
                                0x3E: instructions.ROL_Absolute_X,
                                0x40: instructions.RTI_Implied,
                                0x41: instructions.EOR_Indirect_X,
                                0x45: instructions.EOR_Zero,
                                0x46: instructions.LSR_Zero,
                                0x48: instructions.PHA_Implied,
                                0x49: instructions.EOR_Immediate,
                                0x4A: instructions.LSR_Accumulator,
                                0x4C: instructions.JMP_Absolute,
                                0x4D: instructions.EOR_Absolute,
                                0x4E: instructions.LSR_Absolute,
                                0x50: instructions.BVC_Relative,
                                0x51: instructions.EOR_Indirect_Y,
                                0x55: instructions.EOR_Zero_X,
                                0x56: instructions.LSR_Zero_X,
                                0x58: instructions.CLI_Implied,
                                0x59: instructions.EOR_Absolute_Y,
                                0x5D: instructions.EOR_Absolute_X,
                                0x5E: instructions.LSR_Absolute_X,
                                0x60: instructions.RTS_Implied,
                                0x61: instructions.ADC_Indirect_X,
                                0x65: instructions.ADC_Zero,
                                0x66: instructions.ROR_Zero,
                                0x68: instructions.PLA_Implied,
                                0x69: instructions.ADC_Immediate,
                                0x6A: instructions.ROR_Accumulator,
                                0x6C: instructions.JMP_Indirect,
                                0x6D: instructions.ADC_Absolute,
                                0x6E: instructions.ROR_Absolute,
                                0x70: instructions.BVS_Relative,
                                0x71: instructions.ADC_Indirect_Y,
                                0x75: instructions.ADC_Zero_X,
                                0x76: instructions.ROR_Zero_X,
                                0x78: instructions.SEI_Implied,
                                0x79: instructions.ADC_Absolute_Y,
                                0x7D: instructions.ADC_Absolute_X,
                                0x7E: instructions.ROR_Absolute_X,
                                0x81: instructions.STA_Indirect_X,
                                0x84: instructions.STY_Zero,
                                0x85: instructions.STA_Zero,
                                0x86: instructions.STX_Zero,
                                0x88: instructions.DEY_Implied,
                                0x8A: instructions.TXA_Implied,
                                0x8C: instructions.STY_Absolute,
                                0x8D: instructions.STA_Absolute,
                                0x8E: instructions.STX_Absolute,
                                0x90: instructions.BCC_Relative,
                                0x91: instructions.STA_Indirect_Y,
                                0x94: instructions.STY_Zero_X,
                                0x95: instructions.STA_Zero_X,
                                0x96: instructions.STX_Zero_Y,
                                0x98: instructions.TYA_Implied,
                                0x99: instructions.STA_Absolute_Y,
                                0x9A: instructions.TXS_Implied,
                                0x9D: instructions.STA_Absolute_X,
                                0xA0: instructions.LDY_Immediate,
                                0xA1: instructions.LDA_Indirect_X,
                                0xA2: instructions.LDX_Immediate,
                                0xA4: instructions.LDY_Zero,
                                0xA5: instructions.LDA_Zero,
                                0xA6: instructions.LDX_Zero,
                                0xA8: instructions.TAY_Implied,
                                0xA9: instructions.LDA_Immediate,
                                0xAA: instructions.TAX_Implied,
                                0xAC: instructions.LDY_Absolute,
                                0xAD: instructions.LDA_Absolute,
                                0xAE: instructions.LDX_Absolute,
                                0xB0: instructions.BCS_Relative,
                                0xB1: instructions.LDA_Indirect_Y,
                                0xB4: instructions.LDY_Zero_X,
                                0xB5: instructions.LDA_Zero_X,
                                0xB6: instructions.LDX_Zero_Y,
                                0xB8: instructions.CLV_Implied,
                                0xB9: instructions.LDA_Absolute_Y,
                                0xBA: instructions.TSX_Implied,
                                0xBC: instructions.LDY_Absolute_X,
                                0xBD: instructions.LDA_Absolute_X,
                                0xBE: instructions.LDX_Absolute_Y,
                                0xC0: instructions.CPY_Immediate,
                                0xC1: instructions.CMP_Indirect_X,
                                0xC4: instructions.CPY_Zero,
                                0xC5: instructions.CMP_Zero,
                                0xC6: instructions.DEC_Zero,
                                0xC8: instructions.INY_Implied,
                                0xC9: instructions.CMP_Immediate,
                                0xCA: instructions.DEX_Implied,
                                0xCC: instructions.CPY_Absolute,
                                0xCD: instructions.CMP_Absolute,
                                0xCE: instructions.DEC_Absolute,
                                0xD0: instructions.BNE_Relative,
                                0xD1: instructions.CMP_Indirect_Y,
                                0xD5: instructions.CMP_Zero_X,
                                0xD6: instructions.DEC_Zero_X,
                                0xD8: instructions.CLD_Implied,
                                0xD9: instructions.CMP_Absolute_Y,
                                0xDD: instructions.CMP_Absolute_X,
                                0xDE: instructions.DEC_Absolute_X,
                                0xE0: instructions.CPX_Immediate,
                                0xE1: instructions.SBC_Indirect_X,
                                0xE4: instructions.CPX_Zero,
                                0xE5: instructions.SBC_Zero,
                                0xE6: instructions.INC_Zero,
                                0xE8: instructions.INX_Implied,
                                0xE9: instructions.SBC_Immediate,
                                0xEA: instructions.NOP_Implied,
                                0xEC: instructions.CPX_Absolute,
                                0xED: instructions.SBC_Absolute,
                                0xEE: instructions.INC_Absolute,
                                0xF0: instructions.BEQ_Relative,
                                0xF1: instructions.SBC_Indirect_Y,
                                0xF5: instructions.SBC_Zero_X,
                                0xF6: instructions.INC_Zero_X,
                                0xF8: instructions.SED_Implied,
                                0xF9: instructions.SBC_Absolute_Y,
                                0xFD: instructions.SBC_Absolute_X,
                                0xFE: instructions.INC_Absolute_X,


                                #Unofficial OpCodes
                                0x03: instructions.SLO_Indirect_X,
                                0x04: instructions.DOP_Zero,
                                0x07: instructions.SLO_Zero,
                                0x0C: instructions.TOP_Absolute,
                                0x0F: instructions.SLO_Absolute,
                                0x13: instructions.SLO_Indirect_Y,
                                0x14: instructions.DOP_Zero_X,
                                0x17: instructions.SLO_Zero_X,
                                0x1A: instructions.NOP_Implied,
                                0x1B: instructions.SLO_Absolute_Y,
                                0x1C: instructions.TOP_Absolute_X,
                                0x1F: instructions.SLO_Absolute_X,
                                0x23: instructions.RLA_Indirect_X,
                                0x27: instructions.RLA_Zero,
                                0x2F: instructions.RLA_Absolute,
                                0x33: instructions.RLA_Indirect_Y,
                                0x34: instructions.DOP_Zero_X,
                                0x37: instructions.RLA_Zero_X,
                                0x3A: instructions.NOP_Implied,
                                0x3B: instructions.RLA_Absolute_Y,
                                0x3C: instructions.TOP_Absolute_X,
                                0x3F: instructions.RLA_Absolute_X,
                                0x43: instructions.SRE_Indirect_X,
                                0x44: instructions.DOP_Zero,
                                0x47: instructions.SRE_Zero,
                                0x4F: instructions.SRE_Absolute,
                                0x53: instructions.SRE_Indirect_Y,
                                0x54: instructions.DOP_Zero_X,
                                0x57: instructions.SRE_Zero_X,
                                0x5A: instructions.NOP_Implied,
                                0x5B: instructions.SRE_Absolute_Y,
                                0x5C: instructions.TOP_Absolute_X,
                                0x5F: instructions.SRE_Absolute_X,
                                0x63: instructions.RRA_Indirect_X,
                                0x64: instructions.DOP_Zero,
                                0x67: instructions.RRA_Zero,
                                0x6F: instructions.RRA_Absolute,
                                0x73: instructions.RRA_Indirect_Y,
                                0x74: instructions.DOP_Zero_X,
                                0x77: instructions.RRA_Zero_X,
                                0x7A: instructions.NOP_Implied,
                                0x7B: instructions.RRA_Absolute_Y,
                                0x7C: instructions.TOP_Absolute_X,
                                0x7F: instructions.RRA_Absolute_X,
                                0x80: instructions.DOP_Immediate,
                                0x82: instructions.DOP_Immediate,
                                0x83: instructions.SAX_Indirect_X,
                                0x87: instructions.SAX_Zero,
                                0x89: instructions.DOP_Immediate,
                                0x8F: instructions.SAX_Absolute,
                                0x97: instructions.SAX_Zero_Y,
                                0xA3: instructions.LAX_Indirect_X,
                                0xA7: instructions.LAX_Zero,
                                0xAF: instructions.LAX_Absolute,
                                0xB3: instructions.LAX_Indirect_Y,
                                0xB7: instructions.LAX_Zero_Y,
                                0xBF: instructions.LAX_Absolute_Y,
                                0xC2: instructions.DOP_Immediate,
                                0xC3: instructions.DCP_Indirect_X,
                                0xC7: instructions.DCP_Zero,
                                0xCF: instructions.DCP_Absolute,
                                0xD3: instructions.DCP_Indirect_Y,
                                0xD4: instructions.DOP_Zero_X,
                                0xD7: instructions.DCP_Zero_X,
                                0xDA: instructions.NOP_Implied,
                                0xDB: instructions.DCP_Absolute_Y,
                                0xDC: instructions.TOP_Absolute_X,
                                0xDF: instructions.DCP_Absolute_X,
                                0xE2: instructions.DOP_Immediate,
                                0xE3: instructions.ISB_Indirect_X,
                                0xE7: instructions.ISB_Zero,
                                0xEB: instructions.SBC_Immediate,
                                0xEF: instructions.ISB_Absolute,
                                0xF3: instructions.ISB_Indirect_Y,
                                0xF4: instructions.DOP_Zero_X,
                                0xF7: instructions.ISB_Zero_X,
                                0xFA: instructions.NOP_Implied,
                                0xFB: instructions.ISB_Absolute_Y,
                                0xFC: instructions.TOP_Absolute_X,
                                0xFF: instructions.ISB_Absolute_X
        }

    def initMemory(self):
        if self.cart.mapperNumber != 0:
            print "Mapper not available yet"
            exit(1)

        for i in xrange(len(self.cart.prgRomData)):
            self.memory[i + 0x8000] = self.cart.prgRomData[i]
            if self.cart.prgRomCount == 1:
                self.memory[i + 0xC000] = self.cart.prgRomData[i]
        for i in xrange(0x20):
            self.memory[i + 0x4000] = 0xFF

    def doNMI(self):
        self.pushStack((self.registers['PC'] >> 8) & 0xFF)
        self.pushStack(self.registers['PC'] & 0xFF)
        self.pushStack(self.registers['P'])
        self.registers['PC'] = self.memory[0xFFFA] | (self.memory[0xFFFB] << 8)
        self.z = 1

    def writeMemory(self, address, value):
        if address < 0x2000:
            address &= 0x7FF
            self.memory[address] = value
        elif address < 0x4000:
            # PPU Registers
            address &= 0x2007
            self.memory[address] = value
            if address == 0x2000:
                self.ppu.processControlReg1(value)
            elif address == 0x2001:
                self.ppu.processControlReg2(value)
            elif address == 0x2003:
                self.ppu.spriteRamAddr = value
            elif address == 0x2004:
                self.ppu.writeSprRam(value)
            elif address == 0x2005:
                self.ppu.processPPUSCROLL(value)
            elif address == 0x2006:
                self.ppu.processPPUADDR(value)
            elif address == 0x2007:
                self.ppu.writeVRAM(value)
        elif address < 0x4020:
            if address == 0x4014:
                self.ppu.writeSprRamDMA(value)
            elif address == 0x4016:
                if joypad.LastWrote___ == 1 and value == 0:
                    joypad.ReadNumber__ = 0
                joypad.LastWrote___ = value
            self.memory[address] = value
        elif address < 0x8000:
            pass
        else:
            self.memory[address] = value

    def readMemory(self, address):
        value = 0x00
        if address < 0x2000:
            address &= 0x7FF
            value = self.memory[address]
        elif address < 0x4000:
            address &= 0x2007
            if address == 0x2002:
                value = self.ppu.readStatusFlag()
            elif address == 0x2007:
                value = self.ppu.readVRAM()
            self.memory[address] = value
        elif address < 0x4020:
            if address == 0x4016:
                joypad.Strobe()
                value = joypad.KeysBuffer__
            else:
                value = self.memory[address]
        else:
            value = self.memory[address]

        return value

    def setStatus(self, flag, value):
        if value:
            self.registers['P'] |= 1<<flag
        else:
            self.registers['P'] &= ~(1<<flag)

    def getStatus(self, flag):
        if (self.registers['P'] & (1<<flag)) == 0:
            return 0
        else:
            return 1

    def pushStack(self, value):
        self.writeMemory(0x100 + self.registers['SP'], value)
        self.registers['SP'] -= 1

    def pullStack(self):
        self.registers['SP'] += 1
        value = self.readMemory(0x100 + self.registers['SP'])
        return value

    def run(self):
        cyclesClock = 0
        a = 0
        self.z = 0
        ctrl = 0
        while True:
            ctrl += 1
            if ctrl > 1000:
                ctrl = 0
                pygame.event.poll()
                joypad.keys=pygame.key.get_pressed()
                if joypad.keys[pygame.K_ESCAPE] == 1:
                    exit()

            # Executa a instrucao e armazena
            cycles = self.instructions[self.memory[self.registers['PC']]](self)

            cyclesClock += cycles
            if cyclesClock > 113:
                cyclesClock = 0

                if self.scanline >= 0 and self.scanline < 240:
                    self.ppu.doScanline()
                elif self.scanline == 241:
                    self.ppu.enterVBlank()
                elif self.scanline == 261:
                    self.scanline = -1

                self.scanline += 1