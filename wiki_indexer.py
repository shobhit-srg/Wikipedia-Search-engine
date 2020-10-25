# root_path = '/home/srg/Desktop/3sem/IRE/MP1/'
import sys
import xml.sax
import xml.parsers.expat
import time 
start=time.time()
root_path=sys.argv[1]
index_loc=sys.argv[2]
indexstat_loc=sys.argv[3]
import os
if not os.path.exists(index_loc):
    os.makedirs(index_loc)
# fout = index_loc+"Index.txt"
fout = os.path.join(index_loc,"invertedindex.txt")         

title_array=[]
text_array=[]
inverted_index={}
total_xml_count=0
stemming_word={}
field=["t","c","i","l","r","b"]
class ParseHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.count=0
    self.curpath = []
    self.CurrentData = ""
    self.title = ""
    self.text = ""
    self.f=0
    self.title_words=defaultdict(int)
    self.cat_words=defaultdict(int)
    self.info_words=defaultdict(int)
    self.link_words=defaultdict(int)
    self.body_words=defaultdict(int)
    self.ref_words=defaultdict(int)
    self.remain_words=defaultdict(int)
  def startElement(self, name, attrs):
    # print(name,attrs)
    self.CurrentData = name
    if name == "page":
      self.f = self.f + 1
      # print(self.f)

  # indexing in inverted list start from 1
  def endElement(self, name):
    flag=0
    # print(self.CurrentData)
    if self.CurrentData == "title":
      self.count = self.count + 1
      if(self.count%1000==0):
         print(self.count/1000,time.time()-start) 
      # print(self.count)
      # print("tit",self.count,self.title)
      # title_array.append(self.title)
      self.title_words=pre_process_title(self.title)
    elif self.CurrentData == "text":
      if "#REDIRECT" not in self.text:
        self.cat_words,self.info_words,self.link_words,self.ref_words,self.remain_words=pre_process_text(self.text)
      # print(self.cat_words)
      # print(self.info_words)
      # print(self.link_words)
      # print(self.ref_words)
      # text_array.append(self.text)
      self.text= ""
      if len(self.title_words)>0:
        for w in self.title_words:
          s=str(self.count)+str(field[flag])+str(self.title_words[w])
          lst=[s]
          # print(w,lst)
          if w not in inverted_index:
            inverted_index[w]=[]
          inverted_index[w].extend(lst)
      flag=1
      if len(self.cat_words)>0:
        for w in self.cat_words:
          s=str(self.count)+str(field[flag])+str(self.cat_words[w])
          lst=[s]
          # print(w,lst)
          if w not in inverted_index:
            inverted_index[w]=[]
          inverted_index[w].extend(lst)
      flag=2
      if len(self.info_words)>0:
        for w in self.info_words:
          s=str(self.count)+str(field[flag])+str(self.info_words[w])
          lst=[s]
          # print(w,lst)
          if w not in inverted_index:
            inverted_index[w]=[]
          inverted_index[w].extend(lst)
      flag=3
      if len(self.link_words)>0:
        for w in self.link_words:
          s=str(self.count)+str(field[flag])+str(self.link_words[w])
          lst=[s]
          # print(w,lst)
          if w not in inverted_index:
            inverted_index[w]=[]
          inverted_index[w].extend(lst)
      flag=4
      if len(self.ref_words)>0:
        for w in self.ref_words:
          s=str(self.count)+str(field[flag])+str(self.ref_words[w])
          lst=[s]
          # print(w,lst)
          if w not in inverted_index:
            inverted_index[w]=[]
          inverted_index[w].extend(lst)
      flag=5
      if len(self.remain_words)>0:
        for w in self.remain_words:
          s=str(self.count)+str(field[flag])+str(self.remain_words[w])
          lst=[s]
          # print(w,lst)
          if w not in inverted_index:
            inverted_index[w]=[]
          inverted_index[w].extend(lst)
      # print(inverted_index)
    self.CurrentData= ""

  def characters(self, data):
    if self.CurrentData == "title":
      self.title = data
    elif self.CurrentData == "text":
      self.text += data


from collections import defaultdict
import re
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
import string 
def Num_punch_removal(wordlist):
  fr=0
  res=[]
  for wrd in wordlist:
    s = ""
    for w1 in wrd:
      if w1 in set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
        fr=fr+1
        continue
      if w1 in set(list(string.punctuation) + ['\n', '\t', " "]):
        if len(s) and s.isalpha():
            res.append(s)
        s = ""
        continue
      s += w1
    if len(s) and s.isalpha():
      res.append(s)
  return res

stemmer = nltk.stem.SnowballStemmer('english')
# stemmer = nltk.stem.PorterStemmer()

def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

def stop_words(wordlist):
  res=[]
  for w in wordlist:
    if len(w) <= 1 or w in STOP_WORDS:
      continue
    if "www" in w or "https" in w or "net" in w or "com" in w:
      continue
    if(hasNumbers(w)):
      continue
    if w in stemming_word:
      res.append(stemming_word[w])
    else:  
      w1=stemmer.stem(w)
      stemming_word[w]=w1
      res.append(w1)
  return res




from nltk.stem import WordNetLemmatizer
p = re.compile("[^a-zA-Z]")

def pre_process_title(title):
  global total_xml_count
  title=title.lower()
  title+="\n"
  tokens = re.findall("\d+|[\w]+",title)
  # token=re.split(p,title)
  tokens = [i.lower() for i in tokens]
  total_xml_count = total_xml_count + len(tokens)
  token1 = Num_punch_removal(tokens)
  token2 = stop_words(token1)
  # print(token2)
  title_words=defaultdict(int)
  for w in token2:
    if w != "":
      title_words[w]=title_words[w]+1
  return title_words  


