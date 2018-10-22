'''

@author: RAHUL
'''

import sys
import re
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer 
 



class QueryIndex:

    def __init__(self):
        self.index={}


    def intersectLists(self,lists):
        if len(lists)==0:
            return []
        #start intersecting from the smaller list
        lists.sort(key=len)
        return list((lambda x,y: set(x)&set(y),lists))
        
    
    def getStopwords(self):
        f=open('C:/Users/RAHUL/AppData/Local/Programs/Python/Python35/Scripts/se/stopwords.dat', 'r',encoding="utf8")
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
       

    def getTerms(self, line):
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        line=[x for x in line if x not in self.sw]
        
        return line
        
    
    def getPostings(self, terms):
        #all terms in the list are guaranteed to be in the index
        return [ self.index[term] for term in terms ]
    
    
    def getDocsFromPostings(self, postings):
        #no empty list in postings
        return [ [x[0] for x in p] for p in postings ]


    def readIndex(self):
        f=open('C:/Users/RAHUL/AppData/Local/Programs/Python/Python35/Scripts/se/indexFile.txt', 'r',encoding="utf8");
        for line in f:
            line=line.rstrip()
            term, postings = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
            postings=postings.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
            postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
            postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]   #final postings list  
            self.index[term]=postings
        f.close()
    

    def ftq(self,q):
        """Free Text Query"""
        
        q=self.getTerms(q)
        if len(q)==0:
            print ('')
            return
        
        li=set()
        for term in q:
            try:
                
                p=self.index[term]
                p=[x[0] for x in p]
                li=li|set(p)
                
            except:
                
                pass
            
        
        li=list(li)
        li=sorted(li)
        print("******************************************************")
        fetch_doc(li,q)
        
        
        
        


    def pq(self,q):
        '''Phrase Query'''
        originalQuery=q
        q=self.getTerms(q)
        if len(q)==0:
            print ('')
            return
        elif len(q)==1:
            self.owq(originalQuery)
            return

        phraseDocs=self.pqDocs(q)

        print (' '.join(map(str, phraseDocs)))    #prints empty line if no matching docs
        
        
 

    def queryIndex(self):
        self.readIndex()  
        self.getStopwords() 

        while True:
            print("please search:")
            q=sys.stdin.readline()
           
            if q=='':
                break
            self.ftq(q)

            
def  str_to_int(id):
        return int(id)        


def fetch_doc(id_list,y):
    
    
    df=pd.read_pickle('C:\\Users\RAHUL\\AppData\\Local\\Programs\\Python\\Python35\\Scripts\\myDataframe')
    df['id']=df['id'].apply(str_to_int)
    
    list1=[' '.join(y)]
    for i in id_list:
        list1.append(df[df['id']==i]['text'].iloc[0])
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train=tfidf_vectorizer.fit_transform(list1)
    cosine_similarities=cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    i=related_docs_indices[0][::-1][0:7]


    print("Top 6 results for your query:",list1[i[0]])
    print("\n")

    for number,j in enumerate(i[1:]):
    
        print(number,":",list1[j])
        print("---------------------------------")
            
if __name__=="__main__":
    q=QueryIndex()
    q.queryIndex()

    
    
    
    
