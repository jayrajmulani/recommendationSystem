import xlrd
import math
import copy

#Utility 
#-------------------------------------------------------------------------------------------------------------------------
def createSimilarityMatrix(file):
    sheet = xlrd.open_workbook(file).sheet_by_index(0)
    movies = []
    matrix = {}
    for i in range(1,sheet.ncols):
        movies.append(str(sheet.cell_value(0,i)))
    
    users = []
    for i in range(1,sheet.nrows):
        users.append(int(sheet.cell_value(i,0)))
    
    for user in range(1,sheet.nrows):
        matrix[sheet.cell_value(user,0)] = {}
    
    for i in range(1,sheet.nrows):
        for j in range(1,sheet.ncols):
            matrix[sheet.cell_value(i,0)][sheet.cell_value(0,j)] = sheet.cell_value(i,j)
     
    data = {}
    data['users'] = users
    data['movies'] = movies
    data['ratings'] = matrix
    # print(data) 
    return data
  
    
def getUser(userID,users):
    try:
        return  users.index(userID)
    except Exception:
        return -1
#-------------------------------------------------------------------------------------------------------------------------




#Jaccard Similarity
#-------------------------------------------------------------------------------------------------------------------------

def JaccardSilimarity(userA,userB,data):
    
    union = A_Union_B(userA,userB,data['ratings'])
    intersection = A_Intersection_B(userA,userB,data['ratings'])
    if not union == 0:
        return intersection/union
    else:
        return -1

def A_Intersection_B (userA,userB,ratings):
    rA = list(ratings[userA].values())
    rB = list(ratings[userB].values())
    cnt=0
    for i in range(len(rA)):
        if not rA[i] == 'NULL' and not rB[i] == 'NULL':
            cnt+=1
    return cnt

def A_Union_B (userA,userB,ratings):
    rA = list(ratings[userA].values())
    rB = list(ratings[userB].values())
    cnt=0
    for i in range(len(rA)):
        if not rA[i] == 'NULL' or not rB[i] == 'NULL':
            cnt+=1
    return cnt

#-------------------------------------------------------------------------------------------------------------------------


#Cosine Similarity 
#------------------------------------------------------------------------------------------------------------------------------
def CosineSilimarity(userA,userB,data):
    # print('Cosine', data)
    union = A_B_Modulous(userA,userB,data)
    intersection = A_Multiply_B(userA,userB,data)

    if not union == 0:
        return intersection/union
    else:
        return -1

def A_Multiply_B (userA,userB,ratings):
    rA = list(ratings[userA].values())
    rB = list(ratings[userB].values())
    cnt=0
    for i in range(len(rA)):
        if not rA[i] == 'NULL' and not rB[i] == 'NULL':
            cnt+=rA[i] * rB[i]
    return cnt

def A_B_Modulous (userA,userB,ratings):
    cnt_A = 0
    # print(ratings)
    cnt_B = 0
    rA = list(ratings[userA].values())
    rB = list(ratings[userB].values())
    
    for i in range(len(rA)):
        if not rA[i] == 'NULL':
            cnt_A += rA[i]*rA[i]
    for i in range(len(rB)):
        if not rB[i] == 'NULL':
            cnt_B += rB[i]*rB[i]
    cnt_A = math.sqrt(cnt_A)
    cnt_B = math.sqrt(cnt_B)
    return cnt_A*cnt_B

#-----------------------------------------------------------------------------------------------------------------------------------

#Centered Cosine Similarity
#-------------------------------------------------------------------------------------------------------------------------------------

def CenteredCosineSimilarity(userA,userB,data):
    return CosineSilimarity(userA,userB,data)


def normalizeRatings(ratings):
    ratingsAlias = copy.deepcopy(ratings)
    for user in ratingsAlias.keys():
        r = [x for x in list(ratingsAlias[user].values()) if not x == 'NULL']
        mean = sum(r)/len(r)
        for movie in ratingsAlias[user].keys():
            if not ratingsAlias[user][movie] == 'NULL':
                ratingsAlias[user][movie] = round(ratingsAlias[user][movie]-mean, 2)
            else:
                 ratingsAlias[user][movie] = 0.0
    return ratingsAlias

#-----------------------------------------------------------------------------------------------------------------------------------

def KUsers(method,r,userClient,data_ratings):
    kUsers = []
    if method == 'jaccard':
        accept=[0.4,1.0]
    elif  method == 'cosine':
        accept=[0.6,1.0]
    else:
        accept=[-0.25,0.25]
    
    for user in data_ratings.keys():
        if not user == userClient and r[user]>=accept[0] and r[user]<=accept[1]:
            kUsers.append(user)
    
    
    return kUsers

def ratingPrediction(targetMovie,data_ratings,similarityMatrix,userClient,kUsers):
    usersConsidered = []
    for user in kUsers:
        if not data_ratings[user][targetMovie] == 'NULL':
            usersConsidered.append(user)
    weighted_mean = 0
    print(usersConsidered)
    total_similarity = 0
    for user in usersConsidered:
        print(similarityMatrix[user])
        weighted_mean += similarityMatrix[user] * data_ratings[user][targetMovie]
        total_similarity += similarityMatrix[user]
    weighted_mean = round(weighted_mean/total_similarity,2)
    return weighted_mean




if __name__=='__main__':
    data = createSimilarityMatrix('movie_ratings.xlsx')
    similarityMatrix = data['ratings']
    # print(similarityMatrix)
    userClient = 5
    targetMovie = 'M1'

    js = {}
    for user in data['users']:
        if not user == userClient:
            jaccardSilimarity = JaccardSilimarity(userClient,user,data) 
            js[user] = jaccardSilimarity
    
    cs = {}
    for user in data['users']:
        if not user == userClient:
            cosineSilimarity = round(CosineSilimarity(userClient,user,data['ratings']),2) 
            cs[user] = cosineSilimarity

    ccs = {}
    normalizedRatings = normalizeRatings(data['ratings'])
    for user in data['users']:
        if not user ==  userClient:
            centeredCosineSilimarity = round(CenteredCosineSimilarity(userClient,user,normalizedRatings),2)
            ccs[user] = centeredCosineSilimarity
    
    print('\n\nJaccard Similarity ' ,js,'\n\n')
    print('Cosine Similarity ', cs,'\n\n')
    print('Centered Cosine Similarity' , ccs)

    predicted = ratingPrediction(targetMovie,data['ratings'],cs,userClient,KUsers('centered',ccs,userClient,data['ratings']))
    
    print('Predicted Rating:', predicted)
    


        

