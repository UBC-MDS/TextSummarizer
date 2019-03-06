## test for TextGrams

import pytest
import pandas as pd
import os
import sys
import numpy
sys.path.insert(0, os.path.abspath(".."))
from PySyntext.text_grams import text_grams

# sample output
grams = {
    '2gram' : [("sunny", "day")],
    'Number of Instances' : 2,
}
sample_out = pd.DataFrame.from_dict(grams)

# test for functionality
def test_normal_function():
    ex = "Today is a sunny day. We should go to a beach on this sunny day"
    k=1
    n=[2]
    ex_output = text_grams(ex, k, n)
    assert ex_output["2gram"][0] ==  sample_out['2gram'][0]
    assert  len(ex_output['2gram'][0]) == n[0]
    assert  ex_output.shape[0] == sample_out.shape[0]

    n=2
    ex_output = text_grams(ex, k, n)
    ex_output
    assert ex_output["2gram"][0] ==  ("sunny","day")
    assert  ex_output["Number of Instances"][0] == 2
#test_normal_function()

# test datatype inside output dataframe
def test_verify_output():
    ex = "Today is a sunny day. We should go to a beach on this sunny day"
    k=1
    n=[2]
    ex_output = text_grams(ex, k, n)
    assert type(ex_output) == type(sample_out)
    assert type(ex_output['2gram'][0]) == tuple
    assert type(ex_output['Number of Instances'][0]) == numpy.int64
    
#verify_output(x, k, n)

# test sentence endings (?, !, .)
def test_verify_sentence_endings():
    ex = "Wherefore art thou Romeo! Wherefore art thou Romeo. Wherefore art thou Romeo?"
    ex_output = text_grams(ex)
    assert ex_output.shape[0] != 4 # If it split sentences properly, (Romeo, Wherefore) will not be a gram combination
#test_verify_sentence_endings()

# test stop remove
def test_verify_stop_remove():
    ex = "This is a sentence. This is also a sentence. This is also a sentence."
    ex_output = text_grams(ex, stop_remove = False)
    assert ex_output.shape[0] > 1 # If stopwords are removed, only (also, sentence) will be considered
#verify_stop_remove()

# test punctuation
def test_verify_remove_punctuation():
    ex = "This is / a sentence. This is / also a sentence. This is / also a sentence."
    ex_output = text_grams(ex, remove_punctuation = False)
    assert ex_output.shape[0] > 1 # If punctuation is removed, only (also, sentence) will be considered

# test remove number
def test_verify_remove_number():
    ex = "This is 123 a sentence. This is 123 also a sentence. This is 123 also a sentence."
    ex_output = text_grams(ex, remove_number = False)
    assert ex_output.shape[0] > 1 # If numbers is removed, only (also, sentence) will be considered
#verify_remove_number()

# test case sensitive
def test_verify_case_sensitive():
    ex = "Hey Guys. Hey Guys. hey guys. hey guys."
    ex_output = text_grams(ex, case_sensitive = True)
    assert ex_output.shape[0] > 1 # If case_sensitive is true, only (hey, guys) will be considered


# test invalid values of k
def test_verify_k():
    ex = "Wherefore art thou Romeo! Wherefore art thou Romeo. Wherefore art thou Romeo?"
    ex_output1 = text_grams(ex, k = 0)    
    assert ex_output1.shape[0] == 0 # If k is 0, dataframe should be empty

    with pytest.raises(ValueError) as e:
        text_grams(ex, k = -1)
    assert str(e.value) == "k must be 0 or greater"
    
    with pytest.raises(TypeError) as e:
        text_grams(ex, k = "text")
    assert str(e.value) == "k must be integer."

# test invalid values of n
def test_verify_n():
    ex = "Wherefore art thou Romeo! Wherefore art thou Romeo. Wherefore art thou Romeo?"  
    with pytest.raises(TypeError) as e:
        text_grams(ex, n = "text")  
    assert str(e.value) == "n must be an integer list"

    with pytest.raises(ValueError) as e:
        text_grams(ex, n = [-1,-2])
    assert str(e.value) == "Values of n must be greater than 0"
    
    with pytest.raises(ValueError) as e:
        text_grams(ex, n = -1)
    assert str(e.value) == "n must be 0 or greater"
    
    

# test invalid values of n
def test_verify_bool():
    ex = "Wherefore art thou Romeo! Wherefore art thou Romeo. Wherefore art thou Romeo?"  
    with pytest.raises(TypeError) as e:
        text_grams(ex, stop_remove = "text")  
    assert str(e.value) == "stop_remove, remove_punctuation, remove_number and case_sensitive must be boolean"


# test if sentence length is smaller than n
def test_verify_n_larger_than_sentence():
    ex = "short sentence. short sentence."
    ex_output = text_grams(ex, n = [3])
    assert ex_output.shape[0] == 0 # If n is larger than sentence length, dataframe should be empty


# test to verify if function raises for invalid input
def test_verify_input1():
    """
    Test if input string is valid (not numeric)
    """

    text = 100
    
    with pytest.raises(TypeError) as e:
        text_grams(text)
    assert str(e.value) == "Input must be a string"


# test to verify if function raises for invalid input
def test_verify_input2():

    """
    Test if input is not empty
    """

    text = " "

    with pytest.raises(ValueError) as e:
        text_grams(text)
    assert str(e.value) == "Input text is empty."
    

# test to verify if function raises for invalid input
def test_verify_input3():

    """
    Test if input is not empty
    """

    text = " "

    with pytest.raises(ValueError) as e:
        text_grams(text)
    assert str(e.value) == "Input text is empty."