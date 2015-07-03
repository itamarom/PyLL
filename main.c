#include <stdio.h>

int a();

int main(){
    printf("hello world\n");
    int x = 5;
    printf("gitlitz\n");
    x++;
    a();
    return 0;
}

int a(){
    return 3;
}

int b(int x){
    return x;
}

int c(int x, int y){
    x++;
    y+= x;
    return y;
}
