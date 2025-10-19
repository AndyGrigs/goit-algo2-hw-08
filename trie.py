class TrieNode:
    def __init__(self):
        self.children={}
        self.is_end = False
        self.value = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def put(self, key, value):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.value = value

    def get(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value if node.is_end else None

if __name__ == "__main__":
    trie = Trie()
    trie.put("apple", 0)
    print(trie.get("apple"))
    print(trie.get("app"))