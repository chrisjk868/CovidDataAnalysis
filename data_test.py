import pandas as pd
from cse163_utils import assert_equals
from main import pop_density_coid_growth_rate, \
    hdi_vs_mortality_testing_rate


def test_pop_density_coid_growth_rate(data):
    '''
    Takes in a dataframe that is written by me
    and tests if the pop_density_coid_growth_rate
    returns matches the expected output
    '''
    assert_equals([1190.068063, 62.500000, 2656.060000],
                  pop_density_coid_growth_rate(data))


def test_hdi_vs_mortality_testing_rate(data):
    '''
    Takes in a dataframe that is written by me
    and tests if the hdi_vs_mortality_testing_rate
    returns matches the expected output
    '''
    assert_equals([61.754, 128.570, 463.710, 29.304, 221.962, 570.103],
                  hdi_vs_mortality_testing_rate(data))


def main():
    test_data = pd.read_csv('test/my_test.csv')
    test_pop_density_coid_growth_rate(test_data)
    test_hdi_vs_mortality_testing_rate(test_data)


if __name__ == '__main__':
    main()
