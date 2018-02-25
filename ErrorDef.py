
class ErrorDef:
    #Error types are SPEL / ART / ArtChk / SVACOMP /SVABASE / OTHER
    ErrorType = ""
            
    def __init__(self,etype):
        self.ErrorType = etype
    
    #Determine the Article Determiner  error        
    def checkDeterminer(self,indval,syntval,sentDet):
        ind = indval
        #checking Sibling items for NP so that and also finding Determiner
        condition = True
        foundDet  = False
        lstParse  = []
        lstWords  = []
        detText   = ""
        probEnd   = 0
        probStart = 0
    
        while (condition):
            #print(ind , "problem here")
            condition = 'NP' not in sentDet.parse[ind]
            if(ind==0):
                condition = False
            lstWords.append(sentDet.words[ind])
            lstParse.append(sentDet.parse[ind])
            if (sentDet.synt[ind] in ['DT','PRP$']):
                foundDet = True
                detText  = sentDet.words[ind]
            probStart= ind
            #print(self.synt[ind],self.words[ind],self.parse[ind],condition)
            ind= ind-1
            probEnd = indval
        if foundDet is False:
            #print("problem found")            
            return [probStart,probEnd,syntval,self.ErrorType]
        else:
            foundDet = False
            self.ErrorType = "ArtChk"
            if detText in ['a','an','the','']:
                return [probStart,probEnd,syntval,self.ErrorType]
        return 0
        
    