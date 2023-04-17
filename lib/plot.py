import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColorBar, ColumnDataSource
from bokeh.transform import linear_cmap
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from lib.test_shapiro_w import test_shapiro_w


def plot_irradiance(tab_ref, tab_test, titre):
    
    """
        Plot global irradiance measurements of SPN1 and CMP22

    """
    
    x1 = np.arange(tab_test['GHI_test'].size)
    x2 = np.arange(tab_ref['GHI_ref'].size)
    x3 = np.arange(tab_test['DHI_test'].size)
    x4 = np.arange(tab_ref['DHI_ref'].size)
    
    p = figure(title=titre, x_axis_label='Time (min)', y_axis_label='Solar irradiances (W/m^2)')

    p.line(x1, tab_test['GHI_test'], legend_label='GHI_test', color='orange')
    p.line(x2, tab_ref['GHI_ref'], legend_label='GHI_ref', color='green')
    p.line(x3, tab_test['DHI_test'], legend_label='DHI_test', color='blue')
    p.line(x4, tab_ref['DHI_ref'], legend_label='DHI_ref', color='red')

    return p


def plot_calibration_global(tab, fa_ghi, offa_ghi):

    """
        Print scatter plot of GHI, linear regression line and y=x line

    """
    # ----------------------------GHI----------------------------#
    tab = tab.loc[tab['GHI_ref'] > 10]

    rmse_ghi = round(np.sqrt(mean_squared_error(tab['GHI_ref'], tab['GHI_test'])), 2)
    mae_ghi = round(mean_absolute_error(tab['GHI_ref'], tab['GHI_test']), 2)
    r2_ghi = round(r2_score(tab['GHI_ref'], tab['GHI_test']), 2)

    p = figure(title='GHI calibration of SPN1 RMSE='+str(rmse_ghi)+' '+'W/m^2'+' MAE='+str(mae_ghi)+' '+'W/m^2'+' R^2='+str(r2_ghi),
               x_axis_label='Global irradiance from SPN1 (W/m^2)',
               y_axis_label='Global irradiance from CMP22 (W/m^2)')

    p.dot(tab['GHI_test'], tab['GHI_ref'], color='black', legend_label='measured values')

    y = fa_ghi*tab['GHI_test']+offa_ghi  # linear regression line

    p.line(tab['GHI_test'], y, color='blue', legend_label='linear regression')
    p.line(tab['GHI_test'], tab['GHI_test'], legend_label='y=x', color='red')

    return p


def plot_calibration_diffus(tab, fa_dhi, offa_dhi):

    """
        Print scatter plot of DHI, linear regression line and y=x line

    """
    # ----------------------------DHI----------------------------#
    tab = tab.loc[tab['GHI_ref'] > 10]

    rmse_dhi = round(np.sqrt(mean_squared_error(tab['DHI_ref'], tab['DHI_test'])), 2)
    mae_dhi = round(mean_absolute_error(tab['DHI_ref'], tab['DHI_test']), 2)
    r2_dhi = round(r2_score(tab['DHI_ref'], tab['DHI_test']), 2)

    p = figure(title='DHI calibration of SPN1 RMSE='+str(rmse_dhi)+' '+'W/m^2'+' MAE='+str(mae_dhi)+' '+'W/m^2'+' R^2='+str(r2_dhi),
               x_axis_label='Diffus irradiance from SPN1 (W/m^2)',
               y_axis_label='Diffus irradiance from CMP22 (W/m^2)')

    p.dot(tab['DHI_test'], tab['DHI_ref'], color='black', legend_label='measured values')

    y = fa_dhi*tab['DHI_test']+offa_dhi  # linear regression line

    p.line(tab['DHI_test'], y, color='blue', legend_label='linear regression')
    p.line(tab['DHI_test'], tab['DHI_test'], legend_label='y=x', color='red')

    return p


def plot_calibration_corr(tab):

    """
        afficher le nuage de points, la droite de régression linéaire et la bissectrice y = x

    """
    tab = tab.loc[tab['GHI_ref'] > 10]
    # ----------------------------GHI----------------------------#

    rmse_ghi = round(np.sqrt(mean_squared_error(tab['GHI_ref'], tab['GHI_test'])), 2)
    mae_ghi = round(mean_absolute_error(tab['GHI_ref'], tab['GHI_test']), 2)
    r2_ghi = round(r2_score(tab['GHI_ref'], tab['GHI_test']), 2)

    p1 = figure(title='Corrected scatter plot for GHI RMSE='+str(rmse_ghi)+' '+'W/m^2'+' MAE='+str(mae_ghi)+' '+'W/m^2'+' R^2='+str(r2_ghi),
                x_axis_label='Global irradiance from SPN1 (W/m^2)',
                y_axis_label='Global irradiance from CMP22 (W/m^2)')

    p1.dot(tab['GHI_test'], tab['GHI_ref'], color='black', legend_label='corrected values')
    p1.line(tab['GHI_test'], tab['GHI_test'], legend_label='y=x', color='red')

    # ----------------------------DHI----------------------------#

    rmse_dhi = round(np.sqrt(mean_squared_error(tab['DHI_ref'], tab['DHI_test'])), 2)
    mae_dhi = round(mean_absolute_error(tab['DHI_ref'], tab['DHI_test']), 2)
    r2_dhi = round(r2_score(tab['DHI_ref'], tab['DHI_test']), 2)

    p2 = figure(title='Corrected scatter plot for DHI RMSE='+str(rmse_dhi)+' MAE='+str(mae_dhi)+' R^2='+str(r2_dhi),
                x_axis_label='Diffus irradiance from SPN1 (W/m^2)',
                y_axis_label='Diffus irradiance from CMP22 (W/m^2)')

    p2.dot(tab['DHI_test'], tab['DHI_ref'], color='black', legend_label='measured values')
    p2.line(tab['DHI_ref'], tab['DHI_ref'], legend_label='y=x', color='red')

    return p1, p2


