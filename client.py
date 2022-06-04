from ctypes.wintypes import PINT
from urllib import response
import xmlrpc.client
import sys
import random
import string
import threading
from hashlib import sha1
 
# Calcula total de argumentos
n = len(sys.argv)
 
# Verificação do uso correto/argumentos
if (n!=3):
    print("\nUso correto: rpcCalc_client, server_address, port_number.\n")
    exit(-1)

rpcServerAddr = "http://" + sys.argv[1] + ":" + sys.argv[2] + "/"
proxy = xmlrpc.client.ServerProxy(rpcServerAddr)

multicall = xmlrpc.client.MultiCall(proxy)

seed = []

print("\nMENU:")
print("(1) - getTransactionID.")
print("(2) - getChallenge.")
print("(3) - getTransactionStatus.")
print("(4) - getWinner.")
print("(5) - getSeed.")
print("(6) - Minerar.")


while(True):
    escolha = int(input("\nDigite sua escolha do MENU: "))
    
    # 1 - getTransactionID()
    if(escolha == 1):
        transactionID = proxy.getTransactionID()
        print("\n|O valor do ID da transação atual é {}|".format(transactionID))
    # 2 - getChallenge()
    elif(escolha == 2):
        transactionID = int(input("Digite o ID da transação: "))
        challenger = proxy.getChallenge(transactionID)
        print("\n|O valor do desafio associado ao ID {} e {}|".format(transactionID, challenger))
    # 3 - getTransactionStatus()
    elif(escolha == 3):
        transactionID = int(input("Digite o ID da transação: "))
        status = proxy.getTransactionStatus(transactionID)
    
        if(status == -1):
            print("\n|ID da transação invalido|")
        elif(status == 0):
            print("\n|A Transação já foi solucionada|")
        elif(status == 1):
            print("\n|Transação não foi solucionada, desafio pendente|")
        
    # 4 - getWinner()
    elif(escolha == 4):
        transactionID = int(input("Digite o ID da transação: "))
        clientID = proxy.getWinner(transactionID)
        if(clientID == -1):
            print("\n|ID da transação invalido|")
        elif(clientID == 0):
            print("\n|Transação não foi solucionada, sem vencedor|")
        else:
            print("\n|O valor do id do vencedor associado a transação {} e {}|".format(transactionID, clientID))

    # 5 - getSeed()
    elif(escolha == 5):
        transactionID = int(input("Digite o ID da transação: "))
        tupla = proxy.getSeed(transactionID)
        if(tupla == -1):
            print("\n|ID da transação invalido|")
        else:
            print("\n|{}|".format(tupla))
    # 6 - Minerar
    elif(escolha == 6):
        # 1 - Buscar trasactionID atual
        transactionID = proxy.getTransactionID()

        # 2 - Buscar challenge(desafio) associada ao transactionID atual;
        challenger = proxy.getChallenge(transactionID)

        # 3 - Buscar, localmente, uma seed (semente) que solucione o desafio proposto
        flag = True

        def random_generator(size=6, n=1, chars=string.printable): # Gera string aleatória
            random.seed(n)
            return ''.join(random.choice(chars) for _ in range(size))
        def getSeed(challenger, seed, size): # Gera seed
            n = 0
            while(flag):
                seedTemp = random_generator(size, n)
                texto = str(seedTemp).encode('utf-8')
                hash = sha1(texto).hexdigest()
                
                if(hash[0:challenger] == "0"*challenger and hash[challenger] != "0"):
                    seed.append(seedTemp)
                    break
                n = n + 1

        multThread = []

        for i in range(1,challenger*2+1):
            thread = threading.Thread(target=getSeed, args=(challenger, seed, i, ))
            multThread.append(thread)
            thread.start()
            
            if(len(seed) > 0):
                flag = False
                break   

        while(True):
            if(len(seed) != 0):
                break

        flag = False

        # Verifica se todas as threads acabaram 
        for thread in multThread:
            thread.join()

        # 4 - Imprimir localmente a seed encontrada
        print("\n|A seed encontrada é {}|".format(seed))
            
        # 5 - Submete seed ao servidor e espera resposta.
        ClientID = int(input("Digite o ID do cliente: "))
        
        resposta = proxy.submitChallenge(transactionID, ClientID, seed[0])
        
        # 6 - Imprime e decodfica resposta do servidor.
        if(resposta == -1):
            print("\n|ID da transação invalido|")
        elif(resposta == 0):
            print("\n|A seed passada é invalida, logo não resolve o desafio|")
        elif(resposta == 1):
            print("\n|A seed passada é valida|")
        elif(resposta == 2):
            print("\n|O desafio já foi solucionado|")
    else:
        break

    