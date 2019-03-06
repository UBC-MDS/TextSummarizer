## test for text_quality

"""

Created on February, 2019



@author: Harjyot Kaur


This script tests the text_quality function of the PySyntext package.



text_quality function of the PySyntext package, checks the
quality of the string in terms of spelling errors and toxicity content.
It takes in a string as input and returns a dataframe.

The function performs necessary cleaning
on the input string.

"""

import pytest
import numpy
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(".."))
from PySyntext.text_quality import text_quality



def test_output_type():

    """
    Test that output is of type DataFrame
    """
    text = "This str has words spelllll wrong. This string has a slag word shitty."
    output = text_quality(text)
    assert(type(output) == type(pd.DataFrame()))


def test_output_types():

    """
    Test if input is not empty
    """

    text = "This str has words spelllll wrong. This string has a slag word shitty."
    output = text_quality(text)
    assert type(output['spell_error'][0]) == type(set())
    assert type(output['count_spell_error'][0]) == numpy.int64
    assert type(output['proportion_spell_error'][0]) == numpy.float64
    assert type(output['toxic_words'][0]) == type(set())
    assert type(output['count_toxic_words'][0]) == numpy.int64
    assert type(output['proportion_toxic_words'][0]) == numpy.float64



def test_verify_input1():

    """
    Test if input string is valid (not numeric)
    """

    text = 100

    with pytest.raises(TypeError) as e:
        text_quality(text)

    assert str(e.value) == "Input must be a string"



def test_verify_input2():

    """
    Test if input is not empty
    """

    text = ""
    output = text_quality(text)

    assert output['spell_error'][0] == set()
    assert output['count_spell_error'][0] == 0
    assert output['proportion_spell_error'][0] == 0.0
    assert output['toxic_words'][0] == set()
    assert output['count_toxic_words'][0] == 0
    assert output['proportion_toxic_words'][0] == 0.0


def test_verify_output1():

    """
    Test if input is not empty
    """
    text = "This str has words spelllll wrong. This string has a slag word shitty."
    output = text_quality(text)
    assert output['count_spell_error'][0] >=0
    assert output['proportion_spell_error'][0] >= 0.0
    assert output['count_toxic_words'][0] >= 0
    assert output['proportion_toxic_words'][0] >= 0.0


def test_verify_output2():

    """
    Test if input is not empty
    """
    text = "This string is correct."
    output = text_quality(text)

    assert output['spell_error'][0] == set()
    assert output['count_spell_error'][0] == 0
    assert output['proportion_spell_error'][0] == 0.0
    assert output['toxic_words'][0] == set()
    assert output['count_toxic_words'][0] == 0
    assert output['proportion_toxic_words'][0] == 0.0


def test_verify_output3():

    """
    Test if input is not empty
    """
    text = "This string is correct and has pronouns Harjyot, Alex, Yenan."
    output = text_quality(text)

    assert output['spell_error'][0] == set()
    assert output['count_spell_error'][0] == 0
    assert output['proportion_spell_error'][0] == 0.0
    assert output['toxic_words'][0] == set()
    assert output['count_toxic_words'][0] == 0
    assert output['proportion_toxic_words'][0] == 0.0

def test_verify_output4():

    """
    Test if input is not empty
    """
    text = "This string has words spelllll wrong. This string has a slag word shitty."
    output = text_quality(text)

    assert output['spell_error'][0] == {'spelllll'}
    assert output['count_spell_error'][0] == 1
    assert ((output['proportion_spell_error'][0]>=0.076923-0.2) and  (output['proportion_spell_error'][0]<=0.076923+0.2))
    assert output['toxic_words'][0] == {'shitty'}
    assert output['count_toxic_words'][0] == 1
    assert ((output['proportion_toxic_words'][0]>=0.076923-0.2) and (output['proportion_toxic_words'][0]<=0.076923+0.2))

def test_verify_output5():

    """
    Test if input is not empty
    """
    text = "this is Jim and Alex writing a package."
    output = text_quality(text)

    assert output['spell_error'][0] == set()
    assert output['count_spell_error'][0] == 0
    assert output['proportion_spell_error'][0] == 0.0
    assert output['toxic_words'][0] == set()
    assert output['count_toxic_words'][0] == 0
    assert output['proportion_toxic_words'][0] == 0.0