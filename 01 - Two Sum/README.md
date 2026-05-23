# LeetCode #1: Two Sum — Strategic Study Guide

> **Problem Link:** [LeetCode #1 — Two Sum](https://leetcode.com/problems/two-sum/)

---

## Problem

Given an integer array `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

### Rules

- Each input has exactly one solution.
- You cannot use the same element twice.
- Return the indices, not the values.
- The answer can be returned in any order.

---

## Example

```text
Input:
nums = [2, 7, 11, 15]
target = 9

Output:
[0, 1]

Explanation:
nums[0] + nums[1] = 2 + 7 = 9
```

---

# Core Insight

The problem asks for:

```text
x + y = target
```

Instead of searching for both `x` and `y`, fix one number and calculate the missing number:

```text
complement = target - current_number
```

So the real question becomes:

```text
Have I already seen the complement?
```

---

# Problem-Solving Evolution

```mermaid
timeline
    title Evolution of Thinking for Two Sum

    Brute Force
        : Try every possible pair
        : Easy to understand
        : Too slow for large input

    Two Pointers
        : Sort the numbers
        : Shrink search space
        : Must preserve original indices

    Hash Map
        : Store previously seen values
        : Search by complement
        : One pass optimal solution
```

---

# Strategic Decision Flow

```mermaid
flowchart TD
    A["🧩 Problem<br/>Find two indices whose values sum to target"] --> B["🪓 Baseline<br/>Try every pair"]

    B --> C{"⚠️ Bottleneck?"}
    C --> D["Nested search<br/>Each number scans many others"]

    D --> E["🔁 Reframe<br/>Instead of finding two numbers,<br/>find the missing complement"]

    E --> F{"What data structure gives<br/>fast existence checks?"}

    F --> G["📦 Hash Map<br/>value → index"]

    G --> H["🚀 One-pass scan<br/>Check complement before insert"]

    H --> I["✅ Optimal Result<br/>Time: O(n)<br/>Space: O(n)"]

    classDef problem fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#0f172a;
    classDef danger fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#0f172a;
    classDef insight fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#0f172a;
    classDef optimize fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#0f172a;
    classDef final fill:#ede9fe,stroke:#7c3aed,stroke-width:3px,color:#0f172a;

    class A,B problem;
    class C,D danger;
    class E,F insight;
    class G,H optimize;
    class I final;
```

---

# Approach Comparison

```mermaid
quadrantChart
    title Two Sum Approach Trade-Off
    x-axis Low Space --> High Space
    y-axis Slow Runtime --> Fast Runtime

    quadrant-1 Fast but More Memory
    quadrant-2 Best Balance
    quadrant-3 Worst Zone
    quadrant-4 Memory Efficient but Slow

    Brute Force: [0.15, 0.20]
    Two Pointers: [0.55, 0.60]
    Hash Map: [0.75, 0.90]
```

| Approach | Core Idea | Time | Space | Verdict |
|---|---|---:|---:|---|
| Brute Force | Check every pair | `O(n²)` | `O(1)` | Simple but slow |
| Two Pointers | Sort and shrink search space | `O(n log n)` | `O(n)` | Better, but not ideal |
| Hash Map | Store seen values and lookup complement | `O(n)` | `O(n)` | Best standard solution |

---

# 1. Brute Force Approach

## Idea

Check every possible pair.

This is the most direct solution, but it becomes slow because every number may need to compare with many other numbers.

---

## Visual Logic

```mermaid
flowchart LR
    subgraph Array["nums = [2, 7, 11, 15]"]
        A["2<br/>i = 0"]
        B["7<br/>j = 1"]
        C["11<br/>j = 2"]
        D["15<br/>j = 3"]
    end

    A --> B
    A --> C
    A --> D

    B -. next i .-> C
    B -. next i .-> D

    C -. next i .-> D

    E["Every pair is checked<br/>This creates O(n²) work"]

    D --> E

    classDef base fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#0f172a;
    classDef bad fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#0f172a;

    class A,B,C,D base;
    class E bad;
```

---

## Code

```python
from typing import List


class Solution:
    def twoSum_brute_force(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)

        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]

        return []
```

---

## Complexity

```text
Time:  O(n²)
Space: O(1)
```

## Weakness

The inner loop repeatedly searches for the second number.

That repeated search is the bottleneck.

---

# 2. Two-Pointer Approach

## Idea

If the array is sorted, we can use two pointers:

- `left` points to the smallest value.
- `right` points to the largest value.
- If the sum is too small, move `left`.
- If the sum is too large, move `right`.

But since the problem asks for original indices, we must save indices before sorting.

---

## Pointer Movement

```mermaid
stateDiagram-v2
    [*] --> StoreOriginalIndex
    StoreOriginalIndex --> SortByValue
    SortByValue --> CompareSum

    CompareSum --> Found: sum == target
    CompareSum --> MoveLeft: sum < target
    CompareSum --> MoveRight: sum > target

    MoveLeft --> CompareSum: increase sum
    MoveRight --> CompareSum: decrease sum

    Found --> [*]

    note right of StoreOriginalIndex
        Sorting changes positions,
        so original indices must be saved.
    end note

    note right of CompareSum
        Two pointers make decisions
        based on current sum.
    end note
```

---

## Code

```python
from typing import List


