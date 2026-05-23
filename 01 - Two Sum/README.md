# LeetCode #1: Two Sum — Strategic Study Guide

This document serves as a high-level engineering blueprint for the **Two Sum** problem.

Rather than focusing on simple memorization, this guide breaks down the core problem-solving paradigms, logical transitions, and systemic stress-tests that lead from a naive implementation to an optimal production-ready solution.

---

## 🧠 The Core Problem-Solving Paradigm

When faced with any algorithmic problem, your approach must be clinical and structured.

Do **not** start typing code immediately.

Follow this diagnostic flow:

```text
[Identify Bottleneck] ──> [Fix One Variable] ──> [Optimize the Search Space]
        │                                              │
(Nested loops: O(n²))                          (Hash Map: O(1) lookups)
```

---

### Establish the Baseline

Define the easiest, most primitive way to solve the problem: **Brute Force**.

This sets your performance floor.

---

### Locate the Structural Bottleneck

Find the exact operation that is wasting CPU cycles.

In this case, the bottleneck is repeatedly searching the array backward and forward for a matching number.

---

### Isolate and Pivot

Instead of searching for:

```text
two numbers that sum to target
```

or mathematically:

```text
X + Y = Target
```

Freeze one variable:

```text
X
```

Then turn the problem into a direct search for its missing complement:

```text
Complement = Target - X
```

---

### Trade Space for Time

If your runtime is too slow, leverage an auxiliary data structure such as a **Hash Map**.

A hash map allows you to instantly memorize the past and eliminate redundant calculations.

---

# 1. Solution I: The Brute Force Approach

## Naive Baseline

---

## How to Think

> What is the simplest way to solve this if I don't care about memory, performance, or getting rejected in a technical interview?

We can systematically compare every single number with every other number in the array until we find a pair that adds up to the `target`.

---

## Step-by-Step Execution Plan

1. Use an outer loop with index `i` to select the first number:

   ```python
   nums[i]
   ```

2. Use an inner loop with index `j`, starting from:

   ```python
   i + 1
   ```

3. Select the second number:

   ```python
   nums[j]
   ```

4. Check if the sum of both numbers equals the target:

   ```python
   nums[i] + nums[j] == target
   ```

5. If a match is found, immediately return their indices:

   ```python
   [i, j]
   ```

---

## LeetCode Class Implementation

```python
from typing import List


class Solution:
    def twoSum_brute_force(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)

        # Loop through each element as the first partner
        for i in range(n):

            # Scan only the remaining elements
            # to avoid self-pairing and duplicates
            for j in range(i + 1, n):

                if nums[i] + nums[j] == target:
                    return [i, j]

        return []  # Fallback if no solution is found
```

---

## 🔴 The Stress-Test & Weakest Link

### Time Complexity

```text
O(n²)
```

### Space Complexity

```text
O(1)
```

---

## Why It Fails at Scale

This approach is incredibly naive.

If the array scales to:

```text
n = 10^5
```

the nested loops will execute roughly:

```text
5 × 10^9 operations
```

In production, this causes a **Time Limit Exceeded**, also known as **TLE**, and can completely freeze the thread.

The bottleneck is the linear scan of the inner loop to find the complement.

---

# 2. Solution II: The Two-Pointer Approach

## The Sorted Variant

---

## How to Think

> How can I search more efficiently?

If the elements are sorted, I don't need to guess randomly.

I can strategically shrink my search window from both ends based on whether my current sum is too small or too big.

---

## Step-by-Step Execution Plan

1. Because sorting destroys index positions, first map each number to its original index:

   ```python
   [(value, original_index)]
   ```

2. Sort the newly mapped array in ascending order.

3. Place a `left` pointer at the beginning:

   ```python
   left = 0
   ```

4. Place a `right` pointer at the end:

   ```python
   right = n - 1
   ```

5. Calculate the sum of the values at both pointers.

6. If:

   ```python
   current_sum == target
   ```

   return the saved original indices.

7. If:

   ```python
   current_sum < target
   ```

   move the left pointer to the right.

8. If:

   ```python
   current_sum > target
   ```

   move the right pointer to the left.

