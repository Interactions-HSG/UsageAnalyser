import unittest
import LOWatch
import distanceCalc
import LOUsageMapGenerator
import googleUpload
import config
import time
import numpy as np
import tracemalloc
import warnings


class TestLO(unittest.TestCase):

    def setUp(self):
        config.testMode = 1
        tracemalloc.start()
        self.start_time = time.time()
        self.fimage = r'images/61-402layout.png'
        self.firstImage = r'images/61-402layout.png'
        self.x1 = [635.0, 636.0]
        self.y1 = [347.0, 349.0]
        self.occupancy = 1
        self.Coordinates = [[635.0, 636.0], [347.0, 349.0]]
        self.color = 'b'
        self.raw_image = self.fimage
        self.changeCoordinates = [[635.0, 636.0], [347.0, 349.0]]
        self.personCoordinates = [[637.0, 639.0], [348.0, 342.0]]
        self.name = 'test_data'
        self.file = 'test_data'
        self.fileMetaData = {'name': 'test_data', 'time': time.strftime(
            '%b-%d-%Y_%H%M%S', time.localtime())}

    def tearDown(self):
        tracemalloc.stop()

    '''LOwatch.py'''

    def test_changeDetection(self):
        LOWatch.changeDetection(self.fimage, self.firstImage)

    def test_decision(self):
        self.assertEqual(LOWatch.decision(1, 0), 0)
        self.assertEqual(LOWatch.decision(1, 1), 1)
        self.assertEqual(LOWatch.decision(0, 1), 2)
        self.assertEqual(LOWatch.decision(0, 0), 3)

    def test_startWatching(self):
        LOWatch.startWatching(self.start_time)

    '''distanceCal.py'''

    def test_distanceCalculator(self):
        distanceCalc.distanceCalculator(self.x1, self.y1, self.occupancy)

    def test_iterateNPlot(self):
        distanceCalc.iterateNplot(self.Coordinates, self.color)

    def test_calculateAndMap(self):
        distanceCalc.calculateAndMap(
            self.raw_image, self.changeCoordinates, self.personCoordinates, self.occupancy)

    '''LOUsageMapGenerator.py'''

    def test_createZip(self):
        LOUsageMapGenerator.createZip(self.name)

    def test_generateMap(self):
        LOUsageMapGenerator.generateMap(self.raw_image)

    def test_main(self):
        LOUsageMapGenerator.main()

    '''googleUpload'''

    def test_fileUpload(self):
        googleUpload.upload_files(self.file, self.fileMetaData)


if __name__ == "__main__":
    unittest.main()
