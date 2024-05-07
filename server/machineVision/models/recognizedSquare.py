import cv2 as cv


class RecognizedSquare:
    def __init__(self, image: cv.Mat, is_empty: bool, position_index: int) -> None:
        self.image = image
        self.is_empty = is_empty
        self.number_str = "."
        self.position_index = position_index

    def set_number(self, number_str: str) -> None:
        self.number_str = number_str
