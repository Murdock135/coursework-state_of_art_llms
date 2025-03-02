import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional, Dict, Any


def plot_result(points: List[Tuple[float, float]], 
               center: Tuple[float, float], 
               slope: float, 
               title: str = "Orthogonal Equipartition", 
               save_path: Optional[str] = None,
               quadrant_counts: Optional[Dict[str, int]] = None,
               show_counts: bool = True,
               figsize: Tuple[int, int] = (10, 10)):
    """
    Plot the points and the two perpendicular lines.
    
    Args:
        points: List of (x, y) coordinates
        center: Concurrency point (x, y)
        slope: Slope of the first line
        title: Plot title
        save_path: If provided, save the plot to this path instead of displaying
        quadrant_counts: Dictionary with counts for each quadrant
        show_counts: Whether to show quadrant counts on the plot
        figsize: Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot points
    xs, ys = zip(*points)
    ax.scatter(xs, ys, c='blue', alpha=0.5)
    
    # Plot center point
    ax.scatter(center[0], center[1], c='red', s=100, zorder=5)
    
    # Calculate perpendicular slope
    perp_slope = -1/slope if slope != 0 else float('inf')
    
    # Calculate line limits based on data range
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Add some padding
    padding = 0.1 * max(max_x - min_x, max_y - min_y)
    min_x -= padding
    max_x += padding
    min_y -= padding
    max_y += padding
    
    # Plot first line
    if abs(slope) < 1000:  # Not nearly vertical
        x_vals = np.array([min_x, max_x])
        y_vals = center[1] + slope * (x_vals - center[0])
        ax.plot(x_vals, y_vals, 'r-', label=f'Slope: {slope:.2f}')
    else:  # Nearly vertical
        y_vals = np.array([min_y, max_y])
        ax.axvline(x=center[0], color='r', label='Vertical')
    
    # Plot perpendicular line
    if abs(perp_slope) < 1000:  # Not nearly vertical
        x_vals = np.array([min_x, max_x])
        y_vals = center[1] + perp_slope * (x_vals - center[0])
        ax.plot(x_vals, y_vals, 'g-', label=f'Slope: {perp_slope:.2f}')
    else:  # Nearly vertical
        ax.axvline(x=center[0], color='g', label='Vertical')
    
    # Add quadrant labels with counts if available
    if show_counts and quadrant_counts:
        # Calculate positions for quadrant labels
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2
        
        # Adjust label positions to fit in each quadrant
        q1_pos = (center[0] + 0.3 * (max_x - center[0]), center[1] + 0.3 * (max_y - center[1]))
        q2_pos = (center[0] - 0.3 * (center[0] - min_x), center[1] + 0.3 * (max_y - center[1]))
        q3_pos = (center[0] - 0.3 * (center[0] - min_x), center[1] - 0.3 * (center[1] - min_y))
        q4_pos = (center[0] + 0.3 * (max_x - center[0]), center[1] - 0.3 * (center[1] - min_y))
        
        # Add text for each quadrant count
        ax.text(q1_pos[0], q1_pos[1], f"Q1: {quadrant_counts['Q1']}", 
                fontsize=12, ha='center', va='center', weight='bold', 
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
        ax.text(q2_pos[0], q2_pos[1], f"Q2: {quadrant_counts['Q2']}", 
                fontsize=12, ha='center', va='center', weight='bold',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
        ax.text(q3_pos[0], q3_pos[1], f"Q3: {quadrant_counts['Q3']}", 
                fontsize=12, ha='center', va='center', weight='bold',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
        ax.text(q4_pos[0], q4_pos[1], f"Q4: {quadrant_counts['Q4']}", 
                fontsize=12, ha='center', va='center', weight='bold',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    
    # Equal aspect ratio
    ax.set_aspect('equal')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()
        
        
def plot_multiple_distributions(distributions_points: Dict[str, List[Tuple[float, float]]], 
                              figsize: Tuple[int, int] = (15, 10),
                              save_path: Optional[str] = None):
    """
    Plot multiple point distributions for comparison.
    
    Args:
        distributions_points: Dictionary mapping distribution names to point lists
        figsize: Figure size
        save_path: If provided, save the plot to this path instead of displaying
    """
    n_distributions = len(distributions_points)
    
    # Calculate grid dimensions
    cols = min(3, n_distributions)
    rows = (n_distributions + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if rows == 1 and cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    
    for i, (dist_name, points) in enumerate(distributions_points.items()):
        if i < len(axes):
            ax = axes[i]
            xs, ys = zip(*points)
            ax.scatter(xs, ys, alpha=0.5)
            ax.set_title(f"{dist_name} (n={len(points)})")
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.grid(True)
            ax.set_aspect('equal', adjustable='datalim')
    
    # Hide any unused subplots
    for i in range(n_distributions, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()