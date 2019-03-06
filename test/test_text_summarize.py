## test for text_summarize

import pytest
import pandas as pd
import os
import sys
import numpy
sys.path.insert(0, os.path.abspath(".."))
from PySyntext.text_summarize import text_summarize

#ex_passage = "This is the first sentence in this paragraph. This is the second sentence. This is the third."

ex = {
    'word_count' : 17,
    'sentence_count' : 3,
    'most_common' : [['This']],
    'least_common' : [['first', 'in', 'paragraph', 'second', 'third']],
    'avg_word_len' : 4.35,
    'avg_sentence_len' : 5.67
}
ex = pd.DataFrame.from_dict(ex)

def test_normal_function():
    ex_passage = "This is the first sentence in this paragraph. This is the second sentence. This is the third."
    ex_output = text_summarize(ex_passage, stop_remove = False)
    assert ex_output.word_count[0] == 17
    assert ex_output.sentence_count[0] == 3
    assert ex_output.most_common[0] == ["this"]
    assert set(ex_output.least_common[0]) == set(["first", "in", "paragraph", "second", "third"])
    assert round(ex_output.avg_word_len[0], 2) == 4.35
    assert round(ex_output.avg_sentence_len[0], 2) > 29 and round(ex_output.avg_sentence_len[0], 2) < 32

def test_branches():
    ex_passage = "This is the first sentence in this paragraph. This is the second sentence. This is the third."
    ex_output = text_summarize(ex_passage, stop_remove = True, \
                               remove_punctuation = False, remove_number = False, case_sensitive = True)
    assert ex_output.word_count[0] == 9
    assert ex_output.sentence_count[0] == 3
    assert ex_output.most_common[0] == ["This"]
    assert set(ex_output.least_common[0]) == set(["first","paragraph", "second", "third"])
    assert (ex_output.avg_word_len[0] >=5.888889-0.2 and ex_output.avg_word_len[0] <=5.888889+0.2)
    assert round(ex_output.avg_sentence_len[0], 2) > 20 and round(ex_output.avg_sentence_len[0], 2) < 22


def test_verify_output():
    ex_passage = "This is the first sentence in this paragraph. This is the second sentence. This is the third."
    ex_output = text_summarize(ex_passage)
    assert type(ex_output) == type(pd.DataFrame())
    assert type(ex_output.word_count[0]) == numpy.int64 and ex_output.word_count[0] >= 0
    assert type(ex_output.sentence_count[0]) == numpy.int64 and ex_output.word_count[0] >= 0
    assert type(ex_output.most_common[0]) == list and all(isinstance(n, str) for n in ex_output.most_common[0])
    assert type(ex_output.least_common[0]) == list and all(isinstance(n, str) for n in ex_output.least_common[0])
    assert type(ex_output.avg_word_len[0]) == numpy.float64 and ex_output.avg_word_len[0] >= 0
    assert type(ex_output.avg_sentence_len[0]) == numpy.float64 and ex_output.avg_sentence_len[0] >= 0

def test_verfiy_output2():
    ex_passage = ""
    ex_output = text_summarize(ex_passage, stop_remove = True, \
                               remove_punctuation = False, remove_number = False, case_sensitive = True)
    assert ex_output.word_count[0] == 0
    assert ex_output.sentence_count[0] == 0
    assert ex_output.most_common[0] == []
    assert set(ex_output.least_common[0]) == set([])
    assert ex_output.avg_word_len[0] == 0.0
    assert ex_output.avg_sentence_len[0] == 0.0


def test_verify_input():
    # Test if input is string
    test = 100
    with pytest.raises(TypeError) as e:
        text_summarize(test)
    assert str(e.value) == "Input must be a string"
    
def test_verify_input2():
    # Test if parameters are boolean
    ex_passage = "This is the first sentence in this paragraph. This is the second sentence. This is the third."
    with pytest.raises(TypeError) as e:
        text_summarize(ex_passage, 13)
    assert str(e.value) == "stop_remove, remove_punctuation, remove_number and case_sensitive must be boolean"
    
def test_all_stop_words():
    # Test if text is empty after stopword removal
    ex_passage = "this i in so"
    assert text_summarize(ex_passage, stop_remove = True).word_count[0] == 0 

def test_word_count():
    # Test if special characters counts as words
    test = "this + that"
    assert text_summarize(test).word_count[0] == 2
    # Test if punctuation counts as words
    test = "this , that, and ; the other thing!"
    assert text_summarize(test).word_count[0] == 6
    # Test if hyphens count as one or two words
    test = "compound-word"
    assert text_summarize(test).word_count[0] == 1
    # Test if numbers count as words
    test = "60 and 9 people in MDS"
    assert text_summarize(test).word_count[0] == 4

def test_sentence_count():

    # Test multiple periods "sentence..."
    test = "This is a sentence... This is sentence two. "
    assert text_summarize(test).sentence_count[0] == 2
    # Test if punctuation properly ends a sentence
    test = "Loudly! Question? Sentence three."
    assert text_summarize(test).sentence_count[0] == 3

def test_most_common():
    # Test multiple most common words (same case as no most common word)
    test = "most most common common common"
    assert set(text_summarize(test).most_common[0]) == set(["common"])
    # Check if punctuation/special characters count
    test = "most most most common!!!!! + + + + + "
    assert text_summarize(test).most_common[0] == ['most']
    # Test if numbers count as words
    test = "10 10 10 people people"
    assert text_summarize(test).most_common[0] == ['people']

def test_least_common():
    # Test multiple least common words
    test = "No repeating words"
    assert set(text_summarize(test).least_common[0]) == set(["no", "repeating", "words"])
    # Test multiple least common words
    test = "repeating repeating words words"
    assert set(text_summarize(test).least_common[0]) == set(["repeating", "words"])
    # Check if punctuation/special characters count
    test = "most most most common! +"
    assert text_summarize(test).least_common[0] == ['common']
    # Test if numbers count as words
    test = "10 people"
    assert text_summarize(test).least_common[0] == ['people']

def test_avg_word_len():
    # Test if punctuation/special characters count
    test = "this + that!"
    assert text_summarize(test).avg_word_len[0] == 4
    # Test if numbers count as words
    test = "10 people"
    assert text_summarize(test).avg_word_len[0] == 6

def test_avg_sentence_len():
    # Test if punctuation/special characters count
    test = "this + that! this and that? this and sometimes that."
    assert text_summarize(test).avg_sentence_len[0] >= 15.5 and text_summarize(test).avg_sentence_len[0] <= 17.5