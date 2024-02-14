from core.models import Tecnico
import pandas as pd


class TecnicoServices():

    def __init__(self):
        self.data = [(t.full_name, t.total_payment) for t in Tecnico.objects.all()]
        self.df = pd.DataFrame(self.data, columns=["tecnico", "total_pagado"])
        
        self.avg = 0
        self.max = 0
        self.min = 0
        
    def get_avg(self):
        if self.avg == 0:
            self.avg = self.df['total_pagado'].mean()
        return self.avg
    
    def get_max(self):
        if self.max == 0:
            self.max = self.df['total_pagado'].max()
        return self.max

    def get_min(self):
        if self.min == 0:
            self.min = self.df['total_pagado'].min()
        return self.min

    def get_technicians_lt_avg(self):
        df_query = self.df["total_pagado"] < self.get_avg()
        return self.df[df_query].values.tolist()
