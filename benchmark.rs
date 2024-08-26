// benchmark.rs
// rustc -O benchmark.rs -o benchmark_rs
// rustc -O benchmark.rs -C opt-level=3 -C target-cpu=native -C lto -o benchmark_rs
// /usr/bin/time -v ./benchmark_rs

const ITERATIONS : i64 = 100_000_000;  // Number of times to run the main loop
const ARRAY_SIZE : usize = 1000;       // Size of the object vector

// Structure representing a kernel object
struct KernelObject {
    id : i64,               // Unique identifier for the object
         data : [i64; 64],  // Array to store computed data
}

impl KernelObject {
    // Function to create a new KernelObject
    fn new (id : i64)->Self {
        KernelObject {
            id,
                data : [0; 64],  // Initialize all data elements to 0
        }
    }

    // Method to perform work on a KernelObject
    fn perform_work(&mut self) {
        for
            i in 0..64 {
                self.data[i] = (self.id + i as i64) &
                               0x7FFFFFFFFFFFFFFF;  // Compute data (ensure positive value)
            }
    }

    // Method to get data at specific index
    fn get_data(&self, index : usize) -> i64 {
        self.data[index]
    }
}

fn main() {
    let mut objects = Vec::with_capacity(ARRAY_SIZE);  // Vector to hold KernelObjects
    let mut total : i64 = 0;                           // Accumulator for benchmark results

    // Main benchmark loop
    for
        i in 0..ITERATIONS {
            let index = (i as usize) % ARRAY_SIZE;  // Cyclic index for object vector
            if index
                >= objects.len() {
                    objects.push(KernelObject::new (i));  // Add new object if vector isn't full
                }
            else {
                objects[index] = KernelObject::new (i);  // Replace existing object
            }
            objects[index].perform_work();  // Perform work on the object
            total = (total + objects[index].get_data(0)) &
                    0x7FFFFFFFFFFFFFFF;  // Update total (ensure positive)
            if i
                % 10_000_000 == 0 {
                    println !("Rust Intermediate {}: {}", i,
                              total);  // Print progress every 10 million iterations
                }
        }

    println !("Rust version completed, total: {}", total);  // Print final result
}
