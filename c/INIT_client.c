#include <stdio.h>
#include <stdlib.h>
#include <openssl/sha.h>
#include "INIT.h"
void getTransactionID_client(CLIENT *clnt)
{
	printf("Transacao atual: %d\n", *(gettransactionid_100(NULL, clnt)));
}
void getChallenge_client(CLIENT *clnt, int aux)
{
	int num = aux;
	printf("challenge pedido: %d\n", *(getchallenge_100(&num, clnt)));
}
void getTransactionStatus_client(CLIENT* clnt,int aux){
	int num = aux;
	int *result=gettransactionstatus_100(&num, clnt);
	printf("challenge pedido: %d\n", *result);
}

void getWinner_client(CLIENT* clnt,int aux){
	int num = aux;
	int *result=getwinner_100(&num, clnt);
	printf("challenge pedido: %d\n", *result);
}

void getSeed_client(CLIENT* clnt,int aux){
	int num=aux;
	status *result=getseed_100(&num, clnt);
	printf("challenge: %d\nseed: %d\nstatus: %d\n",result->challenge,result->seed, result->status);
	free(result->seed.seed_val);
}

int main(int argc, char *argv[])
{
	CLIENT *clnt;
	printf("Bem vindo a PPD mineiradores!!!\nEscolha um endereco de servidor e em seguida uma das seguintes opcoes:\n\nServer:\n");
	char server[100];
	scanf("%s", server);
	printf("\nEscolha o que deseja fazer usando numeros:\n1 getTransactionID\n2 getChallenge\n3 getTransactionStatus\n4 getWinner\n5 getSeed\n6 Mineirar\n7 Sair\nopcao: ");
	int op;
	scanf("%d", &op);
	if (op > 7 || op < 1)
	{
		printf("opcao invalida\n");
		exit(1);
	}
	clnt = clnt_create(server, PROG, VERSAO, "udp");

	if (clnt == (CLIENT *)NULL)
	{
		clnt_pcreateerror(argv[1]);
		exit(1);
	}
	while (1)
	{
		int aux;

		switch (op)
		{
			int challenge;
		case 1: // getTransactionID
			getTransactionID_client(clnt);
			break;
		case 2: // getChallanger
			printf("\nentre com o numero de transacao: ");
			scanf("%d", &aux);
			getChallenge_client(clnt, aux);
			/* code */
			break;
		case 3: // getTransactionStatus
			printf("\nentre com o numero de transacao: ");
			scanf("%d", &aux);
			getTransactionStatus_client(clnt, aux);
			break;
		case 4: // getWinner
			printf("\nentre com o numero de transacao: ");
			scanf("%d", &aux);
			getWinner_client(clnt, aux);
			break;
		case 5: // getSeed
			printf("\nentre com o numero de transacao: ");
			scanf("%d", &aux);
			getSeed_client(clnt, aux);
			break;
		case 6: // mineirar
			/* code */
			break;
		case 7: // sair
			exit(EXIT_SUCCESS);
			break;
		default:
			break;
		}
		printf("\nEscolha o que deseja fazer usando numeros:\n1 getTransactionID\n2 getChallenge\n3 getTransactionStatus\n4 getWinner\n5 getSeed\n6 Mineirar\n7 sair\nopcao: ");
		scanf("%d", &op);
		if (op > 7 || op < 1)
		{
			printf("opcao invalida\n");
			exit(1);
		}
	}

	exit(EXIT_SUCCESS);
}