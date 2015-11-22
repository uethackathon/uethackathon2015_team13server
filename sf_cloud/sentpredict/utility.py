"""
    Author: Thanh Dancer
    Created: 13:02:04 21/11/2015
"""

from collections import Counter
import xml.etree.ElementTree as ET
import subprocess
import time
import numpy as np


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

    # ======================================
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
            self.sentences.append(' '.join(conjunction))

        return wordlist_tagged

    # ======================================
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

    # =========================================
    def __init__(self):
        """Constructor for NLPLibrary"""

    # ======================================
    def _add_tag(self, file_input="", file_output=""):
        # IMPORTANT: The input and output file MUST be absolute path
        if file_output == "":
            file_output = '/tmp/tagged%s.smartfeedback' % (str(round(time.time())))
        file_input = self._split_sentence(file_input)
        subprocess.call(['./vnTagger.sh', '-i %s -upo %s' % (file_input, file_output)])
        return file_output

    # ======================================
    def _split_sentence(self, file_input="", file_output=""):
        # IMPORTANT: The input and output file MUST be absolute path
        if file_output == "":
            file_output = '/tmp/sentences%s.smartfeedback' % (str(round(time.time())))
        subprocess.call(['./vnSentDetector.sh', '-i %s -o %s' % (file_input, file_output)])
        return file_output

    # ======================================
    def tag_paragraph(self, paragraph=""):

        """

        :param paragraph: String
        :return: sentences: a list of tagged sentence

        """
        # Write paragraph to file prepare for Tagger

        filepath = '/tmp/%sparagraph.input.smartfeedback' % (str(round(time.time())))
        f = open(filepath, 'w')
        f.write(paragraph)
        f.close()


        # Call add tag to assign tag to sentences
        taggedfile = self._add_tag(file_input=filepath)
        sentences = open(taggedfile, 'r').readlines()
        return sentences


class ClassifySentence:
    # =========================================
    def __init__(self, distribution_param):
        """Constructor for ClassifySentence"""
        self.NLP = NLPLibrary()
        self.Bag = TagParser()
        self.P_vc, self.P_matrix, self.NT_vc, self.NT_matrix, self.N_vc, self.N_matrix, self.clf = distribution_param

    # ======================================
    def _calculate_matrix(self, Positive_VectorCount, Positive_Matrix, Negative_VectorCount, Negative_Matrix,
                          Neutral_VectorCount, Neutral_Matrix, input_sentence):
        tmp_bag = TagParser()
        tmp_bag.add_bag_raw_sentence(input_sentence)
        nouns = tmp_bag._bag_of_tagged_word['N'] if tmp_bag._bag_of_tagged_word.has_key('N') else []
        verbs = tmp_bag._bag_of_tagged_word['V'] if tmp_bag._bag_of_tagged_word.has_key('V') else []
        adjs = tmp_bag._bag_of_tagged_word['A'] if tmp_bag._bag_of_tagged_word.has_key('A') else []
        advs = tmp_bag._bag_of_tagged_word['R'] if tmp_bag._bag_of_tagged_word.has_key('R') else []
        vocab = nouns + verbs + adjs + advs
        positive_prop = np.sum(Positive_Matrix * Positive_VectorCount.transform(vocab).T)
        negative_prop = np.sum(Negative_Matrix * Negative_VectorCount.transform(vocab).T)
        neutral_prop = np.sum(Neutral_Matrix * Neutral_VectorCount.transform(vocab).T)
        print input_sentence
        print self.clf.predict(np.array([positive_prop, neutral_prop, negative_prop]).reshape(1,-1))
        print positive_prop, negative_prop, neutral_prop
        print "------"
        return positive_prop, negative_prop, neutral_prop

    # ======================================
    def predict_sentences(self, paragraph):
        json_data = []
        sentences = self.NLP.tag_paragraph(paragraph)
        for sentence in sentences:
            sentence_pos, sentence_neg, sentence_neu = self._calculate_matrix(Positive_VectorCount=self.P_vc,
                                                                              Positive_Matrix=self.P_matrix,
                                                                              Negative_VectorCount=self.N_vc,
                                                                              Negative_Matrix=self.N_matrix,
                                                                              Neutral_VectorCount=self.NT_vc,
                                                                              Neutral_Matrix=self.NT_matrix,
                                                                              input_sentence=sentence)
            label = self.clf.predict(np.array([sentence_pos, sentence_neu, sentence_neg]).reshape(1,-1))[0]
            json_data.append({
                'content': sentence,
                'classification': label.lower()
            })

        return json_data