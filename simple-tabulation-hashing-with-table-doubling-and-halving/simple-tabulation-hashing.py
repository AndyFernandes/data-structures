import numpy as numpy

class SimpleTabulationHashing():
    def __init__(self, filename):
        self.c = 8
        self.table = []
        self.size =  2
        self.filename = filename

    def init_random_tables(self):
        return 1

    def load_file(self, filename):
        return 1
    
    def write_file(self, filename, filename_out):
        return 1

    # Hash function
    def h(self, x):
        return 1

    # clear the remover's markers + shift values table
    def clear(self):
        return 1

    def table_doubling(self):
        return 1

    def halving(self):
        return 1

    def insert(self, x):
        """
        Insert integer x with 64 bits.
        Keep a copy if x is a copy.
        OBS: Attention to table doubling.
        """
        return 1

    def remove(self, x):
        """
        Remove occurrence of x.
        First, search x. If find x, put flag # in position of x. Else, pass.
        OBS: Attention to halving.
        """
        return 1

    def search(self, x):
        """
        Search table's position of x
        """
        return 1
    