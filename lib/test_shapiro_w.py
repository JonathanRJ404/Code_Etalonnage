from scipy import stats


def test_shapiro_w(x):
    [stat, p_value] = stats.shapiro(x)

    return stat
