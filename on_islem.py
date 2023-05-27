import pandas as pd
import re
import snowballstemmer

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
 