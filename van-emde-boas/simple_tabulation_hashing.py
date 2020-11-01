import numpy as np
from random import seed
import random
import math


# constantes
FLAG = '#'
SIZE_X = 64
SEED = 42
EPSILON = 1
SIZE_HASH_TABLE = 10 # m
SIZE_RANDOM_TABLE_AND_PIECES = 8 # c 
SIZE_RANDOM_LISTS = 256 # 2^c
MAX_VALUE_RANDOM_LISTS = 2**64 - 1


class RandomTable():
    def __init__(self, _seed):
        seed(_seed)
        self.random_table = [[random.randint(0, MAX_VALUE_RANDOM_LISTS) for _ in range(0, SIZE_RANDOM_LISTS)] for _ in range(0, SIZE_RANDOM_TABLE_AND_PIECES)]
    
    def get_list(self, position):
        if (position >= SIZE_RANDOM_TABLE_AND_PIECES):
            return -1
        return self.random_table[position]

    def get_element(self, list_position, element_position):
        if (list_position >= SIZE_RANDOM_TABLE_AND_PIECES or element_position >= SIZE_RANDOM_LISTS):
            return -1
        return self.random_table[list_position][element_position]


# return -1 pra falha na operação
class SimpleTabulationHashing():
    def __init__(self, size_table, random_table = None, seed=42, threshold_halving=0.25, threshold_table_doubling=0.75, threshold_clear=0.25):
        self.log_operations = [] # lista de tuplas que guardará o log das operações

        if random_table == None:
            self.random_tables = RandomTable(seed)
        else:
            self.random_tables = random_table
            
        self.m =  size_table # tamanho da tabela principal
        self.table = self.init_table()

        self.threshold_halving = threshold_halving
        self.threshold_table_doubling = threshold_table_doubling
        self.threshold_clear = threshold_clear
        
        self.count_flags = 0 # p
        self.count_elements = 0 # numero de elementos da tabela principal

    def init_table(self):
        """
            Init hash table with size m Nones
            Params: None
            Return: hash table with size m Nones
        """ 
        self.count_elements = 0
        self.count_flags = 0
        return [None for _ in range(0, self.m)]

    def load_file(self, filename):
        """
            Load file with list operations in this hash table
            Params: filename
            Return: 1, if operation was successful
                    -1, c.c.
        """ 
        try:
            file = open(filename, "r")
            for line in file:
                operation, value = line.split(":")
                if operation == "INC":
                    retorno = self.insert(int(value))
                elif operation == "REM":
                    retorno = self.remove(int(value))
                elif operation == "BUS":
                    retorno = self.search(int(value))
            file.close()
            return 1
        except:
            return -1
            
    
    def write_file(self, filename):
        """
            Write file with log operations in this hash table
            Params: filename
            Return: 1, if operation was successful
                    -1, c.c.
        """ 
        try:
            file = open(filename, 'w')
            file.writelines("TAM:{}\n".format(self.m))
            file.writelines(self.log_operations)
            file.close()
            return 1
        except:
            return -1

    def get_pieces_8bits(self, x): 
        """
            Partition the 64-bit integer into 8-bit chunks
            Params: int 64bits x
            Return: list of partition in binary, list of partition in decimal
        """ 
        x_bin = bin(x).zfill(SIZE_X).replace('b', '')
        pieces = []

        for _ in range(SIZE_RANDOM_TABLE_AND_PIECES):
            pieces.append(x_bin[-SIZE_RANDOM_TABLE_AND_PIECES:])
            x_bin = x_bin[:-SIZE_RANDOM_TABLE_AND_PIECES]

        return pieces[::-1], [int(piece, 2) for piece in pieces[::-1]]


    def h(self, x):
        """
            Hash function of xor between elements random table
            Params: int 64bits x
            Return: value of xor between elements
        """ 
        xor = 0
        pieces_bin, pieces_dec = self.get_pieces_8bits(x)
        for i, x in enumerate(pieces_dec):
            xor = xor ^ self.random_tables.get_element(i, x)
        return xor

    def h_mod(self, x, i=0):
        """
            Hash function of mod m
            Params: int 64bits x
                    i, represents displacement
            Return: value of operation of h
        """ 
        return (self.h(x) + i) % self.m

    def remap_values(self, old_table):
        """
            Auxiliar function to make remap of values table, through the new inserts
            Params: old_table, represents old table with the old size and old positions of values
            Return: None
        """ 
        for i, value in enumerate(old_table):
            if value != None and value != FLAG:
                self.insert(value, False)

    def clear(self):
        """
            Function to remove the remover's markers + shift values table
            OBS:    in classes he was taught to shift values. But the shift 
                    operation can cause problems in the position of the elements 
                    and etc., so I chose to do the insertion, to avoid conflicts 
                    and problems with mapping the elements.
            Params: None
            Return: None
        """ 
        old_table = self.table.copy()
        self.table = self.init_table()
        self.log_operations.append("\nLIMPAR:{}\n".format(self.count_flags))
        self.remap_values(old_table)

    def table_doubling(self): 
        """
            Function to doubling values table and remap this.
            Params: None
            Return: None
        """ 
        old_table = self.table.copy()
        self.m = self.m * 2
        self.table = self.init_table()
        self.remap_values(old_table)
        self.log_operations.append("\nDOBRAR TAM:{}\n".format(self.m))

    def halving(self): 
        """
            Function to doubling values table and remap this.
            Params: None
            Return: 1, if operation was successful
                    -1, c.c.
        """ 
        if (self.m/2 >= (EPSILON+1)):
            old_table = self.table.copy()
            self.m = int(self.m / 2)
            self.table = self.init_table()
            self.remap_values(old_table)
            self.log_operations.append("\nMETADE TAM:{}\n".format(self.m))
            return 1
        return -1

    def insert(self, x, registre_operation=True):
        """
        Insert integer x with 64 bits.
        Keep a copy if x is a copy.
        OBS: Attention to table doubling.

        Params: integer x with 64 bits
                bool registre_operation, to indicate if registre the operation in log (because the remap_values function)
        Return: 1, if operation was successful
                    -1, c.c.
        """
        insert_ = False
        i = 0
        while (not insert_):
            if (i < self.m): # pra garantir que vai ter um break e não vai percorrer a lista varias e varias vezes circulamente
                position_element = self.h_mod(x, i)
                if self.table[position_element] == None or self.table[position_element] == FLAG:
                    if (self.table[position_element] == FLAG):
                        self.count_flags -= 1
                    self.table[position_element] = x
                    self.count_elements += 1

                    if (registre_operation): # registrando log
                        self.log_operations.append("\nINC:{}\n{} {}\n".format(x, self.h_mod(x, 0), self.h_mod(x, i))) 
                    
                    if (self.count_elements >= (self.m * self.threshold_table_doubling)): # verificando se é necessário realizar table doubling
                        self.table_doubling()    
                    return 1
                i += 1
            else:
                insert_ = True
        return -1

    def remove(self, x):
        """
        Remove occurrence of x.
        First, search x. If find x, put flag # in position of x, and return 1.
        Else, pass and return -1.
        OBS: Attention to halving and clear.

        Params: integer x with 64 bits
        Return: 1, if operation was successful
                    -1, c.c.
        """
        position_element = self.search(x, False)

        if position_element != -1:
            self.table[position_element] = FLAG
            self.count_elements -= 1
            self.count_flags += 1

            # registrando log
            h_mod = self.h_mod(x, 0)
            i = position_element - h_mod if position_element > h_mod else h_mod - position_element
            self.log_operations.append("\nREM:{}\n{} {}\n".format(x, self.h_mod(x, 0), self.h_mod(x, i))) 

            if (self.count_flags >= (self.m * self.threshold_clear)): # verificando se é necessário realizar clear
                self.clear() 

            if (self.count_elements <= (self.m * self.threshold_halving)): # verificando se é necessário realizar halving
                self.halving() 
            return 1
        self.log_operations.append("\nREM:{}\n{} {}\n".format(x, self.h_mod(x, 0), -1)) 
        return -1

    def search(self, x, registre_operation=True):
        """
        Search table's position of x.
        If find x, return 1.
        Else, return -1.

        Params: integer x with 64 bits
                bool registre_operation, to indicate if registre the operation in log (because the remove function) 

        Return: 1, if operation was successful
                    -1, c.c.
        """
        find = False
        i = 0
        while (not find):
            if (i < self.m): # pra garantir que vai ter um break e não vai percorrer a lista varias vezes circulamente
                position_element = self.h_mod(x, i)
                if self.table[position_element] == x:
                    if (registre_operation): # registrando log
                        self.log_operations.append("\nBUS:{}\n{} {}\n".format(x, self.h_mod(x, 0), self.h_mod(x, i)))
                    return position_element
                i += 1
            else:
                find = True
        self.log_operations.append("\nBUS:{}\n{} {}\n".format(x, self.h_mod(x, 0), -1))
        return -1
    