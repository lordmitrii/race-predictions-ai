import numpy as np


class Tensor:
    def __init__(self, data: list[float] | np.ndarray | float):
        self.data = np.array(data, dtype=np.float64)

    def __repr__(self) -> str:
        return f"Tensor(data={self.data})"