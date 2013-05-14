"""
The class defined below is designed to be able to read in text (via either
python strings or filepaths containing text) and then answer questions about
the text that it read in.

The current implementation is missing some functionality and has some
broken functionality. Additionally, some of the code here may be a naive
approach where a better solution is available using some feature of the python
standard lib.

Your task is to make these class work as defined in the docstrings and make the
tests written in tests.py pass. As on the previous assignment you will not need
to change a line of code in tests.py.
"""
import re
from collections import Counter


class WordCounter(object):
    """
    WordCounter examines some input text and allows you to query various
    information about the words that exist in that text.
    """

    def __init__(self):
        """
        Instantiates some data structures that may be useful when processing
        text and later querying for information about the text.

        The data structures provided may or may not be the correct data
        structures for the job. You may or may not need to add/remove/replace
        some of these data structures.
        """
        self._all_words = []
        self._unique_words = set()
        self._word_counts = Counter()

    def read_text_string(self, text_string):
        """
        Reads a text string into the 'memory' of our class. This function can
        be called repeatedly to read multiple text strings into memory for
        querying.
        """
        read_words_list = self.get_word_list(text_string)
        self._all_words.extend(read_words_list)
        self._unique_words.update(read_words_list)
        self._update_word_counts(read_words_list)

    def get_word_list(self, text_string):
        """
        Takes a string of text and outputs a list of alphanumeric words
        contained in that text.
        """
        non_alphanum_pattern = re.compile('\W+')
        read_words_list = non_alphanum_pattern.split(text_string)
        # Store the word in lowercase, and exclude empty strings
        # that the regex gives us
        return [word.lower() for word in read_words_list if word]

    def read_text_file(self, file_path):
        """
        Takes a filepath to a plain text file and adds all of the alphanumeric
        words in that text file into the class's memory.
        """
        for f_line in open(file_path):
            self.read_text_string(f_line)

    def _update_word_counts(self, words_list):
        """
        A helper function that's supposed to help track the number of
        occurrences of words as more text is read into the counter by
        manipulating our internal 'memory' structures.
        """
        self._word_counts.update(Counter(words_list))

    def get_most_frequent_words(self, number_of_words):
        """
        Returns a list of words which are the most frequently used words in the
        text we have read so far. This list is ordered most frequently used word
        first and has a length == number_of_words.

        :param number_of_words: Specifies how many top words to return. For
                    instance if number_of_words == 1. The most frequently used
                    word will be returned. If number_of_words == 10, the top
                    ten words will be returned, ordered by most frequent word
                    first.
        """
        # we get tuples: (word, frequency)
        most_common_words = self._word_counts.most_common(number_of_words)
        return [word[0] for word in most_common_words]

    def get_words_by_count(self, count):
        """
        Returns a list of words which have occurred in the input text the number
        of times specified by count. If you pass in 10 for count, you will get
        all words that occur in the text exactly 10 times.
        """
        count_list = []
        for (word, frequency) in self._word_counts.iteritems():
            if frequency == count:
                count_list.append(word)
        return count_list
        #return [word[0] for word in self._word_counts.items() if word[1] == count]

    def get_unique_words(self):
        """
        Returns a list of all of the unique words that occur in the input text.
        By unique words we mean that this list will contain every word in the
        text with no duplicates.
        """
        return list(self._unique_words)

    def shared_words_in_string(self, comparative_string):
        """
        Returns the list of words which occur in both the input text and the
        text contained in comparative_string. Every word that occurs in both
        the input text and the text in comparative_string should be in this
        list with no duplicates.
        """
        comp_word_list = self.get_word_list(comparative_string)
        # Figure out which new words are shared with already counted words.
        return list(self._unique_words & set(comp_word_list))

    def generate_word_count_strings(self):
        """
        Generates strings which follow a specific format which describes how
        many times a given word has been counted. Will generate strings until
        a string has been generated for every unique word that has been read
        by the WordCounter.

        For example, given the text input:
            'Hank is a man. A man is Frank.'
        This function will generate the following series of strings:
             The word 'hank' has been counted 1 time.
             The word 'is' has been counted 2 times.
             The word 'a' has been counted 2 times.
             The word 'man' has been counted 2 times.
             The word frank has been counted 1 time.

        Try to keep this function efficient. If we have read a very large
        text input it would be silly to store a HUGE list of strings in memory
        , each of which differs from all the others by only a few characters.
        """
        string_format = "The word '%s' has been counted %d time%s."
        for word, count in self._word_counts.items():
            yield string_format % (word, count, 's'[count == 1:])

