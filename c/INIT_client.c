#include <stdio.h>
#include <stdlib.h>
#include <openssl/sha.h>
#include "INIT.h"
#include <pthread.h>

void *function(void *arg)
{
	int tr = *(gettransactionid_100(NULL, arg));
	status *sd = getseed_100(&tr, arg);
	int cl = getchallenge_100(&tr, arg);
	while (1)
	{
		const int DataLen = 1;
		SHA_CTX shactx;
		unsigned char digest[SHA_DIGEST_LENGTH];
		int i;

		unsigned char *testdata = (unsigned char *)malloc(DataLen);
		for (i = 0; i < DataLen; i++)
		{
			testdata[i] = 128;
		}
		SHA1_Init(&shactx);
		SHA1_Update(&shactx, "l", DataLen);
		SHA1_Final(digest, &shactx);

		unsigned char hash[SHA_DIGEST_LENGTH * 2];
		for (i = 0; i < SHA_DIGEST_LENGTH; i++)
		{
			int test = (int)digest[i];
			printf("%03d %d ", digest[i], test);
			sprintf((char *)&(hash[i * 2]), "%02x", digest[i]);
		}
		printf("\nHash: %s\n", hash);
		int tag = 1;
		for (int i = 0; i < 1; i++)
		{
			if (hash[i] != '0')
			{
				printf("Não é a seed %d", i);
				tag = 0;
				break;
			}
		}
		if (tag)
		{
			if (hash[1] == '0')
			{
				tag = 0;
				printf("Não é a seed - 2");
			}
			else
			{
				printf("É a seed");
			}
		}

		printf("\nHash: %c\n", hash[0]);
		putchar('\n');
		return 0;
	}
}

void getTransactionID_client(CLIENT *clnt)
{
	printf("Transacao atual: %d\n", *(gettransactionid_100(NULL, clnt)));
}

void getChallenge_client(CLIENT *clnt, int aux)
{
	int num = aux;
	printf("challenge pedido: %d\n", *(getchallenge_100(&num, clnt)));
}
void getTransactionStatus_client(CLIENT *clnt, int aux)
{
	int num = aux;
	int *result = gettransactionstatus_100(&num, clnt);
	printf("challenge pedido: %d\n", *result);
}

void getWinner_client(CLIENT *clnt, int aux)
{
	int num = aux;
	int *result = getwinner_100(&num, clnt);
	printf("challenge pedido: %d\n", *result);
}

void getSeed_client(CLIENT *clnt, int aux)
{
	int num = aux;
	status *result = getseed_100(&num, clnt);
	printf("challenge: %d\nseed: %d\nstatus: %d\n", result->challenge, result->seed, result->status);
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
			// pthread t1;
			// int a;
			// pthread_create(&t1, NULL, function, (void *)(&a));
			pthread_t t[10];
			char **seed;
			for (int i = 0; i < 10; i++)
			{
				int *a = malloc(sizeof(int));
				*a = i;
				if (pthread_create(t + i, NULL, &function, &seed) != 0)
				{
					return 1;
				}
			}
			for (int i = 0; i < 10; i++)
			{
				if (pthread_join(t[i], (void **)&seed) != 0)
				{
					return 2;
				}
			}
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