from cscore import CameraServer
# from cscore.VideoMode.PixelFormat import kYUYV # kMJPEG also exists

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    frontCam = cs.startAutomaticCapture(dev=0)
    backCam = cs.startAutomaticCapture(dev=1)

    # For a list of possible combinations: http://roborio-5994-frc.local:1181/
    frontCam.setResolution(320, 240)
    frontCam.setFPS(30)
    # backCam.setPixelFormat(kYUYV)

    backCam.setResolution(320, 240)
    backCam.setFPS(30)
    # backCam.setPixelFormat(kYUYV)

    cs.waitForever()