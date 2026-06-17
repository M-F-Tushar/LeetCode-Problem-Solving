# 🔢 LeetCode #238 — Product of Array Except Self

> **[Open on LeetCode →](https://leetcode.com/problems/product-of-array-except-self/)**
> **Difficulty:** Medium | **Topic:** Array, Prefix Product

---

## 📋 Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the **product of all elements of `nums` except `nums[i]`**.

**You must write an algorithm that runs in O(n) time and without using the division operation.**

**Constraints:**
```
2 <= nums.length <= 10^5
-30 <= nums[i] <= 30
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
```

### Diagram 1 — Problem Statement Mindmap

```mermaid
mindmap
  root((Product of Array Except Self))
    Input
      Integer array nums
      At least two elements
      Values can be negative zero or positive
    Output
      Build a new answer array
      Each answer position excludes its own value
      Return product of all other values
    Hard Rules
      Must run in linear time
      Division is not allowed
      Prefix and suffix products fit safely
    Core Meaning
      Every index asks the same question
      What is on my left
      What is on my right
      Multiply both sides together
    Main Challenge
      Avoid recomputing every product
      Avoid division shortcuts
      Handle zero naturally
```

---

## 📌 Examples

```
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]

Reason:
  answer[0] = 2 × 3 × 4 = 24   (everything except index 0)
  answer[1] = 1 × 3 × 4 = 12   (everything except index 1)
  answer[2] = 1 × 2 × 4 = 8    (everything except index 2)
  answer[3] = 1 × 2 × 3 = 6    (everything except index 3)


Input:  nums = [-1, 1, 0, -3, 3]
Output: [0, 0, 9, 0, 0]

Reason:
  answer[2] = (-1) × 1 × (-3) × 3 = 9   (the zero is excluded here)
  all other positions multiply with the 0 → result is 0
```

### Diagram 2 — Example Interpretation Mindmap

```mermaid
mindmap
  root((Reading The Examples))
    Example One
      Input values one two three four
      Output values twenty four twelve eight six
      Each result skips one position
      No zeros so every product is straightforward
    Index Zero
      Skip value one
      Multiply two three four
      Result is twenty four
    Index One
      Skip value two
      Multiply one three four
      Result is twelve
    Example Two
      Contains a zero
      Most outputs become zero
      Only the zero position can exclude zero
    Key Lesson
      Division is dangerous with zero
      Left and right products avoid special cases
```

---

## 🗺️ Understanding the Problem First

Before touching any code, make sure you understand what the problem is actually asking: each index needs the product of everything around it, without using that index's own value.

---

## 🧭 The Two Phases of Solving

```mermaid
flowchart LR
    START(["Product of Array Except Self"]) --> U["Understand\nFor each i return the product\nof everything except nums at i"]
    U --> B["Brute Force Instinct\nFind total product and divide by current value\nLinear time but invalid idea"]
    B --> F["Why It Fails\nZero in the array breaks division\nZero divided by zero is undefined"]
    F --> I["Core Insight\nFor each index answer equals LEFT product times RIGHT product\nNo division needed"]
    I --> O["Efficient Solution\nPre-compute left and right arrays\nMultiply them together\nLinear time and linear space"]
    O --> DONE(["Return result"])
```

### Diagram 3 — Constraint Breakdown Mindmap

```mermaid
mindmap
  root((Constraint Breakdown))
    Linear Time Required
      One pass is good
      Two passes are good
      Three passes are still linear
      Nested recomputation is not allowed
    Division Forbidden
      Total product shortcut is banned
      Zero makes division unsafe
      Need direct construction instead
    Prefix Products Fit
      Running products are safe
      No overflow concern for prefix and suffix
      Focus on algorithm design
    Array Length
      At least two elements
      Every index has an outside product
      Empty side product should be one
    Efficient Target
      Scan from left
      Scan from right
      Combine both sides
```

---

## 🔑 Core Insight Before Any Code

For any index `i`, the answer is simply:

```
answer[i] = (product of everything to the LEFT of i)
          × (product of everything to the RIGHT of i)
```

For example, with `nums = [5, 2, 3, 1, 4]`, to find the answer for index 2 (value `3`):

```
Left of index 2  → 5 × 2 = 10
Right of index 2 → 1 × 4 = 4

answer[2] = 10 × 4 = 40  ✅
```

This means if you pre-compute a `left` array and a `right` array in two passes, you can build the final answer in a third pass — entirely without division.

### Diagram 4 — Core Insight Mindmap

```mermaid
mindmap
  root((Left Right Insight))
    One Index View
      Current value must be excluded
      Everything before it belongs to left side
      Everything after it belongs to right side
    Left Product
      Product of values before current index
      Starts as one at the first index
      Built by scanning left to right
    Right Product
      Product of values after current index
      Starts as one at the last index
      Built by scanning right to left
    Final Answer
      Multiply left product and right product
      Current value never participates
      No division required
    Why This Works With Zero
      Zero is included only when it is outside the current index
      Zero is excluded when current index holds zero
      Multiplication handles both cases naturally
```

---

## 📊 Solution Progression Overview

```mermaid
timeline
    title From First Idea to Optimal Solution

    Solution 1 Brute Force Division
        : Compute total product of all elements
        : For each index divide total by nums[i]
        : O of n time, clean and intuitive
        : FAILS when array contains zero
        : Problem explicitly bans division

    Solution 2 Left and Right Arrays
        : left[i] = product of all elements to the LEFT of i
        : right[i] = product of all elements to the RIGHT of i
        : answer[i] = left[i] x right[i]
        : O of n time, O of n space  -  correct and constraint-safe
```

### Diagram 5 — Solution Progression Mindmap

```mermaid
mindmap
  root((Thinking Path))
    First Instinct
      Compute total product
      Divide by current value
      Looks clean at first
      Violates no division rule
    Breaking Point
      Zero breaks the shortcut
      Zero divided by zero is undefined
      Special cases make the approach messy
    Better Question
      Can we build the answer directly
      What values are before current index
      What values are after current index
    Prefix Suffix Shift
      Left scan stores products before each index
      Right scan stores products after each index
      Final pass multiplies both sides
    Efficient Result
      Linear total work
      No division
      Zero handled naturally
      Same pattern as previous prefix style problems
```

---
---

# ✏️ Solution 1 — Brute Force (Division Approach)

## The Problem-Solver's Thinking

**My starting thought:** *"The most natural thing — if the product of the entire array is 24, and I want the product of everything except `nums[i]`, I can just divide: `24 / nums[i]`. One pass to get the total product. One pass to divide it out. Simple."*

```
nums = [1, 2, 3, 4]
Total product = 1 × 2 × 3 × 4 = 24

answer[0] = 24 / 1 = 24
answer[1] = 24 / 2 = 12
answer[2] = 24 / 3 = 8
answer[3] = 24 / 4 = 6  ✅
```

This is clean, O(n), and intuitive. Most people think of this first.

---

## Visual — What Brute Force Does

```mermaid
flowchart TD
    A["nums = [1, 2, 3, 4]"] --> B["Pass 1: Compute total product\n1 x 2 x 3 x 4 = 24"]
    B --> C["Pass 2: For each index\nanswer[i] = 24 divided by nums[i]"]
    C --> D["answer = [24, 12, 8, 6] ✅"]

    E["nums = [-1, 1, 0, -3, 3]"] --> F["Pass 1: Compute total product\n(-1) x 1 x 0 x (-3) x 3 = 0"]
    F --> G["Pass 2: For each index\nanswer[i] = 0 divided by nums[i]"]
    G --> H["answer[2] = 0 divided by 0\n⚠️ UNDEFINED  -  CRASH ❌"]
```

---

## Why This Approach Breaks

```mermaid
flowchart TD
    A["Total product when zero exists = 0"] --> B["Every division becomes 0 divided by nums[i]"]
    B --> C{"Which index holds the zero?"}
    C --> D["answer[i] = 0 divided by 0\nThis is mathematically undefined\nCrashes your program"]
    C --> E["answer[j] = 0 divided by nums[j]\nHere you get 0  -  but for the wrong reason\nYour logic is relying on invalid math"]
    D --> F["Even with if-else patches, the division approach\nis fundamentally broken for zero inputs\nThe problem explicitly bans it for this reason"]
```

You can add special `if` conditions to handle the zero case, but at that point you are fighting the problem rather than solving it. The constraint *"no division"* exists precisely because this approach fails. The interview is testing whether you can find the clean path.

---

## Complexity

```
Time:  O(n)  — two passes through the array
Space: O(1)  — only a variable for total product

Verdict: REJECTED — banned by problem constraints, and fails on zero inputs
```

---

## ✅ Brute Force Code (for understanding — do not submit)

```python
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        total_product = 1
        for num in nums:
            total_product *= num            # compute total product

        result = []
        for num in nums:
            result.append(total_product // num)   # divide out each element

        return result
        # ⚠️ This FAILS when nums contains 0 (0 ÷ 0 is undefined)
        # ⚠️ Also uses division, which the problem forbids
```

---

## The Question to Ask Yourself

> *"Why did division feel natural? Because for index `i`, I wanted the product of everything except `nums[i]`. Division was just a shortcut. But what if I could compute that directly — the product of everything to the LEFT separately, and the product of everything to the RIGHT separately, and then multiply them? No division ever needed."*

That question is the entire key to the efficient solution.

---
---

# ✏️ Solution 2 — Left and Right Prefix Products (Efficient)

## The Problem-Solver's Thinking

**New thought:** *"For each index `i`, the answer I need is: (product of all elements before `i`) × (product of all elements after `i`). These two parts — left product and right product — can each be computed in one pass. Then I combine them. No division, no zero issues, O(n) total."*

The trick is understanding what the "left" and "right" arrays actually store:

```
left[i]  = product of all elements STRICTLY to the LEFT of index i
right[i] = product of all elements STRICTLY to the RIGHT of index i

For the leftmost element,  left[0]        = 1  (nothing to its left)
For the rightmost element, right[n-1]     = 1  (nothing to its right)
```

---

## Visual — Building left[] and right[] for [5, 2, 3, 1, 4]

```mermaid
flowchart TD
    A["nums = [5, 2, 3, 1, 4]"]

    A --> L["LEFT array  -  scan LEFT TO RIGHT\nEach position stores the running product\nof everything before it"]
    L --> LV["left  = [ 1, 5, 10, 30, 30 ]\n         idx: 0  1   2   3   4\n\nleft[0] = 1       (nothing to the left)\nleft[1] = 5       (just nums[0])\nleft[2] = 5x2=10  (nums[0] x nums[1])\nleft[3] = 10x3=30 (nums[0..2])\nleft[4] = 30x1=30 (nums[0..3])"]

    A --> R["RIGHT array  -  scan RIGHT TO LEFT\nEach position stores the running product\nof everything after it"]
    R --> RV["right = [24, 12, 4, 4, 1]\n         idx: 0   1  2  3  4\n\nright[4] = 1       (nothing to the right)\nright[3] = 4       (just nums[4])\nright[2] = 4x1=4   (nums[3..4])\nright[1] = 4x3=12  (nums[2..4])\nright[0] = 12x2=24 (nums[1..4])"]

    LV --> M["answer[i] = left[i] x right[i]"]
    RV --> M
    M --> MV["answer = [1x24, 5x12, 10x4, 30x4, 30x1]\n        = [24,   60,   40,  120,   30]  ✅"]
```

---

## Why Starting Values Are 1

This is the most important thing to internalize before writing code.

```
left[0] = 1  because: there is NOTHING to the left of index 0.
                      The product of zero elements is 1 (multiplicative identity).

right[n-1] = 1  because: there is NOTHING to the right of the last index.
                          Same reason.

If you do NOT start with 1, you corrupt every subsequent product.
Think of it as: "I have seen nothing yet, so my accumulated product is 1."
```

### Diagram 6 — Multiplicative Identity Mindmap

```mermaid
mindmap
  root((Why Start With One))
    Product Identity
      One does not change multiplication
      It represents product of no values
      It is the correct empty side value
    First Index
      Nothing exists to the left
      Left product should be one
      This keeps the first answer valid
    Last Index
      Nothing exists to the right
      Right product should be one
      This keeps the last answer valid
    Common Mistake
      Starting with zero destroys all products
      Starting with current value includes itself
      Both break the except self rule
    Mental Model
      I have seen nothing yet
      My accumulated product is one
      Then I multiply values as I pass them
```

---

## Step-by-Step Dry Run — [5, 2, 3, 1, 4]

**Building `left[]` (left → right, starting index 1):**

```
left = [1, 1, 1, 1, 1]     ← initialize all to 1

i=1: left[1] = left[0] × nums[0] = 1 × 5 = 5     → left = [1, 5, 1, 1, 1]
i=2: left[2] = left[1] × nums[1] = 5 × 2 = 10    → left = [1, 5, 10, 1, 1]
i=3: left[3] = left[2] × nums[2] = 10 × 3 = 30   → left = [1, 5, 10, 30, 1]
i=4: left[4] = left[3] × nums[3] = 30 × 1 = 30   → left = [1, 5, 10, 30, 30]
```

**Building `right[]` (right → left, starting index n-2):**

```
right = [1, 1, 1, 1, 1]    ← initialize all to 1

i=3: right[3] = right[4] × nums[4] = 1 × 4 = 4   → right = [1, 1, 1, 4, 1]
i=2: right[2] = right[3] × nums[3] = 4 × 1 = 4   → right = [1, 1, 4, 4, 1]
i=1: right[1] = right[2] × nums[2] = 4 × 3 = 12  → right = [1, 12, 4, 4, 1]
i=0: right[0] = right[1] × nums[1] = 12 × 2 = 24 → right = [24, 12, 4, 4, 1]
```

**Building `result[]` (one final pass):**

```
result[0] = left[0] × right[0] = 1  × 24 = 24
result[1] = left[1] × right[1] = 5  × 12 = 60
result[2] = left[2] × right[2] = 10 × 4  = 40
result[3] = left[3] × right[3] = 30 × 4  = 120
result[4] = left[4] × right[4] = 30 × 1  = 30

result = [24, 60, 40, 120, 30]  ✅
```

---

## Walkthrough as a Sequence

```mermaid
sequenceDiagram
    autonumber
    participant N as nums = [5,2,3,1,4]
    participant L as left[] array
    participant R as right[] array
    participant ANS as result[]

    Note over L: Pass 1  -  left to right
    N->>L: left[0] = 1 (base case  -  nothing to left)
    N->>L: left[1] = 1 x nums[0] = 5
    N->>L: left[2] = 5 x nums[1] = 10
    N->>L: left[3] = 10 x nums[2] = 30
    N->>L: left[4] = 30 x nums[3] = 30
    Note over L: left = [1, 5, 10, 30, 30]

    Note over R: Pass 2  -  right to left
    N->>R: right[4] = 1 (base case  -  nothing to right)
    N->>R: right[3] = 1 x nums[4] = 4
    N->>R: right[2] = 4 x nums[3] = 4
    N->>R: right[1] = 4 x nums[2] = 12
    N->>R: right[0] = 12 x nums[1] = 24
    Note over R: right = [24, 12, 4, 4, 1]

    Note over ANS: Pass 3  -  multiply left x right at each index
    L->>ANS: result[0] = 1 x 24 = 24
    R->>ANS: result[1] = 5 x 12 = 60
    L->>ANS: result[2] = 10 x 4 = 40
    R->>ANS: result[3] = 30 x 4 = 120
    L->>ANS: result[4] = 30 x 1 = 30

    ANS-->>N: Return [24, 60, 40, 120, 30] ✅
```

---

## Why Zero Is No Longer a Problem

```
nums = [-1, 1, 0, -3, 3]

left  = [1, -1, -1, 0, 0]
right = [0,  0,  9, -9, 1]    (← the 9 appears at right[2] because 0 is excluded)

result[2] = left[2] × right[2] = -1 × -9 = 9  ✅

No division anywhere. Zero is just another number being multiplied.
The algorithm is completely indifferent to zeros.
```

### Diagram 7 — Zero Handling Mindmap

```mermaid
mindmap
  root((Zero Handling Without Division))
    Division Approach
      Total product becomes zero
      Dividing at zero is undefined
      Special cases are required
      Problem bans this route
    Prefix Suffix Approach
      Zero is just multiplied like any value
      No division means no undefined operation
      Left and right products stay meaningful
    One Zero Case
      Only the zero position can avoid multiplying by zero
      Other positions include zero on one side
      Result naturally becomes zero
    Multiple Zero Case
      Every position sees a zero outside itself
      All results become zero naturally
    Main Benefit
      No branching for zero
      No special math rules
      Same loops handle every input
```

---

## Complexity

```
Time:  O(n)  — three separate O(n) passes = 3n → simplified to O(n)
Space: O(n)  — O(n) for left array + O(n) for right array + O(n) for result
```

---

## ✅ Full LeetCode Solution

```python
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)

        # Array to store all left prefix products
        left = [1] * n
        for i in range(1, n):
            left[i] = left[i - 1] * nums[i - 1]

        # Array to store all right suffix products
        right = [1] * n
        for i in range(n - 2, -1, -1):
            right[i] = right[i + 1] * nums[i + 1]

        # Combine: result[i] = product of everything to the left × everything to the right
        result = [1] * n
        for i in range(n):
            result[i] = left[i] * right[i]

        return result
```

---

## Reading the Code Loop by Loop

**Loop 1 — building `left[]`:**

```python
for i in range(1, n):
    left[i] = left[i - 1] * nums[i - 1]
```

We start from index 1 because `left[0] = 1` always (nothing to the left of index 0). At each step: the product to the left of `i` is the product to the left of `i-1`, multiplied by `nums[i-1]` itself.

**Loop 2 — building `right[]`:**

```python
for i in range(n - 2, -1, -1):
    right[i] = right[i + 1] * nums[i + 1]
```

We start from index `n-2` because `right[n-1] = 1` always (nothing to the right of the last element). We go backwards. At each step: the product to the right of `i` is the product to the right of `i+1`, multiplied by `nums[i+1]` itself.

**Loop 3 — combining:**

```python
for i in range(n):
    result[i] = left[i] * right[i]
```

Straightforward multiplication. No conditions. No special casing.

### Diagram 8 — Implementation Mindmap

```mermaid
mindmap
  root((Implementation Blueprint))
    Setup
      Get array length
      Create left array filled with one
      Create right array filled with one
      Create result array
    Left Pass
      Move from left to right
      Each slot stores product before it
      Use previous left value times previous nums value
    Right Pass
      Move from right to left
      Each slot stores product after it
      Use next right value times next nums value
    Combine Pass
      For each index multiply left and right
      Store in result
      Return result
    Complexity
      Three linear passes
      Linear time overall
      Linear helper space
```

---

## Full Comparison

```mermaid
quadrantChart
    title Product of Array Except Self  -  Approach Trade-Off Map
    x-axis Simpler Logic --> More Structured Logic
    y-axis Fails Constraints --> Satisfies All Constraints
    quadrant-1 Correct and well-structured
    quadrant-2 Correct and simple
    quadrant-3 Incorrect approach
    quadrant-4 Structured but fails
    Brute Force Division: [0.20, 0.15]
    Left and Right Arrays: [0.75, 0.92]
```

---

## 🔁 The Reusable Pattern

```python
# Left-Right Prefix Product Pattern
# Use when: you need the product (or sum, or any operation) of
#           everything to the LEFT and RIGHT of each index

left = [1] * n
for i in range(1, n):
    left[i] = left[i - 1] * nums[i - 1]    # build left prefix

right = [1] * n
for i in range(n - 2, -1, -1):
    right[i] = right[i + 1] * nums[i + 1]  # build right suffix

for i in range(n):
    result[i] = left[i] * right[i]          # combine at each index
```

Apply this pattern to: **subarray range queries, span problems, trapping rain water, visibility problems, or any problem where each answer depends on its neighbors in both directions.**

---

## ✅ Final Takeaways

```
1. First instinct (division) is natural but breaks on zero and is banned.
2. Every answer[i] = (product of everything LEFT of i) × (product of everything RIGHT of i).
3. Pre-compute both sides in two separate passes. Combine in a third.
4. left[0] = 1 and right[n-1] = 1 because the multiplicative identity of "nothing" is 1.
5. Three O(n) passes = O(n) total. Space is O(n) for the two helper arrays.
6. Zero in the array is handled naturally — no special casing needed.
```

> 💡 When a problem asks you to compute something "for every element using everything except itself", think about splitting the work into **what's to the left** and **what's to the right**, then combining. Division is never needed.
