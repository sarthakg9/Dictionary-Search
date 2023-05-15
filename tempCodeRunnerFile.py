    similar_words = []
        for dict_word in all_words:
            if abs(len(dict_word) - len(word)) <= max_length_diff:
                distance = self._calculate_similarity(word, dict_word)
                if distance is not None and distance <= max_typos:
                    similarity_score = self._calculate_similarity_score(word, dict_word, distance)
                    if similarity_score >= min_similarity_score:
                        similar_words.append((dict_word, similarity_score))
        similar_words.sort(key=lambda x: x[1], reverse=True)
    