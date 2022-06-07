# Chamada-de-Procedimento-Remoto-(RPC)

## Objetivo
Implementação de um sistema distribuido baseados na arquitetura Cliente/Servidor usando o conceito de chamada de procedimento remoto RPC nas linguagem C e Python

## Desenvolvimento (Python)

O desenvolvimento do código foi elaborado voltado para a ultilização de chamas RPC juntamente com mult-threading, o programa do cliente possue um (MENU) que detre todas as suas opções vale destacar a opção 6 que possue a finalidade de mineração de seeds. Nesta opção o cliente gera e testa localmente seeds que possivelmente resolvam o desafio associado a transição atual passada pelo servidor.
Seu metodo de execução inicialmente busta o challeger atrelado à transição atual, posteriormente gera strigs de forma aleatorias e as decodifica para verificar se o hash associado a string resolve o desafio.

### Paralelismo
O paralelismo é abordado na criação das strings, onde são mantidas 11 threds operantes onde cada thread recrbe a função de gerar strings aleatórias de tamanho = size, quando uma thread termina sem o desafio ser solucionado uma nova thread de tamanho size+1 é criada. A quantidade de threads foi definida como 11, pois apartir de estudos anteriores em laboratorios passados, concluimos que para quantidades de threads maiores que 11, acaba-se gerando uma disputa entre as threads pelo tempo de CPU ocasionando um aumento drástico no tempo de execução.

### Analise Exploratoria
Na imagem logo abaixo temos uma pequena demonstração de como o tempo de execução aumenta de forma exponencia conforme almentamos o numero do desafio, entretanto é possivel que mesmo que o chalenger seje grande ele demore segundos para ser processado, pois as strings geradas de forma aleatória podem auxiliar para a diminuição do tempo de execução.
![alt text](https://github.com/arthurcoelho442/Chamada-de-Procedimento-Remoto-RPC/blob/Arthur/Imagens/Aumento%20de%20tempo%20de%20Execução.png)

### Execução do programa

#### **Local**
 [1] - Acesse a pasta "Python"
 [2] - Execute o servidor utilizando o comando logo abaixo:
```
pyrhon3 Serve.py
```
 [3] - Execute o cliente atravez do comando abaixo:
```
python3 cliente.py 127.0.0.1 8000
```
 [4] - Utilize das opções do Menu para explorar a comunicação local entre cliente e servidor.
#### **Remoto** 
 [1] - Acesse a pasta "Python"
 [2] - Execute o servidor utilizando o comando logo abaixo:
```
pyrhon3 Serve.py
```
 [3] - Execute o cliente atravez do comando abaixo, substituindo **ipSever** pelo ip da maquina ao qual o servido esta sendo rodado ex: (xxx.x.x.x):
```
python3 cliente.py **ipServe** 8000
```
 [4] - Utilize das opções do Menu para explorar a comunicação remota entre cliente e servidor.
