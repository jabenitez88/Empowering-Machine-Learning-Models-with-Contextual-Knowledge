from spacy.lang.en.stop_words import STOP_WORDS
import gensim, spacy, re
from nltk.util import ngrams
from collections import Counter

# Download en-core-web-sm via terminal: python -m spacy dowload en_core_web_sm

def pos_tagging(data):
    # Remove Emails
    data = [re.sub('\S*@\S*\s?', ' ', sent) for sent in data]

    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", " ", sent) for sent in data]

    return data


def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def lemmatization(texts, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    # Remove stop words
    stop_words = set([w.lower() for w in list(STOP_WORDS)])
    nlp.Defaults.stop_words |= {" f ", " s ", " etc"}
    # Lemmatize each word
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append(" ".join([token.lemma_
                                   if (token.lemma_ not in ['-PRON-']) & (token.lemma_ not in stop_words)
                                   else '' for token in doc if token.pos_ in allowed_postags]))
    return texts_out


def preprocess_data(df, col):
    # Convert to list
    data = df[col].values.tolist()

    # POS Tagging: replace numbers, dots, colons, email, new lines, single quotes with a tag
    data = pos_tagging(data)

    data_words = list(sent_to_words(data))

    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    # Remove stop words and do lemmatization (keeping only Noun, Adj, Verb, Adverb)
    data_lemmatized = lemmatization(data_words, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    return data_lemmatized


def get_tokenized_text(df, col):
    # Convert to list
    data = df[col].values.tolist()

    # Tokenization of string
    data = [sub.split() for sub in data]

    return data


def get_embeddings(words, verbose=False):
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    vectors = dict()
    for term in words:
        token = nlp(term)
        vectors[term] = token.vector
        if verbose:
            print(token.text, token.has_vector, token.vector_norm)
    return vectors
