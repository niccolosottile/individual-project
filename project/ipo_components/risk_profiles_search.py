import numpy as np

from project.ipo_components.MVO_optimisation import MVO_optimisation
from project.utils.data_loader import load_and_prepare_returns

def is_valid_portfolio(portfolio):
    # Ensure the portfolio is not a corner solution
    return np.all(portfolio > 0.01) and np.all(portfolio < 0.99)

def find_valid_r_range_at_t(constituents_returns_at_t, r_min=0.01, r_max=20.0, step=0.1):
    valid_r_lower = None
    valid_r_upper = None

    for r in np.arange(r_min, r_max, step):
        optimal_portfolio = np.array(MVO_optimisation(constituents_returns_at_t, r))
        if is_valid_portfolio(optimal_portfolio):
            if valid_r_lower is None:
                valid_r_lower = r
            valid_r_upper = r
        elif valid_r_lower is not None:
            # Break once found the first invalid portfolio after a valid range
            break

    return (valid_r_lower, valid_r_upper)

def find_valid_ranges_over_time(constituents_returns, n_time_steps):
    # Dictionary to hold the range of valid r values for each timestep
    valid_r_ranges = {}

    for t in range(2, n_time_steps):
        # Extract returns at timestep t
        constituents_returns_at_t = constituents_returns.iloc[:t, :]
        valid_r_range_at_t = find_valid_r_range_at_t(constituents_returns_at_t)
        valid_r_ranges[t] = valid_r_range_at_t

        # Optionally print out the valid range for each timestep
        print(f"Timestep {t}: Valid risk profile range: {valid_r_range_at_t}")

    return valid_r_ranges

constituents_returns = load_and_prepare_returns('project/data/ACWI.csv', 'project/data/AGGU.L.csv')
n_time_steps = constituents_returns.shape[0]
valid_r_ranges = find_valid_ranges_over_time(constituents_returns, n_time_steps)

# Optional: to check or process valid ranges further
print(valid_r_ranges)
