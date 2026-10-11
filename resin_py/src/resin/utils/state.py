class State:
    def __init__(self):
        self._store = {}

    def __getitem__(self, key: str):
        return self._store[key]

    def __setitem__(self, key: str, value) -> None:
        self._store[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    def clear(self, key: str = None) -> None:
        """Clears all keys in persistent storage, or `key` if provided."""

        if key is not None:
            if key in self._store:
                del self._store[key]

            else:
                raise KeyError("Key not found in state.")

        else:
            self._store.clear()

    def __repr__(self) -> str:
        return repr(self._store)

state = State()
