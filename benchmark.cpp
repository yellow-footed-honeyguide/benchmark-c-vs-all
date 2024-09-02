// benchmark.cpp
// g++ benchmark.cpp -o benchmark_cpp
// clang++ benchmark.cpp -o benchmark_cpp
// /usr/bin/time -f "Total execution time: %E" ./benchmark_cpp

#include <iostream>   // For input/output operations
#include <vector>     // For dynamic array (vector)
#include <memory>     // For smart pointers (unique_ptr)
#include <cstdint>    // For int64_t type
#include <array>      // For fixed-size array

constexpr int64_t ITERATIONS = 10000000;  // Number of times to run the main loop
constexpr int ARRAY_SIZE = 1000;           // Size of the object array

// Class representing a kernel object
class KernelObject {
public:
    // Constructor: initialize object with given id
    KernelObject(int64_t id) : id(id) {
        std::fill(data.begin(), data.end(), 0);  // Initialize all data elements to 0
    }

    // Method to perform work on the object
    void perform_work() {
        for (int i = 0; i < 64; i++) {
            data[i] = (id + i) & 0x7FFFFFFFFFFFFFFFLL;  // Compute data (ensure positive value)
        }
    }

    // Method to get data at specific index
    int64_t get_data(int index) const { return data[index]; }

private:
    int64_t id;                 // Unique identifier for the object
    std::array<int64_t, 64> data;  // Array to store computed data
};

int main() {
    // Vector to hold smart pointers to KernelObjects
    std::vector<std::unique_ptr<KernelObject>> objects(ARRAY_SIZE);
    int64_t total = 0;  // Accumulator for benchmark results

    // Main benchmark loop
    for (int64_t i = 0; i < ITERATIONS; i++) {
        int index = i % ARRAY_SIZE;  // Cyclic index for object array
        objects[index] = std::make_unique<KernelObject>(i);  // Create new object
        objects[index]->perform_work();  // Perform work on the object
        total = (total + objects[index]->get_data(0)) & 0x7FFFFFFFFFFFFFFFLL;  // Update total (ensure positive)
        if (i % 10000000 == 0) {
            std::cout << "C++ Intermediate " << i << ": " << total << std::endl;  // Print progress every 10 million iterations
        }
    }

    std::cout << "C++ version completed, total: " << total << std::endl;  // Print final result
    return 0;
}
