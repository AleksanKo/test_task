import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from main import parsing_file, parse_date, parse_time, count_time
import datetime

class TestParsingFile(unittest.TestCase):
    def test_parsing_file(self):
        file = 'test.xml'
        result = parsing_file(file)
        assumed_result = pd.DataFrame({'Persons': ['i.ivanov', 'a.stepanova', 'g.stepanova', 'l.stepova'],
                                       'Dates': ['21-12-2011', '21-12-2011', '22-12-2011', '21-12-2019'],
                                       'Time': [datetime.timedelta(0, 31695), datetime.timedelta(0, 29945),
                                                 datetime.timedelta(0, 40625), datetime.timedelta(0, 26345)]})

        assumed_result['Dates'] = pd.to_datetime(assumed_result['Dates'])

        assert_frame_equal(result, assumed_result)

class TestParseDate(unittest.TestCase):
    def test_parse_date(self):
        date = '21-12-2011 10:54:47'
        result = parse_date(date)
        self.assertEqual(result, '21-12-2011')

    def test_parse_wrong_date(self):
        date = '12-21-2011 10:54:47'
        with self.assertRaises(ValueError):
            result = parse_date(date)


if __name__ == '__main__':
    unittest.main()