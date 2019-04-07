
import xlrd
import math
import copy

# Utility
# -------------------------------------------------------------------------------------------------------------------------


def createSimilarityMatrix(file):
    matrix = {}
    sheet = xlrd.open_workbook(file).sheet_by_index(0)
    movies = []
    for movie in range(1, sheet.ncols):
        matrix[sheet.cell_value(0, movie)] = {}
    
    for i in range(1, sheet.nrows):
        for j in range(1, sheet.ncols):
            matrix[sheet.cell_value(0, j)][sheet.cell_value(i, 0)] = sheet.cell_value(i, j)
    
    for i in range(1,sheet.ncols):
        movies.append(str(sheet.cell_value(0,i)))
    users = []
    for i in range(1,sheet.nrows):
        users.append(int(sheet.cell_value(i,0)))
    
    # for user in range(1,sheet.nrows):
    #    matrix[sheet.cell_value(user,0)] = {}
    
     
    data = {}
    data['users'] = users
    data['movies'] = movies
    data['ratings'] = matrix
      
    return data
  
    
def getUser(userID,users):
    try:
        return  users.index(userID)
    except Exception:
        return -1
# -------------------------------------------------------------------------------------------------------------------------




# Jaccard Similarity
# -------------------------------------------------------------------------------------------------------------------------

def A_Intersection_B (movieA,movieB,ratings):
    rA = list(ratings[movieA].values())
    rB = list(ratings[movieB].values())
    cnt=0
    for i in range(len(rA)):
        if not rA[i] == 'NULL' and not rB[i] == 'NULL':
            cnt+=1
    return cnt

def A_Union_B (movieA,movieB,ratings):
    rA = list(ratings[movieA].values())
    rB = list(ratings[movieB].values())
    cnt=0
    for i in range(len(rA)):
        if not rA[i] == 'NULL' or not rB[i] == 'NULL':
            cnt+=1
    return cnt

# -------------------------------------------------------------------------------------------------------------------------


# Cosine Similarity 
# ------------------------------------------------------------------------------------------------------------------------------

def A_Multiply_B (movieA,movieB,ratings):
    rA = list(ratings[movieA].values())
    rB = list(ratings[movieB].values())
    cnt=0
    for i in range(len(rA)):
        if not rA[i] == 'NULL' and not rB[i] == 'NULL':
            cnt+=rA[i] * rB[i]
    return cnt

def A_B_Modulous (movieA,movieB,ratings):
    cnt_A = 0
    cnt_B = 0
    rA = list(ratings[movieA].values())
    rB = list(ratings[movieB].values())
    
    for i in range(len(rA)):
        if not rA[i] == 'NULL':
            cnt_A += rA[i]*rA[i]
    for i in range(len(rB)):
        if not rB[i] == 'NULL':
            cnt_B += rB[i]*rB[i]
    cnt_A = math.sqrt(cnt_A)
    cnt_B = math.sqrt(cnt_B)
    return cnt_A*cnt_B

# -----------------------------------------------------------------------------------------------------------------------------------

# Centered Cosine Similarity
# -------------------------------------------------------------------------------------------------------------------------------------

def CenteredCosineSimilarity(movieA,movieB,data):
    union = A_B_Modulous(movieA,movieB,data)
    intersection = A_Multiply_B(movieA,movieB,data)
    if not union == 0:
        return round(intersection/union,2)
    else:
        return -1


def normalizeRatings(ratings):
    ratingsAlias = copy.deepcopy(ratings)
    for movie in ratingsAlias.keys():
        r = [x for x in list(ratingsAlias[movie].values()) if not x == 'NULL']
        mean = sum(r)/len(r)
        for user in ratingsAlias[movie].keys():
            if not ratingsAlias[movie][user] == 'NULL':
                ratingsAlias[movie][user] = round(ratingsAlias[movie][user]-mean, 2)
            else:
                 ratingsAlias[movie][user] = 0.0
    return ratingsAlias

# -----------------------------------------------------------------------------------------------------------------------------------

def K_Items(r,itemClient,data_ratings,userClient):
    kItems = []
    accept=[0.4,1.0]
    for item in data_ratings.keys():
        if not item == itemClient and not data_ratings[item][userClient] == 'NULL' and r[item]>=accept[0] and r[item]<=accept[1]:
            kItems.append(item)
    return kItems

def ratePrediction(similarity,ratings,kItems,userClient):
    sumRating = 0
    sumSimilarity = 0
    for item in kItems:
        sumRating += similarity[item]*ratings[item][userClient]
        sumSimilarity += similarity[item]
    return round(sumRating/sumSimilarity,2)

if __name__=='__main__':
    data = createSimilarityMatrix('movie_ratings.xlsx')
    similarity = {}
    normalizedRatings = normalizeRatings(data['ratings'])
    for movie in data['movies']:
        similarity[movie] = CenteredCosineSimilarity('M1',movie,normalizedRatings)
    kItems = K_Items(similarity,'M1',data['ratings'],5)
    # print('\n\nJaccard Similarity ' ,jc,'\n\n')
    print('K_Items similar to M1 :',kItems)
    print('Rating Predicted for U05 for M1 : ',ratePrediction(similarity,data['ratings'],kItems,5))
   
