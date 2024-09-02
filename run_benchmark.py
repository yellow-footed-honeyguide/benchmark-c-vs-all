#!/usr/bin/env python3  # Specifies the interpreter to use

# Import necessary libraries
import subprocess               # For running shell commands
import statistics               # For calculating mean execution time
import matplotlib.pyplot as plt # For creating plots
import seaborn as sns           # For enhancing plot aesthetics
import platform                 # For getting system information
from tabulate import tabulate   # For creating formatted tables
import re                       # For regular expression operations
import os                       # For file and directory operations
import shutil                   # For high-level file operations

# Define constant values
NUM_RUNS = 10                   # Number of benchmark runs for each program
WARMUP_RUNS = 3                 # Number of warmup runs before actual benchmarking

def run_command(command):
    """Execute a shell command and return its output."""
    # Run command and capture output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)  
    # Return stripped stdout
    return result.stdout.strip()  

def get_system_info():
    """Retrieve and format system information."""
    cpu_info = run_command("grep 'model name' /proc/cpuinfo | head -n 1 | sed 's/^.*: //' | awk '{print $1 \" \" $3}' | tr -d '\n'")  # Get CPU model
    kernel_version = run_command("uname -r | tr -d '\n'")  # Get kernel version
    return f"CPU: {cpu_info}, Kernel: {kernel_version}"  # Return formatted system info

def get_compiler_versions():
    """Retrieve versions of all compilers used in the benchmark."""
    return {
        # Get GCC version
        "GCC": run_command(r"gcc --version | grep -oP '(?<=GCC\) )\d+\.\d+\.\d+' | tr -d '\n'"),  
        # Get G++ version
        "G++": run_command(r"g++ --version | grep -oP '(?<=GCC\) )\d+\.\d+\.\d+' | tr -d '\n'"),
        # Get Clang version  
        "Clang": run_command(r"clang --version | grep -oP '(?<=version )\d+\.\d+\.\d+'"),
        # Get Clang++ version  
        "Clang++": run_command(r"clang++ --version | grep -oP '(?<=version )\d+\.\d+\.\d+'"),  
        # Get Rust version
        "Rust": run_command(r"rustc --version | grep -oP '\d+\.\d+\.\d+' | head -n 1"),  
        # Get Go version
        "Go": run_command(r"go version | grep -oP '(?<=go)\d+\.\d+\.\d+'")  
    }

def compile_programs():
    """Compile all benchmark programs with advanced optimization flags."""
    compile_commands = [
        "gcc -O3 -march=native -fomit-frame-pointer -flto -funroll-loops benchmark.c -o ./benchmark_gcc", 
        "g++ -O3 -march=native -fomit-frame-pointer -flto -funroll-loops benchmark.cpp -o ./benchmark_gpp",
        "clang -O3 -march=native -fomit-frame-pointer -flto -funroll-loops benchmark.c -o ./benchmark_clang",  
        "clang++ -O3 -march=native -fomit-frame-pointer -flto -funroll-loops benchmark.cpp -o ./benchmark_clangpp",  
        "rustc -C opt-level=3 -C target-cpu=native -C lto=fat -C codegen-units=1 benchmark.rs -o ./benchmark_rust", 
        "go build -o ./benchmark_go -ldflags '-s -w' -gcflags '-l=4' benchmark.go" 
    ]
    for cmd in compile_commands:
        subprocess.run(cmd, shell=True, check=True)  # Execute each compile command

def run_benchmark(command):
    """Execute a single benchmark run and return its execution time."""
    # Prepare command with time measurement
    full_command = f"/usr/bin/time -f 'Total execution time: %E' {command}"  
    # Run benchmark
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True, check=True)  

    time_output = result.stderr.strip()  # Extract time output from stderr
    # Parse time output
    match = re.search(r'Total execution time: (\d+):(\d+\.\d+)', time_output)  
    if match:
        minutes, seconds = match.groups()  # Extract minutes and seconds
        return float(minutes) * 60 + float(seconds)  # Convert to total seconds
    else:
        raise ValueError(f"Couldn't parse time output: {time_output}")  # Raise error if parsing fails

def benchmark():
    """Run benchmarks for all compiled programs."""
    current_dir = os.getcwd()  # Get current working directory
    programs = [
        ("C (GCC)", f"{current_dir}/benchmark_gcc"),  # C compiled with GCC
        ("C++ (G++)", f"{current_dir}/benchmark_gpp"),  # C++ compiled with G++
        ("C (Clang)", f"{current_dir}/benchmark_clang"),  # C compiled with Clang
        ("C++ (Clang++)", f"{current_dir}/benchmark_clangpp"),  # C++ compiled with Clang++
        ("Rust", f"{current_dir}/benchmark_rust"),  # Rust program
        ("Go", f"{current_dir}/benchmark_go")  # Go program
    ]

    results = {}
    for name, command in programs:
        # Print progress
        print(f"Running benchmark for {name}...")  

        for _ in range(WARMUP_RUNS):
            # Perform warmup runs
            run_benchmark(command)  
        # Run actual benchmarks
        times = [run_benchmark(command) for _ in range(NUM_RUNS)]
        # Calculate and store mean execution time  
        results[name] = statistics.mean(times)  

    return results

