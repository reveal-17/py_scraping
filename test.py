import requests  
from bs4 import BeautifulSoup  
import pandas as pd  
import time

list_df = pd.DataFrame(columns=['歌詞']) 

base_url = 'https://www.uta-net.com/'  
url = 'https://www.uta-net.com/artist/1048/'  
response = requests.get(url)  
soup = BeautifulSoup(response.text, 'lxml')  
links = soup.find_all('td', class_='side td1')  

for link in links:  
  a = base_url + (link.a.get('href'))  
  response = requests.get(a)  
  soup = BeautifulSoup(response.text, 'lxml')  
  lyrics = soup.find('div', itemprop='lyrics')  
  lyric = lyrics.text  
  lyric = lyric.replace('\n','')  
  # サーバ負荷防止で１秒待機  
  time.sleep(1)  

  # 取得した歌詞をDataFrameに追加  
  tmp_se = pd.DataFrame([lyric], index=list_df.columns).T  
  list_df = list_df.append(tmp_se)  

# csv保存  GPUにしないとエラーに
list_df.to_csv('list.csv', mode = 'a', encoding='utf-8')  

!pip install janome 
from janome.tokenizer import Tokenizer  

df_file = pd.read_csv('list.csv', encoding='utf-8')  
lyrics = df_file['歌詞'].tolist()  

t = Tokenizer()  
results = []  

for s in lyrics:  
  tokens = t.tokenize(s)  
  r = []  

  for tok in tokens:  
    if tok.base_form == '*':  
      word = tok.surface  
    else:  
      word = tok.base_form  

    ps = tok.part_of_speech  
    hinshi = ps.split(',')[0]  

    if hinshi in ['名詞', '形容詞', '動詞', '副詞']:  
      r.append(word)  

  rl = (' '.join(r)).strip()
  results.append(rl)  
  # 余計な文字コードを置き換え  
  result = [i.replace('\u3000', '') for i in results]  

text_file = 'wakati_list.txt'  
with open(text_file, 'w', encoding='utf-8') as fp:  
  fp.write("\n".join(result))  

from wordcloud import WordCloud  

text_file = open('wakati_list.txt', encoding='utf-8')  
text = text_file.read()  

# 日本語フォント指定  
!apt-get -y install fonts-ipafont-gothic
fpath = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'

#無意味そうな単語除去  
stop_words = ['そう', 'ない', 'いる', 'する', 'まま', 'よう', 'てる', 'なる', 'こと', 'もう', 'いい', 'ある', 'ゆく', 'れる']  

wordcloud = WordCloud(background_color='white', colormap='autumn', font_path=fpath, width=800, height=600, stopwords=set(stop_words)).generate(text)  

wordcloud.to_file('./wordcloud.png')  
