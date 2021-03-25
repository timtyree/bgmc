// Uses a datastructure that has a two-dimensional array as a member. Create an instance of structure inside the function and return it
#include <stdio.h>
#include <stdlib.h>

typedef struct {
 int m[3][3];
} arr2d;

arr2d matrix_sum(int matrix1[][3], int matrix2[][3]){
    int i, j;
    arr2d result;

    for(i = 0; i < 3; i++){
        for(j = 0; j < 3; j++){
            result.m[i][j] = matrix1[i][j] + matrix2[i][j];
        }
    }
    return result;
}

int main(){
    int x[3][3], y[3][3];
    arr2d result;
    int i,j;

    printf("Enter the matrix1: \n");
    for(i = 0; i < 3; i++){
        for(j = 0; j < 3; j++){
            scanf("%d",&x[i][j]);
        }
    }

    printf("Enter the matrix2: \n");
    for(i = 0; i < 3; i++){
        for(j = 0; j < 3; j++){
            scanf("%d",&y[i][j]);
        }
    }

    result = matrix_sum(x,y);
    printf("The sum of the matrix is: \n");
    for(i = 0; i < 3; i++){
        for(j = 0; j < 3; j++){
            printf("%d",result.m[i][j]);
            printf("\t");
        }
        printf("\n");
    }

    return 0;
}
