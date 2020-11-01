"""
INSTRUCTIONS:
    - inicialize one VEB with:
        veb = VEB(W), w by default is 64

    - to use only use remove, insert, search, predecessor or sucessor to standard operations
        veb.insert(X)
        veb.remove(X)
        veb.search(X)
        veb.sucessor(X)
        veb.predecessor(X)

    - to visualize resulte, you can .log_operations or print
        print(veb.log_operations)

    - to load_file or write file using:
        veb.load_file(FILENAME)
        veb.write_file(FILENAME)

"""
from van_emde_boas import VEB

veb = VEB(16) #obs: instanciei aqui com 16 pq eu rodei com 64 e 32 na minha maqunia e travou, rs

veb.load_file("input_file.txt")
print(veb.log_operations)
veb.write_file("out.txt")

################################################### TESTES DOS ELEMENTOS DO ARQUIVO
# veb.insert(10)
# veb.insert(20)
# veb.insert(30)
# veb.insert(37)
# print(veb.sucessor(10))
# print(veb.sucessor(15))
# print(veb.predecessor(42))
# print(veb.remove(37))
# print(veb.predecessor(42))


#################################################### TESTES GERAIS
# from random import randint
# insertions = [randint(1, 200) for i in range(200)]

# veb = VEB(32)
# print(veb.w, veb.u, veb.sqrt_u)

# # Testando inserção
# print("--------------- TESTANDO INSERCAO ------------")
# for index, i in enumerate(insertions):
#     print("--------------")
#     print("Numero = ", i)
#     veb.insert(i)

# # Testando Busca
# print("--------------- TESTANDO BUSCA ------------")
# for element in insertions:
#     print("Elemento {} = {}".format(element, veb.search(element)))

# # Testando Sucessor
# print("--------------- TESTANDO SUCESSOR ------------")
# lista = list(set(sorted(insertions)))
# for index, element in enumerate(lista):
#     try:
#         print("Elemento {} seu sucessor é {}? {}".format(element, lista[index+1], lista[index+1]==veb.sucessor(element)))
#     except:
#         print("Último elemento! {} seu sucessor é {}? {}".format(element, element+1, (element+1)==veb.sucessor(element)))

# # Testando Predecessor
# print("--------------- TESTANDO PREDECESSOR ------------")
# lista_2 = lista[::-1]
# for index, element in enumerate(lista_2):
#     try:
#         print("Elemento {} seu predecessor é {}? {}".format(element, lista_2[index+1], lista_2[index+1]==veb.predecessor(element)))
#     except:
#         print("Último elemento! {} seu predecessor é {}? {}".format(element, element+1, (element+1)==veb.predecessor(element)))

# # Testando Remoção
# veb.search(182)
# veb.remove(182)
# veb.search(182)

# veb.search(20)
# veb.remove(20)
# veb.search(20)