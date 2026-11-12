"""Importable matchup workers for the payoff and cooperation matrices."""

import numpy as np

P2_OUTCOME_MAP = [0, 2, 1, 3]


def game(last_outcome, p1, p2, noise, rng, h2h, return_cooperation=False):
    if last_outcome is None:
        p1_intended, p2_intended = p1[0], p2[0]
    else:
        p1_intended = p1[last_outcome + 1]
        p2_intended = p2[P2_OUTCOME_MAP[last_outcome] + 1]
    if noise == 0:
        p1_move, p2_move = p1_intended, p2_intended
    else:
        p1_move = p1_intended if rng.random() > noise else 1 - p1_intended
        p2_move = p2_intended if rng.random() > noise else 1 - p2_intended
    new_outcome = 2 * p1_move + p2_move
    if return_cooperation:
        return h2h[p1_move, p2_move], new_outcome, int(p1_intended == 0), int(p1_move == 0)
    return h2h[p1_move, p2_move], new_outcome


def play_match(p1, p2, noise, rng, h2h, n_rounds=150, return_cooperation=False):
    last_outcome = None
    total = 0.0
    intended_total = realized_total = 0
    for _ in range(n_rounds):
        payoff, last_outcome, intended, realized = game(
            last_outcome, p1, p2, noise, rng, h2h, return_cooperation=True
        )
        total += payoff
        intended_total += intended
        realized_total += realized
    if return_cooperation:
        return total / n_rounds, intended_total / n_rounds, realized_total / n_rounds
    return total / n_rounds


def calculate_row(task):
    """Compute all three matrix rows for one noise level and row strategy."""
    noise_idx, noise, row_idx, strategies, h2h, seed, n_rounds, replicates = task
    row = []
    for col_idx, opponent in enumerate(strategies):
        # Reproduce the original single RNG stream for each noise level.
        # Every noisy round draws once per player, so each earlier matchup
        # consumes exactly 2 * n_rounds * replicates random values.
        rng = np.random.default_rng(seed + noise_idx)
        if noise != 0:
            earlier_matchups = row_idx * len(strategies) + col_idx
            rng.bit_generator.advance(2 * n_rounds * replicates * earlier_matchups)
        samples = [
            play_match(strategies[row_idx], opponent, noise, rng, h2h,
                       n_rounds=n_rounds, return_cooperation=True)
            for _ in range(1 if noise == 0 else replicates)
        ]
        if noise == 0:
            samples *= replicates  # Preserve the existing mean's rounding.
        row.append(tuple(np.mean(values) for values in zip(*samples)))
    return noise, row_idx, np.asarray(row).T
