from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[Str]]:
        anagram_map = defaultdict(list)

        for s in strs:
            count = [0] * 26

            for char in s:
                count[ord(char) - ord('a')] += 1
            
            signature = tuple(count)
            anagram_map[signature].append(s)

        return list(anagram_map.values())
