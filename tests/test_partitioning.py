from circuit_packing.partitioning import cap_copies_by_zone_count, detect_zones

from .fixtures import sample_coupling_map


def test_detect_zones_returns_non_empty_partition() -> None:
    zones = detect_zones(sample_coupling_map())
    assert zones
    assert all(isinstance(zone, list) for zone in zones)
    assert all(zone for zone in zones)


def test_copy_count_is_capped_by_available_zones() -> None:
    zones = [[0, 1, 2], [3, 4, 5]]
    assert cap_copies_by_zone_count(10, zones) == 2
    assert cap_copies_by_zone_count(1, zones) == 1
