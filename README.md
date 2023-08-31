# NullModel-Python
NullModel-Python是零模型的代码，具体论文参见【零模型的方法与应用——以引文网络分析为例】。内置方法涵盖线性时间置换的Fisher-Yates shuffle，以及解决自环、引用时间限制、优先连接性等提供解决方案，部分方法采用了随机值法进行优化，可以进一步提高随机置换速度。

## 使用示例
```python3
import NullModel
citing,cited = [1,2],[2,3]

#线性时间内打乱
newciting,newcited = Fisher_Yates_shuffle(citing),Fisher_Yates_shuffle(cited)

#无自环，且采用随机值法
newciting,newcited = Fisher_Yates_NoselfLoop(citing,cited,randomValue=True)

#限制发文时间，且采用随机值法
from collections import defaultdict
paper_year = defaultdict(int)
newciting,newcited = Fisher_Yates_limitPubYear(citing,cited,paper_year,randomValue=True)

#优先连接性，传入返回整数的函数
def score(paper):
  return 1
newciting,newcited = Fisher_Yates_preferential(citing,cited,score)

#优先连接性，采用MCMC方式
def Swap(a1,a2):
    #a1 = (citing[i],cited[i])
    #a2 = (citing[j],cited[j])
    #判定a1中的引证文献是否要引用a2中的参考文献
    if score(a1[1])<score(a2[1]):
        return True
    return False
newciting,newcited = Fisher_Yates_MCMC(citing,cited,Swap)


```

## 论文引用

该代码包主要基于以下科研论文，如使用了本工具，请引用以下论文：
* 陈洪侃, 田逸凡, 步一. 零模型的方法与应用——以引文网络分析为例. 2023.

```

@article{NullModel-Python,
  author = {陈洪侃,田逸凡,步一},
  journal = {xxx},
  title = {零模型的方法与应用——以引文网络分析为例},
  url = {xxx},
  volume = {xxx},
  year = 2023
}
```
