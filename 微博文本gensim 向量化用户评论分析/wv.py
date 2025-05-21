import pandas as pd
import numpy as np
import jieba
#import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from tqdm import tqdm
import os
import re
import emoji
import io
import logging
import time
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
###一########################################################################################
#定义一个类TextAnalyzer，其属性包括待分析的文本文件路径，等加载的预训练模型文件路径，训练word2vec的一些简单参数
# （如向量长度，窗口大小）等，初始化的时候需要对这些属性进行定义。

class TextAnalyzer:
    # 配置日志，特别是在处理文件和训练模型时候显示进度
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    def __init__(self, file_path, model_path, len_vec, size_window, cache_path = "processed_words.txt"):
        self.cache_path = cache_path
        self.file_path = file_path
        self.model_path = model_path
        self.len_vec = len_vec
        self.size_window = size_window
        self.processed_words = None
        self.cache_path = cache_path # 用于文件预处理的文件储存，第二次跑的时候可以直接使用不需要重复处理；同时可以查看处理结果不需要打印，以便优化过滤逻辑
        
    def _remove_emojis(self, text): # 移除emoji，不需要手动
        return emoji.replace_emoji(text,replace='')

###二########################################################################################
#在上述类加入一个预处理方法_pre_process，如将待分析的weibo.txt加载到内存（请先解压提供的weibo.txt.zip)，进行基本的文本预处理，
# 如对所有微博内容进行去重，进行分词、去除停用词、标点等，最终建立一个以微博为单位进行分词的二维列表。注意，weibo.txt一行为一条微博的属性，用\t分隔后，第二个元素为微博内容。（提供的weibo.txt包含大量重复和标点等，需要仔细预处理，否则会影响后面的嵌入模型训练。）
    def _pre_process(self): # 文件预处理成一个txt文本，方便训练模型直接使用
        words_path = self.cache_path
        # 免去处理已有文件，一次处理
        if os.path.exists(self.cache_path):
            return words_path

        stopset = set([  # 用集合加速查询
            '，','【','】','#','s','1','2','3','4','5','6','7','8','9','MIUI','@','_','(',')','￣','！','[',']','-',
            '“','”','p','ID',':','：','~','td','t','d','//','/','？','。','%','>>','>','《','》','、','+','ing','TNND','〜',
            '🎂','⊙','o','(⊙o⊙)','⊙o⊙','.','..','..........','℃','H','……','^','*','$','￥','↗','↖','ω','↖(^ω^)↗','😃','…','""','"','Y',
            'http','cn','com','!',',','的','了','～','...','在','.','；',';','◆','「','」','##','?','∀','·','ｲ','&','---',',','≧','▽','≦','`',
            '(',')','（','）'
        ])

        chunks = pd.read_csv(
            self.file_path,
            sep='\t',
            header=0,
            names=['text'],
            chunksize=10000,
            usecols=[1],
            dtype={'text': str},
            engine='c',
            on_bad_lines='skip'
        )

        words = []
        jieba.enable_parallel(4)  # 使用 4 个 CPU 核心
        for chunk in tqdm(chunks, desc="Processing Text"):
            texts = set(chunk['text'].dropna())  # 用 set() 代替 unique()
            # 除去url 和表情符
            cleaned_texts = []
            for text in texts:
                # 去除URL
                text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
                # 去除特殊符号和表情符号
                text = re.sub(r'\[.*?\]', '', text)
                # 去除emoji
                text = self._remove_emojis(text)
                cleaned_texts.append(text)
            words.extend([
                [w for w in jieba.lcut(str(text)) if w not in stopset]
                for text in cleaned_texts
            ])
        with open(self.cache_path, 'w', encoding='utf-8')as f:
            for sentence in words:
                if not sentence:  # 跳过空句子
                    continue
                f.write(' '.join(sentence)+'\n')
        print("Cache file saved.")        
        self.processed_words = words
        return words_path # cache_path

