# -*- coding: utf-8 -*-
__author__ = 'commissar'


try:
    from setuptools import setup
except:
    from distutils.core import setup
# """
# 打包的用的setup必须引入，
# """


NAME = "WordSimilarity"
# """
# 名字，一般放你包的名字即可
# """

PACKAGES = ["word_similarity",'data']
# """
# 包含的包，可以多个，这是一个列表
# """

DESCRIPTION = "基于哈工大同义词词林扩展版的单词相似度计算方法."
# """
# 关于这个包的描述
# """
LONG_DESCRIPTION = DESCRIPTION
# """
# 参见read方法说明
# """

KEYWORDS = ["cilin", "word similarity computation"]
# """
# 关于当前包的一些关键字，方便PyPI进行分类。
# """

AUTHOR = u" wuzhengwei"
# """
# 谁是这个包的作者，
# """

AUTHOR_EMAIL = u"commissarster@qq.com"
# """
# 作者的邮件地址
# """

URL = "https://github.com/BiLiangLtd/WordSimilarity"

VERSION = "0.0.1"
# """
# 当前包的版本
# """

LICENSE = "Apache 2.0"
# """
# 授权方式，
# """

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    package_data={
        "": ['*.txt',"*.jpg","*.pdf"]
    },
    exclude=["test.*","test*","*.log"],
    include_package_data=True,
    zip_safe=True,
)