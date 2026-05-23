# LeetCode #217: Contains Duplicate — Strategic Study Guide

> **Problem Link:** [LeetCode #217 — Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

---

## Problem

Given an integer array `nums`, return `true` if any value appears at least twice in the array.

Return `false` if every element is distinct.

---

## Example

```text
Input:
nums = [1, 2, 3, 1]

Output:
true

Explanation:
The value 1 appears more than once.
```

```text
Input:
nums = [1, 2, 3, 4]

Output:
false

Explanation:
Every element is distinct.
```

---

## Rules

- A duplicate exists if any value appears at least twice.
- If all elements are unique, return `false`.
- Return type is Boolean:

```text
true / false
```

---

# Core Insight

This problem is about detecting repeated values.

The direct question is:

```text
Have I seen this number before?
```

If yes, then a duplicate exists.

If no, remember the number and continue scanning.

---

# Problem-Solving Evolution

```mermaid
timeline
    title Evolution of Thinking for Contains Duplicate

    Brute Force
        : Compare every pair
        : Uses no extra memory
        : Too slow for large input

    Sorting
        : Rearrange values
        : Equal values become neighbors
        : Faster, but changes order

    HashSet
        : Remember seen values
        : Check duplicates instantly
        : Best standard solution
```

---

# Strategic Decision Flow

```mermaid
flowchart TD
    A["🧩 Problem<br/>Detect whether any value appears more than once"] --> B["🪓 Baseline<br/>Compare every pair"]

    B --> C{"⚠️ Bottleneck?"}
    C --> D["Repeated scanning<br/>Same values are checked again and again"]

    D --> E{"Can structure help?"}

    E --> F["📚 Sorting<br/>Force equal values to become neighbors"]
    F --> G["Compare adjacent values only"]

    G --> H{"Can we do better than<br/>O(n log n)?"}

    H --> I["🧠 Use memory<br/>Track values already seen"]

    I --> J["📦 HashSet<br/>O(1) average lookup"]

    J --> K["🚀 Optimal Result<br/>Time: O(n)<br/>Space: O(n)"]

    classDef problem fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#0f172a;
    classDef danger fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#0f172a;
    classDef insight fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#0f172a;
    classDef optimize fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#0f172a;
    classDef final fill:#ede9fe,stroke:#7c3aed,stroke-width:3px,color:#0f172a;

    class A,B problem;
    class C,D danger;
    class E,F,G,H insight;
    class I,J optimize;
    class K final;
```

---

# Approach Trade-Off

```mermaid
quadrantChart
    title Contains Duplicate Approach Trade-Off
    x-axis Low Extra Memory --> High Extra Memory
    y-axis Slow Runtime --> Fast Runtime

    quadrant-1 Fast but More Memory
    quadrant-2 Best Practical Zone
    quadrant-3 Worst Zone
    quadrant-4 Low Memory but Slow

    Brute Force: [0.15, 0.20]
    Sorting: [0.40, 0.65]
    HashSet: [0.75, 0.90]
```

---

# High-Level Comparison

| Approach | Core Strategy | Time | Space | Verdict |
|---|---|---:|---:|---|
| Brute Force | Compare all pairs | `O(n²)` | `O(1)` | Simple but slow |
| Sorting | Sort, then compare neighbors | `O(n log n)` | `O(1)` or `O(n)` | Better, but may modify input |
| HashSet | Store seen values and check instantly | `O(n)` | `O(n)` | Best standard solution |

---

# 1. Brute Force Approach

## Idea

Compare every element with every other element after it.

If any two values are equal, return `true`.

This is the simplest possible solution, but it does too much repeated work.

---

## Visual Logic

```mermaid
flowchart LR
    subgraph Array["nums = [1, 2, 3, 1]"]
        A["1<br/>i = 0"]
        B["2<br/>j = 1"]
        C["3<br/>j = 2"]
        D["1<br/>j = 3"]
    end

    A --> B
    A --> C
    A --> D

    D --> E["Duplicate found<br/>nums[0] == nums[3]"]

    F["Problem:<br/>In the worst case,<br/>every pair is checked"]

    E --> F

    classDef normal fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#0f172a;
    classDef duplicate fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#0f172a;
    classDef warning fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#0f172a;

    class A,B,C normal;
    class D,E duplicate;
    class F warning;
```

---

## Algorithm

1. Use an outer loop at index `i`.
2. Use an inner loop at index `j = i + 1`.
3. Compare:

```python
nums[i] == nums[j]
```

4. If equal, return `True`.
5. If no duplicate is found, return `False`.

---

## Code

```python
from typing import List


class Solution:
    def containsDuplicate_brute_force(self, nums: List[int]) -> bool:
        n = len(nums)

        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] == nums[j]:
                    return True

        return False
```

---

## Complexity

```text
Time:  O(n²)
Space: O(1)
```

---

## Weakness

The nested loop creates too many comparisons.

If the array is large and all elements are distinct, the algorithm must check almost every possible pair.

That makes it inefficient for large inputs.

---

# 2. Sorting Approach

## Idea

If duplicate values exist, sorting forces them to stand next to each other.

Example:

```text
Before sorting:
[3, 1, 4, 1, 5]

After sorting:
[1, 1, 3, 4, 5]
```

Now duplicate detection becomes simple:

```text
Check neighboring values.
```

---

## Sorting Transformation

```mermaid
flowchart TD
    A["Original Array<br/>[3, 1, 4, 1, 5]"] --> B["Sort Values"]

    B --> C["Sorted Array<br/>[1, 1, 3, 4, 5]"]

    C --> D{"Any adjacent values equal?"}

    D -->|Yes| E["Duplicate exists"]
    D -->|No| F["All values are distinct"]

    classDef input fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#0f172a;
    classDef process fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#0f172a;
    classDef decision fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#0f172a;
    classDef success fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#0f172a;

    class A input;
    class B,C process;
    class D decision;
    class E,F success;
```

---

## State View

```mermaid
stateDiagram-v2
    [*] --> UnsortedArray
    UnsortedArray --> SortedArray: sort nums
    SortedArray --> CompareNeighbors

    CompareNeighbors --> DuplicateFound: nums[i] == nums[i + 1]
    CompareNeighbors --> KeepScanning: nums[i] != nums[i + 1]

    KeepScanning --> CompareNeighbors
    DuplicateFound --> [*]

    CompareNeighbors --> AllDistinct: scan completes
    AllDistinct --> [*]

    note right of SortedArray
        Sorting groups equal values together.
    end note

    note right of CompareNeighbors
        Only adjacent values need comparison.
    end note
```

---

## Algorithm

1. Sort the array.
2. Loop from index `0` to `n - 2`.
3. Compare each value with its next neighbor:

```python
nums[i] == nums[i + 1]
```

4. If equal, return `True`.
5. If the scan completes, return `False`.

---

## Code

```python
from typing import List


class Solution:
    def containsDuplicate_sorting(self, nums: List[int]) -> bool:
        nums.sort()

        for i in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                return True

        return False
```

---

## Complexity

```text
Time:  O(n log n)
Space: O(1) or O(n), depending on sorting implementation
```

---

## Weakness

Sorting improves runtime compared to brute force, but it has two issues:

1. It may modify the original input order.
2. It is still slower than the HashSet approach.

If we can use extra memory, we can solve the problem in linear time.

---

# 3. HashSet Approach

## Idea

Use a set to remember every value already seen.

For each number, ask:

```text
Have I seen this before?
```

If yes, return `true`.

If no, store it and keep going.

---

## HashSet Memory Model

```mermaid
flowchart TD
    subgraph Current["Current Scan"]
        A["Read num"]
        B["Ask:<br/>Is num in seen?"]
    end

    subgraph Memory["HashSet Memory"]
        C["seen = {previous values}"]
    end

    A --> B
    C --> B

    B -->|Yes| D["Duplicate found<br/>Return true"]
    B -->|No| E["Add num to seen"]
    E --> F["Move to next number"]
    F --> A

    classDef scan fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#0f172a;
    classDef memory fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#0f172a;
    classDef success fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#0f172a;
    classDef loop fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#0f172a;

    class A,B scan;
    class C,E memory;
    class D success;
    class F loop;
```

---

## Walkthrough Example

Given:

```text
nums = [1, 2, 3, 1]
```

```mermaid
sequenceDiagram
    autonumber
    participant Array as nums
    participant Logic as Duplicate Check
    participant Set as HashSet seen

    Array->>Logic: Read 1
    Logic->>Set: Is 1 in seen?
    Set-->>Logic: No
    Logic->>Set: Add 1

    Array->>Logic: Read 2
    Logic->>Set: Is 2 in seen?
    Set-->>Logic: No
    Logic->>Set: Add 2

    Array->>Logic: Read 3
    Logic->>Set: Is 3 in seen?
    Set-->>Logic: No
    Logic->>Set: Add 3

    Array->>Logic: Read 1
    Logic->>Set: Is 1 in seen?
    Set-->>Logic: Yes
    Logic-->>Array: Return true
```

---

## Algorithm

1. Create an empty set:

```python
seen = set()
```

2. Iterate through every number in `nums`.
3. If the number is already in `seen`, return `True`.
4. Otherwise, add the number to `seen`.
5. If the loop finishes, return `False`.

---

## Code

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False
```

---

## Complexity

```text
Time:  O(n)
Space: O(n)
```

---

## Why HashSet Is Optimal

The brute force approach repeatedly searches through the array.

The sorting approach rearranges the array to make duplicates easier to find.

The HashSet approach avoids both problems.

It remembers values as it scans, allowing duplicate checks in average constant time.

```mermaid
flowchart TB
    subgraph Slow["❌ Brute Force"]
        A1["Pick a value"]
        A2["Compare with many others"]
        A3["Repeat repeatedly"]
        A4["O(n²)"]
    end

    subgraph Medium["⚠️ Sorting"]
        B1["Sort array"]
        B2["Compare neighbors"]
        B3["May mutate input"]
        B4["O(n log n)"]
    end

    subgraph Fast["✅ HashSet"]
        C1["Scan once"]
        C2["Check seen set"]
        C3["Return on first repeat"]
        C4["O(n)"]
    end

    A1 --> A2 --> A3 --> A4
    B1 --> B2 --> B3 --> B4
    C1 --> C2 --> C3 --> C4

    A4 -. "Remove nested scans" .-> C2
    B4 -. "Avoid sorting cost" .-> C2

    classDef slow fill:#fee2e2,stroke:#dc2626,stroke-width:3px,color:#0f172a;
    classDef medium fill:#fef3c7,stroke:#d97706,stroke-width:3px,color:#0f172a;
    classDef fast fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#0f172a;

    class A1,A2,A3,A4 slow;
    class B1,B2,B3,B4 medium;
    class C1,C2,C3,C4 fast;
```

---

# Common Mistakes

## 1. Returning `False` Too Early

Incorrect idea:

```python
for num in nums:
    if num not in seen:
        return False
```

This is wrong because one unique value does not prove that the entire array is distinct.

You can only return `False` after scanning all elements.

---

## 2. Sorting When Input Order Matters

The sorting approach can modify the original array:

```python
nums.sort()
```

If the original order must be preserved, use:

```python
sorted_nums = sorted(nums)
```

or prefer the HashSet approach.

---

## 3. Confusing Set With Dictionary

For this problem, we only need to know whether a value exists.

So a set is enough:

```python
seen = set()
```

A dictionary is unnecessary unless we need counts or indices.

---

# Interview Explanation

```text
I would first consider the brute force solution, where every pair is compared.
That takes O(n²) time and O(1) space.

The bottleneck is repeated comparison.

A better option is sorting. After sorting, duplicates become adjacent, so I only need to compare neighbors.
That takes O(n log n) time.

The optimal solution is to use a HashSet.
As I scan the array, I store each value I have already seen.
If I encounter a value that is already in the set, I return true immediately.
If I finish scanning without finding a repeat, I return false.

This gives O(n) time and O(n) space.
```

---

# Final Recommended Solution

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False
```

---

# Pythonic One-Liner

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))
```

## Why It Works

If duplicates exist, converting the list into a set removes repeated values.

So:

```text
len(nums) != len(set(nums))
```

means at least one duplicate was removed.

---

# Final Mental Model

```mermaid
mindmap
  root((Contains Duplicate))
    Goal
      Detect repeated value
      Return boolean
    Brute Force
      Compare all pairs
      No extra memory
      Slow O(n²)
    Sorting
      Group equal values
      Check neighbors
      O(n log n)
    HashSet
      Remember seen values
      Instant lookup
      Optimal O(n)
```

---

# Key Takeaways

- Brute force proves correctness but is too slow.
- Sorting groups duplicates together.
- HashSet avoids both nested loops and sorting.
- The key question is:

```text
Have I seen this value before?
```

- The optimal standard solution uses:

```text
Time:  O(n)
Space: O(n)
```

---

# Pattern Learned

Contains Duplicate teaches the **Seen Set Pattern**.

```python
seen = set()

for item in collection:
    if item in seen:
        return True

    seen.add(item)

return False
```

Use this pattern when a problem asks whether something has appeared before.

Common use cases:

- duplicate detection
- repeated characters
- visited states
- cycle detection
- membership tracking
- uniqueness validation

---

# Final Thought

Contains Duplicate is simple, but it teaches a major algorithmic principle:

```text
If the question is "Have I seen this before?",
use memory to answer instantly.
```
