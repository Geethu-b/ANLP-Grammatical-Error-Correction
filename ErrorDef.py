import inflect
p = inflect.engine()

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
    
    def checkSVACOMP(self, subj, subjind, verb, verbind, syntverb, sentDet):
        IS_KNOWN_PLURAL = False
        print(subj, verb)
        if subj == "I":
            if p.plural(verb) == "are":
                if verb != "am":
                    print("SVA problem found: ", subj, verb)
                    return [subjind,verbind,syntverb,self.ErrorType]
                else:
                    return 0
            else:
                IS_KNOWN_PLURAL = True
        elif subj in ["you", "they", "we"]:
            IS_KNOWN_PLURAL = True
        elif str(p.singular_noun(subj)) == "False":#subj is singular
            if syntverb == "VBZ":
                return 0
            if verb == "were":
                print("SVA problem found: ", subj, verb)
                return [subjind,verbind,syntverb,self.ErrorType]
            elif syntverb in ["VBD", "VBN", "MD"]:
                return 0
            else:
                print("SVA problem found: ", subj, verb)
                return [subjind,verbind,syntverb,self.ErrorType]
        IS_KNOWN_PLURAL = True		
        if IS_KNOWN_PLURAL:
            if syntverb in ["VBZ", "am"]:
                print("SVA problem found: ", subj, verb)
                return [subjind,verbind,syntverb,self.ErrorType]
            else:
                return 0
        print("WTF?")
	
    def checkSVACOMPplural(self, verb, verbind, syntval, sentDet):
        plural_verb = p.plural_verb(verb)
        print(plural_verb)
        if verb == plural_verb:
            return 0
        else:
            print("SVA Plural problem found: ", verb)
            return [verbind,verbind,syntval,self.ErrorType]
    
