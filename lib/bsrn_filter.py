import numpy as np
from bokeh.plotting import figure


def bsrn_filter(tab):
    """
    Quality control of the measures
    """
    tab['zenith'] = tab['zenith']*np.pi/180
    
    # Earth – Sun distance variation
    e = 0.0167086
    d = [day.timetuple().tm_yday for day in tab['TIMESTAMP']]  # returns 1 for January 1st
    teta = np.asarray(d)*(360*np.pi/180)/365.25

    mu_o = np.cos(tab['zenith'])
    s_o = 1365.69  # solar constant at mean Earth-Sun distance
    au = (1-e*e)/(1+e*np.cos(teta))  # Earth – Sun distance in Astronomical Units
    s_a = s_o/au**2  # solar constant adjusted for Earth – Sun distance

    # Physically-possible limits
    tab['limit_ghi_pp'] = s_a*1.5*mu_o**1.2+100
    tab['limit_dhi_pp'] = s_a*0.95*mu_o**1.2+50

    # Extremely-rare limits
    tab['limit_ghi_er'] = s_a*1.2*mu_o**1.2+50
    tab['limit_dhi_er'] = s_a*0.75*mu_o**1.2+30

    p1 = figure(title='GHI quality control', x_axis_label='Zenith (rad)',
                y_axis_label='Irradiance (W/m^2)')
    p1.line(tab['zenith'], tab['limit_ghi_pp'], color='red', legend_label='Physically-possible limits')
    p1.line(tab['zenith'], tab['limit_ghi_er'], color='blue', legend_label='Extremely-rare limits')
    p1.dot(tab['zenith'], tab['GHI_test'], color='black')

    p2 = figure(title='DHI quality control', x_axis_label='Zenith (rad)',
                y_axis_label='Irradiance (W/m^2)')
    p2.line(tab['zenith'], tab['limit_dhi_pp'], color='red', legend_label='Physically-possible limits')
    p2.line(tab['zenith'], tab['limit_dhi_er'], color='blue', legend_label='Extremely-rare limits')
    p2.dot(tab['zenith'], tab['DHI_test'], color='black')

    tot_measures = tab.shape[0]

    tab = tab.loc[tab['GHI_test'] < tab['limit_ghi_er']]
    tab = tab.loc[tab['DHI_test'] < tab['limit_dhi_er']]

    del_values = tot_measures - tab.shape[0]

    tab['zenith'] = 180*tab['zenith']/np.pi

    del tab['limit_ghi_er']
    del tab['limit_dhi_er']
    return tab, del_values, p1, p2
