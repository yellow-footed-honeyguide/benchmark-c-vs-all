#!/bin/bash

# Function to compile and check for errors
compile() {
    echo "Compiling $1..."
    if $2; then
        echo "$1 compiled successfully."
    else
        echo "Error compiling $1. Exiting."
        exit 1
    fi
}

# Compile all benchmarks with Max optimization
compile_with_timing() {
    lang=$1
    compile_cmd=$2
    
    echo "Compiling $lang benchmark"
    echo "Command: $compile_cmd"
    
    start_time=$(date +%s.%N)
    eval $compile_cmd
    end_time=$(date +%s.%N)
    
    if [ $? -ne 0 ]; then
        echo "Error compiling $lang benchmark. Exiting."
        exit 1
    fi
    
    compile_time=$(echo "$end_time - $start_time" | bc)
    printf "Compilation time: %.2f seconds\n\n" $compile_time
}

# C benchmark
c_compile_cmd="clang -O3 -march=native -flto benchmark.c -o benchmark_c"
compile_with_timing "C" "$c_compile_cmd"

# C++ benchmark
cpp_compile_cmd="clang++ -O3 -march=native -flto  benchmark.cpp -o benchmark_cpp"
compile_with_timing "C++" "$cpp_compile_cmd"

# Rust benchmark
rust_compile_cmd="rustc -O benchmark.rs -C opt-level=3 -C target-cpu=native -C lto -o benchmark_rs"
compile_with_timing "Rust" "$rust_compile_cmd"

# Go benchmark
go_compile_cmd="go build -o benchmark_go benchmark.go"
compile_with_timing "Go" "$go_compile_cmd"

echo "All benchmarks compiled successfully."


# Run benchmarks
echo "Running benchmarks..."
echo "C Benchmark:" && /usr/bin/time -v ./benchmark_c
echo -e "\nC++ Benchmark:" && /usr/bin/time -v ./benchmark_cpp
echo -e "\nRust Benchmark:" && /usr/bin/time -v ./benchmark_rs
echo -e "\nGo Benchmark:" && /usr/bin/time -v ./benchmark_go

# Remove binaries
rm benchmark_c benchmark_cpp benchmark_rs benchmark_go
echo "All benchmarks completed."
