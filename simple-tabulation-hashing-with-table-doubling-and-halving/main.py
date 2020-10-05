file = open("input_file.txt", "r")

operations_dict = {
    "INC": "insert",
    "REM": "remove",
    "BUS": "search"
}

operations = []

for line in file:
    operation, value = line.split(":")
    operations.append((operations_dict[operation], int(value)))

print(operations)
file.close()


rt = RandomTable(42)
rt.get_element(7, 255)


# path = '/content/drive/My Drive/Acadêmico/UFC/Mestrado/2020.1/Estrutura de Dados/Trabalho 02/'

table = SimpleTabulationHashing("input_file.txt", 8)

table.search(5)