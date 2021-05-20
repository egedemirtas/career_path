import json
import time

class Scrapper():
    """
    amazing scrapper that works 100% of the time
    """
    class state(object):
        """
        state of the scrapper
        """
        
        # numunivs = 0
        # currently = ""
        # curruniv = ""
        def __init__(self,dic={
            "numunivs":0,
            "currently":"",
            "curruniv":""
        }):
            self.numunivs = dic["numunivs"]
            self.currently = dic["currently"]
            self.curruniv = dic["curruniv"]
    #filenames
    FILENAME_UNIVERSITIES = "top50_uni_facet.json"  #made by ege
    FILENAME_DATAOUT = ""
    FILENAME_STATE = "scrapperstate.json"
    currentstate = state()

    def __init__(self):
        """
        docstring
        """
        file = open(self.FILENAME_STATE, encoding="utf-8", errors="ignore")
        self.currentstate = self.state(json.loads(file.read()))
        
        file.close()

    def saveState(self):
        file = open(self.FILENAME_STATE,'w', encoding="utf-8", errors="ignore")
        file.write(json.dumps(self.currentstate.__dict__))
        #file.write(json.dumps(scrapper.currentstate))
        file.close()
    
    def waitForTimeout(self):
        return time.sleep(1000*60*30)
    
    def __del__(self):
        self.saveState()
    
        

    def getCurrUniv(self) -> (str):
        """
        get the last left university
        """
        return self.currentstate.curruniv
    def setCurrUniv(self, univ):
        self.currentstate.curruniv = univ