---

## LeetCode Class Implementation

```python
from typing import List


class Solution:
    def twoSum_two_pointer(self, nums: List[int], target: int) -> List[int]:

        # Pair each number with its original index
        # so we don't lose track after sorting
        indexed_nums = [(num, i) for i, num in enumerate(nums)]

        # Sort by the actual values
        indexed_nums.sort(key=lambda x: x[0])

        left = 0
        right = len(nums) - 1

        while left < right:
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]

            if current_sum == target:
                return [indexed_nums[left][1], indexed_nums[right][1]]

            elif current_sum < target:
                # Sum is too small; move pointer to larger numbers
                left += 1

            else:
                # Sum is too large; move pointer to smaller numbers
                right -= 1

        return []  # Fallback if no solution is found
```

---

## 🔴 The Stress-Test & Weakest Link

### Time Complexity

```text
O(n log n)
```

The sorting step dominates the runtime.

### Space Complexity

```text
O(n)
```

This extra memory is required to store the original indices.

---

## Why It Is Highly Imperfect

While:

```text
O(n log n)
```

is a massive upgrade over:

```text
O(n²)
```

sorting is still unnecessary overhead.

Furthermore, because we must preserve the original indices, we have to use:

```text
O(n)
```

extra memory anyway.

If we are already forced to use `O(n)` space, we should aim for a much faster:

```text
O(n)
```

runtime.

---

# 3. Solution III: The Hash Map Approach

## The Optimal Standard

---

## How to Think

> Instead of sorting or looking forward through nested loops, I will look backward at where I have already been.

As I walk through the array, I calculate the exact complement I need:

```text
Target - Current
```

If I have seen that complement before, I win immediately.

If not, I record my current number and its index in a high-speed lookup table so future elements can find it.

---

## Step-by-Step Execution Plan

1. Initialize an empty dictionary/hash map:

   ```python
   hashmap = {}
   ```

2. Loop through the array once using:

   ```python
   index i
   ```

   and current value:

   ```python
   num
   ```

3. Compute the required partner:

   ```python
   complement = target - num
   ```

4. Check if `complement` is already a key in the hash map.

5. If yes, return:

   ```python
   [hashmap[complement], i]
   ```

6. If no, save the current element in the map:

   ```python
   hashmap[num] = i
   ```

7. Move to the next element.

---

## LeetCode Class Implementation

```python
from typing import List


class Solution:
    def twoSum_hash_map(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}  # Format: {value: original_index}

        for i, num in enumerate(nums):
            complement = target - num

            # Check the lookup table.
            # This takes O(1) average time.
            if complement in hashmap:
                return [hashmap[complement], i]

            # Memorize the current number and index
            # for future lookups.
            hashmap[num] = i

        return []  # Fallback if no solution is found
```

---

## 🟢 Why This Is the Ultimate Approach

### Time Complexity

```text
O(n)
```

We scan the list exactly once.

Hash map lookups and insertions operate in:

```text
O(1)
```

average time.

---

### Space Complexity

```text
O(n)
```

In the absolute worst-case scenario, for example, if the matching pair is at the very end of the array, we store `n - 1` elements in the hash map.

---

## The Strategic Trade-Off

We successfully traded space:

```text
O(n) memory
```

to destroy the time bottleneck.

This reduces runtime from a devastating quadratic curve:

```text
O(n²)
```

to a highly scalable linear line:

```text
O(n)
```

---

# Final Comparison

| Approach | Strategy | Time Complexity | Space Complexity | Notes |
|---|---|---:|---:|---|
| Brute Force | Check every pair | `O(n²)` | `O(1)` | Simple but slow |
| Two Pointer | Sort, then shrink window | `O(n log n)` | `O(n)` | Better, but sorting is unnecessary |
| Hash Map | Store complements and lookup directly | `O(n)` | `O(n)` | Optimal standard |

---

# Final Mental Model

```text
Brute Force:
Ask every possible pair.

Two Pointer:
Sort the world, then search intelligently.

Hash Map:
Remember the past so the future can find it instantly.
```

---


