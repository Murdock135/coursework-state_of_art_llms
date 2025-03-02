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
    
    # Sort points by x and y coordinates
    points_by_x = sorted(points, key=lambda p: p[0])
    points_by_y = sorted(points, key=lambda p: p[1])
    
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