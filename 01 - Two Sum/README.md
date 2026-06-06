# 🧩 LeetCode #1 — Two Sum

> **[Open on LeetCode →](https://leetcode.com/problems/two-sum/)**
> **Difficulty:** Easy | **Topic:** Array, Hash Map

---

## 📋 Problem Statement

Given an integer array `nums` and an integer `target`, return the **indices** of the two numbers such that they add up to `target`.

**Constraints:**
- Each input has exactly **one** valid answer.
- You **cannot** use the same element twice.
- Return the answer in **any order**.

---

## 📌 Examples

```
Input:  nums = [2, 7, 11, 15],  target = 9
Output: [0, 1]
Reason: nums[0] + nums[1] = 2 + 7 = 9 ✅

Input:  nums = [3, 2, 4],  target = 6
Output: [1, 2]
Reason: nums[1] + nums[2] = 2 + 4 = 6 ✅

Input:  nums = [3, 3],  target = 6
Output: [0, 1]
Reason: nums[0] + nums[1] = 3 + 3 = 6 ✅
```

---

## 🗺️ Understanding the Problem First

Before writing any code, map out what is actually being asked:

```mermaid
mindmap
  root((Two Sum))
    Given
      Array of integers
      A target integer
    Return
      Two index positions
      Not the values themselves
    Constraints
      Exactly one solution exists
      Cannot reuse same element
      Any order is fine
    Core relationship
      nums-i plus nums-j equals target
      Find j where nums-j equals target minus nums-i
```

---

## 🧭 The Two Phases of Solving

```mermaid
flowchart LR
    START(["Two Sum Problem"]) --> U["Understand\nReturn indices, not values\nCannot reuse same element"]
    U --> I["Key Insight\nFor num x, need target - x"]
    I --> B["Baseline\nTry every pair\nO(n2)"]
    B --> M["Improve Search\nSort + two pointers\nO(n log n)"]
    M --> O["Optimal\nHash map seen values\nO(n)"]
    O --> DONE(["Return the two original indices"])
```

We always start in **Phase 1** — reading slowly, restating the problem, identifying what the output looks like. Only then do we enter **Phase 2** — writing code, improving it, and proving why each step up is better.

---

## 🔑 Core Insight Before Any Code

The key formula that unlocks everything:

```
complement = target - current_number
```

Instead of asking *"which two numbers add up to target?"*,
we ask *"given this number, what is the one other number I need?"*

```mermaid
flowchart TD
    A["I am currently at num = 2\ntarget = 9"] --> B["What do I need?\ncomplement = 9 - 2 = 7"]
    B --> C{"Have I seen 7 before?"}
    C -- Yes --> D["Return both indices ✅"]
    C -- No  --> E["Remember that I saw 2\nMove to next number"]

```

---

## 📊 Solution Progression Overview

```mermaid
timeline
    title From First Idea to Optimal Solution

    Solution 1 Brute Force
        : Try every pair of numbers
        : Simple nested loops
        : O(n2)  -  too slow for large input

    Solution 2 Two Pointers
        : Sort the array first
        : Shrink search space with two pointers
        : O(n log n)  -  better but adds complexity

    Solution 3 Hash Map
        : Store seen values in a map
        : Look up complement instantly
        : O(n)  -  optimal standard solution
```

---

---

# ✏️ Solution 1 — Brute Force

## Thinking From This Perspective

**My starting thought:** *"I need two numbers that add up to target. The simplest thing I can do is try every possible pair and check."*

This is the most natural first instinct. Fix one number, loop over every other number after it, check if they sum to target.

---

## Visual — What Brute Force Does

```mermaid
flowchart LR
    subgraph Array["nums = [2, 7, 11, 15], target = 9"]
        N0["2\ni=0"]
        N1["7\nj=1"]
        N2["11\nj=2"]
        N3["15\nj=3"]
    end

    N0 --> N1
    N0 --> N2
    N0 --> N3
    N1 -. next outer i .-> N2
    N1 -. next outer i .-> N3
    N2 -. next outer i .-> N3

    Found["nums[0]+nums[1] = 2+7 = 9 ✅\nReturn [0, 1]"]
    N1 --> Found

```

---

## Complexity

```
Time:  O(n²)  — for every element, we scan all remaining elements
Space: O(1)   — no extra memory used
```

---

## ✅ Full LeetCode Solution — Brute Force

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)

        for i in range(n):                   # fix the first number
            for j in range(i + 1, n):        # try every number after it
                if nums[i] + nums[j] == target:
                    return [i, j]            # found the pair

        return []                            # guaranteed answer exists, but safe fallback
```

---

## Why I Move to the Next Solution

```mermaid
flowchart TD
    A["Brute Force works ✅"] --> B["But for n = 10,000\nthe inner loop runs ~50 million times"]
    B --> C["The bottleneck:\nfor each number, we search ALL remaining numbers"]
    C --> D["Key question:\nDo we need to scan everything?\nOr can we narrow the search space?"]
    D --> E["New idea: sort the array\nUse two pointers to shrink the search range"]

```

---
---

# ✏️ Solution 2 — Two Pointers (Sort First)

## Thinking From This Perspective

**My new thought:** *"If the array were sorted, I could use two pointers — one at the smallest value, one at the largest. If their sum is too small, move left pointer right. If too large, move right pointer left. I never need a full inner scan."*

The catch: sorting changes index positions, so I must save original indices before sorting.

---

## Visual — How Two Pointers Work

```mermaid
stateDiagram-v2
    direction LR
    [*] --> SaveIndices
    SaveIndices: Save original index with each value\n[(2,0),(7,1),(11,2),(15,3)]

    SaveIndices --> SortByValue
    SortByValue: Sort by value (indices travel with values)

    SortByValue --> Compare
    Compare: left=0, right=3\nsum = arr[left] + arr[right]

    Compare --> Found: sum == target
    Compare --> MoveLeft: sum < target → left++
    Compare --> MoveRight: sum > target → right--

    MoveLeft --> Compare
    MoveRight --> Compare
    Found --> [*]
