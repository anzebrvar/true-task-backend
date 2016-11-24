# coding=utf-8

import re
import spacy

OPERATOR = 'Operator'

en_nlp = spacy.load('en')


def read_from_file(filename):

    return open(filename).readline()


def preprocess(text):
    udata = text

    # extracting customer name
    customer = re.match('<(?!Operator).*?>', text).group()[1:-1]

    # replace smileys
    udata = re.sub(":.?-?\(", "__smiley_sad__", udata)
    udata = re.sub(":.?-?\)", "__smiley_happy__", udata)

    # lowercase
    text_ascii = udata.encode("ascii", "ignore").lower()

    # spacy parsing
    doc = en_nlp(unicode(text_ascii))

    # lemmatizing
    text_lemmatized = " ".join([token.lemma_ for token in doc])

    print "LEMATIZED", text_lemmatized

    # splitting to separate messages
    messages = re.findall('<.*?>[^<]*', text_lemmatized)
    messages = [x.strip() for x in messages]

    return messages, customer


def algorithm(messages, customer):
    return [
        (0.9, u'Ok __customer_name__, what would be your customer reference number?'),
        (0.6, u'Oh great to hear __customer_name__!'),
    ]


def postprocess(suggestions, customer):
    generated = []

    for i, (probability, msg) in enumerate(suggestions):
        part = u'[suggestion %d, confidence %d%%]<%s> %s' % (i + 1, probability * 100, OPERATOR, msg)
        generated.append(part)

    output_with_placeholder = ' '.join(generated)
    output_with_customer = re.sub("__customer_name__", "%s" % customer, output_with_placeholder)

    return output_with_customer
