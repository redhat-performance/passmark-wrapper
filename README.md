# PassMark PerformanceTest Benchmark Wrapper

## Description

This wrapper facilitates the automated execution of the PassMark PerformanceTest benchmark for Linux. PassMark PerformanceTest is a standard metric for objectively benchmarking a Linux system using a variety of different speed tests, measuring CPU and memory performance across multiple test categories and comparing the results to others.

The wrapper provides:
- Automated PassMark extraction and execution.
- Support for x86_64 (AMD/Intel) and aarch64 (ARM) architectures.
- Automatic architecture-specific binary selection.
- Result collection, processing, and verification.
- CSV and JSON output formats.
- System configuration metadata capture.
- Integration with test_tools framework.
- Optional Performance Co-Pilot (PCP) integration.

## Command-Line Options

```
PassMark Options:
  --cpu_add <n>: Add n CPUs each iteration until max CPUs reached.
  --powers_2: Starting from 1 CPU, keep doubling the CPUs until max CPUs reached.

General test_tools options:
  --home_parent <value>: Parent home directory. If not set, defaults to current working directory.
  --host_config <value>: Host configuration name, defaults to current hostname.
  --iterations <value>: Number of times to run the test, defaults to 1.
  --run_user: User that is actually running the test on the test system. Defaults to current user.
  --sys_type: Type of system working with (aws, azure, hostname). Defaults to hostname.
  --sysname: Name of the system running, used in determining config files. Defaults to hostname.
  --tuned_setting: Used in naming the results directory. For RHEL, defaults to current active tuned profile.
      For non-RHEL systems, defaults to 'none'.
  --use_pcp: Enable Performance Co-Pilot monitoring during test execution.
  --tools_git <value>: Git repo to retrieve the required tools from.
      Default: https://github.com/redhat-performance/test_tools-wrappers
  --usage: Display this usage message.
```

## What the Script Does

The `passmark_run` script performs the following workflow:

1. **Environment Setup**:
   - Clones the test_tools-wrappers repository if not present (default: ~/test_tools).
   - Sources error codes and general setup utilities.
   - Detects system architecture (x86_64 or aarch64).

2. **Package Installation**:
   - Installs required dependencies via package_tool (bc, numactl, git, zip, unzip, etc.).
   - Dependencies are defined in passmark.json for different OS variants (RHEL, Ubuntu, SLES, Amazon Linux).
   - On Ubuntu, adds the universe repository and creates a libncurses.so.5 compatibility symlink.
   - On SLES, activates the legacy module via SUSEConnect.

3. **Binary Selection**:
   - **x86_64 Systems**: Extracts and uses `pt_linux_x64` binary.
   - **aarch64 Systems**: Extracts and uses `pt_linux_arm64` binary.

4. **Library Setup**:
   - Verifies libncurses.so.5 is available (required by the PassMark binary).
   - Creates a symlink from libncurses.so.6 to libncurses.so.5 if needed.
   - Searches /usr/lib64 and /usr/lib for the library.

5. **Test Execution**:
   - Runs the PassMark binary with `-r 3` flag (3 internal runs per iteration).
   - Executes for specified number of iterations.
   - Captures raw YAML output (results_all.yml) per iteration.
   - Captures raw text output per iteration.

6. **Data Collection**:
   - Captures system configuration via gather_data.
   - Records timestamps for each test run.
   - Optionally records PCP performance data.

7. **Result Processing**:
   - Extracts performance metrics from YAML output files.
   - Computes averages across iterations for each test category.
   - Generates passmark.summary with aggregated results.
   - Generates CSV file with test names and operations per second.
   - Creates JSON output for verification.
   - Filters architecture-specific tests (e.g., CPU_avx skipped on ARM).

8. **Verification**:
   - Validates results against Pydantic schema (results_schema.py).
   - Ensures all required fields are present and valid.
   - Uses csv_to_json and verify_results from test_tools.

9. **Output**:
   - Saves all raw output files, processed CSV/JSON, and system metadata.
   - Optionally saves PCP performance data.
   - Archives results to configured storage location via save_results.

## Dependencies

Location of underlying workload: https://www.passmark.com/products/pt_linux/index.php

**RHEL/Amazon Linux**: bc, numactl, perf, git, zip, unzip

**Ubuntu**: bc, numactl, git, zip, unzip, libncurses5

**SLES**: bc, libnuma1, perf, git, zip, unzip, libncurses5

To run:
```bash
git clone https://github.com/redhat-performance/passmark-wrapper
cd passmark-wrapper/passmark
./passmark_run
```

The script will automatically detect your CPU architecture and select the appropriate binary.

## The PassMark Benchmark

PassMark PerformanceTest for Linux runs a comprehensive suite of CPU and memory tests:

### CPU Tests

