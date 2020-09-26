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