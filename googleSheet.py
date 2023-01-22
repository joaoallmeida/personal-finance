import gspread

class Sheet:
    def __init__(self) -> None:
        
        self.gc = gspread.service_account()
        
        pass
    
    def googleSheet(self,fileName,sheet=None):
        
        sh = self.gc.open(fileName)
        
        if sheet != None:
            worksheet = sh.worksheet(sheet)
        else: 
            worksheet = sh.get_worksheet(0)
        
        return worksheet
        