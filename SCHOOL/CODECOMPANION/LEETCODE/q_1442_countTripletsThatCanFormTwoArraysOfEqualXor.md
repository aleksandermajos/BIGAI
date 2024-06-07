---
qid: 1442
title: Count Triplets That Can Form Two Arrays of Equal XOR
titleSlug: count-triplets-that-can-form-two-arrays-of-equal-xor
difficulty: Medium
tags: Array, Hash Table, Math, Bit Manipulation, Prefix Sum
---

Given an array of integers `arr`.

We want to select three indices `i`, `j` and `k` where `(0 <= i < j <= k < arr.length)`.

Let's define `a` and `b` as follows:

* `a = arr[i] ^ arr[i + 1] ^ ... ^ arr[j - 1]`
* `b = arr[j] ^ arr[j + 1] ^ ... ^ arr[k]`

Note that **^** denotes the **bitwise-xor** operation.

Return *the number of triplets* (`i`, `j` and `k`) Where `a == b`.



**Example 1:**

```
Input: arr = [2,3,1,6,7]
Output: 4
Explanation: The triplets are (0,1,2), (0,2,2), (2,3,4) and (2,4,4)
```
**Example 2:**

```
Input: arr = [1,1,1,1,1]
Output: 10
```


**Constraints:**

* `1 <= arr.length <= 300`
* `1 <= arr[i] <= 10^{8}`

## Solutions

```python
class Solution:
    def countTriplets(self, arr: List[int]) -> int:
        n = len(arr)
        prefixXOR = [0] * (n + 1)

        # Compute the prefix XOR array
        for i in range(n):
            prefixXOR[i + 1] = prefixXOR[i] ^ arr[i]

        count = 0

        # Iterate over all possible j
        for j in range(1, n):
            for k in range(j, n):
                # If prefixXOR[i] == prefixXOR[k+1], we have a valid triplet (i, j, k)
                if prefixXOR[j] == prefixXOR[k + 1]:
                    count += (k - j)

        return count
```


