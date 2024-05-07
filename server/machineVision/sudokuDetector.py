import math
import os
import string
from typing import Sequence
import cv2 as cv
import matplotlib.pyplot as plt
import pytesseract

from models.recognizedSquare import RecognizedSquare

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

        # plt.show()

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

    def recognize_numbers(self, squares: Sequence[cv.Mat]) -> Sequence[str]:
        processed_squares = self.form_squares(squares)
        non_empty_squares = [
            square for square in processed_squares if not square.is_empty]
        non_empty_images = [square.image for square in non_empty_squares]
        all_squares_image = cv.hconcat(non_empty_images)
        border_size = 2
        bordered = cv.copyMakeBorder(
            all_squares_image, border_size, border_size, border_size, border_size, cv.BORDER_CONSTANT, value=0)
        plt.close()
        plt.imshow(bordered, cmap="gray")
        # plt.show()
        config = '--oem 3 --psm 7 -c tessedit_char_whitelist=123456789'
        numberStr = pytesseract.image_to_string(bordered, config=config)
        numberStr = numberStr.strip()
        print("detected string: " + numberStr)

        if len(numberStr) != len(non_empty_squares):
            print(f"Detected string length ({
                  len(numberStr)}) does not match number of squares ({len(non_empty_squares)})")
            return []

        for i in range(len(numberStr)):
            digit = numberStr[i]
            non_empty_squares[i].set_number(digit)

        sudoku_numbers = [square.number_str for square in processed_squares]
        return sudoku_numbers

        i = 0
        numbers = []
        ss = squares
        for square in ss:
            # 0    Orientation and script detection (OSD) only.
            # 1    Automatic page segmentation with OSD.
            # 2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
            # 3    Fully automatic page segmentation, but no OSD. (Default)
            # 4    Assume a single column of text of variable sizes.
            # 5    Assume a single uniform block of vertically aligned text.
            # 6    Assume a single uniform block of text.
            # 7    Treat the image as a single text line.
            # 8    Treat the image as a single word.
            # 9    Treat the image as a single word in a circle.
            # 10    Treat the image as a single character.
            # 11    Sparse text. Find as much text as possible in no particular order.
            # 12    Sparse text with OSD.
            # 13    Raw line. Treat the image as a single text line,
            # bypassing hacks that are Tesseract-specific.
            # config = '--oem 3 --psm 10 -c tessedit_char_whitelist=123456789'
            preprocessed = self.preprocess_square(square)
            img_pixels = preprocessed.shape[0] * preprocessed.shape[1]
            binary_area = cv.countNonZero(preprocessed)
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

    def form_squares(self, squares: Sequence[cv.Mat]) -> list[RecognizedSquare]:
        recog = []
        for i in range(len(squares)):
            square = squares[i]
            preprocessed = self.preprocess_square(square)
            is_empty = self.is_empty_square(preprocessed)

            recog.append(RecognizedSquare(preprocessed, is_empty, i))

        return recog

    def is_empty_square(self, square: cv.Mat) -> bool:
        img_pixels = square.shape[0] * square.shape[1]
        binary_area = cv.countNonZero(square)
        is_empty = img_pixels - binary_area < 0.01 * img_pixels
        return is_empty

    def preprocess_square(self, square: cv.Mat) -> cv.Mat:
        cropped = self.crop_square(square)
        squared = cv.resize(cropped, (50, 50))
        thresholded = self.threshold(squared)
        return thresholded

    def crop_square(self, square: cv.Mat) -> cv.Mat:
        (x, y, w, h) = cv.boundingRect(square)
        cutoff_factor = 0.15
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
