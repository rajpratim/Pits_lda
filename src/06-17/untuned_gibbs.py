from __future__ import print_function, division

__author__ = 'amrit'

import sys
from demos import atom
from demos import cmd
import lda
import os, pickle
from random import random, shuffle, seed
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import copy
import time


def calculate(topics=[], lis=[], count1=0):
    count = 0
    for i in topics:
        if i in lis:
            count += 1
    if count >= count1:
        return count
    else:
        return 0


def recursion(topic=[], index=0, count1=0):
    count = 0
    global data
    # print(data)
    # print(topics)
    d = copy.deepcopy(data)
    d.pop(index)
    for l, m in enumerate(d):
        # print(m)
        for x, y in enumerate(m):
            if calculate(topics=topic, lis=y, count1=count1) != 0:
                count += 1
                break
                # data[index+l+1].pop(x)
    return count


data = []


def jaccard(a=0, score_topics=[], term=0):
    labels = []  # ,6,7,8,9]
    labels.append(term)
    global data
    l = []
    data = []
    file_data = {}
    for doc in score_topics:
        l.append(doc.split())
    for i in range(0, len(l), a):
        l1 = []
        for j in range(a):
            l1.append(l[i + j])
        data.append(l1)
    dic = {}
    for x in labels:
        j_score = []
        for i, j in enumerate(data):
            for l, m in enumerate(j):
                sum = recursion(topic=m, index=i, count1=x)
                if sum != 0:
                    j_score.append(sum / float(9))
                '''for m,n in enumerate(l):
                    if n in j[]'''
        dic[x] = j_score
        if len(dic[x]) == 0:
            dic[x] = [0]
    file_data['citemap'] = dic


# print(file_data)
    X = range(len(labels))
    Y_median = []
    Y_iqr = []
    for feature in labels:
        Y = file_data['citemap'][feature]
        Y=sorted(Y)
        return Y[int(len(Y)/2)]


def get_top_words(model, path1, feature_names, n_top_words, i=0, file1=''):
    topics = []
    fo = open(path1,'a+')
    fo.write("Run: " + str(i) + "\n")
    for topic_idx, topic in enumerate(model.components_):
        str1 = ''
        fo.write("Topic " + str(topic_idx) + ": ")
        for j in topic.argsort()[:-n_top_words - 1:-1]:
            str1 += feature_names[j] + " "
            fo.write(feature_names[j] + " ")
        topics.append(str1)
        fo.write("\n")
    fo.close()
    return topics


def token_freqs(doc):
    return Counter(doc)


def tf(corpus):
    mat = [token_freqs(doc) for doc in corpus]
    return mat


def make_feature(corpus, n_features=1000):
    label = list(zip(*corpus)[0])
    mat = tf(corpus)
    # matt = hash(mat)
    return mat


def readfile1(filename=''):
    dict = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                row = doc.lower().strip()
                dict.append(row)
            except:
                pass
    return dict


def _test_LDA(l, path1, file=''):
    n_topics = 10
    n_top_words = 10

    fileB = []
    fileB.append(file)

    filepath = '/home/amrit/GITHUB/Pits_lda/dataset/'
    topics=[]
    for j, file1 in enumerate(fileB):
        for i in range(10):
            data_samples = readfile1(filepath + str(file1))

            # shuffling the list
            shuffle(data_samples)

            tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            tf = tf_vectorizer.fit_transform(data_samples)

            lda1 = lda.LDA(n_topics=int(l[0]), alpha=0.1, eta=0.01,n_iter=10)

            lda1.fit_transform(tf)

            # print("done in %0.3fs." % (time() - t0))
            tf_feature_names = tf_vectorizer.get_feature_names()
            topics.extend(get_top_words(lda1, path1, tf_feature_names, n_top_words, i=i, file1=file1))
    return topics


def cmd(com="demo('-h')"):
    "Convert command line to a function call."
    if len(sys.argv) < 2: return com

    def strp(x): return isinstance(x, basestring)

    def wrap(x): return "'%s'" % x if strp(x) else str(x)

    words = map(wrap, map(atom, sys.argv[2:]))
    return sys.argv[1] + '(' + ','.join(words) + ')'

def _test(res=''):
    # 1st r
    seed(1)
    #fileB = ['pitsA', 'pitsB', 'pitsC', 'pitsD', 'pitsE', 'pitsF', 'processed_citemap']
    fileB=[]
    start_time1 = time.time()
    fileB.append(res)
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    l = [10.0]

    result = {}
    for file1 in fileB:
        file_result = {}
        for terms in labels:
            median1=[]
            base = '/home/amrit/GITHUB/Pits_lda/results/06-17/'
            path = os.path.join(base,'untuned_gibbs', res, str(terms))
            if not os.path.exists(path):
                os.makedirs(path)

            for i in range(10):
                start_time = time.time()
                path1 = path + "/run_" + str(i) + ".txt"
                with open(path1, "w") as f:
                    f.truncate()
                topics = _test_LDA(l, path1, file=file1)
                top=[]
                for i in topics:
                    temp=str(i.encode('ascii','ignore'))
                    top.append(temp)
                # 2nd method
                # another_method()
                a = jaccard(a=int(l[0]), score_topics=top, term=terms)
                fo = open(path1, 'a+')
                fo.write("\nRuntime: --- %s seconds ---\n" % (time.time() - start_time))
                fo.write("\nScore: " + str(a))
                fo.close()
                median1.append(a)
            file_result[terms] = median1
        result[file1] = file_result
    print(result)
    with open('dump/gibbs_untuned_'+res+'.pickle', 'wb') as handle:
        pickle.dump(result, handle)
    print("\nTotal Runtime: --- %s seconds ---\n" % (time.time() - start_time1))

if __name__ == '__main__':
    eval(cmd())