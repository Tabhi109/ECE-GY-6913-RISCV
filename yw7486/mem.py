from pathlib import Path

from constants import (BYTE_LEN, DMEM_FILE, DMEM_RESULT_FILE, IMEM_FILE,
                       WORD_LEN, MemSize)
from misc import signed_binary_str_to_int, signed_int_to_binary_str


class InstructionMemory(object):
    def __init__(self, identifier: str, io_directory: Path):
        self.identifier = identifier

        with open(io_directory / IMEM_FILE) as instruction_file:
            self.memory = [line.replace("\n", "") for line in instruction_file.readlines()]

    def fetchInstruction(self, address: int):
        # Fetch instruction from memory
        # Return 32-bit hex value
        return "".join(self.memory[address: address + WORD_LEN])  # Read 4 lines and concatenate them into a 32-bit binary string


class DataMemory(object):
    def __init__(self, identifier: str, io_directory: Path, output_directory: Path):
        self.identifier = identifier
        self.io_directory = io_directory
        self.output_directory = output_directory
        with open(io_directory / DMEM_FILE) as data_file:
            self.memory = [line.replace("\n", "") for line in data_file.readlines()]
        
        # Fill the rest of the memory with zeros
        self.memory.extend(['00000000'] * (MemSize - len(self.memory)))

    def readData(self, address: int):
        # Read data from memory
        binary_str = "".join(self.memory[address: address + WORD_LEN])
        return signed_binary_str_to_int(binary_str)

    def writeData(self, address: int, data: int):
        # Write data into byte-addressable memory
        binary_str = signed_int_to_binary_str(data)
        for i in range(WORD_LEN):
            self.memory[address + i] = binary_str[BYTE_LEN*i: BYTE_LEN*(i+1)]

    def exportDataMemory(self):
        result_path = self.output_directory / f"{self.identifier}_{DMEM_RESULT_FILE}"
        with open(result_path, "w") as result_file:
            result_file.writelines([str(data) + "\n" for data in self.memory])
