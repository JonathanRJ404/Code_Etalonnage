
from lib import datafile as dtf
from lib.bsrn_filter import bsrn_filter
from lib.data_selection import data_selection
from lib.difference_tot_diff import difference_tot_diff
from lib.linear_regression import linear_regression
from lib.overcast_conditions import overcast_conditions
from lib.calibration_validation import calibration_validation
from lib.plot import plot_irradiance, plot_calibration_global, plot_validation_global, plot_calibration_diffus, \
    plot_calibration_corr, plot_solpos, plot_irradiance_corr, plot_diff, dni_plot
from lib.sky_classification import sky_classification
from bokeh.plotting import output_file, show, gridplot
#from lib.csvtoinflux import csvtoinflux
from lib.python_pdf import certificate
from lib.launch import launch
import json
from datetime import date

file_json = launch()

with open(file_json) as json_data:
    data_dict = json.load(json_data)

file_plot =  './output/plot_'+str(date.today().year)+str(date.today().month)+str(date.today().day)+'_'+data_dict['Device']['model']+'_'+data_dict['Device']['serial_num']+'.html'
output_file(file_plot)


# Sensibility coeffficient SensiSPN_GHlold, SensiSPN1_DHlold
sensi_ghi_old = data_dict['Device']['sensi_ghi_old']
sensi_dhi_old = data_dict['Device']['sensi_dhi_old']


# Read the data
tab_test = dtf.read_test(',', 'data/data_test.csv')
tab_ref = dtf.read_ref(',', 'data/data_ref.csv')

# Vizualise the data
p1 = plot_irradiance(tab_ref, tab_test, titre='Measurement campaign')

# Make a selection
[tab_selec, kb, del_percent, noct, mean_temp, test_noct] = data_selection(file_json, tab_ref, tab_test)

p21 =  plot_irradiance(tab_selec,tab_selec, titre='Measurement campaign')

[tab_selec_qc, del_values, p2, p3] = bsrn_filter(tab_selec)

# Vizualise the data after selection
p4 = plot_irradiance(tab_selec_qc, tab_selec_qc, titre='Measurement campaign after selection')

# Calculate overcast conditions values
[SPN1_overcast, overcast_percent] = overcast_conditions(tab_selec_qc)

# Plot the sky condition 
p5 = sky_classification(kb)

# Test 1 and test 2 j "verification of the 7 thermopieles"
p6, p7 = difference_tot_diff(tab_selec_qc)

# Determine the coefficient and offset of the linear regression line of GHI and DHI scatter plot
[a_g, b_g, r_g, a_d, b_d, r_d] = linear_regression(tab_selec_qc)
 
# Plot the GHI's scatter plot, its linear regression and y=x
p8 = plot_calibration_global(tab_selec_qc, a_g, b_g)

# Plot the DHI's scatter plot, its linear regression and y=x
p9 = plot_calibration_diffus(tab_selec_qc, a_d, b_d)

[tab_calib, std_ghi, std_dhi] = calibration_validation(tab_selec_qc, a_g, b_g, a_d, b_d)

# Envoie des données corrigées sur un serveur influxdb
#csvtoinflux(file_json, tab_calib)

# Plot the corrected scatter plot of GHI and DHI
p10, p11 = plot_calibration_corr(tab_calib)

# Histogram
p12, p13 = plot_validation_global(tab_calib)

# Position du soleil
p14, p15 = plot_solpos(tab_calib)

p16 = plot_irradiance_corr(tab_calib)

p17, p18= plot_diff(tab_calib)

p19, p20 = dni_plot(tab_calib, 'after calibration')

p = gridplot([[p1, p4],[p21, None], [p2, p3], [p5, None], [p6, p7], [p8, p9], [p10, p11], [p12, p13], [p14, p15], \
    [p16, None],[p17,p18],[p19,p20]],sizing_mode='scale_both')
show(p)

sensi_ghi_new = round(sensi_ghi_old/a_g, 2)
sensi_dhi_new = round(sensi_dhi_old/a_d, 2)

print("valeurs de référence:", len(tab_ref))
print("valeurs de test:", len(tab_test))
print("valeurs comparables:", len(tab_selec))
print("La température moyenne est de :", round(mean_temp, 2), "°")
print(noct, "valeurs nocturnes")
print(test_noct, "valeurs nocturnes supérieures à 6 W/m^2")
print("valeurs qui passent le test DQC:", len(tab_selec_qc))
print("valeurs étalonnées", len(tab_calib))
print(round(del_percent, 2), '% des valeurs de références ont été supprimés')
print(del_values, 'jeu de mesures ont été supprimés dans le filtre DQC')
print('Old sensibility for GHI =', sensi_ghi_old, 'uV/W/m^2')
print('Old sensibility for DHI =', sensi_dhi_old, 'uV/W/m^2')
print('New sensibility for GHI =', round(sensi_ghi_new, 2), 'uV/W/m^2')
print('New sensibility for DHI =', round(sensi_dhi_new, 2), 'uV/W/m^2')
print('Correction coefficient for GHI =', round(a_g, 2))
print('Correction coefficient for DHI =', round(a_d, 2))

start = tab_selec.iloc[0]['TIMESTAMP']
end = tab_selec.iloc[-1]['TIMESTAMP']
s = str(start.year)+'-'+str(start.month)+'-'+str(start.day)
e = str(end.year)+'-'+str(end.month)+'-'+str(end.day)
certificate(file_json, round(mean_temp, 2), sensi_ghi_new, sensi_dhi_new, s, e)
