from typing import List

import pytest
from q_1442_countTripletsThatCanFormTwoArraysOfEqualXor import Solution


@pytest.mark.parametrize("arr, output", [([2, 3, 1, 6, 7], 4), ([1, 1, 1, 1, 1], 10)])
class TestSolution:
    def test_countTriplets(self, arr: List[int], output: int):
        sc = Solution()
        assert (
            sc.countTriplets(
                arr,
            )
            == output
        )
