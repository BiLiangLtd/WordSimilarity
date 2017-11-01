# -*- coding: utf-8 -*-

__author__ = 'commissar'

import unittest
from word_similarity import WordSimilarity2010

class TestWordSimilarity(unittest.TestCase):

    def test_similarity_2010(self):
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