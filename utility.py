"""
    Author: Thanh Dancer
    Created: 13:02:04 21/11/2015
"""

from collections import Counter

class TagParser():
    """
    Extract tagged data after using Tagger library for Vietnamese sentences
    """

    _data_counter = Counter()
    _tag_list = {
        'Np' : 'Proper noun',
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

    #=========================================
    def __init__(self):
        """Constructor for TagParser"""

    #======================================
    def extract_word_tags(self, input_sentence=""):
        """
        Args:
            (self, input_sentence)
        Returns:

        """
        wordlist_tagged = []
        words = input_sentence.split(' ')
        for word in words:
            word, tag= word.split('/')
            if len(word) > 1 and self._tag_list.has_key(tag):
                wordlist_tagged.append({
                    'tag': tag,
                    'word': word
                })

        return wordlist_tagged








