#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Time    : 2023-08
# @Author  : Hongkan Chen

import random
import heapq
from collections import defaultdict


def Fisher_Yates_shuffle(array,seed=None):
    '''
    输入引证文献列表或者参考文献列表
    随机打乱array
    '''
    new_array = array[:]
    random.shuffle(new_array,seed)
    return new_array



class Node():
    def __init__(self):
        self.l = None
        self.r = None
        self.v = 0

class SegmentTree(object):

    def __init__(self, M):
        self.len_data = M
        self.root = Node()
        self.__build(0,self.len_data-1,self.root)
        self.update_val = 0

    def __build(self, l, r,p):
        if l==r:
            p.v = 1
            return 
        mid = (l+r)//2
        p.l = Node()
        p.r = Node()
        self.__build(l,mid,p.l)
        self.__build(mid+1,r,p.r)
        p.v = p.l.v+p.r.v

    def update(self,l,r,p,pos):
        if l==r:
            p.v = self.update_val
            return 
        mid = (l+r)//2
        if pos<=mid:
            self.update(l,mid,p.l,pos)
        else:
            self.update(mid+1,r,p.r,pos)
        p.v = p.l.v+p.r.v
    
    def update_pos(self,pos,v=0):
        self.update_val = v
        self.update(0,self.len_data-1,self.root,pos)

    def search(self, l, r,L,R,p):
        if((l==L) and (r==R)):
            return p.v
        mid =(l+r)//2
        if R<=mid:
            return self.search(l,mid,L,R,p.l)
        if L>mid:
            return self.search(mid+1,r,L,R,p.r)
        return self.search(l,mid,L,mid,p.l)+self.search(mid+1,r,mid+1,R,p.r)

    def prefix_sum(self,pos):
        return self.search(0,self.len_data-1,0,pos,self.root)
    
    def search_K(self,l,r,p,v):
        if l==r:
            return l
        mid = (l+r)//2
        if p.l.v>=v:
            return self.search_K(l,mid,p.l,v)
        return self.search_K(mid+1,r,p.r,v-p.l.v)

    def Find_prefix_sum(self,K):
        if self.root.v<K:
            raise Exception("没有K个位置")
        return self.search_K(0,self.len_data-1,self.root,K)

class PriorityQueue_special():
    def __init__(self,data):
        self.Cnt = defaultdict(int)
        v,c = None,0
        for d in data:
            # self.Cnt[d]+=1
            if d!=v:
                if c>0:
                    self.Cnt[v]+=c
                c=0
                v=d
            c+=1
        if c>0:
            self.Cnt[v]+=c
        
        self.heap = []
        for Hongkan,Chen in self.Cnt.items():
            heapq.heappush(self.heap,(-Chen,Hongkan))

        if self.Cnt[self.Top()]>len(data)/2:
            raise Exception("不存在无自环解")
    def Top(self):
        t = self.heap[0]
        while(self.Cnt[t[1]]!=-t[0]):
            t = heapq.heappop(self.heap)
            v = self.Cnt[t[1]]
            if v>0 :
                heapq.heappush(self.heap,(-v,t[1]))
            t = self.heap[0]
        return t[1]
    def Del(self,p):
        self.Cnt[p]-=1

class Position():
    def __init__(self,data):
        #data are sorted
        self.postion_L = {}
        self.postion_R = {}
        for i,d in enumerate(data):
            if d not in self.postion_L:
                self.postion_L[d]=i
            self.postion_R[d]=i
    
    def Del(self,p):
        if p not in self.postion_L:
            raise Exception("没有这个")
        if self.postion_L[p]>self.postion_R[p]:
            raise Exception("已经没有了")
        self.postion_R[p]-=1
        return self.postion_R[p]+1

    def has_value(self,p):
        if p not in self.postion_L:
            return False
        return self.postion_L[p]<=self.postion_R[p]

    def value_count(self,p):
        if p not in self.postion_L:
            return 0
        return self.postion_R[p]-self.postion_L[p]+1

    def Position_smaller(self,pos,p):
        if p not in self.postion_L:
            return 0
        if pos<self.postion_L[p]:
            return 0
        return min(self.postion_R[p],pos)-self.postion_L[p]+1
    
class Delable_SortQueue():
    def __init__(self):
        self.heap = []
        self.heap_tail = 0
        self.heap_head = 0
        self.Del_dict= {}
    
    def Top(self):
        if self.heap_head<self.heap_tail:
            return self.heap[self.heap_head]
        raise Exception("没有元素了") 

    def Push(self,v):
        self.heap.append(v)
        self.heap_tail+=1

    def Sort(self):
        self.heap = sorted(self.heap)

    def Del(self,v):
        if v not in self.Del_dict:
            self.Del_dict[v]=1
        else :
            self.Del_dict[v]+=1
        while self.heap_head<self.heap_tail and (self.heap[self.heap_head][1] in self.Del_dict) and (self.Del_dict[self.heap[self.heap_head][1]]>0):
            self.Del_dict[self.heap[self.heap_head][1]]-=1
            self.heap_head+=1
        

