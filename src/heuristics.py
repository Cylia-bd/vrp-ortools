from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

from src.instance import VRPInstance, euclidean_distance_matrix

@dataclass
class HeuristicSolution:
    routes: List[List[int]]     
    route_loads: List[int]
    total_distance: int

def route_distance(route: List[int], dist: np.ndarray) -> int:
    return int(sum(dist[route[i], route[i+1]] for i in range(len(route)-1)))

def clarke_wright_savings(inst: VRPInstance) -> HeuristicSolution:
    """
    Clarke & Wright Savings (version simple):
    - start: une route par client: 0-i-0
    - merge selon savings s(i,j)=d(0,i)+d(0,j)-d(i,j) si capacité respectée
    """
    n = len(inst.demands)
    depot = inst.depot
    dist = euclidean_distance_matrix(inst.coords)

    routes = {i: [depot, i, depot] for i in range(1, n)}
    loads = {i: int(inst.demands[i]) for i in range(1, n)}
    route_id_of = {i: i for i in range(1, n)}

    savings: List[Tuple[int, int, int]] = []
    for i in range(1, n):
        for j in range(i+1, n):
            s = int(dist[depot, i] + dist[depot, j] - dist[i, j])
            savings.append((s, i, j))
    savings.sort(reverse=True)  

    def is_end_customer(route: List[int], customer: int) -> bool:
        return route[1] == customer or route[-2] == customer

    for s, i, j in savings:
        ri = route_id_of.get(i)
        rj = route_id_of.get(j)
        if ri is None or rj is None or ri == rj:
            continue

        route_i = routes[ri]
        route_j = routes[rj]

        if not is_end_customer(route_i, i) or not is_end_customer(route_j, j):
            continue

        new_load = loads[ri] + loads[rj]
        if new_load > inst.capacity:
            continue

        candidates = []

        def orient(route, end_customer):
            if route[1] == end_customer:
                return list(reversed(route)) 
            return route

        oi = orient(route_i, i)
        oj = route_j
        if oj[1] != j:
            oj = list(reversed(oj))  
        candidates.append(oi[:-1] + oj[1:])

        oj2 = orient(route_j, j)
        candidates.append(oi[:-1] + list(reversed(oj2))[1:])

        oi2 = list(reversed(oi))
        oj3 = oj
        candidates.append(oi2[:-1] + oj3[1:])

        oj4 = list(reversed(oj3))
        candidates.append(oi2[:-1] + oj4[1:])

        best = min(candidates, key=lambda r: route_distance(r, dist))

        routes[ri] = best
        loads[ri] = new_load

        for c in best[1:-1]:
            route_id_of[c] = ri

        del routes[rj]
        del loads[rj]

    final_routes = list(routes.values())
    final_loads = [sum(int(inst.demands[c]) for c in r[1:-1]) for r in final_routes]
    total = sum(route_distance(r, dist) for r in final_routes)
    return HeuristicSolution(routes=final_routes, route_loads=final_loads, total_distance=int(total))

def two_opt(route: List[int], dist: np.ndarray) -> List[int]:
    """
    2-opt sur une route (TSP) en gardant depot au début et à la fin.
    """
    best = route
    best_cost = route_distance(best, dist)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for k in range(i + 1, len(best) - 1):
                new_route = best[:i] + list(reversed(best[i:k+1])) + best[k+1:]
                new_cost = route_distance(new_route, dist)
                if new_cost < best_cost:
                    best, best_cost = new_route, new_cost
                    improved = True
                    break
            if improved:
                break

    return best

def improve_with_2opt(inst: VRPInstance, sol: HeuristicSolution) -> HeuristicSolution:
    dist = euclidean_distance_matrix(inst.coords)
    new_routes = [two_opt(r, dist) for r in sol.routes]
    new_loads = [sum(int(inst.demands[c]) for c in r[1:-1]) for r in new_routes]
    total = sum(route_distance(r, dist) for r in new_routes)
    return HeuristicSolution(routes=new_routes, route_loads=new_loads, total_distance=int(total))