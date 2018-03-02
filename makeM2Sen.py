import sentence as sent
import SentenceDetailsModified as sentModi
import pickle

def save_obj(obj, name ):
    #with open('obj/'+ name + '.pkl', 'wb') as f:
        fh = open(name+'.pkl',"wb")
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    fh = open(name+'.pkl',"rb")
    return pickle.load(fh)

def readPickleFileSentdet(pickleFileName):    
    #create a list of object of Sentence details
    lstSentencedet = load_obj(pickleFileName)
    return lstSentencedet

#read the sentence detail
lstSentencedet = readPickleFileSentdet("all")   

#function for generation of list of words
sentLst        = sent.Sentences()
#looping through the sentene details objects
for Index in range(0,1312):
    sentDet = lstSentencedet[Index]
    sentLst.addSentence(sentDet.getWords())

sentLst.printSentences()
##writing to a file 
fileW = open("m2file.txt","w")
fileW.write(sentLst.outStr)
fileW.close()