#include <stdio.h>
#include <stdlib.h>
#include <openssl/sha.h>

typedef unsigned char byte;

int main(int argc, char *argv[]) {
    const int DataLen = 9;
    SHA_CTX shactx;
    byte digest[SHA_DIGEST_LENGTH];
    int i;

    byte* testdata = (byte *)malloc(DataLen);
    for (i=0; i<DataLen; i++) {
        testdata[i] = 128;
    }
    SHA1_Init(&shactx);
    SHA1_Update(&shactx, "(9%G]M]BA", DataLen);
    SHA1_Final(digest, &shactx);

    unsigned char hash[SHA_DIGEST_LENGTH*2];
    for (i=0; i<SHA_DIGEST_LENGTH; i++){
        int test=(int)digest[i];
        printf("%03d %d ", digest[i], test);
        sprintf((char*)&(hash[i*2]), "%02x", digest[i]);
    }
    printf("\nHash: %s\n", hash);
    int tag = 1;
    for(int i=0; i<5; i++){
        if(hash[i]!='0'){
            printf("Não é a seed %d", i);
            tag = 0;
            break;
        }
    }
    if(tag){
        if(hash[5]=='0'){
            tag = 0;
            printf("Não é a seed - 2");
        }else{
            printf("É a seed");
        }
    }
    
    printf("\nHash: %c\n", hash[0]);
    putchar('\n');
    return 0;
}