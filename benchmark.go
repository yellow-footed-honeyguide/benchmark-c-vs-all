// benchmark.go - Performance comparison for kernel-like operations
// go build -o benchmark_go benchmark.go
// go build -o benchmark_go benchmark.go
// /usr/bin/time -v ./benchmark_go


package main

import (
    "fmt"  // For formatted I/O
)

const (
    ITERATIONS = 100000000  // Number of times to run the main loop
    ARRAY_SIZE = 1000       // Size of the object array
)

// Structure representing a kernel object
type KernelObject struct {
    id   int64     // Unique identifier for the object
    data [64]int64 // Array to store computed data
}

// Function to create a new KernelObject
func newKernelObject(id int64) *KernelObject {
    return &KernelObject{id: id}  // Return pointer to new KernelObject with given id
}

// Method to perform work on a KernelObject
func (ko *KernelObject) performWork() {
    for i := 0; i < 64; i++ {
        ko.data[i] = (ko.id + int64(i)) & 0x7FFFFFFFFFFFFFFF  // Compute data (ensure positive value)
    }
}

// Method to get data at specific index
func (ko *KernelObject) getData(index int) int64 {
    return ko.data[index]
}

func main() {
    objects := make([]*KernelObject, ARRAY_SIZE)  // Slice to hold pointers to KernelObjects
    var total int64 = 0  // Accumulator for benchmark results

    // Main benchmark loop
    for i := int64(0); i < ITERATIONS; i++ {
        index := i % ARRAY_SIZE  // Cyclic index for object array
        objects[index] = newKernelObject(i)  // Create new object
        objects[index].performWork()  // Perform work on the object
        total = (total + objects[index].getData(0)) & 0x7FFFFFFFFFFFFFFF  // Update total (ensure positive)
        if i%10000000 == 0 {
            fmt.Printf("Go Intermediate %d: %d\n", i, total)  // Print progress every 10 million iterations
        }
    }

    fmt.Printf("Go version completed, total: %d\n", total)  // Print final result
}
