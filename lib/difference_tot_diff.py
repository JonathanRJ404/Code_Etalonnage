from bokeh.plotting import figure


def difference_tot_diff(tab):

    """
        Verify synchronization of the 7 thermopiles according to the overcast condition data

    """

    tab = tab.loc[tab['GHI_test'] > 10]

    y1 = tab['GHI_test']-3  # limit_Test_1
    y2 = 0.01*tab['GHI_test']+3  # limit_Test_2

    p1 = figure(title='Overcast conditions - Test 1', x_axis_label='Global flux (W/m^2)',
                y_axis_label='Diffus flux (W/m^2)')

    p1.line(tab['GHI_test'], tab['GHI_test'], legend_label='y=x', color='red')
    p1.line(tab['GHI_test'], y1, legend_label='overcast-sky limit Test 1', color='blue')

    p1.dot(tab['GHI_test'], tab['DHI_test'], legend_label='All data > 10 W/m^2', color='black')

    p2 = figure(title='Overcast conditions - Test 2', x_axis_label='Global flux (W/m^2)',
                y_axis_label='Difference: Global-Diffus (W/m^2)')

    p2.line(tab['GHI_test'], tab['GHI_test']*0, legend_label='y=0', color='red')
    p2.line(tab['GHI_test'], y2, legend_label='overcast-sky limit Test 2', color='blue')

    p2.dot(tab['GHI_test'], tab['GHI_test']-tab['DHI_test'], legend_label='All data > 10 W/m^2', color='black')
    
    return p1, p2