```

---

## Pointer Movement on Example

```mermaid
sequenceDiagram
    autonumber
    participant L as left pointer
    participant R as right pointer
    participant C as Check

    Note over L,R: sorted = [(2,0),(7,1),(11,2),(15,3)]

    L->>C: left=0 → value=2
    R->>C: right=3 → value=15
    C->>C: sum = 2+15 = 17 > 9 → move right left

    L->>C: left=0 → value=2
    R->>C: right=2 → value=11
    C->>C: sum = 2+11 = 13 > 9 → move right left

    L->>C: left=0 → value=2
    R->>C: right=1 → value=7
    C->>C: sum = 2+7 = 9 == 9 ✅

    C-->>C: Return original indices [0, 1]
```

---

## Complexity

```
Time:  O(n log n)  — dominated by the sort step
Space: O(n)        — we store (value, original_index) pairs
```

---

## ✅ Full LeetCode Solution — Two Pointers

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Pair each value with its original index before sorting
        indexed = [(num, i) for i, num in enumerate(nums)]
        indexed.sort(key=lambda x: x[0])        # sort by value

        left = 0
        right = len(indexed) - 1

        while left < right:
            current_sum = indexed[left][0] + indexed[right][0]

            if current_sum == target:
                return [indexed[left][1], indexed[right][1]]   # return original indices

            elif current_sum < target:
                left += 1     # need a bigger sum → move left up

            else:
                right -= 1    # need a smaller sum → move right down

        return []
```

---

## Why I Move to the Next Solution

```mermaid
flowchart TD
    A["Two Pointers works ✅\nO(n log n) is better than O(n2)"] --> B["But we introduced sorting\nwhich is not free"]
    B --> C["And we already use O(n) extra memory\nto preserve original indices"]
    C --> D["Key question:\nWe're using O(n) memory anyway.\nCan we use it more cleverly\nto get O(n) time as well?"]
    D --> E["New idea: use a hash map\nStore seen values → look up complement instantly\nNo sort needed at all"]

```

---
---

# ✏️ Solution 3 — Hash Map (Optimal)

## Thinking From This Perspective

**My final thought:** *"Instead of sorting and then searching, I can scan once. For each number, I compute its complement. If that complement was already seen, I'm done. If not, I remember this number. One pass, O(n)."*

---

## Visual — One-Pass Hash Map

```mermaid
flowchart TD
    subgraph Step1["i=0 → num=2"]
        A1["complement = 9 - 2 = 7"]
        A2{"Is 7 in seen?"}
        A3["No → store seen = {2: 0}"]
    end

    subgraph Step2["i=1 → num=7"]
        B1["complement = 9 - 7 = 2"]
        B2{"Is 2 in seen?"}
        B3["YES! Index 0 is stored"]
        B4["Return [0, 1] ✅"]
    end

    A1 --> A2 --> A3 --> B1 --> B2 --> B3 --> B4

```

---

## Full Walkthrough

```mermaid
sequenceDiagram
    autonumber
    participant A as "nums = [2,7,11,15]"
    participant L as Loop Logic
    participant M as "Hash Map seen={}"

    A->>L: i=0, num=2
    L->>L: complement = 9 - 2 = 7
    L->>M: Is 7 in map? No
    L->>M: Store {2: 0}

    A->>L: i=1, num=7
    L->>L: complement = 9 - 7 = 2
    L->>M: Is 2 in map? YES → index 0
    L-->>A: Return [0, 1] ✅
```

---

## Complexity

```
Time:  O(n)   — single pass through the array
Space: O(n)   — hash map stores at most n entries
```

---

## ✅ Full LeetCode Solution — Hash Map

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}                          # maps: number → its index

        for i, num in enumerate(nums):
            complement = target - num      # what value do I need?

            if complement in seen:         # did I already see it?
                return [seen[complement], i]

            seen[num] = i                  # remember this number for future lookups

        return []
```

---

## Why This Is the Final Answer

```mermaid
quadrantChart
    title Two Sum Approach Trade-Off Map
    x-axis Simpler Implementation --> More Strategic Data Structure
    y-axis Slower Runtime --> Faster Runtime
    quadrant-1 Fast and strategic
    quadrant-2 Fast and simple
    quadrant-3 Slow baseline
    quadrant-4 Strategic but still limited
    Brute Force: [0.15, 0.20]
    Sort + Two Pointers: [0.55, 0.62]
    One-Pass Hash Map: [0.90, 0.95]
```

---

## 🔁 The Reusable Pattern

```python
# Hash Map Lookup Pattern
seen = {}
for i, item in enumerate(collection):
    needed = compute_what_is_needed(item)
    if needed in seen:
        return answer_using(seen[needed], i)
    seen[item] = i
```

Apply this pattern to: **two sum variants, pair detection, complement problems, previously-seen lookups.**

---

## ✅ Final Takeaways

```
1. Core formula:  complement = target - num
2. Hash map answers "Have I seen this?" in O(1)
3. Check BEFORE inserting → prevents reusing same element
4. Progression: O(n²) → O(n log n) → O(n)
5. Each step up removes one source of wasted work
```

> 💡 If a problem needs you to find what is **missing** to complete a pair, compute it directly and look it up.