def Fisher_Yates_NoselfLoop(citing,cited,randomValue=False):
    '''
    citing,cited分别表示引证文献 和 参考文献
    randomValue表示是否要使用随机值法
    '''
    M = len(citing)
    if len(cited)!=M:
        raise Exception("两个数组长度不一致")
    if M==0:
        return (citing,cited)
    citing = sorted(citing)
    cited = sorted(cited)
    if randomValue==False:
        citing_seg = SegmentTree(M)
        cited_seg = SegmentTree(M)
        heap = PriorityQueue_special(citing+cited)
        citing_pos = Position(citing)
        cited_pos = Position(cited)
        newciting,newcited = [],[]
        tmp_M = M
        while tmp_M:
            p = heap.Top()
            if citing_pos.has_value(p):
                Kan = random.randint(1,tmp_M-cited_pos.value_count(p))
                #第K个可以的
                if cited_pos.has_value(p):
                    if cited_seg.prefix_sum(cited_pos.postion_L[p])-1>=Kan:
                        del_value = 0
                    else :
                        del_value = cited_pos.value_count(p)
                else :
                    del_value= 0
                pos = cited_seg.Find_prefix_sum(Kan+del_value)
                q = cited[pos]
            elif cited_pos.has_value(p):
                Kan = random.randint(1,tmp_M-citing_pos.value_count(p))
                #第K个可以的
                if citing_pos.has_value(p):
                    if citing_seg.prefix_sum(citing_pos.postion_L[p])-1>=Kan:
                        del_value = 0
                    else :
                        del_value = citing_pos.value_count(p)
                else :
                    del_value= 0
                pos = citing_seg.Find_prefix_sum(Kan+del_value)
                q = citing[pos]

                p,q = q,p
                
            else:
                raise Exception("不存在解")
            
            newciting.append(p)
            pos_p = citing_pos.Del(p)
            citing_seg.update_pos(pos_p)
            newcited.append(q)
            pos_q = cited_pos.Del(q)
            cited_seg.update_pos(pos_q)

            heap.Del(p)
            heap.Del(q)
            tmp_M-=1
        return (newciting,newcited)
    else :
        heap = PriorityQueue_special(citing+cited)
        citing_pos = Position(citing)
        cited_pos = Position(cited)

        newciting,newcited = [],[]
        Citing_heap = Delable_SortQueue()
        UnuseCiting,cnt_Citing =None,0
        for p in citing:
            v = random.random()*random.randint(1,M)
            Citing_heap.Push((v,p))
        Citing_heap.Sort()
        Cited_heap = Delable_SortQueue()
        UnuseCited,cnt_Cited =None,0
        for p in cited:
            Kan = random.random()*random.randint(1,M)
            Cited_heap.Push((Kan,p))
        Cited_heap.Sort()

        tmp_M = M
        while tmp_M:
            p = heap.Top()
            if citing_pos.has_value(p):
                if cnt_Cited>0 and p!=UnuseCited:
                    q = UnuseCited
                else :
                    v = Cited_heap.Top()
                    while v[1]==p:
                        UnuseCited = v[1]
                        cnt_Cited+=1
                        Cited_heap.Del(v[1])
                        v = Cited_heap.Top()
                    q = v[1]
                
            elif cited_pos.has_value(p):
                if cnt_Citing>0 and p!=UnuseCiting:
                    q = UnuseCiting
                else :
                    v = Citing_heap.Top()
                    while v[1]==p:
                        UnuseCiting = v[1]
                        cnt_Citing+=1
                        Citing_heap.Del(v[1])
                        v = Citing_heap.Top()
                    q = v[1]
                p,q = q,p
            else:
                raise Exception("不存在解")
            
            newciting.append(p)
            pos_p = citing_pos.Del(p)
            if cnt_Citing>0 and UnuseCiting==p:
                cnt_Citing-=1
            else :
                Citing_heap.Del(p)

            newcited.append(q)
            pos_q = cited_pos.Del(q)
            if cnt_Cited>0 and UnuseCited==q:
                cnt_Cited-=1
            else :
                Cited_heap.Del(q)
            heap.Del(p)
            heap.Del(q)
            tmp_M-=1
        return (newciting,newcited)

class PriorityQueue():
    def __init__(self):
        self.heap = []
        self.heap_len = 0

    def Push(self,v):
        heapq.heappush(self.heap,v)
        self.heap_len+=1

    def Top(self):
        return self.heap[0]
    
    def Pop(self):
        heapq.heappop(self.heap)



