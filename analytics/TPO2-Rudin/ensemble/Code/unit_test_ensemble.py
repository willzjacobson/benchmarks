import unittest
import datetime as dt
from data_module import Steam,Weather
from data_module import HMM
from gen_hist_band import HistBand
from unit_test_hist_band import HMMTest

class ModelTest(unittest.TestCase):
    '''
    Test class to test ensemble
    '''
    def setUp(self):
        pass

    def test_covariates_length(self):
    '''
    test if all columns in covariates data frame have same length
    '''
    
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HMMTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

