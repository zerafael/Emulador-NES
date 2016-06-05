from romLoader import romLoader
from cpu import cpu
import sys

class Console:

    def __init__(self):
        romPath = sys.argv[1]

        self.cartridge = romLoader(romPath)
        self.cartridge.load()

        CPU = cpu(self.cartridge)
        CPU.run()

Console()