class Solution:
    def twoSum_two_pointer(self, nums: List[int], target: int) -> List[int]:
        indexed_nums = [(num, i) for i, num in enumerate(nums)]
        indexed_nums.sort(key=lambda x: x[0])

        left = 0
        right = len(indexed_nums) - 1

        while left < right:
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]

            if current_sum == target:
                return [indexed_nums[left][1], indexed_nums[right][1]]

            elif current_sum < target:
                left += 1

            else:
                right -= 1

        return []
```

---

## Complexity

```text
Time:  O(n log n)
Space: O(n)
```

## Weakness

Sorting is unnecessary overhead.

Since we already use extra memory to preserve indices, we can use that memory more effectively with a hash map.

---

# 3. Hash Map Approach

## Idea

Use a hash map to remember numbers already seen.

For every number:

```text
complement = target - current_number
```

If the complement is already in the hash map, return the saved index and the current index.

---

## Hash Map Search Strategy

```mermaid
flowchart TD
    subgraph CurrentStep["Current Number"]
        A["num = 7"]
        B["target = 9"]
        C["complement = 9 - 7 = 2"]
    end

    subgraph Memory["Hash Map Memory"]
        D["2 → index 0"]
    end

    C --> E{"Is complement 2<br/>inside hash map?"}
    D --> E

    E -->|Yes| F["Return [0, 1]"]
    E -->|No| G["Store current number<br/>7 → index 1"]

    classDef current fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#0f172a;
    classDef memory fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#0f172a;
    classDef decision fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#0f172a;
    classDef success fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#0f172a;

    class A,B,C current;
    class D memory;
    class E decision;
    class F success;
    class G memory;
```

---

## Code

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num

            if complement in seen:
                return [seen[complement], i]

            seen[num] = i

        return []
```

---

## Complexity

```text
Time:  O(n)
Space: O(n)
```

---

# Hash Map Walkthrough

Given:

```text
nums = [2, 7, 11, 15]
target = 9
```

```mermaid
sequenceDiagram
    autonumber
    participant Array as Array nums
    participant Logic as Complement Logic
    participant Map as Hash Map

    Array->>Logic: Read nums[0] = 2
    Logic->>Logic: complement = 9 - 2 = 7
    Logic->>Map: Does 7 exist?
    Map-->>Logic: No
    Logic->>Map: Store 2 → 0

    Array->>Logic: Read nums[1] = 7
    Logic->>Logic: complement = 9 - 7 = 2
    Logic->>Map: Does 2 exist?
    Map-->>Logic: Yes, index 0
    Logic-->>Array: Return [0, 1]
```

---

# Why Hash Map Wins

```mermaid
flowchart TB
    subgraph Slow["❌ Brute Force"]
        A1["Pick first number"]
        A2["Scan remaining numbers"]
        A3["Repeat again and again"]
        A4["O(n²) time"]
    end

    subgraph Fast["✅ Hash Map"]
        B1["Pick current number"]
        B2["Compute complement"]
        B3["Lookup in hash map"]
        B4["O(n) time"]
    end

    A1 --> A2 --> A3 --> A4
    B1 --> B2 --> B3 --> B4

    A4 -. "Remove repeated search" .-> B3

    classDef slow fill:#fee2e2,stroke:#dc2626,stroke-width:3px,color:#0f172a;
    classDef fast fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#0f172a;

    class A1,A2,A3,A4 slow;
    class B1,B2,B3,B4 fast;
```

---

# Common Mistakes

## 1. Using the Same Element Twice

Always check before inserting:

```python
if complement in seen:
    return [seen[complement], i]

seen[num] = i
```

This prevents using the current element with itself.

---

## 2. Sorting Without Saving Original Indices

If using two pointers, save original indices first:

```python
indexed_nums = [(num, i) for i, num in enumerate(nums)]
```

---

## 3. Forgetting Duplicate Values

Example:

```text
nums = [3, 3]
target = 6
```

Correct output:

```text
[0, 1]
```

The hash map approach handles this because it checks before inserting the current number.

---

# Interview Explanation

```text
I would first solve it with brute force by checking every pair.
That takes O(n²) time.

The bottleneck is repeatedly searching for the second number.

To optimize, I calculate the exact complement needed for each number:
target - current_number.

Then I store previously seen numbers and their indices in a hash map.

If the complement already exists in the hash map, I return the stored index and current index.

This gives O(n) time and O(n) space.
```

---

# Final Recommended Solution

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num

            if complement in seen:
                return [seen[complement], i]

            seen[num] = i

        return []
```

---

# Final Mental Model

```mermaid
mindmap
  root((Two Sum))
    Goal
      Find two indices
      Values sum to target
    Brute Force
      Try every pair
      Simple
      Slow O(n²)
    Two Pointers
      Sort first
      Move inward
      Must preserve indices
    Hash Map
      Compute complement
      Store seen values
      Lookup instantly
      Optimal O(n)
```

---

# Key Takeaways

- Brute force gives the baseline.
- The bottleneck is repeated searching.
- The core formula is:

```text
complement = target - current_number
```

- Hash map changes the problem from repeated search to direct lookup.
- The optimal solution uses:

```text
Time:  O(n)
Space: O(n)
```

---

# Pattern Learned

Two Sum teaches the **Hash Map Lookup Pattern**.

```python
seen = {}

for item in collection:
    needed = compute_needed_value(item)

    if needed in seen:
        return answer

    seen[item] = information
```

Use this pattern when a problem involves:

- complements
- pairs
- duplicates
- frequencies
- previously seen values

---

# Final Thought

Two Sum is not just an easy problem.

It teaches a powerful algorithmic idea:

```text
If searching is expensive, remember what you have already seen.
```
