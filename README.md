# WordSimilarity

这是一个基于哈工大同义词词林扩展版的单词相似度计算方法的python实现，参考论文如下：

    2010 田久乐等，吉林大学学报（信息科学版），基于同义词词林的词语相似度计算方法。

## 安装

```commandline
pip install WordSimilarity
```    
    
## 使用

```python

from word_similarity import WordSimilarity2010

ws_tool = WordSimilarity2010()

b_a = "抄袭"
b_b = "克隆"
sim_b = ws_tool.similarity(b_a, b_b)
print(b_a, b_b, '相似度为', sim_b)
#抄袭 克隆 最终的相似度为 0.585642777645155

w_a = '人民'
sample_list = ["国民", "群众", "党群", "良民", "同志", "成年人", "市民", "亲属", "志愿者", "先锋" ]

for s_a in sample_list:
    sim_a = ws_tool.similarity(w_a,s_a)
    print(w_a, s_a, '相似度为', sim_a)
# 人民 国民 相似度为 1
# 人民 群众 相似度为 0.9576614882494312
# 人民 党群 相似度为 0.8978076452338418
# 人民 良民 相似度为 0.7182461161870735
# 人民 同志 相似度为 0.6630145969121822
# 人民 成年人 相似度为 0.6306922220793977
# 人民 市民 相似度为 0.5405933332109123
# 人民 亲属 相似度为 0.36039555547394153
# 人民 志愿者 相似度为 0.22524722217121346
# 人民 先锋 相似度为 0.18019777773697077
        
```


## 同类项目

* https://github.com/ashengtx/CilinSimilarity  实现了三种计算方法。
* https://github.com/Xls1994/Cilin  
* http://www.codepub.cn/2015/08/04/Based-on-the-extended-version-of-synonyms-Cilin-word-similarity-computing/  Java实现


## 致谢：

本代码的实现要感谢下面几位作者：
* 哈工大信息检索研究室所著的《哈工大信息检索研究室同义词词林扩展版》
* 田久乐  赵 蔚在2010年所发表论文<基于同义词词林的词语相似度计算方法>
* http://codepub.cn/2015/08/04/Based-on-the-extended-version-of-synonyms-Cilin-word-similarity-computing/
* http://www.cnblogs.com/einyboy/archive/2012/09/09/2677265.html?from=singlemessage&isappinstalled=0
* 本代码参考了https://github.com/ashengtx/CilinSimilarity 部分实现