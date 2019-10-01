import unittest
import Messier33

class Messier33Test(unittest.TestCase):
    
    def test_from_pandas(self):
        catalog = Messier33.Catalog.from_pandas("pandas.testdata")
        self.assertEqual(catalog.catalog, "pandas")
        self.assertEqual(len(catalog), 30)

        with open("pandas.testdata", 'r') as f:
            splitline=catalog.split_pandas_line(f.readline(), float)
            ra = catalog.hms_to_degrees(*splitline[:3])
            dec= catalog.dms_to_degrees(*splitline[3:6])
            _bandDATA=catalog.list_to_bandINFO(splitline[6:11], band='g')
            _bandDATA.update(catalog.list_to_bandINFO(splitline[11:16], band='i')) 
            source=Messier33.Source(coords=(ra,dec), bandDATA=_bandDATA)
            self.assertEqual(source.coords, catalog[0].coords)
            self.assertEqual(source.bandDATA, catalog[0].bandDATA)
    
    def test_from_wfcam(self):
        catalog = Messier33.Catalog.from_wfcam("wfcam.testdata")
        self.assertEqual(catalog.catalog, "wfcam")
        self.assertEqual(len(catalog), 30)
        with open("wfcam.testdata", 'r') as f:
            splitline=catalog.split_wfcam_line(f.readline(), float)
            ra = catalog.hms_to_degrees(*splitline[:3])
            dec= catalog.dms_to_degrees(*splitline[3:6])
            _bandDATA=catalog.list_to_bandINFO(splitline[7:12], band='J')
            _bandDATA.update(catalog.list_to_bandINFO(splitline[12:17], band='K'))
            _bandDATA.update(catalog.list_to_bandINFO(splitline[17:22], band='H'))
            source=Messier33.Source(coords=(ra,dec), bandDATA=_bandDATA)
            self.assertEqual(source.coords, catalog[0].coords)
            self.assertEqual(source.bandDATA, catalog[0].bandDATA)

    def test_hmsdms(self):
        self.assertEqual( "%.4f"%Messier33.Catalog.hms_to_degrees(10,10,10), "152.5417")
        self.assertEqual( "%.4f"%Messier33.Catalog.hms_to_degrees(10,10,10), "152.5417")
        self.assertEqual( "%.4f"%Messier33.Catalog.hms_to_degrees(0,0,0), "0.0000")
        self.assertEqual( "%.4f"%Messier33.Catalog.dms_to_degrees(0,0,0), "0.0000")

    def test_filelength(self):
        self.assertEqual(Messier33.Catalog.filelength("pandas.testdata"), 30)
        self.assertEqual(Messier33.Catalog.filelength("empty.testdata"), 1)

if __name__=="__main__":
    unittest.main()

