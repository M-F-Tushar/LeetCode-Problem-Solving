# 🔤 LeetCode #242 — Valid Anagram

> **[Open on LeetCode →](https://leetcode.com/problems/valid-anagram/)**
> **Difficulty:** Easy | **Topic:** String, Hash Map, Sorting

---

## 📋 Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an **anagram** of `s`, and `false` otherwise.

An **anagram** is a word formed by rearranging the letters of another word, using all original letters **exactly once**.

**Constraints:**
```
1 <= s.length, t.length <= 5 * 10^4
s and t consist of lowercase English letters only
```

**Follow-up:** What if the inputs contain Unicode characters?

---

## 📌 Examples

```
Input:  s = "anagram",  t = "nagaram"   →   true
Reason: Same letters, same counts — just rearranged

Input:  s = "rat",  t = "car"           →   false
Reason: 'rat' has 't', 'car' has 'c' — different characters

Input:  s = "aa",  t = "a"              →   false
Reason: Same character but different frequency
```

---

## 🗺️ Understanding the Problem First

```mermaid
mindmap
  root((Valid Anagram))
    What am I given?
      Two strings s and t
    What do I return?
      true or false
    What makes an anagram?
      Same characters
      Same frequency of each character
      Order does NOT matter
    Core insight
      Character order is irrelevant
      Only character COUNT matters
    Best approach
      Build a frequency table for both strings
      Compare the tables
```

---

## 🧭 The Two Phases of Solving

```mermaid
flowchart LR
    START(["Valid Anagram"]) --> U["Understand\nSame chars + same frequencies\nOrder does not matter"]
    U --> L["Free First Check\nDifferent lengths cannot match\nReturn false immediately"]
    L --> S["Baseline\nSort both strings\nO(n log n)"]
    S --> B["Lowercase Optimal\n26-slot bucket array\nO(n), O(1)"]
    B --> H["Flexible Follow-up\nHash map / Counter\nUnicode-safe"]
    H --> DONE(["Return whether frequency tables balance"])
```

---

## 🔑 Core Insight Before Any Code

```
"anagram"  counts as: { a:3, n:1, g:1, r:1, m:1 }
"nagaram"  counts as: { a:3, n:1, g:1, r:1, m:1 }

Tables are identical → True ✅

"rat"  counts as: { r:1, a:1, t:1 }
"car"  counts as: { c:1, a:1, r:1 }

Tables differ (t vs c) → False ❌
```

The order letters appear in does not matter. Only **how many times each letter appears** matters.

---

## ⚡ The Always-First Check: Length

```mermaid
flowchart LR
    A["len(s) != len(t)?"] -- Yes --> B["Return False immediately\nCan't be anagrams\nif lengths differ"]
    A -- No --> C["Proceed to frequency check"]

```

This is a free O(1) optimization that eliminates many inputs immediately.

---

## 📊 Solution Progression Overview

```mermaid
timeline
    title From First Idea to Optimal Solution

    Solution 1 Sorting
        : Sort both strings
        : Anagrams produce identical sorted strings
        : O(n log n) — simple and correct

    Solution 2 Bucket Array
        : 26 fixed counters for a-z
        : Increment for s, decrement for t
        : O(n) time, O(1) space — optimal for lowercase

    Solution 3 Hash Map
        : Dynamic frequency table
        : Works for any character set
        : O(n) time, O(k) space — Unicode-safe
```

---
---

# ✏️ Solution 1 — Sorting

## Thinking From This Perspective

**My starting thought:** *"If two strings are anagrams, they contain the same letters. Sorting both strings rearranges letters into the same order. If they're anagrams, their sorted forms must be identical. I can just compare them."*

```
s = "anagram" → sort → "aaagmnr"
t = "nagaram" → sort → "aaagmnr"

"aaagmnr" == "aaagmnr" → True ✅
```

---

## Visual — Sorting Normalizes Both Strings

```mermaid
flowchart TD
    S["s = 'anagram'"] --> SS["sorted(s) = 'aaagmnr'"]
    T["t = 'nagaram'"] --> ST["sorted(t) = 'aaagmnr'"]

    SS --> Cmp{"Are sorted strings equal?"}
    ST --> Cmp

    Cmp -- Yes --> True["Return True ✅"]
    Cmp -- No  --> False["Return False ❌"]

```

---

## Both Cases Side by Side

```mermaid
sequenceDiagram
    autonumber
    participant I as Input
    participant Sort as sorted()
    participant Cmp as Comparison

    I->>Sort: s = "anagram"
    Sort-->>Cmp: "aaagmnr"

    I->>Sort: t = "nagaram"
    Sort-->>Cmp: "aaagmnr"

    Cmp->>Cmp: "aaagmnr" == "aaagmnr" → True ✅

    Note over I,Cmp: Case 2

    I->>Sort: s = "rat"
    Sort-->>Cmp: "art"

    I->>Sort: t = "car"
    Sort-->>Cmp: "acr"

    Cmp->>Cmp: "art" != "acr" → False ❌
```

---

## Complexity

```
Time:  O(n log n)  — sorting both strings
Space: O(n)        — Python's sorted() creates new list objects
```

---

## ✅ Full LeetCode Solution — Sorting

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):                # quick early exit
            return False

        return sorted(s) == sorted(t)       # anagrams sort to the same string
