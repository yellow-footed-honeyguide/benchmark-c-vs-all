# Language Performance Comparison

This benchmark presents a performance comparison of C, C++, Rust, and Go implementations for a specific task.

## Source Code & Benchmark Scripts

The benchmark was implemented in multiple languages. You can find the source code for each implementation in the following files:

| Language | Source File |
|----------|-------------|
| C        | [`benchmark.c`](benchmark.c) |
| C++      | [`benchmark.cpp`](benchmark.cpp) |
| Rust     | [`benchmark.rs`](benchmark.rs) |
| Go       | [`benchmark.go`](benchmark.go) |


Two scripts are provided to run the benchmarks with different optimization levels:

- [run_benchmark_standard_optimizations.sh](run_benchmark_standard_optimizations.sh): Runs benchmarks with basic optimizations.
- [run_benchmark_advanced_optimizations.sh](run_benchmark_advanced_optimizations.sh): Runs benchmarks with all possible optimizations for this language.


## Performance Results

### Versions: 

| Tool     | Version |
|----------|---------|
| gcc      | 14.1.1  |
| clang    | 18.1.6  |
| rustc    | 1.80.0  |
| go       | 1.22.6  |
| kernel   | 6.9.12  |


### Execution Time

| Language | Basic Optimization | Advanced Optimization | Improvement |
|----------|--------------------|-----------------------|-------------|
| C        | 3.69s              | 1.96s                 | 47%         |
| C++      | 4.29s              | 2.55s                 | 41%         |
| Rust     | 2.87s              | 2.49s                 | 13%         |
| Go       | 32.40s             | 32.74s                | -1%         |

**Note**: C gains the most from advanced optimizations, while Rust's basic optimizations are already highly effective.

### Memory Usage

| Language | Basic (KB) | Advanced (KB) |
|----------|------------|---------------|
| C        | 1920       | 1792          |
| C++      | 3964       | 3848          |
| Rust     | 2176       | 2304          |
| Go       | 24472      | 13672         |

**Note**: Go uses significantly more memory (8MB vs 2-4MB for others).

### Compilation Time

| Language | Basic (s) | Advanced (s) |
|----------|-----------|--------------|
| C        | 0.05      | 0.07         |
| C++      | 0.33      | 0.40         |
| Rust     | 0.16      | 4.91         |
| Go       | 0.07      | 0.08         |

## Additional Metrics

### Context Switches

| Language | Voluntary (Basic/Advanced) | Involuntary (Basic/Advanced) |
|----------|----------------------------|------------------------------|
| C        | 1 / 1                      | 36 / 7                       |
| C++      | 1 / 1                      | 29 / 19                      |
| Rust     | 1 / 1                      | 20 / 8                       |
| Go       | 258662 / 258689            | 118 / 176                    |

### Minor Page Faults

| Language | Basic   | Advanced |
|----------|---------|----------|
| C        | 201     | 203      |
| C++      | 272     | 272      |
| Rust     | 215     | 214      |
| Go       | 198669  | 246864   |

## Conclusion

- Rust shows good performance, with C following closely.
- C++ performs well but uses more memory than C and Rust.
- Advanced optimizations significantly improve C and C++ performance.
- Go has the longest execution time and highest memory usage but compiles quickly.
- Go is already optimized without extra compiler settings.

## Contributing

We aim to maintain a fair and accurate benchmark. 
If you have suggestions for improvement, please consider submitting a pull request with any of the following:

- A new programming language implementation
- Updated source code for an existing language to ensure fairness
- Refined optimization options for a particular implementation

Your contributions are welcome and will help enhance the quality of this benchmark.

## License

Distributed under the MIT License. See LICENSE for more information.

## Contact
Name:  Sergey Veneckiy   

Email: s.venetsky@gmail.com
