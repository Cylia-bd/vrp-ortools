from dataclasses import dataclass
import numpy as np

@dataclass
class VRPInstance:
    coords: np.ndarray      
    demands: np.ndarray     
    capacity: int
    depot: int = 0

def generate_instance(
    n_customers: int = 30,
    seed: int = 42,
    capacity: int = 30,
    demand_low: int = 1,
    demand_high: int = 10,
    coord_low: float = 0.0,
    coord_high: float = 100.0,
) -> VRPInstance:
    """
    Génère une instance VRP avec 1 dépôt (index 0) + n_customers clients.
    """
    rng = np.random.default_rng(seed)
    n = n_customers + 1  

    coords = rng.uniform(coord_low, coord_high, size=(n, 2))
    demands = np.zeros(n, dtype=int)
    demands[1:] = rng.integers(demand_low, demand_high + 1, size=n_customers)

    return VRPInstance(coords=coords, demands=demands, capacity=capacity, depot=0)

def euclidean_distance_matrix(coords: np.ndarray) -> np.ndarray:
    """
    Matrice des distances euclidiennes (arrondies en int) pour OR-Tools.
    """
    diff = coords[:, None, :] - coords[None, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=2))
    return np.rint(dist).astype(int)