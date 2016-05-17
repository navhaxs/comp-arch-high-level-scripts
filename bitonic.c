#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define TRUE  1
#define FALSE 0
#define UP    1
#define DOWN  0
#define HIGH  1
#define LOW   0

// bitonic sort functions
void bitonicSort(int up, int low, int high);
void bitonicMerge(int up, int low, int high);
void bitonicCompare(int direction, int low, int high);

void printArray(int * array, int length);

int *data = NULL; // our "data memory" array to shuffle
int *tag = NULL;

int main(int argc, char * argv[]) {
    srand(100);
    data = (int *) malloc(sizeof(int)*8);
    tag = (int *) malloc(sizeof(int)*8);
    int i = 0;
    for (i = 0; i < 8; i++) {
        tag[i] = rand() % 50;
        data[i] = rand() % 50;
    }

    printf("%s\n", "Input\n");
    printf("%4s ", "Tag\n");
    printArray(tag, 8);
    printf("%4s ", "Data\n");
    printArray(data, 8);

    // sort data according to the 'tag' values, in ascending order.
    bitonicSort(TRUE, 0, 7);
    printf ("main() - returns from bitonic\n\n");
    printf("\n%s\n", "Output\n");
    printf("%4s ", "Tag\n");
    printArray(tag, 8);
    printf("%4s ", "Data\n");
    printArray(data, 8);

    return EXIT_SUCCESS;
}

void printArray(int *array, int length) {
    int i = 0;
    for (i = 0; i < length; i++) {
        printf("[%2d]->", array[i]);
    }
    printf("X\n\n");
}

void bitonicSort(int direction, int low, int high) {

    int length = high - low + 1;
    printf("sort() low=%d high=%d\n", low, high);

    if (length <= 1) {

         // do nothing

     } else {

		int midpoint = (low + high) / 2 + 1;


        bitonicSort(UP, low, midpoint-1);
        bitonicSort(DOWN, midpoint, high);
        bitonicMerge(direction, low, high);

    }

   printf("sort()-ret\n");
   return;
}

void bitonicMerge(int direction, int low, int high)  {
	printf("merge() low=%d high=%d\n", low, high);

    int length = high - low + 1;
    int midpoint = (low + high) / 2 + 1;

    if (length == 1) {

    } else {

        bitonicCompare(direction, low, high);

        bitonicMerge(direction, low, midpoint-1);
        bitonicMerge(direction, midpoint, high);

    }
    return;
}

// returns an array of same length as input x
void bitonicCompare(int direction, int low, int high) {//int *x, int length) {

    int length = high - low + 1;
    int dist = length / 2;

	printf("compare() low=%d high=%d length=%d dist=%d\n", low, high, length, dist);

    int i;
    for (i = low; i < low+dist; i++) {

		printf("\ti=%d < %d\n", i, low+dist);
        if ((tag[i] > tag[i+dist]) == direction) {

            // swap tags
            int tmp = tag[i];
            tag[i] = tag[i+dist];
            tag[i+dist] = tmp;

            // swap data
            int tmp2 = data[i];
            data[i] = data[i+dist];
            data[i+dist] = tmp2;

        }

    }

    return;// x;
}
