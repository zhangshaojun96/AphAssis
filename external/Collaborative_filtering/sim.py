from login.models import register
from show.models import wrong_record
from show.models import Arrange_set
import collab
from numpy import mat
import numpy as np

def Turn(str s):
    if(cmp(s,"农民")==0)
        return 0
    else if(cmp(s,"工人")==0)
        return 1
    else if(cmp(s,"技工")==0)
        return 2
    else if(cmp(s,"商业服务业人员")==0)
        return 3
    else if(cmp(s,"文职工作者")==0)
        return 4
    else if(cmp(s,"军人")==0)
        return 7
    else if(cmp(s,"其他")==0)
        return 5
    

#
def Getsimmatrix(list userlist):
    usermatrix = mat(zeros((len(userlist),3)))
    for i in range(0,len(userlist)):
        #获得用户信息矩阵
        usermatrix[i][0] = (int)userlist[i].age/15
        usermatrix[i][1] =  Turn(userlist[i].profession)
        usermatrix[i][2] = education 
    return usermatrix


def Collaborative_filtering(int user,id questionid,id wronganswer):
    #通过questionid wronganswer查找相同记录用户
    userset = set(wrong_record.objects.userid(question_id = questionid,wrong_choice = wronganswer))
            
   # useridlist =  list(Arrange_set.objects.userid(wrong_ques__contains=questionid+'#'+wronganswer))
    for i in range(0,len(userset))
        if(userset[i]==user):
            matrixlen = len(userset)-1
            break;
        else:
            matrixlen = len(userset)
    usermatrix = mat(zeros((len(matrixlen),3)))
    userlist = []
    #用户相似度矩阵
    for i in range(0,len(userset)):
        if(user!=userset[i]):
            user = register.objects.get(id = userset[i]);
            for j in range(0,maxtixlen):
                #获得用户信息矩阵
                usermatrix[i][0] = (int)(user.age/15)
                usermatrix[i][1] =  Turn(user.profession)
                usermatrix[i][2] = user.education
                userlist.append(user.id)

    #当前用户信息
    this_user = register.objects.get(id = user)
    thisuser_matrix = mat(zeros(1,3))
    thisuser_matrix[0][0] = (int)(this_user.age/15)
    thisuser_matrix[0][1] = Turn(this_user.education)
    #按相似度高低输出用户在userset中的位置
    recomm = collab(thisuser_matrix,usermatrix,1);
    guideid = wrong_record_objects.guide(userid = userlist[recomm[0]],question_id = questionid,wrong_choice = wronganswer);
    return guideid
    
        
