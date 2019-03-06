## function text_quality



"""
Created on 09 February, 2019
@author: Harjyot Kaur
Implementation of text_quality function in the PySyntext package.
"""



# load packages

import os
import pandas as pd
import re
import string
import nltk.tag
from nltk import pos_tag
from PySyntext.eng_words import eng_words
from PySyntext.profane_words import profane_words




def clean(text):
    """
    Remove tickers, special characters, links and numerical strings

    Parameters

    text : str

       User given input

    Returns
    -------
    str

        cleaned text

    Examples

    --------

    >>>text="RT $USD @Amila #Test\nTom\'s newly listed Co. &amp; Mary\'s unlisted Group to supply tech for
    nlTK.\nh.. $TSLA $AAPL https://  t.co/x34afsfQsh'"
    
    >>> clean(text)

    'RT   Amila  TestTom s newly listed Co   amp  Mary s unlisted Group to supply tech for  nlTK h    '
    """

    # remove tickers
    remove_tickers=re.sub(r'\$\w*','',text)

    # remove new line symbol
    remove_newline=re.sub(r'\n','',remove_tickers)

    # remove links
    remove_links=re.sub(r'https?:\/\/.*\/\w*','',remove_newline)

    # remove special characters
    remove_punctuation=re.sub(r'['+string.punctuation+']+', ' ', remove_links)

    # remove numerical strings
    remove_numeric_words=re.sub(r'\b[0-9]+\b\s*', '',remove_punctuation)

    clean_text=remove_numeric_words

    return clean_text


def spell_check(word_list,text):
    """
    Check words spelt wrong (only for english)


    Parameters
    ----------

    word_list: set
    
        set of words in english dictionary

    text : str

       output string from function clean

    Returns
    -------
    
    set
        list of words spelt wrong

    int
        count of words spelt wrong

    float

        proportion of words spelt wrong in the entire text

    Examples
    --------

    >>> text="I thikn you should go for clas todat"
    >>> spell_check(eng_words,text)

    {'spell_error': [{'clas', 'thikn', 'todat'}],
     'count_spell_error': 3,
     'proportion_spell_error': 0.375}

    """
    
    spell_error_dict={'spell_error': [set()],
                          'count_spell_error': 0,
                          'proportion_spell_error':0.0}

    # get mispelt words
    non_eng_words=list(set(text.split()).difference(word_list))

    if len(non_eng_words)!=0:

        # remove proper-nouns and prepositions
        tagged_sentence = nltk.tag.pos_tag(non_eng_words)

        tagged_non_nouns=list(filter(lambda tagged_sentence: tagged_sentence[1] != 'NNP' and
                                tagged_sentence[1] != 'NNPS' and
                                tagged_sentence[1] != 'PRP', tagged_sentence))

        if len(tagged_non_nouns)!=0:
            removed_nouns=list(next(zip(*tagged_non_nouns)))

            # spelling errors
            spell_error=set(map(str.lower,removed_nouns)).difference(word_list)


            if len(spell_error)!=0:
                #remove wrong words

                pattern = re.compile(r'\b(' + r'|'.join(spell_error) + r')\b\s*')
                text_spell_error = (pattern.sub('', text)).split()
                count_spell_error= len(text.split())-len(text_spell_error)

                return {'spell_error': [spell_error],
                        'count_spell_error': count_spell_error,
                        'proportion_spell_error':count_spell_error/len(text.split())}
            else:
                return spell_error_dict
            
        else:

            return spell_error_dict

    else:

        return spell_error_dict



def toxicity_check(word_list,text):
    """

    Check words that are profane

    Parameters
    ----------

    word_list: set

        set of words in english dictionary

    text : str

       output string from function pre-processing

    Returns
    -------
    set
        list of words that are profane

    int
         count of words that are profane

    float

         proportion of words that are profane in the entire text
      
    Examples
    --------
    >>> text="this is so shitty"
    >>> toxicity_check(toxic_words,text)

    {'toxic_words': [{'shitty'}],
     'count_toxic_words': 1,
     'proportion_toxic_words': 0.25}

    """

    toxic_content= {'toxic_words': [set()],
                    'count_toxic_words': 0,
                    'proportion_toxic_words': 0.0}



    if len(text.split())!=0:
        toxic_words=set(text.split()).intersection(word_list)

        if len(toxic_words)!=0:
            #remove toxic words
            pattern = re.compile(r'\b(' + r'|'.join(toxic_words) + r')\b\s*')
            text_toxic_words = (pattern.sub('', text)).split()
            count_toxic_words = len(text.split())-len(text_toxic_words)


            return {'toxic_words': [toxic_words],
                    'count_toxic_words': count_toxic_words,
                    'proportion_toxic_words':count_toxic_words/len(text.split())}

        else:
            return toxic_content

    else:
        return toxic_content



def text_quality(text):

    """
    Check quality of the string in terms of
    spelling errors and toxicity content.


    The function performs necessary cleaning
    on the input string.

    Comparison is done with pre-existing list of
    exhaustive english words to calculate the spelling errors in the string.
    Comparison is done with pre-existing list of
    exhaustive toxic-english words to calculate the toxicity in the string.


    Parameters
    ----------
    text : str

        input string to be analyzed
        given by the user

    Returns
    -------
    dataframe
        First column contains proportion of spelling errors
        in the input contains and the second column stores
        toxicity in the the input string.

    Examples
    --------
    >>> text = "This str has words spelllll wrong.
    This string has a slag word shitty."
    >>> PySyntext.text_quality(text)

    # Example output, generate a dict then turn it into the output DataFrame
    quality = {
    'spell_error': [{'spelllll'}],
    'count_spell_error': 1,
    'proportion_spell_error': 0.07692307692307693,
    'toxic_words': [{'shitty'}],
    'count_toxic_words': 1,
    'proportion_toxic_words': 0.07692307692307693}

    pd.DataFrame.from_dict(quality)
    """
    # Check if text is a string
    
    if type(text) != str:
        raise TypeError("Input must be a string")
        
    # cleaning and calling spell_check,toxicity_check
    cleaned_text=clean(text)
    spelling_errors=spell_check(eng_words,cleaned_text)
    toxic_words=toxicity_check(profane_words,cleaned_text)

    # compiling outputs
    quality = pd.DataFrame(dict(**spelling_errors,**toxic_words))

    return quality

