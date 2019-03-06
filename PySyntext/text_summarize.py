import pandas as pd
import string
import re
from nltk.tokenize import sent_tokenize
from collections import Counter
from nltk.corpus import stopwords
import pytest



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
        #remove_numeric_words=re.sub(r'\b[0-9]+\b\s*', '',remove_punctuation)
        numeric_const_pattern = r"""
                                [-+]? # optional sign
                                (?:
                                    (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
                                    |
                                    (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
                                )
                                # followed by optional exponent part if desired
                                (?: [Ee] [+-]? \d+ ) ?
                                """
        rx = re.compile(numeric_const_pattern, re.VERBOSE)
        remove_numeric_words = rx.sub('',remove_punctuation)
        remove_punctuation = ' '.join(remove_punctuation.strip().split())

    else:
        remove_numeric_words = remove_punctuation

    clean_text = remove_numeric_words

    return clean_text



def pre_processing(text, case_sensitive = False, stop_remove = False):

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


def text_summarize(text, stop_remove = False, remove_punctuation = True, \
               remove_number = True, case_sensitive = False):

    """
    Returns various summary information of a string.

    This function returns a DataFrame with total word count,
    total sentence count, most common and least common word, average
    word length, and average sentence length. Each information resides
    in a separate column.



    Parameters
    ----------

    text : String
        The string to be analyzed.

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

        word_count : Int
            The total number of words in `text`.

        sentence_count : Int
            the total number of sentences in `text`.

        most_common : List of String

            A list of the most common words in `text`. If this returns a
            list of length 1, there is only one most common word. If this
            returns a list of length > 1, there are multiple words that appear
            the most number of times in `text`.

        least_common : List of String

            A list of the least common words in `text`. If this returns a
            list of length 1, there is only one least common word. If this
            returns a list of length > 1, there are multiple words that appear
            the least number of times in `text`.

        avg_word_len : float
            The average word length in `text`.

        avg_sentence_len : float
            The average number of words in a sentence, in `text`.

    Examples
    --------
    >>> ex_passage = "This is the first sentence in this paragraph. \
                      This is the second sentence. This is the third."
    >>> PySyntext.text_summarize(ex_passage)

    # Example output, generate a dict then turn it into the output DataFrame

    answer = {
        'word_count' : 17,
        'sentence_count' : 3,
        'most_common' : [['This']],
        'least_common' : [['first', 'in', 'second', 'third']],
        'avg_word_len' : 4.35,
        'avg_sentence_len' : 5.67
    }
    pd.DataFrame.from_dict(answer)
    """
     # Check all variables are valid:

    # Check if text is a string
    if type(text) != str:
        raise TypeError("Input must be a string")

    # Check for boolean agruments
    if type(stop_remove)!= bool or type(remove_punctuation)!=bool or\
               type(remove_number)!= bool or type(case_sensitive)!= bool:
        raise TypeError("stop_remove, remove_punctuation, remove_number and case_sensitive must be boolean")



    # Clean and pre-process text

    clean_text = clean(text, remove_punctuation, remove_number)
    processed_text = pre_processing(clean_text, case_sensitive, stop_remove)

    text_summary = {'word_count':0,
                'sentence_count': 0,
                'most_common': [[]],
                'least_common': [[]],
                'avg_word_len': 0.0,
                'avg_sentence_len': 0.0}

    # count number of sentences

    if case_sensitive:
        pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    else:
         pat = re.compile(r'([a-z][^\.!?]*[\.!?])', re.M)
    sentences=pat.findall(processed_text)
    text_summary['sentence_count'] = len(sentences)

     # average sentence length
    if len(sentences)==0:
        text_summary['avg_sentence_len']=0.0
    else:
        text_summary['avg_sentence_len']=sum(map(len, sentences))/float(len(sentences))

    # remove sentence ending punctuations
    processed_text=re.sub(r'[\.!?]', '', processed_text)

    # split text
    split_text=processed_text.split()

    if len(split_text)!=0:

        # word count
        text_summary['word_count'] = len(split_text)
        # most common and least words
        counter=Counter(split_text)
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        text_summary['most_common']=[list(df['index'][df[0]==max(df[0])])]
        text_summary['least_common']=[list(df['index'][df[0]==min(df[0])])]

        # average word length
        text_summary['avg_word_len']= sum(map(len, split_text))/float(len(split_text))

    # return list

    return pd.DataFrame(text_summary)
