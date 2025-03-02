# Orthogonal Equipartition Algorithm

This project implements and tests an algorithm for finding two perpendicular lines that partition a set of 2D points into four equal (or nearly equal) quadrants, as described in the study guide.

## Overview

Given a finite set of n points in 2D space, the algorithm finds two perpendicular lines that partition the plane into four quadrants, such that each quadrant contains either 
n/4 or n/4	 points.

## Project Structure

- `algorithm.py`: Core equipartition algorithm implementation
- `point_generators.py`: Point generation utilities using scikit-learn
- `visualization.py`: Plotting and visualization functions
- `experiment.py`: Comprehensive testing framework
- `main.py`: Command-line interface for running experiments
- `plots/`: Directory for generated plots
- `results/`: Directory for experiment results

## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- scikit-learn

## Usage

Run the main script to test the algorithm with various distributions:

```bash
python main.py
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

Example:

```bash
python main.py --points 200 --trials 20 --distributions uniform gaussian
```

## Results

The experiment results are saved in the `results/` directory in JSON format:
- `detailed_results_*.json`: Detailed results for each trial
- `summary_*.json`: Summary statistics for each distribution

Plots are saved in the `plots/` directory:
- Individual distribution plots showing the partitioning
- Comparison plot showing all tested distributions

## Algorithm Details

The algorithm works as follows:

1. Find median points to establish initial halving lines
2. Identify critical angles where quadrant counts change
3. Evaluate each angle to find the one that minimizes imbalance
4. Return the concurrency point and slope of the perpendicular lines

The time complexity is O(n log n), where n is the number of points.

## Point Distributions

The following distributions are supported:

- **Uniform**: Points uniformly distributed in a rectangle
- **Gaussian**: Points from a normal distribution
- **Bimodal**: Points from two Gaussian clusters
- **Circular**: Points arranged in a circular pattern
- **Moons**: Points in two interleaved crescent shapes
- **Grid**: Points in a perturbed grid pattern

## License

This project is available under the MIT License.