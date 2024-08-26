// benchmark.c
// gcc -O2 benchmark.c -o benchmark_c
// clang -O3 -march=native -flto benchmark.c -o benchmark_c
// /usr/bin/time -v ./benchmark_c

#include <stdint.h>  // For int64_t type
#include <stdio.h>   // For input/output operations
#include <stdlib.h>  // For memory allocation

#define ITERATIONS 100000000  // Number of times to run the main loop
#define ARRAY_SIZE 1000       // Size of the object array

// Structure representing a kernel object
struct kernel_object {
    int64_t id;        // Unique identifier for the object
    int64_t data[64];  // Array to store computed data
};

// Function to create and initialize a new kernel object
struct kernel_object *create_object(int64_t id) {
    struct kernel_object *obj =
        malloc(sizeof(struct kernel_object));  // Allocate memory for the object
    if (obj) {                                 // If allocation was successful
        obj->id = id;                          // Set the object's id
        for (int i = 0; i < 64; i++) {
            obj->data[i] = 0;  // Initialize all data elements to 0
        }
    }
    return obj;  // Return the created object (or NULL if allocation failed)
}

// Function to perform work on a kernel object
void perform_work(struct kernel_object *obj) {
    for (int i = 0; i < 64; i++) {
        obj->data[i] =
            (obj->id + i) & 0x7FFFFFFFFFFFFFFFLL;  // Compute data (ensure positive value)
    }
}

int main() {
    struct kernel_object *objects[ARRAY_SIZE] = {NULL};  // Array to hold kernel objects
    int64_t total = 0;                                   // Accumulator for benchmark results

    // Main benchmark loop
    for (int64_t i = 0; i < ITERATIONS; i++) {
        int index = i % ARRAY_SIZE;  // Cyclic index for object array
        if (objects[index]) {
            free(objects[index]);  // Free old object if it exists
        }
        objects[index] = create_object(i);  // Create new object
        perform_work(objects[index]);       // Perform work on the object
        total = (total + objects[index]->data[0]) &
                0x7FFFFFFFFFFFFFFFLL;  // Update total (ensure positive)
        if (i % 10000000 == 0) {
            printf("C Intermediate %ld: %ld\n", i,
                   total);  // Print progress every 10 million iterations
        }
    }

    // Clean up allocated memory
    for (int i = 0; i < ARRAY_SIZE; i++) {
        if (objects[i]) {
            free(objects[i]);
        }
    }

    printf("C version completed, total: %ld\n", total);  // Print final result
    return 0;
}
