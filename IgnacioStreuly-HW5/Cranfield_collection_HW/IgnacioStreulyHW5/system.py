import nltk, string, re, math
from nltk import word_tokenize
from nltk.stem.porter import *

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]

def main():
    try:
        queries = open("cran.qry", "r")
        abstracts = open("cran.all.1400")
        queryLines = queries.read()

        removeStopWordsQueries = strip_queries_from_file(queryLines, closed_class_stop_words)
        QueryVector = createQueryVector(removeStopWordsQueries)

        removeStopWordsAbstracts = strip_abstracts_from_file(abstracts, closed_class_stop_words)
        AbstractVector = createAbstractVector(removeStopWordsAbstracts, removeStopWordsQueries)

        output = []

        for i, Query in enumerate(QueryVector):
            output.append([])
            for k, Abstract in enumerate(AbstractVector[i]):
                cosineSimilarities = cosineSimilarity(Query, Abstract)
                if cosineSimilarities != 0:
                    output[-1].append([i, k, cosineSimilarities])

        outputSortedBySimilarity = []

        for sequence in output:
            sequence.sort(key=lambda x: x[2])
            sequence.reverse()
            outputSortedBySimilarity.append(sequence)

        outputFile = open('final_output.txt','w')

        for st in outputSortedBySimilarity:
            for sort in st:
                sortOne = sort[0] + 1
                sortTwo = sort[1] + 1
                sortThree = sort[2]
                line = str(sortOne) + ' ' + str(sortTwo) + ' '  + str(sortThree)
                outputFile.write(line + '\n')

    except IOError:
        print "One or more files not found."

    except Exception, e:
        print str(e)


def cosineSimilarity(query, abstract):
    ab, qM, aM = 0,0,0

    for i in range(len(query)):
        if abstract[i] is None:
            continue
        else:
            ab += (query[i] * abstract[i])
            qM += query[i] ** 2
            aM += abstract[i] ** 2


    qM = qM ** 0.5
    aM = aM ** 0.5

    if not (qM * aM == 0):
        cosineSimilarity = math.floor(ab / (qM * aM) * 1000) / 1000
    else:
        cosineSimilarity = 0

    return cosineSimilarity

def createQueryVector(removeStopWordsQueries):
    #count table
    wordFreq = {}
    totalQueries = 225
    queryTFIDF = []
    featureVectorQuery = []

    for query in removeStopWordsQueries:
        for term in query:
            term = term.lower()

            if term in wordFreq:
                wordFreq[term] += 1
            else:
                wordFreq[term] = 1

    # TFIDF Scores
    for query in removeStopWordsQueries:
        queryTFIDF.append({})
        wordChecked = []

        for term in query:
            term = term.lower()

            if term in wordChecked:
                queryTFIDF[-1][term] += 1
            else:
                wordChecked.append(term)
                queryTFIDF[-1][term] = 1

            # term freq
            termFrequency = float(queryTFIDF[-1][term])/float(len(query))

            # Inverse Doc Frequency: number of documents / number of documents containing the term
            IDF = math.floor(math.log(float(totalQueries) / float(wordFreq[term])) * 1000) / 1000

            # Full TFIDF (term freq) * (Inverse Doc Freq)
            queryTFIDF[-1][term] = math.floor(termFrequency * IDF * 1000) / 1000


    for i, query in enumerate(removeStopWordsQueries):
        featureVectorQuery.append([])

        for term in query:
            if term in queryTFIDF[i]:
                featureVectorQuery[-1].append(queryTFIDF[i].get(term))

    # featureVectorQuery now holds all feature vectors for each query
    return featureVectorQuery

def createAbstractVector(removeStopWordsAbstracts, removeStopWordsQueries):
    #count table
    wordFreq = {}
    total = 1400
    abstractTFIDF = []

    for abstract in removeStopWordsAbstracts:
        for term in abstract:
            term = term.lower()
            if term in wordFreq:
                wordFreq[term] += 1
            else:
                wordFreq[term] = 1

    # TFIDF abstracts
    for abstract in removeStopWordsAbstracts:
        abstractTFIDF.append({})

        wordChecked = []

        for term in abstract:
            term = term.lower()

            if term in wordChecked:
                abstractTFIDF[-1][term] += 1
            else:
                wordChecked.append(term)
                abstractTFIDF[-1][term] = 1

            # term freq
            termFrequency = float(abstractTFIDF[-1][term])/float(len(abstract))

            # Inverse Doc Frequency: number of documents / number of documents containing the term
            IDF = math.floor(math.log(float(total) / float(wordFreq[term])) * 1000) / 1000

            # Full TFIDF (term freq) * (Inverse Doc Freq)
            abstractTFIDF[-1][term] = math.floor(termFrequency * IDF * 1000) / 1000

    featureVectorAbstract = []

    for i, query in enumerate(removeStopWordsQueries):
        featureVectorAbstract.append([])

        for item in abstractTFIDF:
            featureVectorAbstract[-1].append([])
            for term in query:
                stemmer = PorterStemmer()
                new_term = stemmer.stem(term)

                if item.get(term):
                    featureVectorAbstract[-1][-1].append(item.get(term))
                elif item.get(new_term):
                    featureVectorAbstract[-1][-1].append(item.get(term))
                else:
                    featureVectorAbstract[-1][-1].append(0)


    return featureVectorAbstract


def strip_abstracts_from_file(abstracts_file, closed_class_stop_words):
    cleaned = []
    line_is_abstract = False

    with abstracts_file as f:
        line_tokens = []

        for line in abstracts_file:
            if line[:2] == '.W':
                line_is_abstract = True

            elif line[:2] == '.I': #we've reached the end of an abstract
                cleaned.append(line_tokens)
                line_tokens = []
                line_is_abstract = False

            elif line_is_abstract == True:
                lks = word_tokenize(line)
                for token in lks:
                    if not token in closed_class_stop_words:
                        line_tokens.append(token)

    return cleaned

def strip_queries_from_file(fileRef, closed_class_stop_words):
    lines = []

    sentences = word_tokenize(fileRef)

    for word in sentences:
        if word in closed_class_stop_words or word in string.punctuation or word == ".I" or word == ".W":
            continue
        if word.isdigit() and len(word) == 3:
            lines.append([])

        elif not re.search(r'\d|\W', word):
            lines[-1].append(word)

    return lines

main()
