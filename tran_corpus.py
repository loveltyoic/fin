from __future__ import print_function
from gensim.corpora import WikiCorpus

import codecs
import os
import six
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing
import os
LTP_DATA_DIR = '/home/zhli7/ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`

from pyltp import Segmentor
ext_dict = os.path.join(LTP_DATA_DIR, 'my_words')

segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, ext_dict)  # 加载外部字典
 
class Config:
    data_path = '/home/zhli7/'
    zhwiki_bz2 = 'zhwiki-latest-pages-articles.xml.bz2'
    zhwiki_raw = 'zhwiki_raw.txt'
    zhwiki_raw_t2s = 'zhwiki_t2s.txt'
    zhwiki_seg_t2s = 'zhwiki_seg.txt'
    embedded_model_t2s = 'zhwiki_embedding_t2s.model'
    embedded_vector_t2s = 'vector_t2s'
    
def dataprocess(_config):
    i = 0
    if six.PY3:
        output = open(os.path.join(_config.data_path, _config.zhwiki_raw), 'w')
    output = codecs.open(os.path.join(_config.data_path, _config.zhwiki_raw), 'w')
    wiki = WikiCorpus(os.path.join(_config.data_path, _config.zhwiki_bz2), lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        #if six.PY3:
        #    output.write(b' '.join(text).decode('utf-8', 'ignore') + '\n')
        #else:
        output.write(' '.join(text) + '\n')
        i += 1
        if i % 10000 == 0:
            print('Saved ' + str(i) + ' articles')
    output.close()
    print('Finished Saved ' + str(i) + ' articles')

def is_alpha(tok):
    try:
        return tok.encode('ascii').isalpha()
    except UnicodeEncodeError:
        return False


def zhwiki_segment(_config, remove_alpha=True):
    i = 0
    if six.PY3:
        output = open(os.path.join(_config.data_path, _config.zhwiki_seg_t2s), 'w', encoding='utf-8')
    output = codecs.open(os.path.join(_config.data_path, _config.zhwiki_seg_t2s), 'w', encoding='utf-8')
    print('Start...')
    with codecs.open(os.path.join(_config.data_path, _config.zhwiki_raw_t2s), 'r', encoding='utf-8') as raw_input:
        for line in raw_input.readlines():
            line = line.strip()
            i += 1
            print('line ' + str(i))
            text = line.split()
            if True:
                text = [w for w in text if not is_alpha(w)]
            word_cut_seed = [segmentor.segment(t) for t in text]
            tmp = ''
            for sent in word_cut_seed:
                for tok in sent:
                    tmp += tok + ' '
            tmp = tmp.strip()
            if tmp:
                output.write(tmp + '\n')
        output.close()
def word2vec(_config, saved=False):
    print('Start...')
    model = Word2Vec(LineSentence(os.path.join(_config.data_path, _config.zhwiki_seg_t2s)),
                     size=50, window=5, min_count=5, workers=multiprocessing.cpu_count())
    if saved:
        model.save(os.path.join(_config.data_path, _config.embedded_model_t2s))
        model.wv.save_word2vec_format(os.path.join(_config.data_path, _config.embedded_vector_t2s), binary=False)
    print("Finished!")
    return model
        
if __name__ == '__main__':
    config = Config()
    zhwiki_segment(config)
    #model = word2vec(config, saved=True)
    #dataprocess(config)