def Fisher_Yates_limitPubYear(citing,cited,paper_date,randomValue=False):
    '''
    citing,cited分别表示引证文献 和 参考文献
    paper_date是一个paper:date的字典
    randomValue表示是否要使用随机值法
    '''
    M = len(citing)
    if len(cited)!=M:
        raise Exception("两个数组长度不一致")
    if M==0:
        return (citing,cited)
    citing = sorted(citing,key=lambda x:paper_date[x])
    cited = sorted(cited,key=lambda x:paper_date[x])
    newcited = []
    if randomValue==False:
        cited_seg = SegmentTree(M)
        Rpos = 0
        for i in range(M):
            date = paper_date[citing[i]]
            while(Rpos<M and paper_date[cited[Rpos]]<=date):
                Rpos+=1
            if Rpos-i<=0:
                raise Exception("无解")
            K= random.randint(1,Rpos-i)
            pos = cited_seg.Find_prefix_sum(K)
            newcited.append(cited[pos])
            cited_seg.update_pos(pos)
    else :
        cited_heap = PriorityQueue()
        Rpos = 0
        for i in range(M):
            date = paper_date[citing[i]]
            while(Rpos<M and paper_date[cited[Rpos]]<=date):
                v = random.random()
                cited_heap.Push((v,cited[Rpos]))
                Rpos+=1
            if cited_heap.heap_len<=0:
                raise Exception("无解")
            newcited.append(cited_heap.Top()[1])
            cited_heap.Pop()
    
    return (citing,newcited)


def Fisher_Yates_preferential(citing,cited,score):
    '''
    citing,cited分别表示引证文献 和 参考文献
    score 是一个函数
    '''
    M = len(citing)
    if len(cited)!=M:
        raise Exception("两个数组长度不一致")
    if M==0:
        return (citing,cited)
    seg = SegmentTree(M)
    newciting = Fisher_Yates_shuffle(citing)
    newcited = cited[:]
    for i in range(0):
        seg.update_pos(i,score(newcited[i]))
        sigma_score = seg.prefix_sum(i)
        random_score = random.randint(1,sigma_score)
        j = seg.Find_prefix_sum(random_score)
        if i!=j:
            newcited[i],newcited[j] = newcited[j],newcited[i]
            seg.update_pos(i,score(newcited[i]))
            seg.update_pos(j,score(newcited[j]))
    return (newciting,cited)

def Fisher_Yates_MCMC(citing,cited,Swap):
    '''
    citing,cited分别表示引证文献 和 参考文献
    Swap是一个判定函数(a1,a2)，给定两组引文对，判断a1的citing是否要引用a2的cited
    '''
    M = len(citing)
    if len(cited)!=M:
        raise Exception("两个数组长度不一致")
    if M==0:
        return (citing,cited)
    
    newciting = Fisher_Yates_shuffle(citing)
    newcited = cited[:]
    for i in range(M-1,-1,1):
        j = random.randint(0,i)
        if Swap((newciting[i],newcited[i]),(newciting[j],newcited[j])):
            newcited[i],newcited[j] = newcited[j],newcited[i]
    return (newciting,newcited)

def __main__():
    random.seed(103)
    for i in range(10):
        if i%10==0:
            print(i)
        citing = [random.randint(1,100) for i in range(1000)]
        cited = [random.randint(1,100) for i in range(1000)]
        # citing = [1 for i in range(1000)]
        # cited = [2 for i in range(1000)][1:]+[1]
        
        # a,b = Fisher_Yates_NoselfLoop(citing,cited,randomValue=True)
        a,b = Fisher_Yates_limitPubYear(citing,cited,defaultdict(int),randomValue=True)

        # for j,k in zip(a,b):
        #     if j==k:
        #         print(i,j,k)

    citing = [3, 7, 1, 3, 3, 9, 3, 2, 7, 2, 1, 1, 2, 6, 9, 5, 1, 2, 6, 3, 6, 8, 2, 9, 6, 4, 7, 6, 5, 9, 1, 9, 3, 2, 10, 6, 9, 4, 7, 3, 10, 10, 6, 1, 2, 5, 4, 5, 1, 6, 1, 2, 6, 5, 4, 2, 9, 3, 4, 5, 2, 8, 5, 1, 7, 1, 9, 3, 8, 10, 2, 8, 7, 6, 3, 9, 8, 8, 8, 5, 7, 10, 10, 6, 5, 6, 2, 4, 3, 8, 2, 4, 10, 10, 10, 1, 6, 5, 7, 9]
    cited = [1, 5, 1, 10, 6, 10, 6, 9, 7, 8, 8, 8, 4, 1, 6, 7, 10, 5, 1, 1, 3, 8, 9, 10, 3, 9, 2, 3, 8, 2, 3, 4, 10, 6, 1, 1, 2, 3, 1, 5, 9, 6, 4, 8, 7, 3, 3, 5, 4, 9, 6, 3, 4, 2, 8, 7, 1, 7, 9, 4, 9, 9, 2, 2, 7, 10, 6, 5, 6, 1, 10, 4, 3, 2, 2, 2, 4, 2, 2, 8, 4, 8, 9, 6, 2, 7, 9, 7, 7, 10, 6, 8, 5, 5, 7, 9, 5, 1, 9, 10]
    print(Fisher_Yates_NoselfLoop(citing[:],cited[:],randomValue=True))
    # print(Fisher_Yates_NoselfLoop(citing,cited,randomValue=True))

    # Fisher_Yates_limitPubYear
    # Fisher_Yates_shuffle(citing)