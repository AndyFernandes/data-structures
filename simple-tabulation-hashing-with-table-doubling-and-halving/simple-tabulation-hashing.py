import random
import numpy as np
from random import seed


"""
    Códigos para olhar:
    1. https://gist.github.com/sachinnair90/d2f720ff88f48dd4c057e6ced9d48913
    2. https://gist.github.com/kshitizlondon/71a26b35262d48501afa8d693316089e
    3. https://www.geeksforgeeks.org/implementation-of-hashing-with-chaining-in-python/
    4. https://gist.github.com/divanibarbosa/bd0a83fed85a63042c51723fd82a5014

"""

# constantes
FLAG = '#'
SIZE_X = 64
SEED = 42
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
# return -1 pra falha na operação


class SimpleTabulationHashing():
    def __init__(self, filename, size_table, seed=42, threshold_halving=0.25, threshold_table_doubling=0.75, threshold_clear=0.25):
        self.filename = filename
        self.log_operations = [] # lista de tuplas que guardará o log das operações

        self.random_tables = RandomTable(seed)

        self.m =  size_table # tamanho da tabela principal
        self.table = self.init_table()

        self.threshold_halving = threshold_halving
        self.threshold_table_doubling = threshold_table_doubling
        self.threshold_clear = threshold_clear
        
        self.count_flags = 0 # p
        self.count_elements = 0 # numero de elementos da tabela principal

        self.operations_dict = {
            "INC": self.insert,
            "REM": self.remove,
            "BUS": self.search
        }

    def init_table(self): # ok
        return [None for _ in range(0, self.m)]

    def load_file(self): # ok
        file = open(self.filename, "r")

        try:
            for line in file:
                operation, value = line.split(":")
                # self.log_operations.append((operations_dict[operation], int(value)))
                # CHAMAR OPERACOES AQUI
                result = operations_dict[operation](int(value))
                print(OPERATION, VALUE, RESULT)
            # print(self.log_operations)
            return 1
        except:
            return -1
        finally:
            file.close()
    
    def write_file(self, filename, filename_out):
        # TODO
        return 1

    def get_pieces_8bits(self, x): # ok
        x_bin = bin(x).zfill(SIZE_X).replace('b', '')

        pieces = []
        for _ in range(SIZE_RANDOM_TABLE_AND_PIECES):
            pieces.append(x_bin[-SIZE_RANDOM_TABLE_AND_PIECES:])
            x_bin = x_bin[:-SIZE_RANDOM_TABLE_AND_PIECES]

        return pieces[::-1], [int(piece, 2) for piece in pieces[::-1]]

    def h(self, x): # ok
        xor = 0
        pieces_bin, pieces_dec = self.get_pieces_8bits(x)
        for i, x in enumerate(pieces_dec):
            xor = xor ^ self.random_tables.get_element(i, x)
            # print("lista {}[{}] = {}".format(i, x, rt.get_element(i, x)))
        return xor

    def h_mod(self, x, i=0): # ok
        return (self.h(x) + i) % self.m

    # clear the remover's markers + shift values table
    def clear(self):
        #TODO: escrever no arquivo que passou por aqui
        return 1

    def remap_values(self, old_table):
        for i, value in enumerate(old_table):
            if value != None and value != FLAG:
                self.insert(value)

    def table_doubling(self): # acho que ok
        old_table = self.table.copy()
        self.m = self.m * 2
        self.table = init_table()
        self.remap_values(old_table)
        #TODO: escrever que passou por aqui

    def halving(self): # acho que ok
        old_table = self.table.copy()
        self.m = self.m / 2
        self.remap_values(old_table)
        #TODO: escrever no arquivo que passou por aqui

    def insert(self, x):
        """
        Insert integer x with 64 bits.
        Keep a copy if x is a copy.
        OBS: Attention to table doubling.
        """

        insert_ = False
        i = 0
        while (not insert_):
            if (i < self.m): # pra garantir que vai ter um break e não vai percorrer a lista varias e varias vezes circulamente
                position_element = self.h_mod(x, i)
                # print(i, position_element)
                if self.table[position_element] == None or self.table[position_element] == FLAG:
                    self.table[position_element] = x
                    # TODO: VERIFICAR SE É P CHAMAR TABLE DOUBLING
                    return 1
                i += 1
            else:
                insert_ = True

        self.count_elements += 1 
        #TODO: escrever no arquivo que passou por aqui
        return 1

    def remove(self, x):
        """
        Remove occurrence of x.
        First, search x. If find x, put flag # in position of x. Else, pass.
        OBS: Attention to halving.
        """
        position_element = self.search(x)

        if position_element != -1:
            print(position_element, self.table[position_element])
            self.table[position_element] = FLAG
            self.count_elements -= 1 

            # if (self.count_elements > this.) # TODO ver a formulazinha de 3
            #     self.halving()
            return 1
        # TODO: verificar se é necessário chamar having ou doubling
        # TODO: escrever no arquivo que passou por aqui
        return -1

    def search(self, x): # acho que ok
        """
        Search table's position of x
        """
        
        find = False
        i = 0
        while (not find):
            if (i < self.m): # pra garantir que vai ter um break e não vai percorrer a lista varias e varias vezes circulamente
                position_element = self.h_mod(x, i)
                # print(i, position_element)
                if self.table[position_element] == x:
                    return position_element
                i += 1
            else:
                find = True

        # TODO: escrever no arquivo que passou por aqui
        return -1
    