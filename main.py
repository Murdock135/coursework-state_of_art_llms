"""
Main script for testing the orthogonal equipartition algorithm
with various point distributions.
"""
import argparse
import os

from algorithm import (
    orthogonal_equipartition, 
    orthogonal_equipartition_efficient, 
    count_points_in_quadrants, 
    is_equipartition_valid
)
from point_generators import get_generator
from visualization import plot_result, plot_multiple_distributions
from experiment import run_experiment, compare_algorithms


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Test orthogonal equipartition algorithm with various point distributions.'
    )
    
    parser.add_argument('--points', type=int, default=200,
                        help='Number of points to use (default: 200)')
    
    parser.add_argument('--trials', type=int, default=10,
                        help='Number of trials for each distribution (default: 10)')
    
    parser.add_argument('--seed', type=int, default=42,
                        help='Base random seed (default: 42)')
    
    parser.add_argument('--no-plots', action='store_true',
                        help='Skip generating plots')
    
    parser.add_argument('--quiet', action='store_true',
                        help='Run in quiet mode (minimal output)')
    
    parser.add_argument('--plots-dir', type=str, default='plots',
                        help='Directory to save plots (default: plots)')
    
    parser.add_argument('--results-dir', type=str, default='results',
                        help='Directory to save results (default: results)')
    
    parser.add_argument('--distributions', type=str, nargs='+',
                        default=['uniform', 'gaussian', 'bimodal', 'circular', 'moons', 'grid'],
                        help='Distributions to test (default: uniform gaussian bimodal circular moons grid)')
    
    parser.add_argument('--efficient', action='store_true',
                        help='Use the efficient algorithm implementation')
    
    parser.add_argument('--compare', action='store_true',
                        help='Run comparison between original and efficient algorithms')
    
    parser.add_argument('--point-sizes', type=int, nargs='+',
                        default=[100, 200, 500, 1000, 2000],
                        help='Point sizes to use for comparison (default: 100 200 500 1000 2000)')
    
    return parser.parse_args()


if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    if args.compare:
        # Run comparison between algorithms
        print(f"\nComparing original and efficient algorithms on {len(args.distributions)} distributions...")
        print(f"Testing with point sizes: {args.point_sizes}")
        
        comparison_results = compare_algorithms(
            generator_names=args.distributions,
            num_points_list=args.point_sizes,
            num_trials=args.trials,
            base_seed=args.seed,
            verbose=not args.quiet,
            results_dir=args.results_dir
        )
        
        print(f"\nAlgorithm comparison completed successfully!")
    else:
        # Run normal experiment with either the original or efficient algorithm
        algorithm_name = "efficient" if args.efficient else "original"
        print(f"\nTesting {algorithm_name} orthogonal equipartition algorithm with {args.points} points...")
        
        results, summary, experiment_id = run_experiment(
            generator_names=args.distributions,
            num_points=args.points,
            num_trials=args.trials,
            base_seed=args.seed,
            plot_examples=not args.no_plots,
            verbose=not args.quiet,
            plots_dir=args.plots_dir,
            results_dir=args.results_dir,
            use_efficient=args.efficient
        )
        
        print(f"\nExperiment {experiment_id} completed successfully!")