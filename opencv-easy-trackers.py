# encoding=utf-8
# Prework: python and pip install opencv-python==ver (e.g. 3.1.0)
#                     pip install opencv-contrib-python==ver (should be the same)

import cv2


class Tracker(object):
    def __init__(self, tracker_type="BOOSTING", draw_coord=True):
        # version comparision, some API changed.
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        self.tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
        self.tracker_type = tracker_type
        self.isWorking = False
        self.draw_coord = draw_coord
        if int(minor_ver) < 3:
            self.tracker = cv2.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                self.tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                self.tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                self.tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                self.tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                self.tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                self.tracker = cv2.TrackerGOTURN_create()


    def initWorking(self, frame, box):
        if not self.tracker:
            raise Exception("Init missed")
        status = self.tracker.init(frame, box)
        if not status:
            raise Exception("Init failed")
        self.coord = box
        self.isWorking = True

    def track(self, frame):
         if self.isWorking:
            status, self.coord = self.tracker.update(frame)
            if status:
                 if self.draw_coord:
                    p1 = (int(self.coord[0]), int(self.coord[1]))
                    p2 = (int(self.coord[0] + self.coord[2]), int(self.coord[1] + self.coord[3]))
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                    return frame


if __name__ == '__main__':
    a = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    track_type = a[2]
    tracker = Tracker(tracker_type=track_type)
    video = cv2.VideoCapture(0)
    _, frame = video.read()
    bbox = cv2.selectROI(frame, False)
    tracker.initWorking(frame, bbox)
    while True:
        ret, frame = video.read()
        if ret:
            cv2.imshow("Track using {}".format(track_type), tracker.track(frame))
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
