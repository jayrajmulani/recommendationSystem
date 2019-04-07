
import omsFunctions
def printResultChoice():
    userChoice = str(input('\nDo you want to print the result on output window? (Y/N) :'))
    if(userChoice=='Y' or userChoice=='y'):
        return True
    else:
        return False

# _FolderName='/home/jayraj/datasets/aclImdb_v1/aclImdb/all/'
_FolderName='/home/jayraj/datasets/aclImdb_v1/own/'
_SaveFolderName = '/home/jayraj/datasets/aclImdb_v1/aclImdb/sample_results/'
_ReviewDataset=_FolderName+'3.txt'
_PreProcessedData=_SaveFolderName+'1.PreProcessedData.txt'
_TokenizedReviews=_SaveFolderName+'2.TokenizedReviews.txt'
_PosTaggedReviews=_SaveFolderName+'3.PosTaggedReviews.txt'
_Aspects=_SaveFolderName+'4.Aspects.txt'
_Opinions=_SaveFolderName+'5.Opinions.txt'
print("\n WELCOME TO FEATURE-BASED RECOMMENDER SYSTEM ")
print("-------------------------------------------------------------")
input("Please Enter any key to continue...")
print("\nPREPROCESSING DATA")
omsFunctions.preProcessing(_ReviewDataset,_PreProcessedData,printResultChoice())
print("\nREADING REVIEW COLLECTION...")
omsFunctions.tokenizeReviews(_ReviewDataset,_TokenizedReviews,printResultChoice())
print("\nPART OF SPEECH TAGGING...")
omsFunctions.posTagging(_TokenizedReviews,_PosTaggedReviews,printResultChoice())
print(open(_ReviewDataset,'r').read())
print("\n These are the features found in the movie. Along with Sentiment Scores. ")
omsFunctions.featureExtraction(_PosTaggedReviews,_Aspects,printResultChoice())
# print("\n\n\n\n\n\nIDENTIFYING OPINION WORDS...")
# omsFunctions.identifyOpinionWords(_PosTaggedReviews,_Aspects,_Opinions,printResultChoice())




