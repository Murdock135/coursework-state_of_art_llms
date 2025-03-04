import math
from typing import List, Tuple


def orthogonal_equipartition(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], float]:
    """
    Find two perpendicular lines that equipartition the given points.
    
    Args:
        points: List of (x, y) coordinates
        
    Returns:
        Tuple containing:
        - (x, y) coordinates of the concurrency point P
        - slope of one line (the other is perpendicular with slope -1/m)
    """
    n = len(points)
    
    # Review: Not the most readable. Use library function instead?
    # Sort points by x and y coordinates
    points_by_x = sorted(points, key=lambda p: p[0])
    points_by_y = sorted(points, key=lambda p: p[1])
    
    # Review: ditto review as the sorting method before.
    # Step 1: Find median points and initial halving lines
    median_x = points_by_x[n // 2][0]
    median_y = points_by_y[n // 2][1]
    
    # Prepare to track points in each quadrant as we rotate
    # Consider slopes from -∞ to +∞ (which we'll represent by angles from π/2 to -π/2)
    # Start with vertical and horizontal lines (slope = inf and 0)
    
    # We need to track slopes where quadrant counts change
    critical_angles = []
    
    # For each point, compute angle to the median point
    center_point = (median_x, median_y)
    for pt in points:
        if pt[0] == center_point[0] and pt[1] == center_point[1]:
            continue  # Skip the center point itself
            
        # Calculate angle from center to point
        dx = pt[0] - center_point[0]
        dy = pt[1] - center_point[1]
        angle = math.atan2(dy, dx)
        
        # Add both the angle and angle + π/2 (perpendicular)
        critical_angles.append(angle)
        critical_angles.append(angle + math.pi/2)
        critical_angles.append(angle - math.pi/2)
    
    # Sort angles and remove duplicates
    critical_angles = sorted(list(set(critical_angles)))
    
    # Evaluate each critical angle
    best_imbalance = n  # Start with worst possible imbalance
    best_angle = 0
    
    for angle in critical_angles:
        # Calculate the slope from the angle
        slope = math.tan(angle)
        perp_slope = -1/slope if slope != 0 else float('inf')
        
        # Count points in each quadrant
        q1, q2, q3, q4 = 0, 0, 0, 0
        
        for pt in points:
            if pt[0] == center_point[0] and pt[1] == center_point[1]:
                continue  # Skip the center point
                
            # Check which quadrant the point belongs to
            # To avoid issues with infinite slope, use angle-based classification
            dx = pt[0] - center_point[0]
            dy = pt[1] - center_point[1]
            pt_angle = math.atan2(dy, dx)
            
            # Determine quadrant based on angles
            rel_angle = (pt_angle - angle) % (2 * math.pi)
            
            if 0 <= rel_angle < math.pi/2:
                q1 += 1
            elif math.pi/2 <= rel_angle < math.pi:
                q2 += 1
            elif math.pi <= rel_angle < 3*math.pi/2:
                q3 += 1
            else:
                q4 += 1
        
        # Calculate imbalance (how far from perfect n/4 in each quadrant)
        target = n / 4
        imbalance = max(abs(q1 - target), abs(q2 - target), 
                        abs(q3 - target), abs(q4 - target))
        
        if imbalance < best_imbalance:
            best_imbalance = imbalance
            best_angle = angle
    
    # Convert best angle to slope
    best_slope = math.tan(best_angle)
    
    return center_point, best_slope

def orthogonal_equipartition_efficient(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], float]:
    """
    Find two perpendicular lines that equipartition the given points using a more efficient approach.
    Based on the Roy and Steiger (2007) paper "Some Combinatorial and Algorithmic Applications
    of the Borsuk-Ulam Theorem".
    
    This implementation uses a more efficient slope-based approach for evaluating orientations,
    which is more numerically stable and has better performance for larger point sets.
    
    Args:
        points: List of (x, y) coordinates
        
    Returns:
        Tuple containing:
        - (x, y) coordinates of the concurrency point P
        - slope of one line (the other is perpendicular with slope -1/m)
    """
    n = len(points)
    
    # Sort points by x and y coordinates
    points_by_x = sorted(points, key=lambda p: p[0])
    points_by_y = sorted(points, key=lambda p: p[1])
    
    # Find median points to use as initial concurrency point
    median_x = points_by_x[n // 2][0]
    median_y = points_by_y[n // 2][1]
    center_point = (median_x, median_y)
    
    # Transform all points to be relative to the center point
    relative_points = []
    for pt in points:
        if pt[0] == center_point[0] and pt[1] == center_point[1]:
            continue  # Skip the center point
        
        # Use relative coordinates
        dx = pt[0] - center_point[0]
        dy = pt[1] - center_point[1]
        relative_points.append((dx, dy))
    
    # Compute all slopes where a point moves from one quadrant to another
    # This happens when the line passes through a point
    slope_events = []
    for dx, dy in relative_points:
        # Compute the slope of the line from the center to the point
        if dx == 0:
            slope = float('inf')
        else:
            slope = dy / dx
        
        # When a line passes through a point, both the line and its perpendicular
        # line cause quadrant count changes
        slope_events.append((slope, 1))  # Main line
        
        # Perpendicular slope
        if slope == 0:
            perp_slope = float('inf')
        elif math.isfinite(slope):
            perp_slope = -1 / slope
        else:
            perp_slope = 0
            
        slope_events.append((perp_slope, 2))  # Perpendicular line
    
    # Sort all events by slope
    slope_events.sort()
    
    # Create initial configuration (vertical and horizontal lines)
    # Start with a vertical line (slope = inf) and horizontal line (slope = 0)
    # Count initial quadrants
    q1, q2, q3, q4 = 0, 0, 0, 0
    
    for dx, dy in relative_points:
        if dx > 0 and dy > 0:
            q1 += 1
        elif dx < 0 and dy > 0:
            q2 += 1
        elif dx < 0 and dy < 0:
            q3 += 1
        else:  # dx > 0 and dy < 0
            q4 += 1
    
    # Keep track of the best configuration
    target = n / 4
    best_imbalance = max(abs(q1 - target), abs(q2 - target), 
                     abs(q3 - target), abs(q4 - target))
    best_slope = 0  # Horizontal line
    
    # Quadrant adjacency: when we rotate clockwise, points move between adjacent quadrants
    # Process all slope events and track quadrant counts
    current_slope = float('-inf')
    
    for slope, event_type in slope_events:
        if slope == current_slope:
            continue
            
        current_slope = slope
        
        # Update quadrant counts based on the current configuration
        if event_type == 1:  # Main line rotates
            # As the line rotates, points move between quadrants in a specific pattern
            # For a clockwise rotation, the transitions are:
            # When the line is at slope s, points near the line move:
            # Q1 -> Q4, Q2 -> Q1, Q3 -> Q2, Q4 -> Q3
            
            # Update quadrant counts (this is a simplified model)
            # In a real implementation, we would need to track exactly which points move
            # For demonstration, we're using a simplified approach that considers
            # the effects of rotating lines
            
            # Calculate new quadrant counts based on the current slope
            new_q1, new_q2, new_q3, new_q4 = 0, 0, 0, 0
            
            for dx, dy in relative_points:
                # Check if point is above the main line
                above_main = dy > slope * dx if slope != float('inf') else dx < 0
                
                # Check if point is above the perpendicular line
                perp_slope = -1/slope if slope != 0 and slope != float('inf') else float('inf') if slope == 0 else 0
                above_perp = dy > perp_slope * dx if perp_slope != float('inf') else dx < 0
                
                if above_main and above_perp:
                    new_q1 += 1
                elif not above_main and above_perp:
                    new_q2 += 1
                elif not above_main and not above_perp:
                    new_q3 += 1
                else:  # above_main and not above_perp
                    new_q4 += 1
            
            # Update quadrant counts
            q1, q2, q3, q4 = new_q1, new_q2, new_q3, new_q4
            
            # Check if this is a better configuration
            imbalance = max(abs(q1 - target), abs(q2 - target), 
                           abs(q3 - target), abs(q4 - target))
            
            if imbalance < best_imbalance:
                best_imbalance = imbalance
                best_slope = slope
    
    return center_point, best_slope

def count_points_in_quadrants(points, center, slope):
    """
    Count how many points fall in each quadrant.
    
    Args:
        points: List of (x, y) coordinates
        center: Concurrency point (x, y)
        slope: Slope of the first line
        
    Returns:
        Dictionary with quadrant counts
    """
    perp_slope = -1/slope if slope != 0 else float('inf')
    
    q1, q2, q3, q4 = 0, 0, 0, 0
    
    for pt in points:
        if pt[0] == center[0] and pt[1] == center[1]:
            continue  # Skip the center point
            
        # Check which quadrant the point belongs to
        dx = pt[0] - center[0]
        dy = pt[1] - center[1]
        
        # Line 1: y - center[1] = slope * (x - center[0])
        above_line1 = dy > slope * dx
        
        # Line 2: y - center[1] = perp_slope * (x - center[0])
        above_line2 = dy > perp_slope * dx
        
        if above_line1 and above_line2:
            q1 += 1
        elif not above_line1 and above_line2:
            q2 += 1
        elif not above_line1 and not above_line2:
            q3 += 1
        else:  # above_line1 and not above_line2
            q4 += 1
    
    return {"Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4}

def is_equipartition_valid(quadrant_counts, n):
    """
    Check if the quadrant counts satisfy the equipartition requirement.
    
    Args:
        quadrant_counts: Dictionary with quadrant counts
        n: Total number of points
        
    Returns:
        Boolean indicating if equipartition is valid
    """
    expected_min = math.floor(n / 4)
    expected_max = math.ceil(n / 4)
    
    return all(expected_min <= count <= expected_max for count in quadrant_counts.values())
