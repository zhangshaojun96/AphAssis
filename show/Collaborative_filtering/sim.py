from login.models import register
from show.models import wrong_record
from show.models import Arrange_set
from show.Collaborative_filtering.collab import collab
from show.models import wrong_record
from numpy import mat
from numpy import *


def turn(s):
    if str(s) == str("农民"):
        return 0
    elif str(s) == str("工人"):
        return 1
    elif str(s) == str("技工"):
        return 2
    elif str(s) == str("商业服务业人员"):
        return 3
    elif str(s) == str("文职工作者"):
        return 4
    elif str(s) == str("军人"):
        return 7
    elif str(s) == str("其他"):
        return 5


#
def getsimmatrix(userlist):
    s = (len(userlist), 3)
    usermatrix = zeros(s)
    for i in range(0, len(userlist)):
        # 获得用户信息矩阵
        usermatrix[i][0] = (int)(userlist[i].age / 15)
        usermatrix[i][1] = turn(userlist[i].profession)
        usermatrix[i][2] = userlist[i].education
    return usermatrix


def collaborative_filtering(userid, questionid, wronganswer):
    # 通过questionid wronganswer查找相同记录用户
    users = list(wrong_record.objects.filter(question_id=questionid, wrong_choice=wronganswer))
    userset=list()
    for u in users:
        if u.userid not in userset:
            userset.append(u.userid)
    if len(userset) == 0:
        return None
    # useridlist =  list(Arrange_set.objects.userid(wrong_ques__contains=questionid+'#'+wronganswer))
    matrixlen = 0
    for i in range(0, len(userset)):
        if (userset[i] == userid):
            matrixlen = len(userset) - 1
            break
        else:
            matrixlen = len(userset)
    if matrixlen <= 0:
        return None
    print('matrixlen: '+str(matrixlen))
    s=(matrixlen,3)
    usermatrix = zeros(s)
    print(usermatrix)
    userlist = []
    # 用户相似度矩阵
    for i in range(0, len(userset)):
        if (userid != userset[i]):
            user = register.objects.get(id=userset[i])
            for j in range(0, matrixlen):
                # 获得用户信息矩阵
                usermatrix[i][0] = (int)(user.age / 15)
                usermatrix[i][1] = turn(user.profession)
                usermatrix[i][2] = user.education
                userlist.append(user.id)

    # 当前用户信息
    print('user '+str(userid))
    this_user = register.objects.get(id=int(userid))
    s=(1,3)
    thisuser_matrix = zeros(s)
    thisuser_matrix[0][0] = (int)(this_user.age / 15)
    thisuser_matrix[0][1] = turn(this_user.education)
    # 按相似度高低输出用户在userset中的位置
    recomm = collab(thisuser_matrix, usermatrix, 1)
    guideid = list(wrong_record.objects.filter(userid=userlist[recomm[0]], question_id=questionid, wrong_choice=wronganswer))[0].guide
    if guideid==0:
        return None
    else:
        return guideid
