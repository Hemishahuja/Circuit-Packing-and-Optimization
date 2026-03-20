from __future__ import annotations

from collections.abc import Iterable

import networkx as nx
from networkx.algorithms import community


def build_coupling_graph(coupling_map: Iterable[tuple[int, int]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_edges_from(coupling_map)
    return graph


def detect_zones(coupling_map: Iterable[tuple[int, int]]) -> list[list[int]]:
    """Partition coupling graph with greedy modularity communities."""
    graph = build_coupling_graph(coupling_map)
    zones = list(community.greedy_modularity_communities(graph))
    return [sorted(list(zone)) for zone in zones]


def cap_copies_by_zone_count(requested_copies: int, zones: list[list[int]]) -> int:
    if requested_copies < 1:
        raise ValueError("requested_copies must be >= 1.")
    return min(requested_copies, len(zones))
