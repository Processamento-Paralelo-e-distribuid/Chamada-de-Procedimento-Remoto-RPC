from ctypes.wintypes import PINT
from operator import imod
from urllib import response
import xmlrpc.client
import sys
import random
import string
import threading
import pickle
from hashlib import sha1
import xdrlib as xdr

def printFort(text, aux, n=1):
    print(text, end="")
    print(" "*(aux-len(text)-n)+"|")
 
# Calcula total de argumentos
n = len(sys.argv)
 
# Verificação do uso correto/argumentos
if (n!=3):
    print("\nUso correto: rpcCalc_client, server_address, port_number.\n")
    exit(-1)

rpcServerAddr = "http://" + sys.argv[1] + ":" + sys.argv[2] + "/"
proxy = xmlrpc.client.ServerProxy(rpcServerAddr)

multicall = xmlrpc.client.MultiCall(proxy)

aux = 95
print("#"*aux)
printFort("|", aux)
text = "| MENU:"
printFort(text, aux)
text = "| (1) - getTransactionID."
printFort(text, aux)
text = "| (2) - getChallenge."
printFort(text, aux)
text = "| (3) - getTransactionStatus."
printFort(text, aux)
text = "| (4) - getWinner"
printFort(text, aux)
text = "| (5) - getSeed."
printFort(text, aux)
text = "| (6) - Minerar."
printFort(text, aux)
text = "| (7) - Printar MENU."
printFort(text, aux)

while(True):
    printFort("|", aux)
    print("#"*aux)
    printFort("|", aux)
    
    escolha = int(input("| Digite sua escolha do MENU: "))
    printFort("|", aux)
    print("#"*aux)
    printFort("|", aux)
    
    # 1 - getTransactionID()
    if(escolha == 1):
        transactionID = proxy.getTransactionID()
        text = "| O valor do ID da transação atual é "+str(transactionID)
        printFort(text, aux)
    # 2 - getChallenge()
    elif(escolha == 2):
        transactionID = int(input("| Digite o ID da transação: "))
        challenger = proxy.getChallenge(transactionID)
        if(challenger == -1):
            text = "| ID da transação invalido"
        else:
            text = "| O valor do desafio associado ao ID "+str(transactionID)+" e "+str(challenger)
        printFort(text, aux)
    # 3 - getTransactionStatus()
    elif(escolha == 3):
        transactionID = int(input("| Digite o ID da transação: "))
        status = proxy.getTransactionStatus(transactionID)
    
        text = ""
        if(status == -1):
            text = "| ID da transação invalido"
        elif(status == 0):
            text = "| A Transação já foi solucionada"
        elif(status == 1):
            text = "| Transação não foi solucionada, desafio pendente"
        printFort(text, aux)
        
    # 4 - getWinner()
    elif(escolha == 4):
        transactionID = int(input("| Digite o ID da transação: "))
        clientID = proxy.getWinner(transactionID)
        
        text = ""
        if(clientID == -1):
            text = "| ID da transação invalido"
        elif(clientID == 0):
            text = "| Transação não foi solucionada, sem vencedor"
        else:
            text = "| O valor do id do vencedor associado a transação "+str(transactionID)+" e "+str(clientID)
        printFort(text, aux)
    # 5 - getSeed()
    elif(escolha == 5):
        transactionID = int(input("| Digite o ID da transação: "))
        tupla = proxy.getSeed(transactionID)
        
        text = ""
        if(tupla == -1):
            text = "| ID da transação invalido"
        else:
            tupla= pickle.loads(tupla.data)
            if(tupla[2] == -1):
                text = "| Desafio não resolvido"
            else:
                text = "| Para a trasição de ID "+str(transactionID)+" e CHALLENGER "+str(tupla[0])+" foi encontrada uma seed \""+str(tupla[1])+"\" pelo cliente "+str(tupla[2])
        printFort(text, aux)
    # 6 - Minerar
    elif(escolha == 6):
        seed = []
        # 1 - Buscar trasactionID atual
        transactionID = proxy.getTransactionID()

        # 2 - Buscar challenge(desafio) associada ao transactionID atual;
        challenger = proxy.getChallenge(transactionID)

        # 3 - Buscar, localmente, uma seed (semente) que solucione o desafio proposto
        flag = True

        text = "| ID da transação atual: "+str(transactionID)+", desafio associado: "+str(challenger)
        printFort(text, aux)
        
        text = "| Procurando seed ..."
        printFort(text, aux)
        
        def random_generator(size=6, n=1, chars=string.printable): # Gera string aleatória
            random.seed(n)
            return ''.join(random.choice(chars) for _ in range(size))
        def getSeed(challenger, seed, size): # Gera seed
            n = 0
            size = 2
            while(flag):
                seedTemp = random_generator(size, n)
                texto = str(seedTemp).encode('utf-8')
                hash = sha1(texto).hexdigest()
                
                if(hash[0:challenger] == "0"*challenger and hash[challenger] != "0"):
                    seed.append(seedTemp)
                    break
                n = n + 1

        multThread = []

        for i in range(1,2):
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
        text = "| A seed encontrada é "+str(seed)
        printFort(text, aux)
        
        # 5 - Submete seed ao servidor e espera resposta.
        ClientID = int(input("| Digite o ID do cliente: "))
        
        resposta = proxy.submitChallenge(transactionID, ClientID, seed[0])
        
        # 6 - Imprime e decodfica resposta do servidor.
        text = ""
        if(resposta == -1):
            text = "| ID da transação invalido"
        elif(resposta == 0):
            text = "| A seed passada é invalida, logo não resolve o desafio"
        elif(resposta == 1):
            text = "| A seed passada é valida"
        elif(resposta == 2):
            text = "| O desafio já foi solucionado"
        printFort(text, aux)
    elif(escolha == 7):
        text = "| MENU:"
        printFort(text, aux)
        text = "| (1) - getTransactionID."
        printFort(text, aux)
        text = "| (2) - getChallenge."
        printFort(text, aux)
        text = "| (3) - getTransactionStatus."
        printFort(text, aux)
        text = "| (4) - getWinner"
        printFort(text, aux)
        text = "| (5) - getSeed."
        printFort(text, aux)
        text = "| (6) - Minerar."
        printFort(text, aux)
        text = "| (7) - Printar MENU."
        printFort(text, aux)
    else:
        break

    