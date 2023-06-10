import pandas as pd
import re
import snowballstemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec


# sayısal deüerlerin kaldırılması
def remove_numeric(value):
    bfr = [item for item in value if not item.isdigit()]
    bfr = "".join(bfr)
    return bfr


# Emojilerin Kaldırılması
def remove_emoji(value):
    bfr = re.compile("[\U00010000-\U0010ffff]",flags = re.UNICODE)
    bfr = bfr.sub(r'',value)
    return bfr


# Tek Karakterli İfadelerin Kaldırılması
def remove_singe_chracter(value):
    return re.sub(r'(?:^| )\w(?:$| )','',value)

# Noktalama İşaretlerinin Kaldırılması
def remove_noktalama(value):
    return re.sub(r'[^\w\s]','',value)

# Linklerin Kaldırılması
def remove_link(value):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',value)
    
# Hashtaglerin Kaldırılması
def remove_hashtag(value):
    return re.sub(r'#[^\s]+','',value)

# Kullanıcı Adlarının Kaldırılması
def remove_username(value):
    return re.sub('@[^\s]+','',value)
# Kök İndirgeme ve stop words işlemleri
def stem_word(value):
    stemmer = snowballstemmer.stemmer("turkish")
    value = value.lower()
    value = stemmer.stemWords(value.split())
    stop_words=['acaba', 'ama', 'aslinda', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz',
                'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi',
                'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'm', 'mu', 'mü', 'nasil', 'ne', 'neden',
                'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'su',
                'tum', 've', 'veya', 'ya', 'yani', 'bir', 'iki', 'üç', 'dört', 'beş', 'alti', 'yedi', 'sekiz', 'dokuz', 'on']
    value = [item for item in value if not item in stop_words]
    value=' '.join(value)
    return value
# Ön işleme
def pre_processing(value):
    return [remove_numeric(remove_emoji
                          (remove_singe_chracter
                           (remove_noktalama
                            (remove_link
                             (remove_hashtag
                              (remove_username
                               (stem_word(word)))))))) for word in value.split()]

#Boşlukların Kaldırılması
def remove_space(value):
    return[item for item in value if item.strip()]
 
# Bag of Words model
def bag_of_words(value) : 
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(value)
    return X.toarray().tolist()

# Tf-idf model

def tfidfmodel(value):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(value)
    return X.toarray().tolist()

# Word2Vec Model
def word2vec(value):
    model = Word2Vec.load("C:/Users/frknq/Code/NLP/NLP_Proje/word2vec.model")
    bfr_list = []
    bfr_len = len(value)

    for k in value:
        bfr = model.wv.key_to_index[k]
        bfr = model.wv[bfr]
        bfr_list.append(bfr)

    bfr_list = sum(bfr_list)
    bfr_list = bfr_list/bfr_len
    return bfr_list.tolist()
    