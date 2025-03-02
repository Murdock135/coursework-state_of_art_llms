import time
import math
import os
import json
import datetime
from typing import Dict, List, Tuple, Callable, Optional, Any
from collections import defaultdict

from algorithm import (
    orthogonal_equipartition, 
    orthogonal_equipartition_efficient, 
    count_points_in_quadrants, 
    is_equipartition_valid
)
from point_generators import get_generator
from visualization import plot_result, plot_multiple_distributions


def run_experiment(generator_names: List[str], 
                 num_points: int = 200, 
                 num_trials: int = 10, 
                 base_seed: int = 42, 
                 plot_examples: bool = True,
                 verbose: bool = True,
                 plots_dir: str = "plots",
                 results_dir: str = "results",
                 use_efficient: bool = False):
    """
    Run a comprehensive experiment testing the orthogonal equipartition algorithm.
    
    Args:
        generator_names: List of generator names to test
        num_points: Number of points to use
        num_trials: Number of trials for each generator
        base_seed: Base random seed for reproducibility
        plot_examples: Whether to generate plots for examples
        verbose: Whether to print detailed output
        plots_dir: Directory to save plots
        results_dir: Directory to save results
        use_efficient: Whether to use the efficient algorithm implementation
        
    Returns:
        Tuple of (all_results, summary)
    """
    n = num_points
    
    # Select the algorithm to use
    algorithm = orthogonal_equipartition_efficient if use_efficient else orthogonal_equipartition
    algorithm_name = "efficient" if use_efficient else "original"
    
    # Ensure directories exist
    os.makedirs(plots_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # Results tracking
    all_results = []
    
    # Create timestamp for this experiment run
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_id = f"exp_{n}pts_{algorithm_name}_{timestamp}"
    
    if verbose:
        print(f"\nRunning tests with {n} points across {len(generator_names)} distributions")
        print(f"Using algorithm: {algorithm_name}")
        print(f"Experiment ID: {experiment_id}")
        print("=" * 70)
        print(f"{'Distribution':<20} {'Trial':<6} {'Q1':<5} {'Q2':<5} {'Q3':<5} {'Q4':<5} {'Valid':<8} {'Time (s)':<10}")
        print("=" * 70)
    
    # Track points for visualization comparison
    distribution_points = {}
    
    # Run tests for each distribution
    for dist_name in generator_names:
        generator = get_generator(dist_name)
        
        for trial in range(num_trials):
            # Generate points with unique seed for each trial
            seed = base_seed + trial
            points = generator.generate(n, seed=seed)
            
            # Store the first trial's points for visualization
            if trial == 0:
                distribution_points[dist_name] = points
            
            # Measure execution time
            start_time = time.time()
            center, slope = algorithm(points)
            execution_time = time.time() - start_time
            
            # Count points in quadrants
            quadrant_counts = count_points_in_quadrants(points, center, slope)
            
            # Check if equipartition is valid
            is_valid = is_equipartition_valid(quadrant_counts, n)
            
            # Record result
            result = {
                'experiment_id': experiment_id,
                'distribution': dist_name,
                'trial': trial + 1,
                'counts': quadrant_counts,
                'is_valid': is_valid,
                'time': execution_time,
                'center': center,
                'slope': slope,
                'n': n,
                'seed': seed,
                'algorithm': algorithm_name
            }
            all_results.append(result)
            
            if verbose:
                print(f"{dist_name:<20} {trial+1:<6} {quadrant_counts['Q1']:<5} {quadrant_counts['Q2']:<5} "
                      f"{quadrant_counts['Q3']:<5} {quadrant_counts['Q4']:<5} {str(is_valid):<8} {execution_time:.6f}")
            
            # Generate plot for first trial of each distribution
            if plot_examples and trial == 0:
                plot_title = f"{dist_name.capitalize()} Distribution - {n} Points ({algorithm_name})"
                plot_filename = f"{dist_name.lower().replace(' ', '_')}_{n}_{algorithm_name}.png"
                save_path = os.path.join(plots_dir, plot_filename)
                plot_result(points, center, slope, title=plot_title, save_path=save_path, 
                           quadrant_counts=quadrant_counts)
    
    # Plot all distributions for comparison
    if plot_examples:
        comparison_filename = f"all_distributions_{algorithm_name}_{experiment_id}.png"
        comparison_path = os.path.join(plots_dir, comparison_filename)
        plot_multiple_distributions(distribution_points, save_path=comparison_path)
    
    # Calculate summary statistics
    summary = analyze_results(all_results, n, verbose)
    
    # Save the detailed results as JSON
    detailed_results_file = os.path.join(results_dir, f"detailed_results_{algorithm_name}_{experiment_id}.json")
    
    # Convert to JSON-serializable format (tuples to lists)
    json_results = []
    for result in all_results:
        json_result = result.copy()
        json_result['center'] = list(json_result['center'])  # Convert tuple to list
        json_results.append(json_result)
    
    with open(detailed_results_file, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    # Save the summary as JSON
    summary_file = os.path.join(results_dir, f"summary_{algorithm_name}_{experiment_id}.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    if verbose:
        print(f"\nResults saved to:")
        print(f"  - Detailed results: {detailed_results_file}")
        print(f"  - Summary: {summary_file}")
        print(f"  - Plots directory: {plots_dir}")
    
    return all_results, summary, experiment_id


def analyze_results(results, n, verbose=True):
    """
    Analyze experiment results.
    
    Args:
        results: List of experiment results
        n: Number of points
        verbose: Whether to print detailed output
        
    Returns:
        Dictionary with analysis summary
    """
    # Expected counts
    expected_min = math.floor(n / 4)
    expected_max = math.ceil(n / 4)
    
    if verbose:
        print(f"\nExpected counts for valid equipartition: {expected_min} or {expected_max}")
    
    # Group results by distribution
    distributions = set(r['distribution'] for r in results)
    
    # Analyze results by distribution
    if verbose:
        print("\nSummary by Distribution:")
        print("-" * 70)
        print(f"{'Distribution':<20} {'Valid/Total':<12} {'Valid %':<10} {'Avg Q1':<8} {'Avg Q2':<8} {'Avg Q3':<8} {'Avg Q4':<8}")
        print("-" * 70)
    
    summary = {}
    summary['experiment_metadata'] = {
        'n_points': n,
        'expected_min': expected_min,
        'expected_max': expected_max,
        'timestamp': datetime.datetime.now().isoformat(),
    }
    
    for dist_name in distributions:
        dist_results = [r for r in results if r['distribution'] == dist_name]
        valid_count = sum(1 for r in dist_results if r['is_valid'])
        valid_percent = (valid_count / len(dist_results)) * 100
        
        # Calculate average counts
        avg_q1 = sum(r['counts']['Q1'] for r in dist_results) / len(dist_results)
        avg_q2 = sum(r['counts']['Q2'] for r in dist_results) / len(dist_results)
        avg_q3 = sum(r['counts']['Q3'] for r in dist_results) / len(dist_results)
        avg_q4 = sum(r['counts']['Q4'] for r in dist_results) / len(dist_results)
        
        # Calculate standard deviations
        std_q1 = math.sqrt(sum((r['counts']['Q1'] - avg_q1)**2 for r in dist_results) / len(dist_results))
        std_q2 = math.sqrt(sum((r['counts']['Q2'] - avg_q2)**2 for r in dist_results) / len(dist_results))
        std_q3 = math.sqrt(sum((r['counts']['Q3'] - avg_q3)**2 for r in dist_results) / len(dist_results))
        std_q4 = math.sqrt(sum((r['counts']['Q4'] - avg_q4)**2 for r in dist_results) / len(dist_results))
        
        # Calculate average imbalance (max difference from n/4)
        target = n / 4
        avg_imbalance = sum(max(abs(r['counts']['Q1'] - target), 
                                abs(r['counts']['Q2'] - target),
                                abs(r['counts']['Q3'] - target), 
                                abs(r['counts']['Q4'] - target)) 
                             for r in dist_results) / len(dist_results)
        
        if verbose:
            print(f"{dist_name:<20} {valid_count}/{len(dist_results):<12} {valid_percent:>6.1f}% {avg_q1:>8.1f} {avg_q2:>8.1f} {avg_q3:>8.1f} {avg_q4:>8.1f}")
        
        summary[dist_name] = {
            'valid_ratio': f"{valid_count}/{len(dist_results)}",
            'valid_count': valid_count,
            'total_trials': len(dist_results),
            'valid_percent': valid_percent,
            'avg_counts': {
                'Q1': avg_q1,
                'Q2': avg_q2,
                'Q3': avg_q3,
                'Q4': avg_q4
            },
            'std_counts': {
                'Q1': std_q1,
                'Q2': std_q2,
                'Q3': std_q3,
                'Q4': std_q4
            },
            'avg_imbalance': avg_imbalance,
            'performance': {
                'avg_time': sum(r['time'] for r in dist_results) / len(dist_results),
                'min_time': min(r['time'] for r in dist_results),
                'max_time': max(r['time'] for r in dist_results),
                'std_time': math.sqrt(sum((r['time'] - sum(r['time'] for r in dist_results) / len(dist_results))**2 
                                         for r in dist_results) / len(dist_results))
            }
        }
    
    # Calculate overall statistics
    total_valid = sum(1 for r in results if r['is_valid'])
    total_trials = len(results)
    overall_valid_percent = (total_valid / total_trials) * 100
    
    if verbose:
        print(f"\nOverall valid equipartitions: {total_valid}/{total_trials} ({overall_valid_percent:.1f}%)")
    
    # Add overall statistics to summary
    summary['overall'] = {
        'valid_ratio': f"{total_valid}/{total_trials}",
        'valid_count': total_valid,
        'total_trials': total_trials,
        'valid_percent': overall_valid_percent,
        'avg_time': sum(r['time'] for r in results) / len(results),
        'min_time': min(r['time'] for r in results),
        'max_time': max(r['time'] for r in results)
    }
    
    return summary


def compare_algorithms(generator_names: List[str], 
                      num_points_list: List[int] = [100, 200, 500, 1000, 2000], 
                      num_trials: int = 5, 
                      base_seed: int = 42,
                      verbose: bool = True,
                      results_dir: str = "results"):
    """
    Compare the performance of the original and efficient algorithms.
    
    Args:
        generator_names: List of generator names to test
        num_points_list: List of point counts to test
        num_trials: Number of trials for each configuration
        base_seed: Base random seed for reproducibility
        verbose: Whether to print detailed output
        results_dir: Directory to save results
        
    Returns:
        Dictionary with comparison results
    """
    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)
    
    # Create timestamp for this experiment run
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_id = f"comparison_{timestamp}"
    
    # Results tracking
    comparison_results = {
        'comparison_id': comparison_id,
        'timestamp': datetime.datetime.now().isoformat(),
        'num_trials': num_trials,
        'base_seed': base_seed,
        'generators': generator_names,
        'points_counts': num_points_list,
        'results': {}
    }
    
    if verbose:
        print(f"\nComparing algorithms across {len(generator_names)} distributions and {len(num_points_list)} point counts")
        print(f"Running {num_trials} trials for each configuration")
        print("=" * 80)
        print(f"{'Points':<10} {'Distribution':<15} {'Algorithm':<10} {'Avg Time (s)':<15} {'Valid %':<10} {'Speedup':<10}")
        print("=" * 80)
    
    # Run tests for each point count
    for n in num_points_list:
        comparison_results['results'][n] = {}
        
        for dist_name in generator_names:
            generator = get_generator(dist_name)
            comparison_results['results'][n][dist_name] = {'original': {}, 'efficient': {}}
            
            # Create seeds for all trials
            seeds = [base_seed + i for i in range(num_trials)]
            
            # Generate point sets for all trials
            point_sets = [generator.generate(n, seed=seed) for seed in seeds]
            
            # Test original algorithm
            original_times = []
            original_valid_count = 0
            
            for points in point_sets:
                # Measure execution time
                start_time = time.time()
                center, slope = orthogonal_equipartition(points)
                execution_time = time.time() - start_time
                original_times.append(execution_time)
                
                # Check if equipartition is valid
                quadrant_counts = count_points_in_quadrants(points, center, slope)
                is_valid = is_equipartition_valid(quadrant_counts, n)
                if is_valid:
                    original_valid_count += 1
            
            original_avg_time = sum(original_times) / len(original_times)
            original_valid_percent = (original_valid_count / num_trials) * 100
            
            # Test efficient algorithm
            efficient_times = []
            efficient_valid_count = 0
            
            for points in point_sets:
                # Measure execution time
                start_time = time.time()
                center, slope = orthogonal_equipartition_efficient(points)
                execution_time = time.time() - start_time
                efficient_times.append(execution_time)
                
                # Check if equipartition is valid
                quadrant_counts = count_points_in_quadrants(points, center, slope)
                is_valid = is_equipartition_valid(quadrant_counts, n)
                if is_valid:
                    efficient_valid_count += 1
            
            efficient_avg_time = sum(efficient_times) / len(efficient_times)
            efficient_valid_percent = (efficient_valid_count / num_trials) * 100
            
            # Calculate speedup
            speedup = original_avg_time / efficient_avg_time if efficient_avg_time > 0 else float('inf')
            
            # Store results
            comparison_results['results'][n][dist_name]['original'] = {
                'avg_time': original_avg_time,
                'valid_percent': original_valid_percent,
                'times': original_times,
                'valid_count': original_valid_count
            }
            
            comparison_results['results'][n][dist_name]['efficient'] = {
                'avg_time': efficient_avg_time,
                'valid_percent': efficient_valid_percent,
                'times': efficient_times,
                'valid_count': efficient_valid_count,
                'speedup': speedup
            }
            
            if verbose:
                print(f"{n:<10} {dist_name:<15} {'Original':<10} {original_avg_time:<15.6f} {original_valid_percent:<10.1f} {'-':<10}")
                print(f"{'':<10} {'':<15} {'Efficient':<10} {efficient_avg_time:<15.6f} {efficient_valid_percent:<10.1f} {speedup:<10.2f}x")
        
    # Save the comparison results as JSON
    comparison_file = os.path.join(results_dir, f"algorithm_comparison_{comparison_id}.json")
    
    with open(comparison_file, 'w') as f:
        json.dump(comparison_results, f, indent=2)
    
    if verbose:
        print(f"\nComparison results saved to: {comparison_file}")
    
    return comparison_results