from typing import Union
import cv2

def open_source(source: Union[int, str]):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video source: {source}")
    return cap
