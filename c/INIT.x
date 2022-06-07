struct tabela {
    int transactionId;
    int challenge;
    char seed<>;
    int winner;
};

struct info{
    int transactionId;
    int clientId;
    int seed;
};

struct status {
    int challenge;
    char seed<>;
    int status;
};

program PROG {
    version VERSAO {
        int getTransactionId()=1;
        int getChallenge(int)=2;
        status getSeed(int)=3;
        int getWinner(int)=4;
        int submitChallenge(info)=5;
        int getTransactionStatus(int)=6;
    } = 100;
} = 55555555;