"""Test"""

import time
import unittest
import tracemalloc
import csv
import os
import cv2
import numpy as np
import Record
import distanceCalc
import LOUsageMapGenerator
import googleUpload
import config


class TestLO(unittest.TestCase):

    def setUp(self):
        config.TEST_MODE = 1
        tracemalloc.start()
        self.start_time = time.time()
        self.fimage = r'images/61-402layout.png'
        self.first_image = r'images/61-402layout.png'
        self.x1 = np.array([635.0, 347.0])
        self.y1 = np.array([636.0, 349.0])
        self.occupancy = 1
        self.coordinates = [[635.0, 636.0], [347.0, 349.0]]
        self.color = 'b'
        self.raw_image = self.fimage
        self.change_coordinates = [[635.0, 636.0], [347.0, 349.0]]
        self.person_coordinates = [[637.0, 639.0], [348.0, 342.0]]
        self.name = 'test_data'
        self.file = 'test_data'
        self.file_meta_data = {'name': 'test_data', 'time': time.strftime(
            '%b-%d-%Y_%H%M%S', time.localtime())}
        self.output_epmty_array = []
        self.filtered_array = np.array([(347.0, 349.0)])
        self.image_data = cv2.imread(self.first_image)
        
        self.change = np.array([[256, 452], [253, 443], [251, 439], [255, 435], [254, 435], [256, 435], [257, 431], [254, 432], [247, 428], [254, 424], [269, 421], [273, 421], [272, 421], [268, 421], [270, 421], [269, 420], [271, 420], [273, 416], [561, 375], [268, 417], [570, 379], [266, 418], [572, 380], [264, 418], [574, 381], [265, 416], [574, 382], [267, 418], [574, 383], [265, 418], [574, 384], [202, 428], [276, 417], [573, 385], [274, 417], [573, 385], [270, 417], [568, 390], [269, 418], [569, 389], [278, 417], [568, 390], [286, 415], [568, 390], [289, 414], [568, 390], [291, 414], [568, 390], [291, 414], [568, 391], [291, 414], [568, 391], [288, 414], [568, 391], [283, 415], [568, 391], [278, 415], [568, 391], [273, 415], [568, 391], [269, 416], [568, 391], [267, 416], [568, 391], [201, 428], [273, 415], [569, 392], [202, 428], [243, 433], [327, 401], [569, 391], [200, 429], [242, 433], [356, 401], [570, 391], [232, 432], [379, 398], [570, 391], [231, 432], [394, 393], [570, 390], [231, 433], [402, 389], [570, 390], [232, 432], [399, 394], [570, 390], [232, 433], [375, 397], [570, 390], [200, 428], [241, 434], [346, 402], [570, 391], [199, 428], [285, 417], [570, 391], [199, 429], [277, 423], [570, 391], [270, 423], [570, 391], [263, 423], [570, 391], [249, 425], [571, 389], [241, 426], [571, 389], [234, 428], [574, 386], [235, 430], [575, 386], [241, 433], [574, 386], [247, 435], [574, 386], [255, 440], [574, 386], [257, 454], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385], [575, 385]])

        self.f = open('Test.csv', "w")
        self.writer = csv.DictWriter(self.f, fieldnames=[
                                "Timestamp", "Furniture_Type", "Usage_Count", "Usage_Type", "Room_Occupancy", "Device_ID"])
        self.writer.writeheader()
        
    def tearDown(self):
        tracemalloc.stop()
        self.f.close()

    '''Record.py'''

    def test_change_detection(self):
        self.assertEqual(Record.change_detection(self.fimage, self.first_image)[2], 0)
        self.assertEqual(Record.change_detection(self.fimage, self.first_image)[1], self.output_epmty_array)
        self.assertEqual(Record.change_detection(self.fimage, self.first_image)[0].all(), self.image_data.all())
        
    def test_recording(self):
       self.assertEqual(Record.start_recording(self.start_time).all(), self.change.all())

    '''distanceCal.py'''

    def test_distanceCalculator(self):
        self.assertEqual(distanceCalc.distance_calculator(self.x1, self.y1, 1, self.writer).all(), self.filtered_array.all())

    def test_iterateNPlot(self):
        self.assertEqual(distanceCalc.iterate(self.coordinates)[0].all(), self.x1.all())
        self.assertEqual(distanceCalc.iterate(self.coordinates)[1].all(), self.y1.all())
        
    def test_check_continuity(self):
        self.assertTrue(distanceCalc.check_continuity(self.change))

    def test_calculateAndMap(self):
        distanceCalc.calculate_and_map(self.raw_image, self.change_coordinates, self.writer)

    '''LOUsageMapGenerator.py'''
    def test_createZip(self):
        LOUsageMapGenerator.create_zip(self.name)
        self.assertTrue(os.path.exists('test_data.zip'))
        
    def test_generateMap(self):
        LOUsageMapGenerator.generate_map()

    '''googleUpload'''

    def test_fileUpload(self):
        LOUsageMapGenerator.create_zip(self.name)
        self.assertIsInstance(googleUpload.upload_files(self.file, self.file_meta_data).get('id'), str)


if __name__ == "__main__":
    unittest.main()
