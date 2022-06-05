from copyreg import pickle
import pandas as pd
import random
import xdrlib as xdr
import pickle
from hashlib import sha1
from xmlrpc.server import SimpleXMLRPCServer

global arquivo 
arquivo = 'banco-de-dados.csv'

def getTransactionID():
    print(arquivo)
    try:
        df = pd.read_csv(arquivo)
        print("Arquivo encontrado")

    except:
        print("Criando Banco de dados")
        df = None
    transactionID = 0
    
    if(df is None):
        lista = {"TransactionID":[0],"Challenge":[random.randint(1,129)],"Seed":[" "],"Winner":[-1]}
        df = pd.DataFrame(lista)
    else:
        tam = len(df.iloc[:,0])
        if(df.iloc[tam-1,3] == -1):
            return int(df.iloc[tam-1,0])
        else:
            transactionID = df.iloc[(tam-1),0]+1
            lista = {"TransactionID":transactionID,"Challenge":[random.randint(1,129)],"Seed":[" "],"Winner":[-1]}
            transaction = pd.DataFrame(lista)
            
            df = pd.concat([df,transaction], ignore_index=True)    
    
    df.to_csv(arquivo, index=False)

    return int(transactionID)
def getChallenge(transactionID):
    try:
        df = pd.read_csv(arquivo)
    except:
        return -1
        
    trasition = df.query("TransactionID == "+str(transactionID))
    
    if(trasition.empty == False):
        return int(trasition["Challenge"].values[0])
    else:
        return -1
def getTransactionStatus(transactionID):
    try:
        df = pd.read_csv(arquivo)
    except:
        return -1
    
    trasition = df.query("TransactionID == "+str(transactionID))
    
    if(trasition.empty == False):
        if(trasition["Winner"].values != -1):
            return 0
        else:
            return 1
    else:
        return -1
    
def submitChallenge(transactionID, ClientID, seed):
    try:
        df = pd.read_csv(arquivo)
    except:
        return -1
    
    trasition = df.query("TransactionID == "+str(transactionID))    
    
    if(trasition.empty == True):
        return -1
    elif(trasition["Winner"].values != -1):
        return 2
    
    texto = str(seed).encode('utf-8')
    hash = sha1(texto).hexdigest()
    
    challenge = trasition["Challenge"].values[0]
    
    if(hash[0:challenge] == "0"*challenge and hash[challenge] != "0"):
        trasition.loc[transactionID,"Seed"]   = str(seed)
        trasition.loc[transactionID,"Winner"] = ClientID
        df.iloc[transactionID,:] = trasition.iloc[0,:]
        
        df.to_csv(arquivo, index=False)
        return 1
    else:
        return 0

def getWinner(transactionID):
    try:
        df = pd.read_csv(arquivo)
    except:
        return -1
    
    trasition = df.query("TransactionID == "+str(transactionID))
    
    if(trasition.empty == False):
        if(trasition["Winner"].values == -1):
            return 0
        else:
            return int(trasition["Winner"].values[0])
    else:
        return -1
def getSeed(transactionID):
    try:
        df = pd.read_csv(arquivo)
    
        trasition = df.query("TransactionID == "+str(transactionID))        
        tupla = tuple(trasition.iloc[0,1:].values)

        return pickle.dumps(tupla)
    except:
        return -1

server = SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Listening on port 8000...")

server.register_function(getTransactionID, 'getTransactionID')
server.register_function(getChallenge, 'getChallenge')
server.register_function(getTransactionStatus, 'getTransactionStatus')
server.register_function(submitChallenge, 'submitChallenge')
server.register_function(getWinner, 'getWinner')
server.register_function(getSeed, 'getSeed')
server.register_multicall_functions()

server.serve_forever()