###三########################################################################################
#在上述类加入一个方法_get_word2vec_model来利用2中构建的微博二维列表来训练Word2Vec模型，可参照demo使用gensim完成Word2Vec模型的建立。
    def _get_word2vec_model(self):
        if os.path.exists(self.model_path):
            print(f"Loading existing model from {self.model_path}")
            return Word2Vec.load(self.model_path)
        
        words_path = self._pre_process()
        if not words_path:  # 避免训练空模型
            raise ValueError("No valid words to train the model.")
        
        start_time = time.time()
        print("开始训练模型...")
        
        # 使用LineSentence读取大型文本文件(逐行读取，避免内存不足)
        sentences = LineSentence(words_path)
        
        model = Word2Vec(
            #list(tqdm(words_list, desc="Training Word2Vec")),#使用 tqdm 显示 Word2Vec 训练进度
            #sentences=tqdm(words_list,desc="Training Word2Vec", total=len(words_list)),
            sentences=sentences,
            vector_size=self.len_vec,
            window=self.size_window,
            min_count=5,
            workers=8,          # 使用多线程
            sg=1,               # 使用skip-gram模型(1), 0表示CBOW
            epochs=50,          # 可选：设置训练轮数10    
            #compute_loss=True,  # 可选：显示训练损失
            hs=0,               # 使用负采样
            negative=5,          # 负采样数量
            sample=1e-3         # 高频词下采样阈值
        )
        model.save(self.model_path)
        # 保存词向量(纯文本格式，可用于其他工具)
        model.wv.save_word2vec_format('/Users/wtsama/Documents/code/code2/python_assignment/week5/weibo_word2vec.vec', binary=False)
        
        end_time = time.time() # 时间戳
        print(f"训练完成! 耗时: {end_time-start_time:.2f}秒")
        print(f"模型已保存至: {self.model_path}")
        print(f"词向量已保存至: /Users/wtsama/Documents/code/code2/python_assignment/week5/weibo_word2vec.vec")
        return model

###四########################################################################################
#在上述类加入一个方法get_similar_words来利用训练得到的word2vec模型来推断相似词汇。如输入一个任意词，使用model.similarity方法可以来返回与目标词汇相近的一定数目的词。
    def get_similar_words(self, word):
        model = self._get_word2vec_model()
        return model.wv.most_similar(word, topn=10)
    def get_least_similar_words(self,word):
        model = self._get_word2vec_model()
        return model.wv.most_similar(word, topn=10, negative=word)

###六######################################################################################
#词向量能够将每个词定位为高维空间中的一个点，且不同词间的“差异”可以通过点间的距离来反应。在类加再增加一个方法vis_word_tsne
# 使用TSNE算法，对与某个输入词的最相关以及最不相关的词语（用参数来控制数目）进行降维和可视化。    
    def vis_word_tsne(self,input_word):
        model=self._get_word2vec_model()
        most_similar = model.wv.most_similar(input_word,topn=10)
        least_similar = model.wv.most_similar(input_word,topn=10,negative=input_word)
        
        #       np.array([model.wv[word] for word, similarity in most_similar + least_similar])
        vectors=np.array([model.wv[w]for w,similarity in most_similar+least_similar])
        w_list = [w for w, similarity in most_similar+least_similar]
        # 使用t-SNE算法对词向量进行降维
        tsne = TSNE(n_components=2, perplexity=15)
        vectors_tsne = tsne.fit_transform(vectors)
        # 可视化降维后的词向量
        #fonts
        STH = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')
        
        fig, ax = plt.subplots()
        ax.set_title(word, fontproperties = STH)
        # t-SNE降维至2维
        ax.scatter(vectors_tsne[:10, 0], vectors_tsne[:10, 1], color='purple',label = 'most_simi')
        ax.scatter(vectors_tsne[10:, 0], vectors_tsne[10:, 1], color='orange', label = 'least_simi')
        ax.legend()
        # 打印词
        for i, w in enumerate(w_list):
            ax.annotate(w, (vectors_tsne[i, 0], vectors_tsne[i, 1]),fontproperties = STH)
        plt.show()

if __name__ == "__main__":
    text_ana = TextAnalyzer(
        file_path='/Users/wtsama/Documents/code/code2/python_assignment/week5/weibo.txt',
        model_path='/Users/wtsama/Documents/code/code2/python_assignment/week5/weibo_word2vec.model',
        len_vec=200,
        size_window=5,
        cache_path='/Users/wtsama/Documents/code/code2/python_assignment/week5/processed_words.txt'
    )
    word='旅行'
    print(f"和{word}最相似的10个词：",text_ana.get_similar_words(word))
    print(f"和{word}最不相似的10个词：",text_ana.get_least_similar_words(word))
    text_ana.vis_word_tsne(word)
    
