import unittest
from app import pogoda_get

class Tests(unittest.TestCase):

    def test_api(self):
        nowe_miasto = 'London'
        spr = pogoda_get(nowe_miasto)
        self.assertEqual(200, spr['cod'])

    def test_api_blad(self):
        nowe_miasto = 'dfsdfas'
        spr = pogoda_get(nowe_miasto)
        self.assertEqual('404', spr['cod'])

 

if __name__ == '__main__':
    unittest.main()