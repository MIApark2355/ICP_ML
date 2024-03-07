
class Patient:
    def __init__(self, Hct, hAbp, hIcp):
        self.Hct = Hct
        self.hAbp = hAbp
        self.hIcp = hIcp
    
    def __str__(self) -> str:
        return f"HCT : {self.Hct} \n hABP : {self.hAbp} \n hICP : {self.hIcp}"