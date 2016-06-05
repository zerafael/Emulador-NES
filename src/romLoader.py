class romLoader:
    rom = 0

    def __init__(self, romPath):
        self.rom = self.openFile(romPath)

    def openFile(self, romPath):
        try:
            rom = open(romPath, 'rb')
            print romPath, " ......LOADED"
        except ValueError:
            print "Invalid Path."

        return rom

    def load(self):
        # Pula os 4 primeiros bytes
        if(self.rom.read(3) != 'NES'):
            exit()
        self.rom.seek(4)

        # Le o cabecalho do Rom
        self.prgRomCount =  ord(self.rom.read(1))
        self.chrRomCount =  ord(self.rom.read(1))
        self.flags6 = ord(self.rom.read(1))
        self.flags7 = ord(self.rom.read(1))
        self.prgRamCount = ord(self.rom.read(1))
        self.flags9 = ord(self.rom.read(1))
        self.flags10 = ord(self.rom.read(1))

        # Calcula o mapper
        # Pega os 4 ultimos bits das flags6, faz um shift para a direita de 4 bits e soma os 4 ultimos bits das flags 7
        self.mapperNumber = ((self.flags6 & 240) >> 4) + (self.flags7 & 240)

        self.rom.seek(16)

        # Verifica se eh preciso ler o Trainer
        if self.flags6 & 4:
            self.trainerData = self.rom.read(0x200)

        self.mirror = self.flags6 & 1

        # Le o PRG ROM e o CHR ROM e os mapeia em arrays de inteiros
        self.prgRomData = self.rom.read(0x4000 * self.prgRomCount)
        self.prgRomData = map(ord, self.prgRomData)

        self.chrRomData = self.rom.read(0x2000 * self.chrRomCount)
        self.chrRomData = map(ord, self.chrRomData)

    def printHeader(self):

        print "Mapper Number: ", self.mapperNumber
        print "PRG Count: ", self.prgRomCount
        print "CHR Count: ", self.chrRomCount
        print "Flags 6: ", self.flags6
        print "Flags 7: ", self.flags7
        print "Size of PRG Data: ", len(self.prgRomData)
        print "Size of CHR Data: ", len(self.chrRomData)
        print "\n"
