from scipy.stats import linregress


def linear_regression(tab):

    """
        Determine linear regression line (coefficient and offset) of scatter plot f(GHI_REF_selec) = GHI_TEST_selec
    """               

    # ----------------------------GHI----------------------------#
    # coefficient and offset linear regression line
    a_g, b_g, r_g, p_value, std_err = linregress(tab['GHI_test'], tab['GHI_ref'])

    # ----------------------------DHI----------------------------#
    # coefficient and offset linear regression line
    a_d, b_d, r_d, p_value, std_err = linregress(tab['DHI_test'], tab['DHI_ref'])

    return a_g, b_g, r_g, a_d, b_d, r_d