def pre_process_text(text):
  # print(text)
  # category ki list
  cat_words=defaultdict(int)
  info_words=defaultdict(int)
  link_words=defaultdict(int)
  body_words=defaultdict(int)
  ref_words=defaultdict(int)
  body_words1=defaultdict(int)
  global total_xml_count
  cat=re.findall("\[\[Category:(.*?)\]\]",text)
  # print(cat)
  total_xml_count = total_xml_count + len(cat)
  cat = Num_punch_removal(cat)
  # print(cat1)
  # cat_str=""
  # for w in cat:
    # cat_str += w
  # cat=re.split(r'[^A-Za-z0-9]+',cat_str)
  cat2 = stop_words(cat)
  cat2 = [i.lower() for i in cat2]
  # print("cat2",cat2)
  for w in cat2:
    cat_words[w]=cat_words[w]+1

  # infobox ki list
  info=[]
  info_str = ""
  info_array = text.split("{{Infobox")
  if len(info_array) > 1:
    info_array=info_array[1:]
    # print(info_array)
    for i in range(len(info_array)):
      element=info_array[i].split('\n')
      for line in element:
        if line == "}}":
          break
        info_str += line      
  info_tokens=re.split(r'[^A-Za-z0-9]+', info_str)
  total_xml_count = total_xml_count + len(info_tokens)
  # print(info_tokens)
  # info_tokens = Num_punch_removal(info_tokens)
  info_t2 = stop_words(info_tokens)
  info_t2 = [i.lower() for i in info_t2]
  r2 = re.compile(r'{{infobox(.*?)}}',re.DOTALL)

  for w in info_t2:
    if w not in info_words:
      info_words[w]=0
    info_words[w] = info_words[w] + 1
  
  # links ki lists
  # text=text.lower()
  link_string=""
  links=text.split("== External links ==")
  # print(len(links))
  if len(links) > 1:
    links=links[1].split("\n")
    # print("l.",links)
    for line in links:
      if line and line[0]=='*':
        link_string += line
  
  links1=text.split("==External links==")
  if len(links1) > 1:
    links1=links1[1]
    links1=links1.split("\n")
    # print(links)
    for line in links1:
      if line and line[0]=='*':
        link_string += line
    
  link_tok = re.split(r'[^A-Za-z0-9]+', link_string)
  total_xml_count = total_xml_count + len(link_tok)
  # link_tok = Num_punch_removal(link_tok)
  link_t2 = stop_words(link_tok)
  link_t2 = [i.lower() for i in link_t2]
  r1 = re.compile(r'\[\[Category:(.*?)\]\]',re.DOTALL)
  for w in link_t2:
    link_words[w]=link_words[w]+1


 # references ki list
  # text=text.lower()
  refs=text.split("==References==")
  ref_str=""
  if len(refs)>1:
    refs=refs[1]
    # print(refs)
    refs=refs.split("==")
    ref_str=refs[0]
  ref_tok = re.split(r'[^A-Za-z0-]+9', ref_str)
  total_xml_count = total_xml_count + len(ref_tok)
  ref_tok = Num_punch_removal(ref_tok)
  ref_t2 = stop_words(ref_tok)
  ref_t2 = [i.lower() for i in ref_t2]

  for w in ref_t2:
    if w =="reflist" or w == "ref" or w == "name":
      continue
    ref_words[w]=ref_words[w]+1

  # full_body_tok = re.split(r'[^A-Za-z0-9]+', text)
  # f_body_t1 = Num_punch_removal(full_body_tok)
  # f_body_t2 = stop_words(f_body_t1)
  # f_body_t2 = [i.lower() for i in f_body_t2]

  # for w in f_body_t2:
    # body_words[w]=body_words[w]+1
  
  body = r1.sub(' ', text)
  r3 = re.compile(r'{{')
  body = r2.sub(' ', body)
  body = r3.sub(' ', body)
  body_tok1 = re.split(r'[^A-Za-z0-9]+', body)
  total_xml_count = total_xml_count + len(body_tok1)
  table = str.maketrans('', '', string.punctuation)
  body_tok1 = [w.translate(table) for w in body_tok1]
  body_t2_1 = stop_words(body_tok1)
  body_t2_1 = [i.lower() for i in body_t2_1]
  for w in body_t2_1:
    body_words1[w]=body_words1[w]+1
  
  
  # print(cat_words)
  # print(info_words) 
  # print(link_words)  
  # print(ref_words)
  # print(body_words1)
  # print(body_words)




  return cat_words,info_words,link_words,ref_words,body_words1


parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
  
Handler = ParseHandler()
parser.setContentHandler( Handler )
parser.parse(root_path)

# print(len(title_array))
# print(title_array)
# print(len(text_array))




# fout = root_path+"InvertedIndex.txt"
fo = open(fout, "w")

def listToString(s):   
  str1 = " "   
  return (str1.join(s)) 
for k, v in inverted_index.items():
  x=listToString(v)
  x=x.replace(" ",",")
  fo.write(str(k) + ':'+ x + '\n')
fo.close()

end=time.time()
# print("time",end-start)
# print(len(inverted_index))


fout = indexstat_loc
fo = open(fout, "w")
fo.write(str(total_xml_count) + '\n' + str(len(inverted_index)))
fo.close()
