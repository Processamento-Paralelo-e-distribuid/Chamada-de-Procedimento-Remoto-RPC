# Chamada-de-Procedimento-Remoto-(RPC)

## Objetivo
Implementação de um sistema distribuido baseados na arquitetura Cliente/Servidor usando o conceito de chamada de procedimento remoto RPC nas linguagem C e Python

## Desenvolvimento
O desenvolvimento do código foi elaborado voltado para a ultilização de chamas RPC juntamente com mult-threading, o programa do cliente possue um (MENYU) que detre todas as suas opções vale destacar a opção 6 que possue a finalidade de mineração de seeds. Nesta opção o cliente gera e testa localmente seeds que possivelmente resolvam o desafio associado a transição atual passada pelo servidor.
Seu metodo de execução inicialmente busta o challeger atrelado à transição atual, posteriormente gera strigs de forma aleatorias e as decodifica para verificar se o hash associado a string resolve o desafio.

### Paralelismo
O paralelismo é abordado na criação das strings, onde são mantidas 11 threds operantes onde cada thread recrbe a função de gerar strings aleatórias de tamanho = size, quando uma thread termina sem o desafio ser solucionado uma nova thread de tamanho size+1 é criada. A quantidade de threads foi definida como 11, pois apartir de estudos anteriores em laboratorios passados, concluimos que para quantidades de threads maiores que 11, acaba-se gerando uma disputa entre as threads pelo tempo de CPU ocasionando um aumento drástico no tempo de execução.
E possivel fazer uma analise exploratoria 

