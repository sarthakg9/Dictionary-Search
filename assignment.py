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

    def find_similar_words(self, word, threshold=2):
        all_words = self._get_all_words()
        similar_words = []
        for dict_word in all_words:
            distance = self._calculate_similarity(word, dict_word)
            if distance <= threshold:
                similar_words.append(dict_word)
        return similar_words

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

    @staticmethod
    def _calculate_similarity(word1, word2):
        len1 = len(word1)
        len2 = len(word2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if word1[i - 1] == word2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,       # Deletion
                    dp[i][j - 1] + 1,       # Insertion
                    dp[i - 1][j - 1] + cost  # Substitution
                )

                if i > 1 and j > 1 and word1[i - 1] == word2[j - 2] and word1[i - 2] == word2[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + cost)  # Transposition

        return dp[len1][len2]

def build_dictionary():
    dictionary_trie = DictionaryTrie()
    with open("datafile.txt", "r") as file:
        for line in file:
            word = line
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

