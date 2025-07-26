#!/usr/bin/env python3
import subprocess
import shutil
import statistics
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import time

# Config
MIN_ARRAY_SIZE = 10000
MAX_ARRAY_SIZE = 100000
SAMPLES = 10 # sample points between min/max array sizes
WARMUP = 2 # warmup runs before measuring
RUNS = 5 # number of timed runs per sample

# language -> build / run commands
LANGS = {
    'gcc':   {'build': ['gcc', '-O3', '-ffast-math', '-march=native', "-s", 'benchmark.c', '-o', 'benchmark_gcc'],
              'run':   './benchmark_gcc'},
    'clang': {'build': ['clang', '-O3', '-ffast-math', '-march=native', "-s", 'benchmark.c', '-o', 'benchmark_clang'],
              'run':   './benchmark_clang'},
    'g++':   {'build': ['g++', '-O3', '-ffast-math', '-fno-rtti', '-fno-exceptions', '-march=native', "-s", 'benchmark.cpp', '-o', 'benchmark_gpp'],
              'run':   './benchmark_gpp'},
    'clang++':{'build': ['clang++', '-O3' ,'-ffast-math', '-fno-rtti', '-fno-exceptions', '-march=native', "-s", 'benchmark.cpp', '-o', 'benchmark_clangpp'],
              'run':   './benchmark_clangpp'},
    'go':    {'build': ['go', 'build', '-o', 'benchmark_go', '-ldflags=-s -w', 'benchmark.go'],
              'run':   './benchmark_go'},
}

# Detect and build Rust separately if Cargo is available (downloading, building and linking std is not trivial)
if shutil.which('cargo'):
    print('Building Rust...')
    subprocess.run(
        ['cargo', 'build', '-Zbuild-std=std,panic_abort', '--release'],
        cwd='benchmark-rs', check=True
    )
    rust_bin = Path('benchmark-rs/target/release') / (
        'bench-rs.exe' if sys.platform == 'win32' else 'bench-rs'
    )
    if rust_bin.exists():
        LANGS['rust'] = {'build': None, 'run': str(rust_bin)}
    else:
        print(f'Skipping rust: {rust_bin} not found')
else:
    print('Skipping rust: cargo not found')

# Build available languages
for lang, cfg in list(LANGS.items()):
    build_cmd = cfg.get('build')
    # skip if compiler missing
    if build_cmd and not shutil.which(build_cmd[0]):
        print(f'Skipping {lang}: compiler not found')
        LANGS.pop(lang)
        continue
    # actaully build
    if build_cmd:
        print(f'Building {lang}...')
        subprocess.run(build_cmd, check=True)

# Generate range of sample sizes
sizes = [int(MIN_ARRAY_SIZE + i*(MAX_ARRAY_SIZE-MIN_ARRAY_SIZE)/(SAMPLES-1)) for i in range(SAMPLES)]
results = {lang: [] for lang in LANGS}

# Run benchmarks
total_langs = list(LANGS.keys())
for size in sizes:
    iters = size * 10 # just arbitrary integer scaling
    print(f'Problem size={size}, iterations={iters}')
    for lang in total_langs:
        cfg = LANGS.get(lang)
        if not cfg:
            continue
        exe = cfg['run']
        # warmup
        for _ in range(WARMUP):
            subprocess.run([exe, str(iters), str(size)], stdout=subprocess.DEVNULL)
        # timed runs
        times = []
        for _ in range(RUNS):
            t0 = time.perf_counter()
            subprocess.run([exe, str(iters), str(size)], stdout=subprocess.DEVNULL)
            times.append(time.perf_counter() - t0)
        avg = statistics.mean(times)
        results[lang].append(avg)

# Plot results (skipping not presented)
for lang, times in results.items():
    if not times:
        continue
    plt.plot(sizes, times, marker='o', label=lang)

plt.xlabel('Array Size')
plt.ylabel('Time (s)')
plt.title('Benchmark')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('assets/benchmark_results.png', dpi=300)
print('Saved scaling.png')
