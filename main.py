import sys

# First Come First Serve (FCFS) algorithm
def fcfs(requests, initial_position):
    total_head_movements = 0
    current_position = initial_position
    for request in requests:
        total_head_movements += abs(request - current_position)
        current_position = request
    return total_head_movements

# SCAN algorithm
def scan(requests, initial_position):
    # Sort requests
    requests.sort()
    # Split requests into left and right of the initial position
    left = [r for r in requests if r <= initial_position]
    right = [r for r in requests if r > initial_position]

    # Move to the innermost cylinder (smallest number) initially
    movements = calculate_head_movements(left[::-1], initial_position)
    if right:
        # Move to the closest request in the opposite direction
        movements += abs(left[0] - right[0])
        # Continue servicing requests in the right direction
        movements += calculate_head_movements(right, right[0])
    return movements

# C-SCAN algorithm
def c_scan(requests, initial_position):
    # Sort requests
    requests.sort()
    # Split requests into left and right of the initial position
    left = [r for r in requests if r <= initial_position]
    right = [r for r in requests if r > initial_position]

    # Move to the innermost cylinder (smallest number) initially
    movements = calculate_head_movements(left[::-1], initial_position)
    if right:
        # Move to the beginning of the opposite direction (0)
        movements += abs(left[0] - 0)
        # Move to the far end
        movements += abs(4999 - 0)
        # Continue servicing requests in the right direction
        movements += calculate_head_movements(right, 4999)
    return movements

# Optimized FCFS algorithm
def optimized_fcfs(requests, initial_position):
    # Determine the order of requests based on the position
    highest_difference = abs(initial_position - max(requests))
    lowest_difference = abs(initial_position - min(requests))
    if lowest_difference < highest_difference:
        requests.sort()
    else:
        requests.sort(reverse=True)

    # Calculate total head movements
    total_head_movements = 0
    current_position = initial_position
    for request in requests:
        total_head_movements += abs(request - current_position)
        current_position = request
    return total_head_movements

# Optimized SCAN algorithm
def optimized_scan(requests, initial_position):
    # Split requests based on the initial position
    lower_half = [r for r in requests if r <= initial_position]
    upper_half = [r for r in requests if r > initial_position]

    total_movements = 0

    # Process lower half with SCAN
    if lower_half:
        lower_half.sort(reverse=True)
        total_movements += calculate_head_movements(lower_half, initial_position)

    # Process upper half with SCAN
    if upper_half:
        upper_half.sort()
        if lower_half:
            total_movements += abs(lower_half[0] - upper_half[0])
            total_movements += calculate_head_movements(upper_half, upper_half[0])
        else:
            total_movements += calculate_head_movements(upper_half, initial_position)

    return total_movements

# Optimized C-SCAN algorithm
def optimized_c_scan(requests, initial_position):
    # Split requests based on the initial position
    left = [r for r in requests if r < initial_position]
    right = [r for r in requests if r >= initial_position]
    movements = 0

    # Service right requests if available
    if right:
        movements += calculate_head_movements(right, initial_position)
        # Jump to the closest request in the opposite direction
        if left:
            optimal_jump = min(left, key=lambda x: abs(4999 - x))
            movements += abs(right[-1] - optimal_jump)
            movements += calculate_head_movements(left, optimal_jump)
    else:
        # Service left requests if no right requests
        optimal_jump = min(left, key=lambda x: abs(4999 - x))
        movements += abs(initial_position - optimal_jump)
        movements += calculate_head_movements(left, optimal_jump)

    return movements

# Read requests from file
def read_requests(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file.readlines()]

# Calculate head movements between requests
def calculate_head_movements(requests, initial_position):
    movements = 0
    current_position = initial_position
    for request in requests:
        movements += abs(request - current_position)
        current_position = request
    return movements

# Main function
if __name__ == "__main__":
    initial_position = int(sys.argv[1])
    filename = sys.argv[2]
  
    requests_fcfs = read_requests(filename)
    requests_scan = requests_fcfs.copy()
    requests_cscan = requests_fcfs.copy()
    
    # Output total head movements for each algorithm
    print("FCFS Total Movements:", fcfs(requests_fcfs, initial_position))
    print("SCAN Total Movements:", scan(requests_scan, initial_position))
    print("C-SCAN Total Movements:", c_scan(requests_cscan, initial_position))

    # Output total head movements for each optimized algorithm
    print("Optimized FCFS Total Movements:", optimized_fcfs(requests_fcfs, initial_position))
    print("Optimized SCAN Total Movements:", optimized_scan(requests_scan, initial_position))
    print("Optimized C-SCAN Total Movements:", optimized_c_scan(requests_cscan, initial_position))
