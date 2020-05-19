import picamera
import picamera.array

theGodArray = None

# Inherit from PiRGBAnalysis
class MyAnalysisClass(picamera.array.PiRGBAnalysis):
    def analyse(self, array):
        print('here')
        global theGodArray
        theGodArray = array

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBAnalysis(camera) as output:
        camera.resolution = (256, 256)
        camera.framerate = 30
        output = MyAnalysisClass(camera)
        camera.start_recording(output, format='rgb')
        camera.wait_recording(2000)
        camera.stop_recording()

# https://raspberrypi.stackexchange.com/questions/32926/convert-the-frame-data-from-recording-into-a-numpy-array
# https://gist.github.com/waveform80/22dea34379d5a7171ce4


  """

    import picamera
    import picamera.array

    frames = None

    # Inherit from PiRGBAnalysis
    class MyAnalysisClass(picamera.array.PiRGBAnalysis):
        def analyse(self, array):
            print('here')
            global frames
            frames = array

    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBAnalysis(camera) as output:
            camera.resolution = (256, 256)
            camera.framerate = 30
            fps = camera.framerate
            config.FPS = fps
            logging.info("Start FPS: {}".format(fps))
            output = MyAnalysisClass(camera)
            camera.start_recording(output, format='rgb')
            camera.wait_recording(10)
            camera.stop_recording()
            room_default_brightness = config.ROOM_BRIGHTNESS_THRESHOLD

https://www.raspberrypi.org/forums/viewtopic.php?t=202781
           
            while True:
                ''' check room brightness '''

                
    """