def plot_validation_global(tab):
    """
        s’assurer que l’erreur relative suit une loi normale

    """

    sw_ghi = test_shapiro_w(tab['erreur_ghi'])
    sw_dhi = test_shapiro_w(tab['erreur_dhi'])
    # GHI
    hist, edges = np.histogram(tab['erreur_ghi'], density=True, bins=30)

    titre = 'Relative error'+' Shapiro-Wilk_test= ' + str(round(sw_ghi, 3))

    p1 = figure(title=titre, x_axis_label='relative error of GHI (%)',
                y_axis_label='effectif')

    p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="navy", line_color="white", alpha=0.5)

    # DHI
    hist, edges = np.histogram(tab['erreur_dhi'], density=True, bins=30)

    titre = 'Relative error'+' Shapiro-Wilk_test= ' + str(round(sw_dhi,3))
    p2 = figure(title=titre, x_axis_label='relative error of DHI (%)',
                y_axis_label='effectif')

    p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="navy", line_color="white", alpha=0.5)

    return p1, p2


def plot_solpos(tab):
    
    """Tracer la trajectoire du soleil"""

    p1 = figure(title='Solar position - GHI relative error', x_axis_label='Azimuth (°)',
                y_axis_label='Élévation (°)')

    source = ColumnDataSource(tab)

    mapper = linear_cmap(field_name='erreur_ghi', palette='Turbo256',
                         low=min(tab['erreur_ghi']), high=max(tab['erreur_ghi']))

    p1.dot(x="azimuth", y="elevation", size=10, legend_label='Élevation', source=source, line_color=mapper, color=mapper)
    color_bar = ColorBar(color_mapper=mapper["transform"], width=8,
                         location=(0, 0),
                         title='relative error (%)')

    p1.add_layout(color_bar, 'right')

    p2 = figure(title='Solar position - DHI relative error', x_axis_label='Azimuth (°)',
                y_axis_label='Élévation (°)')

    source = ColumnDataSource(tab)

    mapper = linear_cmap(field_name='erreur_dhi', palette='Turbo256',
                         low=min(tab['erreur_dhi']), high=max(tab['erreur_dhi']))

    p2.dot(x="azimuth", y="elevation", size=10, legend_label='Élevation', source=source, line_color=mapper, color=mapper)
    color_bar = ColorBar(color_mapper=mapper["transform"], width=8,
                         location=(0, 0),
                         title='relative error (%)')
    p2.add_layout(color_bar, 'right')

    return p1, p2


def plot_irradiance_corr(tab):
    """
        Plot global irradiance measurements of SPN1 and CMP22

    """

    x = np.arange(len(tab))

    p = figure(title='Corrected measurement campaign', x_axis_label='Time (min)', y_axis_label='Irradiance (W/m^2)')

    p.line(x, tab['GHI_test'], legend_label='GHI_test', color='orange')
    p.line(x, tab['GHI_ref'], legend_label='GHI_ref', color='green')
    p.line(x, tab['DHI_test'], legend_label='DHI_test', color='blue')
    p.line(x, tab['DHI_ref'], legend_label='DHI_ref', color='red')

    return p


def plot_diff(tab):

    x = np.arange(len(tab))
    p1 = figure(title='GHI difference after calibration', x_axis_label='Time (min)', y_axis_label='GHI difference after calibration (W/m^2)')

    p1.dot(x, tab['GHI_test']-tab['GHI_ref'], color='black')
    p1.line(x, 0, color='red')

    p2 = figure(title='DHI difference after calibration', x_axis_label='Time (min)', y_axis_label='DHI difference (W/m^2)')

    p2.dot(x, tab['DHI_test']-tab['DHI_ref'], color='black')
    p2.line(x, 0, color='red')

    return p1, p2


def dni_plot(tab, a):


    DNI_ref = (tab['GHI_ref']-tab['DHI_ref'])/tab['zenith']
    DNI_test = (tab['GHI_test']-tab['DHI_test'])/tab['zenith']

    p1 = figure(title='Absolute deviation between DNI from SPN1 pyranometer and reference DNI '+ a,
               y_axis_label='Direct SPN1-Direct CMP22 (W/m^2)',
               x_axis_label='Direct irradiance from CMP22 (W/m^2)')

    p1.dot(DNI_ref, DNI_test-DNI_ref, color='black', legend_label='DNI_test-DNI_ref')

    p2 = figure(title='Relative deviation between DNI as derived from SPN1 pyranometer and reference DNI '+ a,
               y_axis_label='(Direct SPN1-Direct CMP22)/Direct CMP22 ()',
               x_axis_label='Direct irradiance from CMP22 (W/m^2)')

    p2.dot(DNI_ref, (DNI_test-DNI_ref)/DNI_ref, color='black', legend_label='(DNI_test-DNI_ref)/DNI_ref')

    return p1, p2