| Test | Description |
|------|-------------|
| CPU_INTEGER_MATH | Integer arithmetic operations |
| CPU_FLOATINGPOINT_MATH | Floating-point arithmetic operations |
| CPU_PRIME | Prime number search |
| CPU_SORTING | Data sorting algorithms |
| CPU_ENCRYPTION | Encryption/decryption operations |
| CPU_COMPRESSION | Data compression operations |
| CPU_SINGLETHREAD | Single-threaded performance |
| CPU_PHYSICS | Physics simulation |
| CPU_MATRIX_MULT_SSE | Matrix multiplication using SSE |
| CPU_mm | MMX/SSE multimedia extensions |
| CPU_sse | SSE instructions |
| CPU_fma | Fused multiply-add instructions |
| CPU_avx | AVX instructions (x86_64 only) |
| CPU_avx512 | AVX-512 instructions (x86_64 only) |

### Cryptography Tests

| Test | Description |
|------|-------------|
| m_CPU_enc_SHA | SHA hashing performance |
| m_CPU_enc_AES | AES encryption performance |
| m_CPU_enc_ECDSA | ECDSA signing performance |

### Memory Tests

| Test | Description |
|------|-------------|
| ME_ALLOC_S | Memory allocation (small) |
| ME_READ_S | Memory read (small) |
| ME_READ_L | Memory read (large) |
| ME_WRITE | Memory write |
| ME_LARGE | Large memory operations |
| ME_LATENCY | Memory latency |
| ME_THREADED | Threaded memory operations |

### Summary Scores

| Test | Description |
|------|-------------|
| SUMM_CPU | Overall CPU score |
| SUMM_ME | Overall memory score |

Each test reports an **Operations** metric. Higher values indicate better performance. Results are averaged across iterations.

## Output Files

The results directory contains:

- **results_passmark.csv**: CSV file with test names and performance metrics.
- **results_passmark.json**: JSON conversion of CSV results.
- **passmark.summary**: Aggregated summary of all test results averaged across iterations.
- **passmark_\<iter\>.out**: Raw output from each PassMark iteration.
- **results_all_\<iter\>.yml**: YAML results from PassMark binary for each iteration.
- **test_results_report**: Simple status file (contains "Ran" or "Failed").
- **PCP data** (if --use_pcp option used): Performance Co-Pilot monitoring data in `/tmp/pcp_passmark_<YYYY.MM.DD-HH.MM.SS>/`.

## Examples

### Basic run with defaults
```bash
./passmark_run
```
This runs with:
- Automatic architecture detection and binary selection
- 1 iteration
- 3 internal runs per iteration

### Run multiple iterations
```bash
./passmark_run --iterations 3
```
Runs the benchmark 3 times and averages results across iterations.

### Run with PCP monitoring
```bash
./passmark_run --use_pcp
```
Collects Performance Co-Pilot data during the run.

### Run with custom tools repository
```bash
./passmark_run --tools_git https://github.com/my-org/test_tools-wrappers
```
Uses a custom test_tools-wrappers repository.

### Combination example
```bash
./passmark_run --iterations 5 --use_pcp --sys_type aws
```
Runs 5 iterations with PCP monitoring on an AWS system.

## Return Codes

The script uses standardized error codes from test_tools error_codes:
- **0**: Success.
- **101**: Git clone failure (pulling test_tools-wrappers).
- **E_GENERAL**: General execution errors (ZIP extraction failures, missing libncurses libraries, binary execution failures).
- **E_USAGE**: Invalid usage/arguments.

Exit codes indicate specific failure points for automated testing workflows.

## Notes

### Architecture Support
- **x86_64**: Full support for AMD and Intel CPUs. Runs all test categories including AVX and AVX-512.
- **aarch64**: Full support for ARM CPUs. AVX-related tests are automatically filtered from results.

### libncurses Dependency
- The PassMark binary requires libncurses.so.5, which may not be present on newer distributions.
- The wrapper automatically creates a compatibility symlink from libncurses.so.6 if needed.
- On Ubuntu, the universe repository is enabled to ensure library availability.
- On SLES, the legacy module is activated via SUSEConnect.

### OS-Specific Handling
- **RHEL/Amazon Linux**: Standard package installation via package_tool.
- **Ubuntu**: Adds universe repository, creates libncurses.so.5 symlink at `/usr/lib/x86_64-linux-gnu/`.
- **SLES**: Activates legacy module via `SUSEConnect --product sle-module-legacy/<version>/<arch>`.

### Performance Tips
- Run multiple iterations to verify consistency.
- Ensure system is idle (no other workloads) for best results.
- Consider the active tuned profile on RHEL systems.
- Each iteration runs 3 internal PassMark runs for averaging.

### PCP Integration
- Activated via `--use_pcp` option.
- Captures per-iteration metrics for all CPU, memory, and cryptography tests.
- PCP data is saved alongside results for post-run analysis.
- Uses default PCP configuration from test_tools.

### Troubleshooting
- If the binary fails to run, verify libncurses.so.5 is available.
- If extraction fails, verify the PassMark ZIP file is present in the uploads directory.
- If results are missing, check that results_all.yml was generated by the PassMark binary.
- Use `--use_pcp` to collect detailed performance counters for analysis.
