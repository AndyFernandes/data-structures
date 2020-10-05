file = open("input_file.txt", "r")

operations_dict = {
    "INC": "insert",
    "REM": "remove",
    "BUS": "search"
}

table = SimpleTabulationHashing("input_file.txt", 8)

operations = []

for line in file:
    operation, value = line.split(":")
    operations.append((operations_dict[operation], int(value)))
    if operation == "INC":
        retorno = table.insert(int(value))
        print(operation, value, retorno)
    elif operation == "REM":
        retorno = table.remove(int(value))
        print(operation, value, retorno)
    elif operation == "BUS":
        retorno = table.search(int(value))
        print(operation, value, retorno)

print(operations)
file.close()


rt = RandomTable(42)
rt.get_element(7, 255)


# path = '/content/drive/My Drive/Acadêmico/UFC/Mestrado/2020.1/Estrutura de Dados/Trabalho 02/'

table = SimpleTabulationHashing("input_file.txt", 8)

table.search(5)