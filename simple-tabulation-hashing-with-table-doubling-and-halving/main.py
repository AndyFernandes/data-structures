path = '/content/drive/My Drive/Acadêmico/UFC/Mestrado/2020.1/Estrutura de Dados/Trabalho 02/'

# file = open(path+"input_file.txt", "r")

table = SimpleTabulationHashing(8)

table.load_file(path+"input_file.txt")
print(table.table)

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

table.write_file(path+"out.txt")