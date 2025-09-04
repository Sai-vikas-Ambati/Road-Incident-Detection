import cv2
from typing import List, Tuple

class MotionIncidentDetector:
    """
    Naive motion-based incident heuristic:
    - Background subtraction (MOG2)
    - Contour area threshold
    - Sustained large-area motion across N frames => 'incident'
    """
    def __init__(self, min_area: int = 8000, sustain_frames: int = 30):
        self.bg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
        self.min_area = int(min_area)
        self.sustain_frames = int(sustain_frames)
        self.counter = 0

    def process(self, frame) -> Tuple[bool, List[Tuple[int,int,int,int]]]:
        mask = self.bg.apply(frame)
        mask = cv2.medianBlur(mask, 5)
        mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        large = False
        for c in contours:
            area = cv2.contourArea(c)
            if area >= self.min_area:
                x, y, w, h = cv2.boundingRect(c)
                boxes.append((x, y, w, h))
                large = True

        if large:
            self.counter += 1
        else:
            self.counter = max(0, self.counter - 1)

        incident = self.counter >= self.sustain_frames
        return incident, boxes
