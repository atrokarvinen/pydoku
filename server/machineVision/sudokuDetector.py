import math
import os
import string
from typing import Sequence
import cv2 as cv
import matplotlib.pyplot as plt
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


class SudokuDetector:
    def __init__(self) -> None:
        pass

    def detect(self, file) -> str:
        img = self.load_image(file)

        plt.subplot(1, 3, 1)
        plt.imshow(img, cmap="gray")

        preprocessed = self.preprocess(img)
        edges = self.detect_edges(preprocessed)

        plt.subplot(1, 3, 2)
        plt.imshow(edges, cmap="gray")

        contours = self.get_sudoku_contours(edges)
        largest_contour = self.take_largest_contour(contours)
        roi = self.get_region_of_interest(preprocessed, largest_contour)

        plt.subplot(1, 3, 3)
        plt.imshow(roi, cmap="gray")

        plt.show()

        squares = self.get_squares(roi)
        numbers = self.recognize_numbers(squares)
        print("sudoku length: " + str(len(numbers)))
        print(numbers)
        full_sudoku = "".join(numbers)

        return full_sudoku

    def preprocess(self, img: cv.Mat) -> cv.Mat:
        img = cv.GaussianBlur(img, (1, 1), 0)
        return img

    def get_sudoku_contours(self, img: cv.Mat) -> Sequence[cv.Mat]:
        contours = cv.findContours(
            img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if (len(contours) == 0):
            raise Exception("No contours found")

        cnt = contours[0]
        print("contours count: " + str(len(cnt)))

        return cnt

    def take_largest_contour(self, contours: Sequence[cv.Mat]) -> cv.Mat:
        contour_areas = [cv.contourArea(c) for c in contours]
        largest_contour = contours[contour_areas.index(max(contour_areas))]
        return largest_contour

    def get_region_of_interest(self, img: cv.Mat, contour: cv.Mat) -> cv.Mat:
        (x, y, w, h) = cv.boundingRect(contour)
        roi = img[y:y+h, x:x+w]
        return roi

    def get_squares(self, img: cv.Mat) -> Sequence[cv.Mat]:
        board_range = [*range(0, 9)]
        squares = []
        for row in board_range:
            for col in board_range:
                x = round(img.shape[0] / 9 * row)
                y = round(img.shape[1] / 9 * col)
                w = round(img.shape[0] / 9)
                h = round(img.shape[1] / 9)
                square = img[x:x+w, y:y+h]
                squares.append(square)
        return squares

    def recognize_numbers(self, squares: Sequence[cv.Mat]) -> Sequence[int]:
        numbers = []
        i = 0
        ss = squares
        # ss = [squares[0], squares[1], squares[4], squares[78]]
        # ss = [squares[78]]
        plt.close()
        for square in ss:
            config = '--oem 3 --psm 10 -c tessedit_char_whitelist=123456789'
            # config = '--oem 3 --psm 10 outputbase digits'
            preprocessed = self.preprocess_square(square)
            img_pixels = preprocessed.shape[0] * preprocessed.shape[1]
            binary_area = cv.countNonZero(preprocessed)
            sub = img_pixels - binary_area
            # print("sub: " + str(sub) + ", " + str(0.01 * img_pixels))
            is_empty = img_pixels - binary_area < 0.01 * img_pixels
            if is_empty:
                # print("empty square")
                numbers.append(".")
                i = i + 1
                continue

            rbg = cv.cvtColor(preprocessed, cv.COLOR_GRAY2RGB)

            numberStr = pytesseract.image_to_string(
                rbg, config=config)

            # data = pytesseract.image_to_data(
            #     preprocessed, output_type=pytesseract.Output.DICT, config=config)
            # print(data)

            print("detected string: " + numberStr)

            trimmed = numberStr.strip()
            try:
                parsed = int(trimmed)
                postprocessed = parsed if parsed < 10 else parsed % 10
                if postprocessed <= 0:
                    postprocessed = "."
                number = str(postprocessed)
            except:
                number = "."

            print("detected number: " + number +
                  " in square (row, col): " + str(i // 9) + ", " + str(i % 9))

            # plt.imshow(preprocessed, cmap="gray")
            # plt.waitforbuttonpress()

            numbers.append(number)
            i = i + 1
        return numbers

    def preprocess_square(self, square: cv.Mat) -> cv.Mat:
        cropped = self.crop_square(square)
        squared = cv.resize(cropped, (50, 50))
        thresholded = self.threshold(squared)
        return thresholded

    def crop_square(self, square: cv.Mat) -> cv.Mat:
        (x, y, w, h) = cv.boundingRect(square)
        cutoff_factor = 0.1
        x2 = math.floor(w * cutoff_factor * 0.5)
        y2 = math.floor(h * cutoff_factor * 0.5)
        w2 = w - 2 * x2
        h2 = h - 2 * y2

        cropped = square[y+2*y2:y+h2, x+2*x2:x+w2]
        return cropped

    def center_number(self, img: cv.Mat) -> cv.Mat:
        contours = self.get_sudoku_contours(img)
        largest_contour = self.take_largest_contour(contours)
        (x, y, w, h) = cv.boundingRect(largest_contour)
        x2 = math.floor((img.shape[0] - w) / 2)
        y2 = math.floor((img.shape[1] - h) / 2)
        centered = img[y2:y2+h, x2:x2+w]
        return centered

    def detect_edges(self, img: cv.Mat) -> cv.Mat:
        edges = cv.Canny(img, 25, 50, apertureSize=3)
        return edges

    def threshold(self, img: cv.Mat) -> cv.Mat:
        smooth = cv.GaussianBlur(img, (3, 3), 0)
        ret, thresh = cv.threshold(smooth, 150, 255, cv.THRESH_BINARY)
        return thresh

    def load_image(self, file) -> cv.Mat:
        print("Loading image...")

        file_exists = os.path.isfile(file)
        if (not file_exists):
            print(f"File '{file}' not found")
            raise FileNotFoundError(f"File '{file}' not found")

        img = cv.imread(file, cv.IMREAD_GRAYSCALE)

        if (img is None):
            print("Image not loaded")
            raise Exception("Image not loaded")

        print("Loaded image")

        return img
