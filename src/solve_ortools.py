from dataclasses import dataclass
from typing import List, Optional, Tuple
import time

import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from src.instance import VRPInstance, euclidean_distance_matrix

@dataclass
class VRPSolution:
    routes: List[List[int]]           
    route_loads: List[int]            
    total_distance: int               
    solve_time_sec: float
    objective: Optional[int] = None

def solve_vrp_ortools(
    inst: VRPInstance,
    n_vehicles: int = 5,
    time_limit_sec: int = 5,
    first_solution: str = "PATH_CHEAPEST_ARC",
    local_search: str = "GUIDED_LOCAL_SEARCH",
) -> VRPSolution:
    coords = inst.coords
    demands = inst.demands
    capacity = inst.capacity
    depot = inst.depot
    dist = euclidean_distance_matrix(coords)

    manager = pywrapcp.RoutingIndexManager(len(dist), n_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_cb(from_index: int, to_index: int) -> int:
        a = manager.IndexToNode(from_index)
        b = manager.IndexToNode(to_index)
        return int(dist[a, b])

    transit_idx = routing.RegisterTransitCallback(distance_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

    # Demand/capacity constraint
    def demand_cb(from_index: int) -> int:
        a = manager.IndexToNode(from_index)
        return int(demands[a])

    demand_idx = routing.RegisterUnaryTransitCallback(demand_cb)
    routing.AddDimensionWithVehicleCapacity(
        demand_idx,
        0,                       # slack
        [capacity] * n_vehicles,  # capacities
        True,                    # start cumul at zero
        "Capacity",
    )

    # Search params
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.time_limit.seconds = int(time_limit_sec)

    params.first_solution_strategy = getattr(
        routing_enums_pb2.FirstSolutionStrategy, first_solution
    )
    params.local_search_metaheuristic = getattr(
        routing_enums_pb2.LocalSearchMetaheuristic, local_search
    )

    t0 = time.time()
    assignment = routing.SolveWithParameters(params)
    t1 = time.time()

    if assignment is None:
        return VRPSolution(routes=[], route_loads=[], total_distance=0, solve_time_sec=t1 - t0, objective=None)

    # Extract routes
    routes: List[List[int]] = []
    loads: List[int] = []
    total_dist = 0

    cap_dim = routing.GetDimensionOrDie("Capacity")

    for v in range(n_vehicles):
        index = routing.Start(v)
        route = [manager.IndexToNode(index)]
        route_dist = 0

        while not routing.IsEnd(index):
            prev = index
            index = assignment.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            route_dist += routing.GetArcCostForVehicle(prev, index, v)

        # load: cumul at end (depot end)
        end_index = routing.End(v)
        load = assignment.Value(cap_dim.CumulVar(end_index))
        if len(route) > 2:  # used vehicle (depot->...->depot)
            routes.append(route)
            loads.append(int(load))
            total_dist += int(route_dist)

    obj = assignment.ObjectiveValue()
    return VRPSolution(routes=routes, route_loads=loads, total_distance=total_dist, solve_time_sec=t1 - t0, objective=int(obj))