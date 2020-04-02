# Import all the dependencies
import pandas as pd
import numpy as np
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator

from sklearn.pipeline import make_pipeline

import argparse

# Log starting time
from datetime import datetime
t1 = datetime.now()

# Define something to allow simple t/f args such as "-train"
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Parser of args ;D
parser = argparse.ArgumentParser(description='Add training/loading fuctionality')
parser.add_argument("-train", type=str2bool, nargs='?', const=True, default=False,
                        help="Train (will otherwise load)")
parser.add_argument("-path", type=str, default="bot\learning\data\pipe.p",
                        help="training output path")
parser.add_argument("-input", type=str, default="bot/learning/data/input.txt",
                        help="training output path")
parser.add_argument("-size", type=int, default=350,
                        help="size for the training compression") 
parser.add_argument("-tftrain", type=str2bool, nargs='?', const=True, default=False, help='train using a tensorflow backend!')

parser.add_argument('-test', type=str2bool, nargs='?', const=True, default=False, help='none..')


parser.add_argument("-markov", type=str2bool, nargs='?', const = True, default= False, help='soijsddfagoijafgdf')
args = parser.parse_args()

# Nou, matplotlib
import warnings
warnings.filterwarnings("ignore")

if args.train == True:
    # Read file

    
    lines = [line.rstrip('\n').replace('\\n',' ').replace('>','') for line in open(args.input)]

    subtitles = pd.DataFrame(columns=['context', 'reply'])
    subtitles['context'] = lines
    subtitles['context'] = subtitles['context'].apply(lambda x: x.lower())
    subtitles['reply'] = lines[1:] + ['...']
    subtitles['reply'] = subtitles['reply'].apply(lambda x: x.lower())

    for sign in ['!', '?', ',', '.', ':']:
        subtitles['context'] = subtitles['context'].apply(lambda x: x.replace(sign, f' {sign}'))
        subtitles['reply'] = subtitles['reply'].apply(lambda x: x.replace(sign, f' {sign}'))

    subtitles.info()

    vectorizer = TfidfVectorizer()
    vectorizer.fit(subtitles.context)

    #vectorizer = model? possibly


    matrix_big = vectorizer.transform(subtitles.context)

    matrix_big.shape

    # Depending on the size of your data, you want ARPACK 
    # to at least keep around 50% or more of your data
    svd = TruncatedSVD(n_components=args.size, algorithm='arpack')
    svd.fit(matrix_big)

    matrix_small = svd.transform(matrix_big)

    # Print new dimensionality and explained variance ratio
    print(matrix_small.shape)
    print(svd.explained_variance_ratio_.sum())


def softmax(x):
    proba = np.exp(-x)
    return proba/sum(proba)

# Choosing one of the k nearest neighbors with BallTree algorithm

from bot.learning.sampler.sampler import NeSampler, ns

if args.train == True:
    ns.fit(matrix_small, subtitles.reply)

    #put a fit thing for epochs and all that cause this kinda fucking sucks at training
    
    # Vectorize, SVD and then chose an answer
    pipe = make_pipeline(vectorizer, svd, ns)

    #save the pipe variable for the sake of faster loading
    with open(args.path, 'wb') as pickle_file:
        pickle.dump(pipe, pickle_file, protocol=4)
else:
    with open(args.path, 'rb') as fp:
        pipe = pickle.load(fp)

#undo the vectorization from ealier
def fixpunctuation(sentence):
    sentence=sentence.replace(' !', "!")
    sentence=sentence.replace(' ?', "?")
    sentence=sentence.replace(' ,', ",")
    sentence=sentence.replace(' .', ".")
    sentence=sentence.replace(' :', ":")

    return sentence
