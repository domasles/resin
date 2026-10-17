import resin_hw


class Button:
    """Available button types."""

    W = 1 << 0
    A = 1 << 1
    S = 1 << 2
    D = 1 << 3
    I = 1 << 4
    J = 1 << 5
    K = 1 << 6
    L = 1 << 7


_curr_held = 0
_prev_held = 0
_pressed_mask = 0
_released_mask = 0


def update() -> None:
    """Updates button states."""

    global _curr_held, _prev_held, _pressed_mask, _released_mask

    _prev_held = _curr_held
    _curr_held = resin_hw.get_input()

    _pressed_mask = _curr_held & (~_prev_held)
    _released_mask = (~_curr_held) & _prev_held


def is_held(button: Button) -> bool:
    """Returns True if `button` is currently held down."""
    return bool(_curr_held & button)


def is_pressed(button: Button) -> bool:
    """Returns True if `button` was pressed on this frame."""
    return bool(_pressed_mask & button)


def is_released(button: Button) -> bool:
    """Returns True if `button` was released on this frame."""
    return bool(_released_mask & button)


def get_button_bitmask() -> int:
    """Returns the raw bitmask of currently held buttons."""
    return _curr_held
