def overcast_conditions(tab):

    """
        Select data ( > 10 W.m2) of overcast conditions, 
        2 conditions must be respected: globale irradiance < 24 w/m^2 and globale irradiance/diffus irradiance < 1.35

    """
    # Selec values greater than 10 W/m^2 
    tab = tab.loc[tab['GHI_test'] > 10, :]
    p = len(tab)

    # extract rows where globale/diffus < 1.35 and extract rows where SPN1 globale < 24
    spn1_overcast = tab.loc[(tab['GHI_test']/tab['DHI_test'] < 1.35) & (tab['GHI_test'] < 24), :]

    overcast_percent = (100*spn1_overcast['GHI_test'].size)/p  # percentage of overcast conditions

    return spn1_overcast, overcast_percent
