"""
Main script for testing the orthogonal equipartition algorithm
with various point distributions.
"""
import argparse
import os

from algorithm import orthogonal_equipartition, count_points_in_quadrants, is_equipartition_valid
from point_generators import get_generator
from visualization import plot_result, plot_multiple_distributions
from experiment import run_experiment


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
    
    return parser.parse_args()


if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Run experiment with the specified parameters
    print(f"\nTesting orthogonal equipartition algorithm with {args.points} points...")
    
    results, summary, experiment_id = run_experiment(
        generator_names=args.distributions,
        num_points=args.points,
        num_trials=args.trials,
        base_seed=args.seed,
        plot_examples=not args.no_plots,
        verbose=not args.quiet,
        plots_dir=args.plots_dir,
        results_dir=args.results_dir
    )
    
    print(f"\nExperiment {experiment_id} completed successfully!")