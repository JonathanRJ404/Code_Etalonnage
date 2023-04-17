import numpy as np
import pandas as pd
import json
from lib.sol_pos import solarposition
from datetime import datetime


def data_selection(file_json, tab_ref, tab_test):
    """
        Make a data selection

    """
    with open(file_json) as json_data:
        data_dict = json.load(json_data)

    tab_test = tab_test.loc[~tab_test.index.duplicated(keep='first')]
    tab_ref = tab_ref.loc[~tab_ref.index.duplicated(keep='first')]

    tab_selec = tab_ref.merge(tab_test, on='TIMESTAMP')  # Merge the dataframes

    tab_selec = tab_selec.reset_index()
    
    # Calculate solar position
    pos = solarposition(tab_selec, latitude=data_dict['Location']['latitude'], longitude=data_dict['Location']['longitude'], tz=data_dict['Location']['TZ'])
    pos = pos.reset_index()
    pos['azimuth'].loc[pos['azimuth'] > 180] = pos['azimuth'].loc[pos['azimuth'] > 180]-360  # Normalize -180/180
    tab_selec = pd.concat([tab_selec, pos], axis=1)
    del tab_selec['index']

    # save dataframe in csv file
    # tab_selec.to_csv('./data/irrad_spn1_cmp22.csv', index=False)

    # Replace inf, -inf values into NaN values and delete rows where there is NaN values
    tab_selec = tab_selec.replace([np.inf, -np.inf], np.nan).dropna()

    # nombres de valeurs nocturnes
    noct = len(tab_selec.loc[tab_selec['elevation'] < 0])
    # test des valeurs nocturnes
    test_noct = len(tab_selec.loc[(tab_selec['elevation'] < 0) & (tab_selec['GHI_test'] > 6)])

    # enelever les valeurs nocturnes
    tab_selec = tab_selec.loc[(tab_selec['elevation'] > 0) & (tab_selec['GHI_test'] > 10)]

    # enlever les lignes où GHI < DHI
    tab_selec = tab_selec.loc[(tab_selec.GHI_test > tab_selec.DHI_test) & (tab_selec.GHI_ref > tab_selec.DHI_ref)]

    delete_values = len(tab_ref) - len(tab_selec)  # deleted values
    del_percent = (100 * delete_values) / len(tab_ref)

    # Calculate kb
    kb = (tab_selec['GHI_test']-tab_selec['DHI_test'])/tab_selec['GHI_test']

    # mean temperature
    mean_temp = np.mean(tab_selec['Temp'])

    tab_selec['TIMESTAMP'] = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in tab_selec['TIMESTAMP']]

    return tab_selec, kb, del_percent, noct, mean_temp, test_noct
