import nltk
import ast
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def preProcessing(inputFileStr,outputFileStr,printResult):
    inputFile = open(inputFileStr,"r").read()
    outputFile=open (outputFileStr,"w+")
    cachedStopWords = nltk.corpus.stopwords.words("english")
    cachedStopWords.append('OMG')
    cachedStopWords.append(':-)')
    result=(' '.join([word for word in inputFile.split() if word not in cachedStopWords]))
    if(printResult):
        print('Following are the Stop Words')
        print(cachedStopWords)
        print(str(result))
    outputFile.write(str(result))
    outputFile.close()

def tokenizeReviews(inputFileStr,outputFileStr,printResult):
    tokenizedReviews={}
    inputFile = open(inputFileStr,"r").read()
    outputFile=open (outputFileStr,"w")
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    uniqueId=1
    cachedStopWords = nltk.corpus.stopwords.words("english")
    for sentence in tokenizer.tokenize(inputFile):      
        tokenizedReviews[uniqueId]=sentence
        uniqueId+=1
    outputFile.write(str(tokenizedReviews))
    if(printResult):
        for key,value in tokenizedReviews.items():
            print(key,' ',value)
    outputFile.close()


def posTagging(inputFileStr,outputFileStr,printResult):
    inputFile = open(inputFileStr,"r").read()
    outputFile=open (outputFileStr,"w")
    inputTupples=ast.literal_eval(inputFile)
    outputPost={}
    for key,value in inputTupples.items():
        outputPost[key]=nltk.pos_tag(nltk.word_tokenize(value))
    if(printResult):
        for key,value in outputPost.items():
            print(key,' ',value)
    outputFile.write(str(outputPost))
    outputFile.close()

def findSentenceNo(feature):
    feature = feature[0].lower()
    _SaveFolderName = '/home/jayraj/datasets/aclImdb_v1/aclImdb/sample_results/'
    posTags = ast.literal_eval(open(_SaveFolderName+'3.PosTaggedReviews.txt').read())
    allWords = {}
    for sentenceNo in posTags.keys():
        allWords[sentenceNo] = []
        for (word,_) in posTags[sentenceNo]:
           allWords[sentenceNo].append(word.lower())
    # print(allWords)

    for sentenceNo in allWords.keys():
        if feature in allWords[sentenceNo]:
            return sentenceNo

    return None

def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(sentence)['compound']



def featureExtraction(inputFileStr,outputFileStr,printResult):
    inputFile = open(inputFileStr,"r").read()
    outputFile=open (outputFileStr,"w")
    inputTupples=ast.literal_eval(inputFile)
    prevWord=''
    prevTag=''
    currWord=''
    featureList=[]
    outputDict={}    
    _SaveFolderName = '/home/jayraj/datasets/aclImdb_v1/aclImdb/sample_results/'
    file = _SaveFolderName + '2.TokenizedReviews.txt'
    #Extracting Aspects
    allSentences = ast.literal_eval(open(file).read())

    for key,value in inputTupples.items():
        for word,tag in value:
            if(tag=='NN' or tag=='NNP'):
                if(prevTag=='NN' or prevTag=='NNP'):
                    currWord= prevWord + ' ' + word
                else:
                    featureList.append(prevWord.upper())
                    currWord= word
            prevWord=currWord
            prevTag=tag
    #Eliminating aspect which has 1 or less count
    for feature in featureList:
        if(outputDict.keys()!=feature):
            outputDict[feature]=featureList.count(feature)
    outputFeature=sorted(outputDict.items(), key=lambda x: x[1],reverse = True)
    finalFeature = []
    requiredFeatures = {'direction','director','stars',
    'acting','performance','production design','show',
    'talent','choreography','cinematography','actor',
    'cast','movie','dance','location','time','song',
    'singing','playback singer',' screenplay','action',
    'romance','comedy','plot','story','storyline','drama',
    'melodrama','casting','critics','mystery','suspense',
    'thrill','dedication','nature','flow','lead','support',
    'lyrics','albumn','dialogue','editing','costume','production',
    'design','vfx','film'}
    # featureIndex = {}
    FOP = {}
    for feature in outputFeature:
        if feature[0].lower() in requiredFeatures:
            finalFeature.append(feature)
            sentenceNo = findSentenceNo(feature)
            sentence = allSentences[sentenceNo]
            sentimentScore = sentiment_analyzer_scores(sentence)
            FOP[feature[0]] = sentimentScore

    
    if(printResult):
        print(finalFeature)
        print('------------------------------------------')
        print('Sentiment Scores: ')
        print(FOP)
    outputFile.write(str(FOP))
    outputFile.close()
