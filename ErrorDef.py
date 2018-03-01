import spelchek
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
        #subj = subj.lower()
        verb = verb.lower()
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
        elif subj.lower() in ["you", "they", "we", "both", "most"]:
            IS_KNOWN_PLURAL = True
        elif str(p.singular_noun(subj)) == "False":#subj is singular
            IS_KNOWN_PLURAL = False
        elif subj.lower() in ["nothing", "this"]:
            IS_KNOWN_PLURAL = False
        else:
            IS_KNOWN_PLURAL = True	#NNS NNPS
        #print(IS_KNOWN_PLURAL)
        if IS_KNOWN_PLURAL:
            if syntverb in ["VBZ"]:
                print("SVA problem found: ", subj, verb)
                return [subjind,verbind,syntverb,self.ErrorType]
            elif verb in ["was"]:
                print("SVA problem found: ", subj, verb)
                return [subjind,verbind,syntverb,self.ErrorType]
            else:
                #print(subj)
                return 0
        else:
            if syntverb == "VBZ":
                #print(subj)
                return 0
            elif verb == "were":
                print("SVA problem found: ", subj, verb)
                return [subjind,verbind,syntverb,self.ErrorType]
            elif syntverb in ["VBD", "VBN", "MD"]:
                #print(subj)
                return 0
            else:
                print("SVA problem found: ", subj, verb)
                return [subjind,verbind,syntverb,self.ErrorType]

        print("This should not happen?")
	
    def checkSVACOMPplural(self, verb, verbind, syntval, sentDet):
        plural_verb = p.plural_verb(verb)
        print(plural_verb)
        if verb == plural_verb:
            return 0
        else:
            print("SVA Plural problem found: ", verb)
            return [verbind,verbind,syntval,self.ErrorType]
        
    def checkSpel(self, indval,word,sentDet):
        
        word = word.lower()
        checkedWord =spelchek.correct(word) 
        # not spell checked words
        if word in [',','.',"'"]:
            return 0
        if checkedWord == word:
            return 0
        else:
            suggList = spelchek.guesses(word)
            suggList.append(checkedWord)
            return [indval,indval+1,suggList,self.ErrorType]

    def checkOther(self,indval,syntval,sentDet):
        validtags = ['JJ','JJR','JJS','NNS','NN','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBZ']
        if syntval in validtags:
            return [indval,indval+1,syntval,self.ErrorType]
        else:
            return 0    
        

      
    
