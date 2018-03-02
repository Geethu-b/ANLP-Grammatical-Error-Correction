import sentence as sent
import SentenceDetailsModified as sentModi
import pickle

#Saves a given object under a given name as a .pkl file
#input:
#	obj		the given object
#	name	a string containing the name the object is saved under
def save_obj(obj, name ):
    #with open('obj/'+ name + '.pkl', 'wb') as f:
        fh = open(name+'.pkl',"wb")
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)

#Loads a .pkl file of a given name
#input:
#	name			the name of the .pkl file
#output:
#	pickle.load(fh)	the content of the .pkl file
def load_obj(name ):
    fh = open(name+'.pkl',"rb")
    return pickle.load(fh)

#Creats a list of objects of Sentence Details from a .pkl file
#input:
#	name			the name of the .pkl file
#output:
#	lstSentencedet	the list of Sentence Details
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