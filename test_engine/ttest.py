from scipy import stats

def test_result(signal_return):
    # Perform a t-test with the null hypothesis being that the expected mean return is zero.

    t_stat, p_value = stats.ttest_1samp(signal_return, 0)

    return t_stat, p_value / 2
