from typing import Dict, List


def set_turning_leds(direction: str) -> Dict[int, List[float]]:
    """Return LED colors indicating turning direction.

    Duckiebot has 4 RGB LEDs with indices:
      - 0: front-left
      - 2: front-right
      - 3: back-left
      - 4: back-right
    """
    yellow = [1.0, 1.0, 0.0]
    off = [0.0, 0.0, 0.0]

    state: Dict[int, List[float]] = {
        0: off[:],
        2: off[:],
        3: off[:],
        4: off[:],
    }

    d = (direction or "").strip().lower()
    if d == "left":
        state[0] = yellow[:]
        state[3] = yellow[:]
    elif d == "right":
        state[2] = yellow[:]
        state[4] = yellow[:]
    # Unknown/straight directions: leave all LEDs off.

    return state
