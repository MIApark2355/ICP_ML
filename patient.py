
class Patient:
    def __init__(self, avg_abp, avg_icp, hct, hAbp, hIcp):
        self.avg_abp = avg_abp
        self.avg_icp = avg_icp
        self.hct = hct
        self.hAbp = hAbp
        self.hIcp = hIcp
    
    def __str__(self) -> str:
        return f"Average ABP : {self.avg_abp} \n Average ICP : {self.avg_icp} \n HCT : {self.hct} \n hABP : {self.hAbp} \n hICP : {self.hIcp}"