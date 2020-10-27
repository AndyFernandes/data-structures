"""
INSTRUCTIONS:
    - inicialize one simple_tabulation_hashing with:
        table = simple_tabulation_hashing.SimpleTabulationHashing(SIZE_TABLE)

    - to use here, only use remove, insert or search to standard operations
        table.insert(X)
        table.remove(X)
        table.search(X)

    - to visualize resulte, you can acess .table or .log_operations
        print(table.table)
        print(table.log_operations)

    - to test halving, clear or table doubling acess:
        table.halving()
        table.clear()
        table.table_doubling()

    - to load_file or write file using:
        table.load_file(FILENAME)
        table.write_file(FILENAME)

"""

import simple_tabulation_hashing

file = open("input_file.txt", "r")

table = simple_tabulation_hashing.SimpleTabulationHashing(8)

table.load_file("input_file.txt")

print("Table after load file: \n")
print(table.table)

print("\nLog operations after load file: \n")

print(table.log_operations)

print("\n---------------------------------------------")
print("\nTest operations: \n")

table.remove(42)
table.remove(25)
table.insert(25)
table.insert(425)
# table.insert(42)
# table.search(42)
# table.remove(42)
# table.remove(42)

print(table.table)
print(table.log_operations)

table.write_file("out.txt")