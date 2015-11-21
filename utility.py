"""
    Author: Thanh Dancer
    Created: 13:02:04 21/11/2015
"""

from collections import Counter
import xml.etree.ElementTree as ET
import subprocess
import time


class TagParser():
    """
    Extract tagged data after using Tagger library for Vietnamese sentences
    """



    # =========================================
    def __init__(self, popular=None, bag_of_tagged_word=None, wordlist=None):
        """Constructor for TagParser"""

        self._tag_list = {
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

        if popular is not None:
            self._popular_data = popular
        else:
            self._popular_data = Counter()

        if bag_of_tagged_word is not None:
            self._bag_of_tagged_word = bag_of_tagged_word
        else:
            self._bag_of_tagged_word = {}

        if wordlist is not None:
            self._wordlist = wordlist
        else:
            self._wordlist = {}

        self.sentences = []

    #======================================
    def _add_bag(self, tagged_word_list=None):
        """
        Args:
            self, tagged_word_list=None
        Returns:

        """
        for word in tagged_word_list:
            # Check if the global bag don't have tag
            if not self._bag_of_tagged_word.has_key(word['tag']):
                self._bag_of_tagged_word[word['tag']] = []

            # Insert a word into _
            # if word['word'] not in self._bag_of_tagged_word:
            self._bag_of_tagged_word[word['tag']].append(word['word'])

            # Count the word to find the popular of word
            self._popular_data[word['word']] += 1

            # Word to tag mapping
            self._wordlist[word['word']] = word['tag']

            # Add vocabulary
            # self._vocabulary.append(word['word'])

        return True



    # ======================================
    def extract_word_tags_raw_sentence(self, input_sentence=""):
        """
        Args:
            (self, input_sentence)
        Returns:

        """
        wordlist_tagged = []
        words = input_sentence.strip().split(' ')
        for word in words:
            word, tag = word.split('/')
            if len(word) > 1 and self._tag_list.has_key(tag):
                wordlist_tagged.append({
                    'tag': tag,
                    'word': word.decode('utf-8').lower()
                })

        return wordlist_tagged

    # ======================================
    def add_bag_raw_sentence(self, input_sentence=""):
        """
        Args:

        Returns:
        :param input_sentence:

        """
        tagged_words = self.extract_word_tags_raw_sentence(input_sentence)
        self._add_bag(tagged_words)

    # ======================================
    def extract_words_xml_file(self, filepath=""):
        doc = ET.parse(filepath)

        wordlist_tagged = []
        root = doc.getroot()
        for sentence in root.findall('s'):
            conjunction = []
            for word in sentence.findall('w'):
                wordlist_tagged.append({
                    'tag': word.get('pos'),
                    'word': word.text
                })
                conjunction.append(word.text)
            print conjunction
            print ' '.join(conjunction)
            self.sentences.append(' '.join(conjunction))

        return wordlist_tagged

    #======================================
    def add_bag_xml_file(self, filepath=""):
        """
        Args:
            self, filepath=""
        Returns:

        """
        tagged_words = self.extract_words_xml_file(filepath)
        self._add_bag(tagged_words)




class NLPLibrary:
    """"""

    #=========================================
    def __init__(self):
        """Constructor for NLPLibrary"""
        self.TP = TagParser()

    #======================================
    def _add_tag(self, file_input="", file_output=""):
        # IMPORTANT: The input and output file MUST be absolute path
        if file_output == "":
            file_output = '/tmp/out.smartfeedback'
        subprocess.call(['./vnTagger.sh', '-i %s -uo %s' % (file_input, file_output)])
        self.TP.add_bag_xml_file(file_output)

    #======================================
    def tag_paragraph(self, paragraph=""):
        # Write paragraph to file prepare for Tagger
        filepath = '/tmp/%sparagraph.input.smartfeedback' % (str(round(time.time())))
        f = open(filepath, 'w')
        f.write(paragraph)
        f.close()
        self._add_tag(file_input=filepath)




