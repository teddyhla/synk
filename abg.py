#this code should genearte abg values

import random

class newsgen:
    """this class allows generation of observation
    can select well or unwell status and then generate obs accordingly using a 
    method 'makeobs'
    """
    def __init__(self,status = 'well'):
        self.status = status.lower()
        self.avail_status = {
            'well': [rr_well, spo2_well, gas_well, sbp_well, dbp_well, hr_well, neuro_well, temp_well],
            'sick': [rr_unwell, spo2_unwell, gas_unwell, sbp_unwell, dbp_unwell, hr_unwell, neuro_unwell, temp_unwell]  
        }
        
    def makeobs(self,n):
        if self.status in self.avail_status:
            stat = self.avail_status[self.status]
            news = []
            news_calc = []
            for _ in range(n):
                rnews = [random.choice(sublist) for sublist in stat]
                news.append(rnews)
                rcalc = [rnews[0],rnews[1],rnews[2],rnews[3],rnews[5],rnews[6],rnews[7]]
                news_calc.append(rcalc)
            return {'t':list(range(1,n + 1)), self.status: news, 'for_calc':news_calc}
        else:
            raise ValueError(f'Selected status {self.status} is not available.')
    