```

---

## Why I Move to the Next Solution

```mermaid
flowchart TD
    A["Sorting works ✅\nClean, readable, easy"] --> B["But sorting does more work than needed\nWe don't care about ORDER\nWe only care about COUNTS"]
    B --> C["Key question:\nCan I check character frequencies\nwithout sorting?"]
    C --> D["New idea: count each character\nFor lowercase a-z, there are exactly 26 possibilities\nUse a fixed array of 26 slots\nO(n) time, O(1) space"]

```

---
---

# ✏️ Solution 2 — Bucket Array (26 Fixed Counters)

## Thinking From This Perspective

**My new thought:** *"There are only 26 lowercase letters. I can give each letter a slot in a fixed-size array. For each character in s, increment its slot. For each character in t, decrement its slot. If s and t are anagrams, every slot returns to zero."*

Formula to map a letter to its index:
```
index = ord(char) - ord('a')

'a' → 0
'b' → 1
...
'z' → 25
```

---

## Visual — Mapping Letters to Buckets

```mermaid
flowchart LR
    A["'a'"] --> I0["slot 0"]
    B["'b'"] --> I1["slot 1"]
    G["'g'"] --> I6["slot 6"]
    Z["'z'"] --> I25["slot 25"]

    subgraph Formula["ord(char) - ord('a')"]
        F["'g' → ord(103) - ord(97) = 6"]
    end

```

---

## Balance Strategy — Increment s, Decrement t

```mermaid
flowchart TD
    A["counts = [0] * 26\n(26 zeroed slots)"] --> B["Loop through s and t together\nat each position i:"]
    B --> C["counts for s[i]  +=1"]
    B --> D["counts for t[i]  -=1"]
    C --> E["After full scan:"]
    D --> E
    E --> F{"All slots == 0?"}
    F -- Yes --> G["Return True ✅\nEvery addition was balanced by a subtraction"]
    F -- No  --> H["Return False ❌\nSome character count doesn't match"]

```

---

## Walkthrough on "anagram" / "nagaram"

```mermaid
sequenceDiagram
    autonumber
    participant S as s = "anagram"
    participant T as t = "nagaram"
    participant C as counts[26]

    S->>C: 'a'→slot0 +1, 'n'→slot13 +1, 'a'→slot0 +1 ...
    Note over C: slot0(a)=3, slot13(n)=1, slot6(g)=1, slot17(r)=1, slot12(m)=1

    T->>C: 'n'→slot13 -1, 'a'→slot0 -1, 'g'→slot6 -1 ...
    Note over C: All slots return to 0

    C-->>C: all(c==0) → True ✅
```

---

## Complexity

```
Time:  O(n)   — one pass through both strings simultaneously
Space: O(1)   — always exactly 26 slots, regardless of input size
```

---

## ✅ Full LeetCode Solution — Bucket Array

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):                         # quick early exit
            return False

        counts = [0] * 26                            # one slot for each letter a–z

        for i in range(len(s)):
            counts[ord(s[i]) - ord('a')] += 1        # s adds to its letter's slot
            counts[ord(t[i]) - ord('a')] -= 1        # t removes from its letter's slot

        return all(count == 0 for count in counts)   # balanced = anagram
```

---

## Why I Move to the Next Solution

```mermaid
flowchart TD
    A["Bucket Array is optimal for lowercase a-z ✅\nO(n) time, O(1) space"] --> B["But it is CONSTRAINT-SPECIFIC\nOnly works for exactly 26 lowercase English letters"]
    B --> C["What if input has:\nUppercase letters?\nSpaces or punctuation?\nAccented letters (é, ü)?\nUnicode / emojis?"]
    C --> D["The fixed-array index would break or be incorrect"]
    D --> E["New idea: dynamic hash map\nLet the map grow to fit any character\nSame logic: increment s, decrement t\nCheck all zeros at the end\nO(n) time, O(k) space — works for everything"]

```

---
---

# ✏️ Solution 3 — Hash Map (Unicode-Safe, Flexible)

## Thinking From This Perspective

