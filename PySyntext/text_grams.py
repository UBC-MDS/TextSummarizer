## function TextGrams

"""

Created on 09 February, 2019


@author: Alex Pak
         Harjyot Kaur


Implementation of text_grams function

"""

# load packages
import pandas as pd
import string
import re
from nltk.corpus import stopwords
import collections as collect
import pytest
#nltk.download("stopwords")
#nltk.download('averaged_perceptron_tagger')


def clean(text, remove_punctuation = True, remove_number = True):
    """
    Remove tickers, special characters, links and numerical strings

    Parameters
    ----------
    text : str
        User given input
    remove_punctuation : Boolean
        Check if user would like to remove punctuation
    remove_number : Boolean
        Check if user would like to remove numerical strings

    Returns
    -------
    str
        cleaned text

    Examples
    --------
    >>> text="RT $USD @Amila #Test\nTom\'s newly listed Co. &amp; Mary\'s unlisted Group to supply tech for nlTK.\nh.. $TSLA $AAPL https://  t.co/x34afsfQsh'"
    >>> clean(text)

    'RT   Amila  TestTom s newly listed Co   amp  Mary s unlisted Group to supply tech for nlTK h'
    """

    # Need to keep periods, question marks, and exclamation marks for sentence endings
    punct_wo_endings = string.punctuation.replace('.', '').replace('!', '').replace('?', '')

    # Remove tickers, new lines, and webpage links from text
    remove_tickers=re.sub(r'\$\w*','',text)
    remove_newline=re.sub(r'\n','',remove_tickers)
    remove_links=re.sub(r'https?:\/\/.*\/\w*','',remove_newline)

    # Check if user wants to remove punctuation
    if remove_punctuation:
        remove_punctuation=remove_links.translate({ord(char): None for char in punct_wo_endings})
    else:
        remove_punctuation = remove_links

    # Check if user wants to remove numerical strings
    if remove_number:
        remove_numeric_words=re.sub(r'\b[0-9]+\b\s*', '',remove_punctuation)
    else:
        remove_numeric_words = remove_punctuation

    clean_text = remove_numeric_words

    return clean_text

def pre_processing(text, case_sensitive = False, stop_remove = True):
    """
    Checks if user wants to make all strings lower case, and if user wants to remove
    stop words

    Parameters
    ----------
    text : str
        User given input
    case_sensitive : Boolean
        Check if user would like to treat Upper and lower case separately
    stop_remove : Boolean
        Check if user would like to remove stop words

    Returns
    -------
    str
        cleaned text

    Examples
    --------
    >>> text="This is an example sentence."
    >>> pre_processing(text)

    "example sentence."
    """

    # If text is case_sensitive, do NOT change everything to lower case
    if not case_sensitive:
        text = text.lower()
    # Remove stop words if conditional is true
    if stop_remove:
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        text = pattern.sub('', text)

    return text


def text_grams(text, k = 5, n = [2, 3], stop_remove = True, remove_punctuation = True, \
               remove_number = True, case_sensitive = False):

    """
    Returns top k ngrams of the text

    Parameters
    ----------
    text : String
        The string to be analyzed.

    k : int
        top ngrams reguired

    n:  list
        number of combination of words with highest frequency

    stop_remove : Boolean
        Remove common stop words (ex. 'and', 'the', 'him') from `text`.

    remove_punctuation : Boolean
        If True, strip `text` of punctuation.

    remove_number : Boolean
        If True, strip `text` of numbers.

    case_sensitive : Boolean
        If True, text_summarize will be case sensitive (ex. "this" and
        "This" will be two separate words).

    Returns
    -------
    DataFrame
        ngram: top k combination of n words
        frequency: frequenct of the occurrence of ngram in text

    Examples
    --------
    >>> text = "It is a sunny day outside. We should go to a beach on this sunny day."
    >>> text_grams(text, 1, [2])

    # Example output, generate a dict then turn it into the output DataFrame
    grams = {
        '2gram' : (sunny, day),
        'Number of instances' : 2,
    }
    pd.DataFrame.from_dict(grams)
    """

    # Check all variables are valid:

    # Check if text is a string
    if type(text) != str:
        raise TypeError("Input must be a string")
        
    # Check text is not empty
    if not text.split():
        raise ValueError("Input text is empty.")
        
    # Check for type of k
    if type(k)!=int and type(k)!='numpy.int64':
        raise TypeError("k must be integer.")
        
     # Check k >= 0
    if k < 0:
        raise ValueError("k must be 0 or greater")
    
    # Check for n
    if type(n)!=int and type(n)!='numpy.int64' and type(n)!=list:
        raise TypeError("n must be an integer list")
            
    if type(n)==list:
        if any(i < 0 for i in n):
             raise ValueError("Values of n must be greater than 0")
                
    # Check for boolean agruments
    if type(stop_remove)!= bool or type(remove_punctuation)!=bool or\
               type(remove_number)!= bool or type(case_sensitive)!= bool:
        raise TypeError("stop_remove, remove_punctuation, remove_number and case_sensitive must be boolean")
    
    
    
    ngrams_list = []
    ngrams_dfs = []
    
    try:
        # Initialize variables
       
        lbls = [str(num_grams) + "gram" for num_grams in n]  # Make labels for every n grams user wants
        pass
        
    except TypeError:
        if n>0:
            n=[n]
            # Initialize variables
            lbls = [str(num_grams) + "gram" for num_grams in n]  # Make labels for every n grams user wants
        else:
            raise ValueError("n must be 0 or greater")
                    
    # Clean and pre-process text
    clean_text = clean(text, remove_punctuation, remove_number)
    clean_text = pre_processing(clean_text, case_sensitive, stop_remove)

    # Split input text on sentence endings (ie. . or ? or !)
    split_sentences = list(filter(None, re.split("[,.!?:]+", clean_text)))
    #print(split_sentences)

    # Function must find most frequent gram for every ngram in n
    for num_grams in n:
        ngrams = collect.Counter()

        # Need to find grams for every sentence individually (because grams shouldn't take into account two words that
        # are beside each other, but in two different sentences)
        for sentence in split_sentences:
            #print(sentence)
            split_words = sentence.split()
            #print(split_words)
            list_of_grams = [split_words[i:i + num_grams] for i in range(len(split_words) - num_grams + 1)]  # General way to split a sentence into n grams
            #print(list_of_grams)

            # Update the counter +1 for every instance of a gram
            ngrams.update([tuple(item) for item in list_of_grams])

        # Append the k most common grams
        ngrams_list.append(ngrams.most_common(k))

    # Create the final dataframe
    for list_of_top_grams in ngrams_list:
        ngrams_dfs.append(pd.DataFrame.from_records([list(i) for i in list_of_top_grams], columns = [lbls[0], "Number of Instances"]))
        lbls.pop(0)

    if len(n) == 1:
        final_df = ngrams_dfs[0]
    else:
        for i in range(len(ngrams_dfs)-1):
            final_df = pd.concat([ngrams_dfs[0].reset_index(drop = True), ngrams_dfs[i+1]], axis = 1)


    return final_df