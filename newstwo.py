# newstwo.py script
# this should generate fake observations 
# newsgen class can have status 'well','sick' and then will allow generation of news


import random

# to allow reproducibility
random.seed(24)

# custom function1 to generate the well observations
def unwellobs(x,y):
    """esentially to do anti-set  

    Args:
        x (list): list of all possible observation 
        y (list of well observations): list of well observations

    Returns:
        list: basically returns a list that is not in y from x. 
    """
    return [i for i in x if i not in y]


class NEWSgen:
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
    

def calcnews_score(l):
    """This is as per RCP NEWS2 algorithm
    takes an argument as a list and returns a tuple
    of news score component, sum and clinical risk. 
    MUST - -arguments fed has to be ORDERED. 
    rr,spo2,gas,sbp,pulse,neuro,temp

    Args:
        list (_type_): takes a list arguments and calculates news score

    Returns:
        tuple: returns a tuple, first value is NEWS score (integer) and second is clinical risk (categorical)
    """
    #FIRST PART : ASSIGN SCORES TO EACH DOMAIN
    # resp score
    print(f'rr is {l[0]}')
    if  not isinstance(l[0], (int)):
        resp_score = 'not_num'
    elif l[0] <= 8 or l[0]>= 25:
        resp_score = 3
    elif 9 <= l[0] <= 11:
        resp_score = 1
    elif 21 <= l[0] <= 24:
        resp_score = 2
    else:
        resp_score = 0
    
    # spo2
    print(f'spo2 is {l[1]}')
    if not isinstance(l[1],(int)):
        spo2_score = 'not_num'
    elif l[1] <= 91:
        spo2_score = 3
    elif 92 <= l[1] <= 93:
        spo2_score = 2
    elif 94 <= l[1] <= 95:
        spo2_score = 1
    else: 
        spo2_score = 0 
    
    # gas
    print(f'gas is {l[2]}')
    if l[2] == 'air':
        gas_score = 0
    elif l[2] == 'oxygen':
        gas_score = 2
    else: 
        gas_score = 'not_avail'
    
    #sbp 
    print(f'sbp is {l[3]}')
    if not isinstance(l[3],(int)):
        sbp_score = 'not_num'
    elif l[3] <= 90 or l[3] >= 220:
        sbp_score = 3
    elif 101 <= l[3] <= 110:       
        sbp_score = 1
    elif 91 <= l[3] <= 100:
        sbp_score = 2
    else:
        sbp_score = 0
    
    #pulse
    print(f'hr is {l[4]}')
    if not isinstance(l[4],(int)):
        hr_score = 'not_num',
    elif l[4] <= 40 or l[4] >= 131:
        hr_score = 3
    elif 111 <= l[4] <= 130:
        hr_score = 2
    elif 41 <= l[4] <= 50 or 91 <= l[4] <= 110:
        hr_score = 1
    else:
        hr_score = 0
        
    # neuro
    print(f'neuro stat is {l[5]}')
    if l[5] == 'alert':
        neuro_score = 0
    else: 
        neuro_score = 3
    
    #temp 
    print(f'temp is {l[6]}')
    if not isinstance(l[6],(int,float)):
        temp_score = 'not_num'
    elif 35.0 <= l[6]:
        temp_score = 3
    elif l[6] >= 39.1:
        temp_score = 2
    elif 35.1 <= l[6] <= 36.0 or 38.1 <= l[6] <= 39.0:
        temp_score = 1
    else:
        temp_score = 0
    
    ans = [resp_score, spo2_score, gas_score, sbp_score, hr_score, neuro_score, temp_score]
    # SECOND PART : ADD UP ALL NUMERIC GENEARTED FROM THIS DOMAIN
    
    total = 0 
    numeric_ans = [item for item in ans if isinstance(item, (int, float))]
    total = sum(numeric_ans)
    
    # THIRD PART : ASSIGN RISK LABEL BASED ON ABOVE TWO.
    if total > 7:
        risk = 'high'
    elif 5 <= total <= 6:
        risk = 'medium'
    elif 3 in numeric_ans:
        risk = 'low-medium'
    else:
        risk = 'low'
    
    return ans,total,risk

# Original domain of observations 
# in order rr = resp rate, hr = heart rate, sbp = systolic bp, dbp - diastolic bp
# temp = pt tempeature
# spo2 = oxygen saturation, gas = air or oxygen, neuro = consciousness

rr_domain = [i for i in range(1,61)]
hr_domain = [i for i in range(30,200)]
sbp_domain = [i for i in range(40,220)]
dbp_domain = [i for i in range(20,120)]
temp_domain = [i/10.0 for i in range(350,400)]
spo2_domain = [i for i in range(83,100)]
gas_domain = ['air','oxygen']
neuro_domain = ['alert','confused','verbal','pain','unconscious']

# WELL domain
rr_well = [i for i in rr_domain if 9 < i < 24]
hr_well = [i for i in hr_domain if 50 < i < 120]
sbp_well = [i for i in sbp_domain if 110 < i < 200]
dbp_well = [i for i in dbp_domain if 50 < i < 120]
temp_well = [i for i in temp_domain if 35.1 < i < 38.0]
spo2_well = [i for i in spo2_domain if i <92]
gas_well = ['air']
neuro_well = ['alert']


#UNWELL DOMAIN
rr_unwell = unwellobs(x = rr_domain, y= rr_well)
hr_unwell = unwellobs(x = hr_domain, y= hr_well)
sbp_unwell = unwellobs(x = sbp_domain, y= sbp_well)
dbp_unwell = unwellobs(x=dbp_domain, y= dbp_well)
temp_unwell = unwellobs(x=temp_domain, y=temp_well)
spo2_unwell = unwellobs(x=spo2_domain,y=spo2_well)
gas_unwell = ['oxygen']
neuro_unwell = ['confused','verbal','pain','unconscious']




#TESTING
unwellpts = NEWSgen(status ='sick')
dit = unwellpts.makeobs(5)

wellpts = NEWSgen(status = 'well')
dit2 = wellpts.makeobs(5)

# NOW LETS TEST IF CUSTOM FUNCTION NEWSCALC PASSES

x = [23, 90, 'air', 145, 76, 'alert', 37.0]

r1,r2,r3 = calcnews_score(x)

# this works ! :)