import pandas as pd


def read_test(file=str):


    # read the file and convert it into a dataframe
    tab = pd.read_csv(file, header=3)

    ghi = tab.loc[tab['_field']=='GHI']
    dhi = tab.loc[tab['_field']=='DHI']

    d = {'TIMESTAMP': tab['_time'], 'GHI_test': ghi['value'], 'DHI_test': dhi['value'] }

    tab_test = pd.DataFrame(data=d)

    return tab_test

def read_ref(file=str):


    # read the file and convert it into a dataframe
    tab = pd.read_csv(file, header=3)

    ghi = tab.loc[tab['_field']=='GHI']
    dhi = tab.loc[tab['_field']=='DHI']
    temp = tab.loc[tab['_field']=='temp']


    d = {'TIMESTAMP': tab['_time'], 'GHI_ref': ghi['value'], 'DHI_ref': dhi['value'], 'Temp': temp['value'] }

    tab_ref = pd.DataFrame(data=d)

    return tab_ref