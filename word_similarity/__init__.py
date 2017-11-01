# -*- coding: utf-8 -*-
__author__ = 'commissar'

import logging
import math
import os

log = logging.getLogger("WordSimilarity")


class SimilarBase(object):
    def __init__(self):

        self._data = {}  # key为词，value为list,五层编码，
        self._code_tree = {}    # 五层编码树，key为每层的名称。value为[dict],

        t_cur_path = os.path.dirname(os.path.realpath(__file__))
        t_cilin_path = os.path.realpath(os.path.join(t_cur_path, os.pardir, "data", "cilin_ex.txt"))

        self._load_cilin(t_cilin_path)
        pass

    @classmethod
    def _parse_code(cls, c):
        """
        将编码按层次结构化
        Aa01A01=
        第三层和第五层是两个数字表示
        第一、二、四层分别是一个字母
        最后一个字符用来去分所有字符相同的情况
        """
        return [c[0], c[1], c[2:4], c[4], c[5:7], c[7]]
    
    def _load_cilin(self, file_path):

        '''
        加载词林数据。
        :return:
        '''

        file_obj = open(file_path, 'r')
        line_num = 0
        while True:
            line_num += 1
            line = file_obj.readline()

            try:
                if line:
                    line = line.strip()
                    parts = line.split(" ")

                    word_code = parts[0]

                    layer_codes = self._parse_code(word_code)

                    last_tree_node = self._code_tree
                    # 构建编码树
                    for lay_idx,lay_char in enumerate(layer_codes):

                        t_cur_node_name = lay_char

                        if t_cur_node_name in last_tree_node:
                            last_tree_node = last_tree_node[t_cur_node_name]
                        else:
                            t_cur_node = {}

                            # 如果是后一个分类标识项，则将词的个数写到树叶上。
                            if lay_idx == len(layer_codes) - 1:
                                t_cur_node = len(parts)-1

                            last_tree_node[t_cur_node_name] = t_cur_node
                            last_tree_node = last_tree_node[t_cur_node_name]

                    # 构建词到编码的映射。
                    for t_word in parts[1:]:

                        if t_word in self._data:
                            # 一个词有多个编码的情况
                            self._data[t_word].append(word_code)
                        else:
                            self._data[t_word] = [word_code]
                else:
                    break
            except Exception as e:
                log.warning("load cilin warn.[line:%d] %s" % (line_num, e))

        file_obj.close()

        if not self._data:
            log.error("load cilin failed![%s]" % file_path)


class WordSimilarity2010(SimilarBase):
    '''
        本类根据下面的论文方法：
        基于同义词词林的词语相似度计算方法，田久乐, 赵 蔚(东北师范大学 计算机科学与信息技术学院, 长春 130117 )
        计算两个单词所有编码组合的相似度，取最大的一个
    '''

    def __init__(self):
        super(WordSimilarity2010, self).__init__()
        self.a = 0.65
        self.b = 0.8
        self.c = 0.9
        self.d = 0.96
        self.e = 0.5
        self.f = 0.1
        self.degree = 180
        self.PI = math.pi

    def similarity(self, w1, w2):
        '''
        判断两个词的相似性。
        :param w1: [string]
        :param w2: [string]
        :return: [float]0~1之间。
        '''

        code1 = self._data.get(w1, None)
        code2 = self._data.get(w2, None)

        if not code1 or not code2:
            return 0  # 只要有一个不在库里则代表没有相似性。

        # 最终返回的最大相似度
        sim_max = 0

        # 两个词可能对应多个编码
        for c1 in code1:
            for c2 in code2:
                cur_sim = self.sim_by_code(c1, c2)
                # print(c1, c2, '的相似度为：', cur_sim)
                if cur_sim > sim_max:
                    sim_max = cur_sim

        return sim_max

    def sim_by_code(self, c1, c2):
        """
        根据编码计算相似度
        """

        # 先把code的层级信息提取出来
        clayer1 = self._parse_code(c1)
        clayer2 = self._parse_code(c2)

        common_layer = self.get_common_layer(clayer1,clayer2)
        length = len(common_layer)

        # 如果有一个编码以'@'结尾，那么表示自我封闭，这个编码中只有一个词，直接返回f
        if c1.endswith('@') or c2.endswith('@') or 0 == length:
            return self.f

        cur_sim = 0
        if 6 <= length:
            # 如果前面七个字符相同，则第八个字符也相同，要么同为'='，要么同为'#''
            if c1.endswith('=') and c2.endswith('='):
                cur_sim = 1
            elif c1.endswith('#') and c2.endswith('#'):
                cur_sim = self.e
        else:
            k = self.get_k(clayer1, clayer2)
            n = self.get_n(common_layer)
            if 1 == length:
                cur_sim = self.sim_formula(self.a, n, k)
            elif 2 == length:
                cur_sim = self.sim_formula(self.b, n, k)
            elif 3 == length:
                cur_sim = self.sim_formula(self.c, n, k)
            elif 4 == length:
                cur_sim = self.sim_formula(self.d, n, k)

        return cur_sim

    def sim_formula(self, coeff, n, k):
        """
        计算相似度的公式，不同的层系数不同
        """
        return coeff * math.cos(n * self.PI / self.degree) * ((n - k + 1) / n)

    def get_common_layer(self, ca, cb):
        '''
        返回相应的layer层
        :param ca:     [list(str)] 分解后的编码。
        :param cb:     [list(str)] 分解后的编码。
        :return:   [list(str)]列表代表相应的根编码。
        '''
        common_layer = []

        for i, j in zip(ca, cb):
            if i == j:
                common_layer.append(i)
            else:
                break
        return common_layer



    def get_k(self, c1, c2):
        """
        返回两个编码对应分支的距离，相邻距离为1
        """
        if c1[0] != c2[0]:
            return abs(ord(c1[0]) - ord(c2[0]))
        elif c1[1] != c2[1]:
            return abs(ord(c1[1]) - ord(c2[1]))
        elif c1[2] != c2[2]:
            return abs(int(c1[2]) - int(c2[2]))
        elif c1[3] != c2[3]:
            return abs(ord(c1[3]) - ord(c2[3]))
        else:
            return abs(int(c1[4]) - int(c2[4]))

    def get_n(self, common_layer):
        '''
        返回相应结点下有多少个同级子结点。
        :param common_layer:    [listr(str)]相同的结点。
        :return:    int
        '''

        end_node = self._code_tree
        for t_node_name in common_layer:
            end_node = end_node[t_node_name]

        if not isinstance(end_node, dict):
            return end_node
        return len(end_node.keys())
