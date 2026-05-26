
# 🔁 LeetCode #217 — Contains Duplicate

> **[Open on LeetCode →](https://leetcode.com/problems/contains-duplicate/)**
> **Difficulty:** Easy | **Topic:** Array, Hash Set, Sorting

---

## 📋 Problem Statement

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array.

Return `false` if every element is **distinct**.

---

## 📌 Examples

```
Input:  [1, 2, 3, 1]   →   true    (1 appears at index 0 and 3)
Input:  [1, 2, 3, 4]   →   false   (all elements are unique)
Input:  [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]   →   true
```

---

## 🗺️ Understanding the Problem First

```mermaid
mindmap
  root((Contains Duplicate))
    Given
      An array of integers
    Return
      true if ANY value appears more than once
      false if ALL values are unique
    Core question
      Have I seen this number before in this list?
    What I need
      A way to remember what I have already seen
      A fast way to check membership
```

---

## 🧭 The Two Phases of Solving

```mermaid
flowchart LR
    A["Phase 1\nUnderstand the Problem\nWhat does duplicate mean?\nWhat edge cases exist?"] --> B["Phase 2\nBuild the Solution\nNaive first\nRemove bottlenecks step by step"]

    style A fill:#dbeafe,stroke:#2563eb,stroke-width:2px
    style B fill:#dcfce7,stroke:#16a34a,stroke-width:2px
```

---

## 🔑 Core Insight Before Any Code

This is a **membership detection** problem. The one question we answer repeatedly is:

```
"Have I seen this number before?"
```

```mermaid
flowchart TD
    A["Read a number from the list"] --> B{"Is it already in my memory?"}
    B -- Yes --> C["🎉 Duplicate! Return True"]
    B -- No  --> D["Add it to memory\nContinue scanning"]
    D --> A
    A --> E["Finished list? Return False"]

    style C fill:#dcfce7,stroke:#16a34a,stroke-width:3px
    style E fill:#fee2e2,stroke:#dc2626
```

---

## 📊 Solution Progression Overview

```mermaid
timeline
    title From First Idea to Optimal Solution

    Solution 1 Brute Force
        : Compare every element with every other
        : O(n²) time, O(1) space
        : Too slow for large arrays

    Solution 2 Sorting
        : Sort so duplicates become neighbors
        : Only compare adjacent elements
        : O(n log n) — better, but still not linear

    Solution 3 Hash Set
        : Track seen values as we scan
        : Check membership instantly
        : O(n) time — optimal
```

---
---

# ✏️ Solution 1 — Brute Force

## Thinking From This Perspective

**My starting thought:** *"I need to know if any two elements are equal. The simplest thing: pick each element, compare it to every element after it. If any two match, return true."*

No data structures needed. Just two loops.

---

## Visual — What Brute Force Does

```mermaid
flowchart LR
    subgraph Array["nums = [1, 2, 3, 1]"]
        N0["1\ni=0"]
        N1["2\nj=1"]
        N2["3\nj=2"]
        N3["1\nj=3"]
    end

    N0 --> N1
    N0 --> N2
    N0 --> N3

    N3 --> Found["nums[0] == nums[3] == 1\nDuplicate found! Return True ✅"]

    subgraph Issue["The problem"]
        P["For arrays with no duplicates,\nevery pair must be checked → O(n²)"]
    end

    style Found fill:#dcfce7,stroke:#16a34a,stroke-width:3px
    style Issue fill:#fee2e2,stroke:#dc2626
```

---

## Complexity

```
Time:  O(n²)  — every element is compared with every element after it
Space: O(1)   — no extra data structures
```

---

## ✅ Full LeetCode Solution — Brute Force

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        n = len(nums)

        for i in range(n):                     # fix one element
            for j in range(i + 1, n):          # compare with every element after it
                if nums[i] == nums[j]:
                    return True                # duplicate found

        return False                           # no duplicates found
```

---

## Why I Move to the Next Solution

```mermaid
flowchart TD
    A["Brute Force is correct ✅"] --> B["But the inner loop repeats work\nFor each element, we scan many others"]
    B --> C["Key observation:\nDuplicates must have the same VALUE\nIf we SORT the array,\nduplicates will be NEXT TO EACH OTHER"]
    C --> D["New idea: sort first\nThen only check adjacent pairs\nNo inner scan needed"]

    style A fill:#dcfce7,stroke:#16a34a
    style B fill:#fee2e2,stroke:#dc2626
    style D fill:#fef3c7,stroke:#d97706,stroke-width:2px
```

---
---

# ✏️ Solution 2 — Sorting

## Thinking From This Perspective

**My new thought:** *"Duplicates are equal values. If equal values are guaranteed to be neighbors after sorting, I only need to check adjacent pairs — no inner loop at all."*

```
Before sort: [3, 1, 4, 1, 5]
After sort:  [1, 1, 3, 4, 5]
                ↑↑
           duplicates are now adjacent
```

---

## Visual — Sorting Brings Duplicates Together

```mermaid
flowchart TD
    A["Original: [3, 1, 4, 1, 5]"] --> B["Sort in place"]
    B --> C["Sorted: [1, 1, 3, 4, 5]"]
    C --> D["Compare adjacent pairs:\nnums[0] vs nums[1] → 1 == 1 ✅"]
    D --> E["Return True"]

    style E fill:#dcfce7,stroke:#16a34a,stroke-width:3px
```

---

## State View of the Algorithm

```mermaid
stateDiagram-v2
    [*] --> SortArray
    SortArray: Sort nums in place

    SortArray --> ScanNeighbors
    ScanNeighbors: Compare nums[i] with nums[i+1]

    ScanNeighbors --> DuplicateFound: nums[i] == nums[i+1]
    ScanNeighbors --> NextPair: nums[i] != nums[i+1]

    NextPair --> ScanNeighbors: i++
    DuplicateFound --> ReturnTrue: return True

    ScanNeighbors --> ReturnFalse: scan complete, no match

    ReturnTrue --> [*]
    ReturnFalse --> [*]
```

---

## Complexity

```
Time:  O(n log n)  — dominated by sorting
Space: O(1)        — sort in place (or O(n) if input must be preserved)
```

---

## ✅ Full LeetCode Solution — Sorting

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        nums.sort()                            # bring equal values next to each other

        for i in range(len(nums) - 1):         # check each adjacent pair
            if nums[i] == nums[i + 1]:
                return True                    # neighbors are equal → duplicate

        return False                           # all neighbors differ → no duplicates
```

---

## Why I Move to the Next Solution

```mermaid
flowchart TD
    A["Sorting works ✅\nO(n log n) is much better than O(n²)"] --> B["But sorting modifies the original array\nThat may not always be acceptable"]
    B --> C["And we still do O(n log n) work\neven though the answer might be on the second element"]
    C --> D["Key insight:\nWe don't need sorted order\nWe just need to remember what we've seen\nand check instantly as we scan"]
    D --> E["New idea: HashSet\nFor each element, ask 'seen before?'\nIf yes → duplicate\nIf no → remember it\nOne pass, O(n)"]

    style A fill:#dcfce7,stroke:#16a34a
    style B fill:#fee2e2,stroke:#dc2626
    style E fill:#fef3c7,stroke:#d97706,stroke-width:2px
```

---
---

# ✏️ Solution 3 — Hash Set (Optimal)

## Thinking From This Perspective

**My final thought:** *"I don't need to sort anything. As I scan left to right, I keep a set of everything I've already seen. For each new number — is it already in the set? If yes: duplicate. If no: add it and continue. One pass. Done."*

---

## Visual — How the Set Grows

```mermaid
sequenceDiagram
    autonumber
    participant A as nums = [1,2,3,1]
    participant L as Loop Logic
    participant S as Set (seen)

    A->>L: Read 1
    L->>S: Is 1 in seen? No
    L->>S: Add 1 → seen = {1}

    A->>L: Read 2
    L->>S: Is 2 in seen? No
    L->>S: Add 2 → seen = {1,2}

    A->>L: Read 3
    L->>S: Is 3 in seen? No
    L->>S: Add 3 → seen = {1,2,3}

    A->>L: Read 1
    L->>S: Is 1 in seen? YES!
    L-->>A: Return True ✅
```

---

## Internal Set Mechanics (Simplified)

```mermaid
flowchart LR
    Num["Incoming: 1"] --> Hash["hash(1) → bucket location"]
    Hash --> Check{"Is that bucket\nalready occupied by 1?"}
    Check -- Yes --> Found["Duplicate → True ✅"]
    Check -- No  --> Store["Store 1 in bucket\nContinue"]

    style Found fill:#dcfce7,stroke:#16a34a,stroke-width:3px
```

A Python `set` resolves membership in **O(1) average time** regardless of how many items are in it.

---

## Complexity

```
Time:  O(n)   — single pass, O(1) set lookup per element
Space: O(n)   — set grows to at most n elements
```

---

## ✅ Full LeetCode Solution — Hash Set

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()                   # our memory of visited values

        for num in nums:
            if num in seen:            # have we seen this before?
                return True
            seen.add(num)              # no → remember it

        return False                   # scanned everything, no duplicate
```

---

## Bonus — Pythonic One-Liner

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))
```

```mermaid
flowchart LR
    A["nums = [1,2,3,1]\nlen = 4"] --> B["set(nums) = {1,2,3}\nlen = 3"]
    B --> C["4 != 3 → True\nA duplicate was removed by the set"]

    style C fill:#dcfce7,stroke:#16a34a,stroke-width:3px
```

---

## Full Comparison

```mermaid
flowchart TB
    subgraph BF["Solution 1: Brute Force"]
        BF1["Nested loop — compare all pairs"]
        BF2["O(n²) time, O(1) space"]
        BF3["❌ Slow for large input"]
    end

    subgraph SO["Solution 2: Sorting"]
        SO1["Sort → check neighbors"]
        SO2["O(n log n) time, O(1) space"]
        SO3["⚠️ Better, but modifies input\nand can't early-exit from sort"]
    end

    subgraph HS["Solution 3: Hash Set"]
        HS1["One pass, track seen values"]
        HS2["O(n) time, O(n) space"]
        HS3["✅ Optimal — this is the answer"]
    end

    BF --> SO --> HS

    style BF3 fill:#fee2e2,stroke:#dc2626
    style SO3 fill:#fef3c7,stroke:#d97706
    style HS3 fill:#dcfce7,stroke:#16a34a,stroke-width:3px
```

---

## 🔁 The Reusable Pattern

```python
# Seen Set Pattern — use whenever the question is "have I seen this before?"
seen = set()
for item in collection:
    if item in seen:
        return True          # revisit / duplicate detected
    seen.add(item)
return False
```

Apply this pattern to: **duplicate detection, cycle detection, visited-state tracking, uniqueness checks.**

---

## ✅ Final Takeaways

```
1. This is a membership detection problem
2. One key question: "Have I seen this before?"
3. A set answers that in O(1)
4. Progression: O(n²) → O(n log n) → O(n)
5. Each step removes one unnecessary scan
```

> 💡 Whenever a problem asks "has this appeared before?" — reach for a set.
