# Orthogonal Equipartition Algorithm

This project implements and tests algorithms for finding two perpendicular lines that partition a set of 2D points into four equal (or nearly equal) quadrants, based on the approach described in Roy and Steiger's paper "Some Combinatorial and Algorithmic Applications of the Borsuk-Ulam Theorem" (2007).

## Overview

Given a finite set of n points in 2D space, the algorithm finds two perpendicular lines that partition the plane into four quadrants, such that each quadrant contains either ⌊n/4⌋ or ⌈n/4⌉ points.

## Project Structure

- `algorithm.py`: Core equipartition algorithm implementations (original and efficient)
- `point_generators.py`: Point generation utilities using scikit-learn
- `visualization.py`: Plotting and visualization functions
- `experiment.py`: Comprehensive testing framework
- `main.py`: Command-line interface for running experiments
- `plots/`: Directory for generated plots
- `results/`: Directory for experiment results
- `study_guide.md`: Theoretical background and problem description

## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- scikit-learn

## Installation

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install numpy matplotlib scikit-learn
```

## Usage

Run the main script to test the algorithm with various distributions:

```bash
# Run with original algorithm
python3 main.py

# Run with efficient algorithm
python3 main.py --efficient

# Compare both algorithms across different point sizes
python3 main.py --compare
```

### Command-line Arguments

- `--points N`: Number of points to use (default: 200)
- `--trials N`: Number of trials per distribution (default: 10)
- `--seed N`: Base random seed (default: 42)
- `--no-plots`: Skip generating plots
- `--quiet`: Run in quiet mode (minimal output)
- `--plots-dir DIR`: Directory to save plots (default: plots)
- `--results-dir DIR`: Directory to save results (default: results)
- `--distributions DIST [DIST ...]`: Distributions to test (options: uniform, gaussian, bimodal, circular, moons, grid)
- `--efficient`: Use the efficient algorithm implementation
- `--compare`: Run comparison between original and efficient algorithms
- `--point-sizes N [N ...]`: Point sizes to use for comparison (default: 100 200 500 1000 2000)

Example:

```bash
python3 main.py --points 500 --trials 20 --distributions uniform gaussian --efficient
```

## Results

The experiment results are saved in the `results/` directory in JSON format:
- `detailed_results_*.json`: Detailed results for each trial
- `summary_*.json`: Summary statistics for each distribution

Plots are saved in the `plots/` directory:
- Individual distribution plots showing the partitioning
- Comparison plot showing all tested distributions

## Algorithm Implementations

### Original Implementation

The original algorithm works as follows:

1. Find median points to establish initial halving lines
2. Identify critical angles where quadrant counts change
3. Evaluate each angle to find the one that minimizes imbalance
4. Return the concurrency point and slope of the perpendicular lines

The time complexity is O(n log n), where n is the number of points.

### Efficient Implementation

The efficient implementation uses a more optimized approach:

1. Find median points as the concurrency point
2. Transform all points to be relative to the concurrency point
3. Compute all slope events where quadrant counts change
4. Process slope events in sorted order to find optimal orientation
5. Return the concurrency point and optimal slope

This implementation is more numerically stable and has better performance for larger point sets.

## Point Distributions

The following distributions are supported:

- **Uniform**: Points uniformly distributed in a rectangle
- **Gaussian**: Points from a normal distribution
- **Bimodal**: Points from two Gaussian clusters
- **Circular**: Points arranged in a circular pattern
- **Moons**: Points in two interleaved crescent shapes
- **Grid**: Points in a perturbed grid pattern

## Performance Comparison

The efficient algorithm implementation typically achieves:
- Better numerical stability
- Faster execution times, especially for larger point sets
- Similar or slightly better equipartition results

Run the comparison test to see detailed benchmarks:

```bash
python3 main.py --compare
```

## License

This project is available under the MIT License.