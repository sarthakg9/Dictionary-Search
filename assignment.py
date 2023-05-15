import difflib

class DictionaryTrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class DictionaryTrie:
    def __init__(self):
        self.root = DictionaryTrieNode()

    def insert_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = DictionaryTrieNode()
            node = node.children[char]
        node.is_word = True

    def search_word(self, word):
        node = self.root
        results = []
        self._dfs_traversal(node, word, '', results)
        return results

    def _dfs_traversal(self, node, remaining_word, current_word, results):
        if not remaining_word:
            if node.is_word:
                results.append(current_word)
            return

        char = remaining_word[0]
        if char in node.children:
            child_node = node.children[char]
            next_word = current_word + char
            self._dfs_traversal(child_node, remaining_word[1:], next_word, results)

        for char, child_node in node.children.items():
            next_word = current_word + char
            self._dfs_traversal(child_node, remaining_word, next_word, results)

    def find_similar_words(self, word, threshold=0.7):
        all_words = self._get_all_words()
        matches = difflib.get_close_matches(word, all_words, cutoff=threshold)
        return matches

    def _get_all_words(self):
        words = []
        self._dfs_collect_words(self.root, '', words)
        return words

    def _dfs_collect_words(self, node, current_word, words):
        if node.is_word:
            words.append(current_word)

        for char, child_node in node.children.items():
            next_word = current_word + char
            self._dfs_collect_words(child_node, next_word, words)

def build_dictionary():
    dictionary_trie = DictionaryTrie()
    with open("datafile.txt", "r") as file:
        for line in file:
            word = line.strip().lower()  # Remove leading/trailing whitespaces and convert to lowercase
            dictionary_trie.insert_word(word)
    return dictionary_trie

# Example usage:
dictionary = build_dictionary()
search_term = input("Enter a word to search: ").lower()

results = dictionary.search_word(search_term)
similar_words = dictionary.find_similar_words(search_term)

if results:
    print("Found words:")
    for word in results:
        print(word)

if similar_words:
    print("Similar words:")
    for word in similar_words:
        print(word)

if not results and not similar_words:
    print("No matches found.")
