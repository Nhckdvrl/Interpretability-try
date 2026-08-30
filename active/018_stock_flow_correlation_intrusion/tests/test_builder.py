from stock_flow_intrusion.build_bank import direction, stable_hash


def test_direction_and_stable_hash():
    assert direction(1) == "up" and direction(-1) == "down"
    assert stable_hash("a", 1) == stable_hash("a", 1)
    assert stable_hash("a", 1) != stable_hash("a", 2)
