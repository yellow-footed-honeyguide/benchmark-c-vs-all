#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Kernel {
  uint64_t id;
  uint64_t data[64];
} Kernel;

Kernel *create_kernel(uint64_t id) {
  Kernel *kernel = malloc(sizeof(*kernel));
  if (!kernel)
    return NULL;
  kernel->id = id;
  // fill with zeros
  memset(kernel->data, 0, sizeof kernel->data);
  return kernel;
}

void destroy_kernel(Kernel *kernel) {
  // its safe to free NULL
  free(kernel);
}

void perform_work(Kernel *kernel) {
  for (size_t i = 0; i < 64; i++) {
    kernel->data[i] = kernel->id + i;
  }
}

int main(int argc, char *argv[]) {
  uint64_t iterations = strtoull(argv[1], NULL, 10);
  size_t array_size = strtoull(argv[2], NULL, 10);

  Kernel **objects = calloc(array_size, sizeof(*objects));
  assert(objects != NULL);

  uint64_t total = 0;

  for (uint64_t i = 0; i < iterations; i++) {
    size_t idx = i % array_size;

    destroy_kernel(objects[idx]);

    objects[idx] = create_kernel(i);
    assert(objects[idx] != NULL);

    perform_work(objects[idx]);
    total += objects[idx]->data[0];
  }

  // free everything. Its safe to free NULL
  for (size_t i = 0; i < array_size; i++) {
    free(objects[i]);
  }
  free(objects);

  printf("C version completed, total = %llu\n", total);

  return EXIT_SUCCESS;
}