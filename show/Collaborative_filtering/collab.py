import numpy as np

#（本人信息，其他符合要求用户信息矩阵，返回的用户数）
def collab(target,info,num):
    dim = len(info[:,0])
    #print(dim)
    result = np.zeros(dim)
    #print(result)
    #获得每个用户和比较用户的差值
    for j in range(0,dim):
        #array为权重矩阵，可根据实际情况调整
        r = np.sum(np.abs(target-info[j])*np.array([0.25,0.5,0.5]))
        #print(r)
        result[j]=r
    #print(result)
    neighbor_ind = np.argpartition(result,-num)[:num]
   # print(neighbor_ind)
    #neighbor_ind = neighbor_ind[-1::-1]
    recomm = neighbor_ind.astype(int)
    return recomm

if __name__=='__main__':
    target = np.array([4,1,2])
    info = np.array([[4,0,2],
                     [1,3,3],
                     [4,1,2]])
    print(collab(target,info,1))

