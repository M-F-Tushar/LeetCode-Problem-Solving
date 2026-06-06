# 🔤 LeetCode #49 — Group Anagrams

> **[Open on LeetCode →](https://leetcode.com/problems/group-anagrams/)**
> **Difficulty:** Medium | **Topic:** String, Hash Map, Sorting

---

## 📋 Problem Statement

Given an array of strings `strs`, group the **anagrams** together. You can return the answer in **any order**.

An **anagram** is a word formed by rearranging the letters of another word, using all original letters **exactly once**.

**Constraints:**
```
1 <= strs.length <= 10^4
0 <= strs[i].length <= 100
strs[i] consists of lowercase English letters only
```

---

## 📌 Examples

```
Input:  strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
Reason: "eat", "tea", "ate" are anagrams of each other
        "tan", "nat" are anagrams of each other
        "bat" has no anagram partner

Input:  strs = [""]
Output: [[""]]

Input:  strs = ["a"]
Output: [["a"]]
```

---

## 🗺️ Understanding the Problem First

```mermaid
mindmap
  root((Group Anagrams))
    What am I given?
      An array of strings
    What do I return?
      Grouped lists of anagrams
    What makes two strings anagrams?
      Same characters
      Same frequency of each character
      Order does NOT matter
    Core insight
      Transform each string into a universal signature
      Anagrams share the same signature
    Best approach
      Use a Hash Map keyed by signature
      All anagrams naturally collide under the same key
```

---

## 🧭 The Two Phases of Solving

```mermaid
flowchart LR
    START(["Group Anagrams"]) --> U["Understand\nGroup strings, not just compare two\nEach group shares a signature"]
    U --> S["Signature Idea\nTransform every anagram\ninto the same canonical key"]
    S --> B["Baseline Signature\nSort each string\nO(n x k log k)"]
    B --> F["Optimal Signature\n26-count frequency tuple\nO(n x k)"]
    F --> M["Hash Map Grouping\nsignature -> list of words"]
    M --> DONE(["Return all grouped values"])
```

---

## 🔑 Core Insight Before Any Code

```
"eat"  →  signature  →  "aet"
"tea"  →  signature  →  "aet"
"ate"  →  signature  →  "aet"

All three map to the same key → grouped together ✅

"tan"  →  signature  →  "ant"
"nat"  →  signature  →  "ant"

Both map to the same key → grouped together ✅

"bat"  →  signature  →  "abt"

Unique key → its own group ✅
```

The key architectural question: **"How do I transform every anagram into the exact same universal signature?"**

```
[Raw Strings] ──> [Signature Generator] ──> [Hash Map (Grouping)]
      │                      │                          │
"eat","tea","ate"  ──>     "aet"        ──>  { "aet": ["eat","tea","ate"] }
```

---

## 📊 Strategic Decision Flow & Stress-Testing

```mermaid
flowchart TD
    A["🧩 Input: Array of Strings"] --> B["🪓 Baseline Idea\nCompare all pairs"]

    B --> C{"⚠️ Bottleneck?"}
    C -->|"Yes"| D["O(n2) comparisons.\nInstant Timeout Failure."]

    D --> E["🔁 Pivot 1: Sorted Signature\nSort each string. Use sorted string as Hash Key."]

    E --> F{"⚠️ Is Sorting Optimal?"}
    F -->|"No"| G["O(k log k) sorting overhead per string.\nWaste of CPU cycles."]

    G --> H["🧠 Pivot 2: Frequency Array Signature\nCount char frequency. Use count tuple as Hash Key."]
    H --> I["🚀 Optimal Result\nTime: O(n * k)"]


```

---

## 📊 Solution Progression Overview

```mermaid
timeline
    title From First Idea to Optimal Solution

    Solution 1 Sorting
        : Sort each string to create its signature
        : Anagrams produce identical sorted strings
        : O(n * k log k)  -  simple and correct

    Solution 2 Frequency Tuple
        : 26 fixed counters for a-z per string
        : Convert count array to immutable tuple as key
        : O(n * k) time  -  eliminates sorting overhead entirely
```

---
---

# ✏️ Solution 1 — Sorting as a Signature

## Thinking From This Perspective

**My starting thought:** *"If I sort 'eat', 'tea', and 'ate' alphabetically, they all become 'aet'. Therefore, if I loop through the array, sort each string, and use the sorted version as a dictionary key, all anagrams will automatically group together under that key."*

```
"eat" → sorted → "aet"
"tea" → sorted → "aet"
"ate" → sorted → "aet"

All three share the key "aet" → grouped ✅
```

---

## Visual — Sorting Normalizes All Anagrams

```mermaid
flowchart TD
    A["strs = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']"] --> B["Loop through each string s"]

    B --> C["Sort s to get signature\ne.g. 'tea' → 'aet'"]
    C --> D["anagram_map[signature].append(s)"]

    D --> E["anagram_map after full loop"]

    E --> F["'aet' → ['eat', 'tea', 'ate']"]
    E --> G["'ant' → ['tan', 'nat']"]
    E --> H["'abt' → ['bat']"]

    F --> I["Return list of all values ✅"]
    G --> I
    H --> I

```

---

## Step-by-Step Walkthrough

```mermaid
sequenceDiagram
    autonumber
    participant S as strs input
    participant SIG as Signature (sorted)
    participant MAP as anagram_map

    S->>SIG: "eat"
    SIG-->>MAP: key = "aet" → ["eat"]

    S->>SIG: "tea"
    SIG-->>MAP: key = "aet" → ["eat", "tea"]

    S->>SIG: "tan"
    SIG-->>MAP: key = "ant" → ["tan"]

    S->>SIG: "ate"
    SIG-->>MAP: key = "aet" → ["eat", "tea", "ate"]

    S->>SIG: "nat"
    SIG-->>MAP: key = "ant" → ["tan", "nat"]

    S->>SIG: "bat"
    SIG-->>MAP: key = "abt" → ["bat"]

    MAP-->>S: Return [["eat","tea","ate"], ["tan","nat"], ["bat"]] ✅
```

---

## Complexity

```
Time:  O(n * k log k)  — sorting each string of length k, for n strings
Space: O(n * k)        — storing all strings in the hash map
```

---

## ✅ Full LeetCode Solution — Sorting

```python
from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_map = defaultdict(list)

        for s in strs:
            # Sort the string to create the universal signature
            # e.g., "tea" -> ['a', 'e', 't'] -> "aet"
            signature = "".join(sorted(s))
            anagram_map[signature].append(s)

        return list(anagram_map.values())
```

---

## Why I Move to the Next Solution

```mermaid
flowchart TD
    A["Sorting works ✅\nClean, readable, easy"] --> B["But sorting does more work than needed\nWe don't care about ORDER\nWe only care about COUNTS"]
    B --> C["Key question:\nCan I generate a signature from\ncharacter frequencies without sorting?"]
    C --> D["New idea: count each character\nFor lowercase a-z, there are exactly 26 possibilities\nUse a fixed array of 26 slots\nConvert to a tuple as the hash key\nO(n * k) time  -  no log k overhead"]

```

---
---

# ✏️ Solution 2 — Character Frequency Tuple (Optimal)

## Thinking From This Perspective

**My new thought:** *"I don't need to sort strings. Anagrams are defined by character counts. Since the problem guarantees lowercase English letters, I can create a fixed array of 26 zeros. For each string, I'll count the characters, convert that 26-element array into a tuple (since lists cannot be dictionary keys in Python), and use that as my O(1) hashing signature."*

Formula to map a letter to its index:
```
index = ord(char) - ord('a')

'a' → 0
'b' → 1
...
'z' → 25
```

---

## Visual — Mapping Characters to a 26-Bucket Array

```mermaid
flowchart LR
    A["'a'"] --> I0["slot 0"]
    B["'b'"] --> I1["slot 1"]
    G["'e'"] --> I4["slot 4"]
    Z["'z'"] --> I25["slot 25"]

    subgraph Formula["ord(char) - ord('a')"]
        F["'e' → ord(101) - ord(97) = 4"]
    end

```

---

## Building the Frequency Tuple Signature

```mermaid
flowchart TD
    A["s = 'eat'"] --> B["count = [0] * 26\n(26 zeroed slots)"]
    B --> C["Loop through each char in s"]
    C --> D["count[ord(char) - ord('a')] += 1"]
    D --> E["count after 'eat':\nslot0(a)=1, slot4(e)=1, slot19(t)=1\nall others = 0"]
    E --> F["signature = tuple(count)\n= (1,0,0,0,1,0,...,1,0,0,0,0,0)"]
    F --> G["anagram_map[signature].append('eat')"]

```

---

## Walkthrough — "eat", "tea", "ate" All Share the Same Tuple

```mermaid
sequenceDiagram
    autonumber
    participant S as strs input
    participant C as count[26]
    participant MAP as anagram_map

    S->>C: "eat" → a=1, e=1, t=1
    C-->>MAP: tuple → (1,0,0,0,1,0,...,1,...) → ["eat"]

    S->>C: "tea" → t=1, e=1, a=1
    C-->>MAP: tuple → (1,0,0,0,1,0,...,1,...) → ["eat", "tea"]

    Note over C,MAP: Same tuple key  -  same frequencies!

    S->>C: "ate" → a=1, t=1, e=1
    C-->>MAP: tuple → (1,0,0,0,1,0,...,1,...) → ["eat", "tea", "ate"]

    MAP-->>S: Return [["eat","tea","ate"], ["tan","nat"], ["bat"]] ✅
```

---

## Complexity

```
Time:  O(n * k)   — scan each character of each string once; no sorting
Space: O(n * k)   — storing all strings in the hash map
```

---

## ✅ Full LeetCode Solution — Frequency Tuple

```python
from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_map = defaultdict(list)

        for s in strs:
            # Initialize an empty 26-bucket array for character frequencies
            count = [0] * 26

            for char in s:
                # Increment the specific character's index (a=0, b=1... z=25)
                count[ord(char) - ord('a')] += 1

            # Convert the list to an immutable tuple to use as a dictionary key
            signature = tuple(count)
            anagram_map[signature].append(s)

        return list(anagram_map.values())
```

---

## Full Comparison of Both Solutions

```mermaid
quadrantChart
    title Group Anagrams Approach Trade-Off Map
    x-axis Simpler Signature --> More Optimized Signature
    y-axis Slower Runtime --> Faster Runtime
    quadrant-1 Fast optimized grouping
    quadrant-2 Fast simple grouping
    quadrant-3 Slow but easy baseline
    quadrant-4 Complex without enough payoff
    Sorted String Signature: [0.25, 0.45]
    Frequency Tuple Signature: [0.82, 0.92]
```

---

## Approach Trade-Off Map

```mermaid
quadrantChart
    title Speed vs Simplicity for Group Anagrams Approaches
    x-axis Less Code Complexity --> More Code Complexity
    y-axis Slower --> Faster

    quadrant-1 Fast and Worth the Complexity
    quadrant-2 Fast and Simple
    quadrant-3 Avoid
    quadrant-4 Simple but Slower

    Sorting Signature: [0.25, 0.45]
    Frequency Tuple: [0.65, 0.88]
```

---

## 🔁 The Reusable Pattern

```python
# Signature-Based Grouping Pattern
from collections import defaultdict

groups = defaultdict(list)
for item in input_list:
    signature = generate_signature(item)   # transform into a canonical key
    groups[signature].append(item)         # collide all equivalents under same key
return list(groups.values())
```

Apply this pattern to: **anagram grouping, classifying strings by shape, grouping words by character distribution, categorizing objects by a canonical form.**

---

## ✅ Final Takeaways

```
1. Never compare every string to every other string — that is an O(n²) trap
2. Instead, assign each string a universal "signature" so anagrams naturally collide in a Hash Map
3. Sorting is a valid signature (O(k log k)) but carries unnecessary overhead
4. Frequency tuple is the optimal signature (O(k)) — pure character counting, no sorting
5. Use defaultdict(list) to avoid KeyError when appending to a new key
6. Tuples are immutable → hashable → valid dictionary keys; lists are not
7. Progression: O(n²) brute force → O(n * k log k) sorting → O(n * k) frequency tuple
```

> 💡 When asked to **group or categorize** items that are "equivalent" by some rule — find a way to **transform each item into a canonical key** and let the Hash Map do the grouping automatically.
