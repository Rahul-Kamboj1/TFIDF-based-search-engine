'''
@author: RAHUL
'''
import sys
import re
from collections import defaultdict
from array import array

class CreateIndex:

    def __init__(self):
        self.index=defaultdict(list)    #the inverted index

    
    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        f=open('C:/Users/RAHUL/AppData/Local/Programs/Python/Python35/Scripts/se/stopwords.dat', 'r',encoding="utf8")
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def getTerms(self, line):
        '''given a stream of text, get the terms from the text'''
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        line=[x for x in line if x not in self.sw]  #eliminate the stopwords
        return line


    def parseCollection(self):
        ''' returns the id, title and text of the next page in the collection '''
        doc=[]
        for line in self.collFile:
            if line=='</page>\n':
                break
            doc.append(line)
        
        curPage=''.join(doc)
        pageid=re.search('<id>(.*?)</id>', curPage, re.DOTALL)
        pagetitle=re.search('<title>(.*?)</title>', curPage, re.DOTALL)
        pagetext=re.search('<text>(.*?)</text>', curPage, re.DOTALL)
        
        if pageid==None or pagetitle==None or pagetext==None:
            return {}

        d={}
        d['id']=pageid.group(1)
        d['title']=pagetitle.group(1)
        d['text']=pagetext.group(1)

        return d


    def writeIndexToFile(self):
        
        '''write the inverted index to the file'''
        f=open('C:/Users/RAHUL/AppData/Local/Programs/Python/Python35/Scripts/se/indexFile.txt', 'w',encoding="utf8")
        
        for term in self.index.keys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            print (f, ''.join((term,'|',';'.join(postinglist))))
            new=''.join((term,'|',';'.join(postinglist)))
            
            f.write(new)
            f.write('\n')
            
            
            
        f.close()
 
    def createIndex(self):
        '''main of the program, creates the index'''
        
        self.collFile=open('C:/Users/RAHUL/AppData/Local/Programs/Python/Python35/Scripts/se/testCollection.dat','r',encoding="utf8")
        self.getStopwords()
        
        
        
        pagedict={}
        pagedict=self.parseCollection()
        #main loop creating the index
        while pagedict != {}:                    
            lines='\n'.join((pagedict['title'],pagedict['text']))
            pageid=int(pagedict['id'])
            terms=self.getTerms(lines)
            
            #build the index for the current page
            termdictPage={}
            for position, term in enumerate(terms):
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[pageid, array('I',[position])]
            
            #merge the current page index with the main index
            for termpage, postingpage in termdictPage.items():
                self.index[termpage].append(postingpage)
            
            pagedict=self.parseCollection()


        
            
        self.writeIndexToFile()
        
    
if __name__=="__main__":
    c=CreateIndex()
    c.createIndex()
    

