from trie import Trie

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            return 0
        if pattern == "":
            return 0
        count = 0
        def searcher(node, current_word):
            nonlocal count
            if node.is_end:
                if current_word.endswith(pattern):
                    count += 1
            for char, child_node in node.children.items():
                searcher(child_node, current_word + char)
        searcher(self.root, "")
        return count

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            return False
        if prefix == "":
            return False
        
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False  
            node = node.children[char]  
        
        return True 


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat

    print("Всі тести пройдені успішно!")
