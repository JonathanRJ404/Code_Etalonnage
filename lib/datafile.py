import pandas


def read_test(sepa, file=str):
    """
        Isolate SPN1's measurements in numerical values in a dataframe 

    """
    # read the file and convert it into a dataframe
    tab_test = pandas.read_csv(file, sep=sepa, header=0)

    tab_test = tab_test.set_index('TIMESTAMP')
    tab_test['GHI_test'] = tab_test['GHI_test'].astype(float)
    tab_test['DHI_test'] = tab_test['DHI_test'].astype(float)

    return tab_test


def read_ref(sepa, file=str):
    """
        Isolate reference's measurements in numerical values in a dataframe

    """
    
    # read the file and convert it into a dataframe
    tab_ref = pandas.read_csv(file, sep=sepa, header=0)

    tab_ref = tab_ref.set_index('TIMESTAMP')
    tab_ref['GHI_ref'] = tab_ref['GHI_ref'].astype(float)
    tab_ref['DHI_ref'] = tab_ref['DHI_ref'].astype(float)
   
    return tab_ref
