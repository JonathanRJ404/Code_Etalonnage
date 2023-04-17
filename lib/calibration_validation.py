import numpy as np


def calibration_validation(tab, fa_ghi, offa_ghi, fa_dhi, offa_dhi):
    """
        Determine relative error between 2 dataframe (with 99.7% filter)
    """
    
    del_values = tab.shape[0]
    # ---------GHI---------#
    tab['GHI_test'] = tab['GHI_test'] * fa_ghi + offa_ghi
    
    tab['erreur_ghi'] = 100*(tab['GHI_test']-tab['GHI_ref'])/tab['GHI_ref']

    tab = tab.replace([np.inf, -np.inf], np.nan).dropna()

    std_ghi = np.std(tab['erreur_ghi'])

    tab = tab.loc[abs(tab['erreur_ghi']) < 3 * std_ghi, :]

    tab['erreur_ghi'] = 100*(tab['GHI_test']-tab['GHI_ref'])/tab['GHI_ref']    
    std_ghi = np.std(tab['erreur_ghi'])

    # ---------DHI---------#
    tab['DHI_test'] = tab['DHI_test'] * fa_dhi + offa_dhi
    
    tab['erreur_dhi'] = 100*(tab['DHI_test']-tab['DHI_ref'])/tab['DHI_ref']

    tab = tab.replace([np.inf, -np.inf], np.nan).dropna()

    std_dhi = np.std(tab['erreur_dhi'])

    tab = tab.loc[abs(tab['erreur_dhi']) < 3 * std_dhi, :]

    tab['erreur_dhi'] = 100*(tab['DHI_test']-tab['DHI_ref'])/tab['DHI_ref']

    std_dhi = np.std(tab['erreur_dhi'])
    
    del_values = del_values - len(tab)

    # enlever les lignes où GHI < DHI
    tab = tab.loc[(tab.GHI_test > tab.DHI_test) & (tab.GHI_ref > tab.DHI_ref)]

    print(del_values, 'valeurs abérrantes ont été supprimés')
    return tab, std_ghi, std_dhi
