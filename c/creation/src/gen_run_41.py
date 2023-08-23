import numpy as np
Ninitial=2
for seed in range(num_trials):
    #LR
    args=seed, Ninitial, 0, 1.142, 3.28, 0.715, 2.08, 75, 0.314, 9.3, 0.42, 0.202, 5, 0.1, 1e-05
    print(f"{*args}")
