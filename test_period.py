def nlfsr_period_test(feedback_func, n, max_steps=None, verbose=False):
    if max_steps is None:
        max_steps = (1 << n) + n  # 2^n + n as safe upper bound
    
    # Initialize with non-zero state (all 1s)
    state = [1] * n
    initial_state = tuple(state.copy())
    
    if verbose:
        print(f"Testing NLFSR with n={n}")
        print(f"Initial state: {initial_state}")
    
    visited = {initial_state: 0}
    period = 0
    
    for step in range(1, max_steps + 1):
        # Compute feedback bit
        feedback_bit = feedback_func(*state)
        
        # Shift and update state (right shift)
        new_state = [feedback_bit] + state[:-1]
        state_tuple = tuple(new_state)
        
        # Check for cycle
        if state_tuple in visited:
            period = step - visited[state_tuple]
            is_maximal = (period == (1 << n) - 1)
            
            if verbose:
                print(f"Cycle detected at step {step}")
                print(f"State repeated: {state_tuple}")
                print(f"Period: {period}")
                print(f"Maximal period ({2**n - 1}) achieved: {is_maximal}")
            
            return period, is_maximal
        
        visited[state_tuple] = step
        state = new_state
    
    # No cycle found within max_steps
    if verbose:
        print(f"No cycle detected within {max_steps} steps")
    return 0, False


# Example usage:
if __name__ == "__main__":
    # Test a known non-maximal period NLFSR 5-bits
    def non_maximal_feedback_5bit(x0, x1, x2, x3, x4):
        return x0 ^ x2 ^ x4 ^ (x1 & x2 & x3)
    print("\nTesting 5-bit NLFSR with non-maximal period:")
    period, is_maximal = nlfsr_period_test(non_maximal_feedback_5bit, n=5, verbose=True)