**My final thought:** *"Same idea as the bucket array, but instead of a fixed 26-slot array, I use a dictionary keyed by the actual character. This handles any alphabet — lowercase, uppercase, Unicode, emojis. The logic is identical: +1 for s, -1 for t, check all zeros."*

---

## Visual — Dynamic Frequency Map

```mermaid
flowchart TD
    subgraph Scan_s["Scan s: increment counts"]
        A["Read char from s"]
        B["freq[char] += 1"]
    end

    subgraph Scan_t["Scan t: decrement counts"]
        C["Read char from t"]
        D["freq[char] -= 1"]
    end

    B --> E["Combined frequency map\nbalanced if anagrams"]
    D --> E

    E --> F{"All values == 0?"}
    F -- Yes --> G["Return True ✅"]
    F -- No  --> H["Return False ❌"]

```

---

## Walkthrough on "rat" / "car" (Non-Anagram)

```mermaid
sequenceDiagram
    autonumber
    participant S as s = "rat"
    participant T as t = "car"
    participant F as freq dict

    S->>F: 'r' +1 → {r:1}
    S->>F: 'a' +1 → {r:1, a:1}
    S->>F: 't' +1 → {r:1, a:1, t:1}

    T->>F: 'c' -1 → {r:1, a:1, t:1, c:-1}
    T->>F: 'a' -1 → {r:1, a:0, t:1, c:-1}
    T->>F: 'r' -1 → {r:0, a:0, t:1, c:-1}

    F->>F: t:1 and c:-1 are not zero
    F-->>S: Return False ❌
```

---

## Complexity

```
Time:  O(n)   — one pass through both strings
Space: O(k)   — k = number of unique characters in s and t combined
               For lowercase a-z: k ≤ 26
               For Unicode: k can be larger but bounded by input
```

---

## ✅ Full LeetCode Solution — Hash Map

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):                          # quick early exit
            return False

        freq = {}                                     # dynamic character frequency map

        for i in range(len(s)):
            freq[s[i]] = freq.get(s[i], 0) + 1       # increment for s
            freq[t[i]] = freq.get(t[i], 0) - 1       # decrement for t

        return all(v == 0 for v in freq.values())     # balanced = anagram
```

---

## Bonus — Pythonic Counter One-Liner

```python
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
```

`Counter` builds the frequency map automatically. Two Counters are equal only if every key has the same count in both — exactly what we need.

---

## Full Comparison of All Three Solutions

```mermaid
quadrantChart
    title Valid Anagram Approach Trade-Off Map
    x-axis Lowercase Only --> Any Character Set
    y-axis Slower Runtime --> Faster Runtime
    quadrant-1 Fast and universal
    quadrant-2 Fast but constraint-specific
    quadrant-3 Slow and limited
    quadrant-4 Flexible but slower
    Sorting O(n log n), general: [0.80, 0.42]
    26-Bucket Array O(n), O(1): [0.18, 0.96]
    Hash Map O(n), Unicode-safe: [0.88, 0.90]
    Counter One-Liner O(n), readable: [0.94, 0.84]
```

---

## Approach Trade-Off Map

```mermaid
quadrantChart
    title Speed vs Flexibility for Valid Anagram Approaches
    x-axis Only Lowercase a-z --> Works for Any Characters
    y-axis Slower --> Faster

    quadrant-1 Fast and Universal
    quadrant-2 Fast but Limited Scope
    quadrant-3 Avoid
    quadrant-4 Universal but Slower

    Sorting: [0.80, 0.42]
    Bucket Array: [0.20, 0.92]
    Hash Map: [0.85, 0.88]
    Counter one-liner: [0.90, 0.82]
```

---

## 🔁 The Reusable Pattern

```python
# Frequency Counting Pattern
freq = {}
for ch in first_string:
    freq[ch] = freq.get(ch, 0) + 1      # count up
for ch in second_string:
    freq[ch] = freq.get(ch, 0) - 1      # count down
return all(v == 0 for v in freq.values())  # balanced = match
```

Apply this pattern to: **anagram detection, frequency comparison, inventory matching, multiset equality, character distribution problems.**

---

## ✅ Final Takeaways

```
1. Anagram = same characters with same frequencies (order does NOT matter)
2. Always check lengths first — O(1) early exit
3. Sorting works but O(n log n) is unnecessary when you only need counts
4. Bucket array: O(n) time, O(1) space — best for lowercase a-z
5. Hash map: O(n) time, O(k) space — works for any character set
6. Progression: O(n log n) → O(n) with O(1) space → O(n) with any charset
```

> 💡 When the question is *"do these two collections contain the same stuff?"* — count frequencies and compare the tables.