def create_plot(results, versions, system_info):
    """Generate a bar plot of benchmark results."""
    plt.figure(figsize=(12, 6))  # Create figure with specified size
    sns.set_style("whitegrid")  # Set Seaborn style
    sns.set_palette("deep")  # Set color palette

    sorted_results = sorted(results.items(), key=lambda x: x[1])  # Sort results by execution time
    languages = []
    for lang, _ in sorted_results:
        if lang.startswith("C ("):
            compiler = lang.split("(")[1][:-1]
            languages.append(f"{lang} {versions[compiler]}")  # Format C compiler versions
        elif lang.startswith("C++ ("):
            compiler = lang.split("(")[1][:-1]
            languages.append(f"{lang} {versions[compiler]}")  # Format C++ compiler versions
        elif lang == "Rust":
            languages.append(f"{lang} ({versions['Rust']})")  # Format Rust version
        elif lang == "Go":
            languages.append(f"{lang} ({versions['Go']})")  # Format Go version
    times = [time for _, time in sorted_results]  # Extract execution times

    bars = plt.bar(languages, times)  # Create bar plot

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.4f}s',
                 ha='center', va='bottom', fontweight='bold')  # Add labels to bars
    # Set x-axis label
    plt.xlabel('Language / Compiler', fontsize=12, fontweight='bold')  
    # Set y-axis label
    plt.ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold') 
    # Set plot title 
    plt.title('Benchmark Results: Execution Time Comparison', fontsize=16, fontweight='bold') 
    # Rotate x-axis labels 
    plt.xticks(rotation=45, ha='right')  

    # Add system info to plot
    plt.figtext(0.5, 0.01, f"System: {system_info}", ha="center", fontsize=8)  

    plt.tight_layout()  # Adjust layout
    # Save plot as PNG
    plt.savefig('assets/benchmark_results.png', dpi=300, bbox_inches='tight')  
    print("Chart saved as 'benchmark_results.png'")  # Confirm save

def print_results(results, versions, system_info):
    """Print benchmark results in a formatted table."""
    # Sort results by execution time
    sorted_results = sorted(results.items(), key=lambda x: x[1])  
    table_data = []
    for i, (lang, time) in enumerate(sorted_results, start=1):
        if lang.startswith("C ("):
            compiler = lang.split("(")[1][:-1]
            formatted_lang = f"{lang} {versions[compiler]}"  # Format C compiler versions
        elif lang.startswith("C++ ("):
            compiler = lang.split("(")[1][:-1]
            formatted_lang = f"{lang} {versions[compiler]}"  # Format C++ compiler versions
        elif lang == "Rust":
            formatted_lang = f"{lang} ({versions['Rust']})"  # Format Rust version
        elif lang == "Go":
            formatted_lang = f"{lang} ({versions['Go']})"    # Format Go version
        table_data.append([i, formatted_lang, f"{time:.4f}s"])  # Prepare table row
    
    headers = ["Rank", "Language (Compiler Version)", "Execution Time"]
    print("\nBenchmark Results:")
    # Print formatted table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))  
    # Print system info
    print(f"\nSystem Information: {system_info}")  
    # Print Python version
    print(f"Python version: {platform.python_version()}")  

def cleanup_binaries():
    """Remove all binary files created during the benchmark."""
    binaries = [
        "benchmark_gcc", "benchmark_gpp", "benchmark_clang",
        "benchmark_clangpp", "benchmark_rust", "benchmark_go"
    ]
    for binary in binaries:
        try:
            os.remove(binary)  # Attempt to remove each binary
            print(f"Removed {binary}")  # Confirm removal
        except OSError as e:
            print(f"Error removing {binary}: {e}")  # Print error if removal fails

def main():
    """Main function to orchestrate the benchmark process."""
    print("Starting benchmark process...")

    system_info = get_system_info()  # Retrieve system information
    versions = get_compiler_versions()  # Get compiler versions

    print("Compiling programs...")
    compile_programs()  # Compile all benchmark programs

    print("Running benchmarks...")
    results = benchmark()  # Run benchmarks and collect results

    print("Creating plot...")
    create_plot(results, versions, system_info)  # Generate result plot

    print("Printing results...")
    print_results(results, versions, system_info)  # Print results table

    print("Cleaning up binaries...")
    cleanup_binaries()  # Remove compiled binaries

    print("\nBenchmark completed successfully!")  # Indicate completion

if __name__ == "__main__":
    main()  # Execute main function if script is run directly
