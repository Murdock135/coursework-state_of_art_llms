# Experiments and Results

## Experimental Setup

The project implements and evaluates the orthogonal equipartition algorithm, which finds two perpendicular lines that divide a set of points in the plane into four quadrants with approximately equal numbers of points. The implementation is based on the Roy and Steiger (2007) paper "Some Combinatorial and Algorithmic Applications of the Borsuk-Ulam Theorem".

The experiments were designed to evaluate:

1. The correctness of the algorithm across different point distributions
2. The performance differences between the original and efficient implementations
3. The impact of point count on algorithm performance and accuracy

### Algorithm Variants

Two implementations of the orthogonal equipartition algorithm were tested:

1. **Original Algorithm**: Uses an angle-based approach that evaluates critical angles to find the optimal line orientation.
2. **Efficient Algorithm**: Uses a more numerically stable slope-based approach with better theoretical performance for larger point sets.

### Point Distributions

Six different point distributions were tested to evaluate algorithm robustness:

1. **Uniform**: Points randomly distributed across a rectangular region (0-100 range)
2. **Gaussian**: Points following a normal distribution centered at (50, 50) with std=20
3. **Bimodal**: Two Gaussian clusters centered at (25, 25) and (75, 75) with std=15
4. **Circular**: Points distributed in a circle centered at (50, 50) with radius=40
5. **Moons**: Two crescent moon shapes, using scikit-learn's `make_moons` generator
6. **Grid**: Points in a perturbed grid pattern with small random perturbations

### Experimental Parameters

The experiments used the following parameters:
- **Number of points**: 200 points for standard experiments, with comparison tests at 100, 200, 500, 1000, and 2000 points
- **Number of trials**: 10 trials for each distribution in standard experiments, 5 trials in comparison experiments
- **Random seed base**: 42, incremented for each trial to ensure reproducibility
- **Metric for equipartition validity**: A partition is considered valid if each quadrant contains exactly n/4 points (or floor(n/4) and ceil(n/4) when n is not divisible by 4)

## Results Analysis

### Algorithm Performance

The algorithm comparison experiments show that the efficient implementation is consistently faster than the original implementation, with an average speedup of approximately 3.5x across all distributions with 200 points:

| Distribution | Original Avg Time (s) | Efficient Avg Time (s) | Speedup |
|--------------|----------------------|------------------------|---------|
| Uniform      | 0.0228               | 0.0066                 | 3.45x   |
| Gaussian     | 0.0236               | 0.0067                 | 3.50x   |
| Bimodal      | 0.0235               | 0.0067                 | 3.50x   |
| Circular     | 0.0240               | 0.0070                 | 3.46x   |
| Moons        | 0.0237               | 0.0066                 | 3.57x   |
| Grid         | 0.0231               | 0.0065                 | 3.58x   |

Both implementations have similar theoretical time complexity, but the efficient implementation reduces the constant factors through a more optimized approach to tracking quadrant changes.

### Equipartition Validity

The experiments show that achieving a perfect equipartition (exactly n/4 points in each quadrant) is challenging. The successful rate varies by distribution:

| Distribution | Valid Rate (Original) | Valid Rate (Efficient) |
|--------------|----------------------|------------------------|
| Uniform      | 20%                  | 10%                    |
| Gaussian     | 0%                   | 30%                    |
| Bimodal      | 0%                   | 0%                     |
| Circular     | 20%                  | 10%                    |
| Moons        | 0%                   | 0%                     |
| Grid         | 0%                   | 10%                    |
| **Overall**  | **6.7%**             | **10%**                |

Interestingly, the efficient algorithm achieved a slightly higher overall valid equipartition rate (10% vs 6.7%), though this may be within the margin of statistical variation given the limited number of trials.

### Distribution Effects

The results show significant differences in the algorithm's performance across distributions:

1. **Gaussian Distribution**: Achieved the highest rate of valid equipartitions (30% with the efficient algorithm), suggesting that symmetric distributions with a clear center point are more amenable to perfect partitioning.

2. **Bimodal and Moons Distributions**: Both algorithms struggled to find valid equipartitions (0% success rate). This indicates that distributions with multiple clusters or complex shapes pose a greater challenge for the orthogonal equipartition problem.

3. **Uniform and Grid Distributions**: Moderate success rates (10-20%) suggest that regular, symmetric distributions are relatively favorable for equipartition.

4. **Average Imbalance**: When perfect equipartition wasn't achieved, the efficient algorithm showed varying degrees of imbalance across distributions:
   - Bimodal: 5.7 points average imbalance (highest)
   - Moons: 3.1 points average imbalance
   - Uniform: 1.5 points average imbalance
   - Circular: 1.3 points average imbalance
   - Gaussian: 1.2 points average imbalance (lowest)
   - Grid: 1.0 points average imbalance (lowest)

### Quadrant Distribution Analysis

Even when perfect equipartition wasn't achieved, the algorithm still produced reasonably balanced quadrants in most cases. For the efficient algorithm with 200 points:

| Distribution | Avg Q1 | Avg Q2 | Avg Q3 | Avg Q4 | Target (n/4) |
|--------------|--------|--------|--------|--------|--------------|
| Uniform      | 49.5   | 49.8   | 50.6   | 50.1   | 50           |
| Gaussian     | 49.1   | 50.7   | 50.1   | 50.1   | 50           |
| Bimodal      | 51.9   | 48.5   | 49.6   | 50.0   | 50           |
| Circular     | 49.8   | 50.2   | 50.3   | 49.7   | 50           |
| Moons        | 51.1   | 49.2   | 48.6   | 51.1   | 50           |
| Grid         | 49.3   | 50.1   | 49.6   | 51.0   | 50           |

The standard deviations show that bimodal and moons distributions had the highest variability in quadrant counts (std ≈ 5 and 2.8 respectively), while the other distributions showed more consistent results across trials (std ≈ 1).