import numpy as np
from sklearn.datasets import make_blobs, make_circles, make_moons
from typing import List, Tuple, Optional, Union, Dict, Any

class PointGenerator:
    """Base class for point generators that ensure general position."""
    
    @staticmethod
    def ensure_general_position(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Ensure points are in general position (no two points share x or y coordinates).
        
        Args:
            points: List of (x, y) coordinates
            
        Returns:
            Modified points in general position
        """
        # Add small perturbations to ensure general position
        used_x = set()
        used_y = set()
        
        result = []
        for x, y in points:
            # Perturb x if necessary
            while x in used_x:
                x += np.random.uniform(-0.01, 0.01)
            
            # Perturb y if necessary
            while y in used_y:
                y += np.random.uniform(-0.01, 0.01)
            
            used_x.add(x)
            used_y.add(y)
            result.append((float(x), float(y)))
            
        return result
    
    def generate(self, n: int, seed: Optional[int] = None, **kwargs) -> List[Tuple[float, float]]:
        """
        Generate n points in general position.
        
        Args:
            n: Number of points to generate
            seed: Random seed for reproducibility
            **kwargs: Additional parameters specific to each generator
            
        Returns:
            List of (x, y) coordinates
        """
        raise NotImplementedError("Subclasses must implement this method")


class UniformGenerator(PointGenerator):
    """Generate points from a uniform distribution."""
    
    def generate(self, n: int, seed: Optional[int] = None, 
                low: float = 0, high: float = 100) -> List[Tuple[float, float]]:
        """
        Generate n points from a uniform distribution in general position.
        
        Args:
            n: Number of points to generate
            seed: Random seed for reproducibility
            low: Lower bound for coordinates
            high: Upper bound for coordinates
            
        Returns:
            List of (x, y) coordinates
        """
        if seed is not None:
            np.random.seed(seed)
            
        # Generate points from uniform distribution
        points = []
        while len(points) < n:
            batch_size = min(n * 2, n * 10)  # Generate extra points in case of duplicates
            x_coords = np.random.uniform(low, high, batch_size)
            y_coords = np.random.uniform(low, high, batch_size)
            
            for x, y in zip(x_coords, y_coords):
                points.append((float(x), float(y)))
                if len(points) >= n:
                    break
        
        # Ensure general position
        return self.ensure_general_position(points[:n])


class GaussianGenerator(PointGenerator):
    """Generate points from a Gaussian (normal) distribution."""
    
    def generate(self, n: int, seed: Optional[int] = None,
                mean: Tuple[float, float] = (50, 50), 
                std: float = 20) -> List[Tuple[float, float]]:
        """
        Generate n points from a Gaussian distribution in general position.
        
        Args:
            n: Number of points to generate
            seed: Random seed for reproducibility
            mean: Mean (center) of the Gaussian distribution
            std: Standard deviation
            
        Returns:
            List of (x, y) coordinates
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Use scikit-learn's make_blobs with a single cluster
        X, _ = make_blobs(
            n_samples=n * 2,  # Generate extra points in case of duplicates
            n_features=2,
            centers=[mean],
            cluster_std=std,
            random_state=seed
        )
        
        # Convert to list of tuples
        points = [(float(x), float(y)) for x, y in X]
        
        # Ensure general position
        return self.ensure_general_position(points[:n])


class BimodalGenerator(PointGenerator):
    """Generate points from a bimodal distribution (two Gaussian clusters)."""
    
    def generate(self, n: int, seed: Optional[int] = None,
                means: List[Tuple[float, float]] = [(25, 25), (75, 75)],
                std: float = 15) -> List[Tuple[float, float]]:
        """
        Generate n points from a bimodal distribution in general position.
        
        Args:
            n: Number of points to generate
            seed: Random seed for reproducibility
            means: Centers of the Gaussian clusters
            std: Standard deviation for clusters
            
        Returns:
            List of (x, y) coordinates
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Use scikit-learn's make_blobs with multiple clusters
        X, _ = make_blobs(
            n_samples=n * 2,  # Generate extra points in case of duplicates
            n_features=2,
            centers=means,
            cluster_std=std,
            random_state=seed
        )
        
        # Convert to list of tuples
        points = [(float(x), float(y)) for x, y in X]
        
        # Ensure general position
        return self.ensure_general_position(points[:n])


class CircularGenerator(PointGenerator):
    """Generate points in a circular pattern."""
    
    def generate(self, n: int, seed: Optional[int] = None,
                center: Tuple[float, float] = (50, 50),
                radius: float = 40,
                noise: float = 0.1) -> List[Tuple[float, float]]:
        """
        Generate n points in a circular pattern in general position.
        
        Args:
            n: Number of points to generate
            seed: Random seed for reproducibility
            center: Center of the circle
            radius: Radius of the circle
            noise: Amount of noise to add (0 to 1)
            
        Returns:
            List of (x, y) coordinates
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Use scikit-learn's make_circles
        X, _ = make_circles(
            n_samples=n * 2,  # Generate extra points in case of duplicates
            noise=noise,
            random_state=seed
        )
        
        # Scale to the desired radius and translate to center
        X = X * radius + np.array(center)
        
        # Convert to list of tuples
        points = [(float(x), float(y)) for x, y in X]
        
        # Ensure general position
        return self.ensure_general_position(points[:n])


class MoonsGenerator(PointGenerator):
    """Generate points in a two crescent moon shapes."""
    
    def generate(self, n: int, seed: Optional[int] = None,
                center: Tuple[float, float] = (50, 50),
                scale: float = 40,
                noise: float = 0.1) -> List[Tuple[float, float]]:
        """
        Generate n points in a two crescent moon shapes in general position.
        
        Args:
            n: Number of points to generate
            seed: Random seed for reproducibility
            center: Center point to translate to
            scale: Scale factor for the moons
            noise: Amount of noise to add (0 to 1)
            
        Returns:
            List of (x, y) coordinates
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Use scikit-learn's make_moons
        X, _ = make_moons(
            n_samples=n * 2,  # Generate extra points in case of duplicates
            noise=noise,
            random_state=seed
        )
        
        # Scale and translate
        X = X * scale + np.array(center) - np.array([scale/2, scale/2])
        
        # Convert to list of tuples
        points = [(float(x), float(y)) for x, y in X]
        
        # Ensure general position
        return self.ensure_general_position(points[:n])


class GridGenerator(PointGenerator):
    """Generate points in a perturbed grid pattern."""
    
    def generate(self, n: int, seed: Optional[int] = None,
                perturbation: float = 0.2) -> List[Tuple[float, float]]:
        """
        Generate n points in a perturbed grid pattern in general position.
        
        Args:
            n: Number of points to generate
            seed: Random seed for reproducibility
            perturbation: Amount of perturbation (0 to 1)
            
        Returns:
            List of (x, y) coordinates
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Determine grid size
        grid_size = int(np.ceil(np.sqrt(n)))
        
        # Generate grid points with perturbation
        points = []
        for i in range(grid_size):
            for j in range(grid_size):
                # Add small random perturbation to grid positions
                x = i + np.random.uniform(-perturbation, perturbation)
                y = j + np.random.uniform(-perturbation, perturbation)
                points.append((float(x), float(y)))
                
                if len(points) >= n:
                    break
            
            if len(points) >= n:
                break
        
        # Ensure general position
        return self.ensure_general_position(points[:n])


# Factory function to get generator by name
def get_generator(name: str) -> PointGenerator:
    """
    Get a point generator by name.
    
    Args:
        name: Name of the generator
        
    Returns:
        PointGenerator instance
    """
    generators = {
        'uniform': UniformGenerator(),
        'gaussian': GaussianGenerator(),
        'bimodal': BimodalGenerator(),
        'circular': CircularGenerator(),
        'moons': MoonsGenerator(),
        'grid': GridGenerator()
    }
    
    if name.lower() not in generators:
        raise ValueError(f"Unknown generator: {name}. Available generators: {', '.join(generators.keys())}")
    
    return generators[name.lower()]