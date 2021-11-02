import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
from matplotlib.legend_handler import HandlerLineCollection,HandlerBase


def write_files_precontrol(t):
    forcing = 'forcing/forcing_389ppm_Pulse100GtC_Res1yr.dat'
    dir = 'forcing'
    
    # write runfiles for precontrol run
    lines = "3\n.true.\n.true "
    f1 = 'pre_control_1yr_'+str(t)
    with open('runfiles/run_'+f1,'w') as out:
        out.write('{}\n{}\n'.format(lines, f1))
    
    df_p = pd.read_csv(forcing,delim_whitespace=True).set_index('#Year')
    
    # remove last 14 rows as they are commented out anyway
    df_p = df_p.iloc[:-14]
    df_p.index = df_p.index.rename('Year').astype('int')
    
    # hold co2 in atmosphere constant after year t
    df_p.loc[t-6:,'co2_atm']=df_p.loc[t-6,'co2_atm']
    
    # set budget uptake to zero after t-5
    df_p.loc[1700:,'budget_C_uptake']=-9999.9999
    
    # set RF budget to zero
    df_p.loc[t-5:,'RF_budget']=0
    
    # set global_temp_dev to nan
    df_p.loc[t-4:,'glob_temp_dev']=-9999.9999
    
    # set RF_nonCO2 to constant value
    df_p.loc[t-3:,'RF_nonCO2'] = df_p.loc[t-3,'RF_nonCO2']
    
    # set fossil_CO2_em to constant value
    df_p.loc[t-6:,'fossil_CO2_em'] = 0
    
    # write control file
    df_p.to_csv(os.path.join(dir,'forcing_'+f1+'.dat'),sep='\t')

def write_files_control(t):
    dir = 'forcing'
    forcing = 'forcing/forcing_389ppm_Pulse100GtC_Res1yr.dat'
    
    # write runfiles for precontrol run
    lines = "3\n.true.\n.true "
    f1 = 'control_1yr_'+str(t)
    with open('runfiles/run_'+f1,'w') as out:
        out.write('{}\n{}\n'.format(lines, f1))
    
    # read forcing template
    df = pd.read_csv(forcing,delim_whitespace=True).set_index('#Year')
    
    # read output from precontrol run
    out1 = 'output/pre_control_1yr_'+str(t)+'_D1I_BernSCM_t_f_CS30.dat'
    df1 = pd.read_csv(out1, skiprows=131, delim_whitespace=True).set_index('#time')
    
    # remove last 14 rows as they are commented out anyway
    df = df.iloc[:-14]
    df.index = df.index.rename('Year').astype('int')
    
    # hold co2 in atmosphere constant after year t-6
    df.loc[t-6:,'co2_atm']=-9999.9999
    
    # set budget uptake the one from precontrol run
    df.loc[1700:,'budget_C_uptake']=-9999.9999
    df.loc[t-7:,'budget_C_uptake']= df1.budget_C_uptake[t-7:]
    
    # set RF budget to zero
    df.loc[t-20:,'RF_budget']=0
    
    # set global_temp_dev to nan
    df.loc[t-19:,'glob_temp_dev']=-9999.9999
    
    # set RF_nonCO2 to constant value
    df.loc[t-5:,'RF_nonCO2'] = df.loc[t-5,'RF_nonCO2']
    
    # set fossil_CO2_em to constant value
    #df_p.loc[t:,'fossil_CO2_em'] = -df1.budget_C_uptake[1906:]
    df.loc[:,'fossil_CO2_em'] = df1.fossil_CO2_em
    
    # write control file
    df.to_csv(os.path.join(dir,'forcing_control_1yr_'+str(t)+'.dat'),sep='\t')

def write_files_pulse(t,x):
    dir = 'forcing'
    
    # write runfiles for precontrol run
    lines = "3\n.true.\n.true "
    f1 = 'pulse_1yr_'+str(t)
    with open('runfiles/run_'+f1,'w') as out:
        out.write('{}\n{}\n'.format(lines, f1))
    
    
    df_p = pd.read_csv(os.path.join(dir,'forcing_control_1yr_'+str(t)+'.dat'),delim_whitespace=True).set_index('Year')

    # set budget uptake to zero after t-5
    df_p.loc[t,'fossil_CO2_em']=x
        
    # write control file
    df_p.to_csv(os.path.join(dir,'forcing_pulse_1yr_'+str(t)+'.dat'),sep='\t')
    
    
def color_to_cmap(color):
    l = [(colors.to_rgba('#'+color,i)) for i in np.linspace(0.2,1,10)]
    cmap = colors.ListedColormap(l)
    return cmap

class HandlerColormap(HandlerBase):
    def __init__(self, cmap, num_stripes=8, **kw):
        HandlerBase.__init__(self, **kw)
        self.cmap = cmap
        self.num_stripes = num_stripes
    def create_artists(self, legend, orig_handle, 
                       xdescent, ydescent, width, height, fontsize, trans):
        stripes = []
        for i in range(self.num_stripes):
            s = Rectangle([xdescent + i * width / self.num_stripes, ydescent], 
                          width / self.num_stripes, 
                          height, 
                          fc=self.cmap((2 * i + 1) / (2 * self.num_stripes)), 
                          transform=trans)
            stripes.append(s)
        return stripes