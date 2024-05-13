import os
from pathlib import Path


class ImageSaver:
    def save(self, file) -> str:
        print("importing image file: " + str(file))
        filename = self.get_file_path(file.filename)
        print("saving to path: " + filename)
        file.save(filename)
        return filename

    def ensure_directory_exists(self, name):
        directory_exists = os.path.exists(name)
        if not directory_exists:
            os.makedirs(name)

    def get_file_path(self, name: str) -> str:
        current_path = Path(__file__).parent
        directory = os.path.join(current_path, "import-images")
        self.ensure_directory_exists(directory)
        filename = os.path.join(directory, name)
        return filename

    def try_delete_image(self, name):
        filename = self.get_file_path(name)
        try:
            os.remove(filename)
            print("deleted file: " + filename)
        except:
            print("could not delete file: " + filename)
            pass
