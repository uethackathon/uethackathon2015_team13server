"""
    Author: Thanh Dancer
    Created: 13:02:04 21/11/2015
"""

from collections import Counter


class TagParser():
    """
    Extract tagged data after using Tagger library for Vietnamese sentences
    """

    _popular_data = Counter()
    _tag_list = {
        'Np': 'Proper noun',
        'Nc': 'Classifier',
        'Nu': 'Unit noun',
        'N': 'Common noun',
        'V': 'Verb',
        'A': 'Adjective',
        'P': 'Pronoun',
        'R': 'Adverb',
        'L': 'Determiner',
        'M': 'Numeral',
        'E': 'Preposition',
        'C': 'Subordinating conjunction',
        'CC': 'Coordinating conjunction',
        'I': 'Interjection',
        'T': 'Auxiliary, modal words',
        'Y': 'Abbreviation',
        'Z': 'Bound morphemes',
        'X': 'Unknown'
    }
    _bag_of_tagged_word = {}
    _wordlist = {}

    # =========================================
    def __init__(self, popular=None, bag_of_tagged_word=None, wordlist=None):
        """Constructor for TagParser"""
        if popular is not None:
            self._popular_data = popular

        if bag_of_tagged_word is not None:
            self._bag_of_tagged_word = bag_of_tagged_word

        if wordlist is not None:
            self._wordlist = wordlist

    # ======================================
    def extract_word_tags(self, input_sentence=""):
        """
        Args:
            (self, input_sentence)
        Returns:

        """
        wordlist_tagged = []
        words = input_sentence.split(' ')
        for word in words:
            word, tag = word.split('/')
            if len(word) > 1 and self._tag_list.has_key(tag):
                wordlist_tagged.append({
                    'tag': tag,
                    'word': word.decode('utf-8').lower()
                })

        return wordlist_tagged

    # ======================================
    def add_bag_item(self, input_sentence=""):
        """
        Args:

        Returns:
        :param input_sentence:

        """
        tagged_words = self.extract_word_tags(input_sentence)
        for word in tagged_words:
            # Check if the global bag don't have tag
            if not self._bag_of_tagged_word.has_key(word['tag']):
                self._bag_of_tagged_word[word['tag']] = {}

            # Insert a word into _
            self._bag_of_tagged_word[word['tag']].add(word['word'])

            # Count the word to find the popular of word
            self._popular_data[word['word']] += 1

            # Word to tag mapping
            self._wordlist[word['word']] = word['tag']


