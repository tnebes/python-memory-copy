import logging
import os
import shutil
import datetime

from validator import FileDirectoryValidator
from validator import SliceSizeValidator
from constants import Constants
from extractor import Extractor
from slicer import Slicer


class Main():

    def __init__(self) -> None:
        self.__set_up_logging()
        self.contents_location = ""
        logging.info("Starting program")
        self.__print_welcome_message()
        self.__run()

    def __run(self) -> None:
        path = ""
        try:
            path = self.__get_path()
            max_size = self.__get_max_size()
            logging.debug(f"Path: {path}, Max Size: {max_size}MB")
            self.contents_location = Extractor(path).extract()
            print("Extraction complete")

            Slicer().slice(self.contents_location, max_size)

            self.__delete_extracted_folder
            print(f"Done! Files are in {Constants.OUTPUT_FOLDER_NAME} folder.")
        except Exception as e:
            logging.error(f"Error while slicing {path}", e)
            print(e)
            return
        
    def __get_path(self) -> str:
        print("Enter the absolute path to a compressed file that you wish to slice:")
        path = input()
        try:
            file_validator = FileDirectoryValidator(path)
            if file_validator.validate_zip():
                return path      
            return self.__get_path()
        except Exception as e:
            logging.error(e)
            print(e)
            return self.__get_path()

    def __get_max_size(self) -> int:
        print("Enter the maximum size of each uncompressed slice in MB:")
        max_size = input()
        try:
            size_validator = SliceSizeValidator(max_size)
            if size_validator.validate_number():
                return int(max_size)
            return self.__get_max_size()
        except Exception as e:
            logging.error(e)
            print(e)
            return self.__get_max_size()

    def __print_welcome_message(self) -> None:
        author = "tnebes"
        version = "1.0"
        this_year = datetime.datetime.now().year
        welcome_message = f"Welcome to the Python Memory Copy Tool by {author}, {this_year}. Version {version}"
        welcome_message_length = len(welcome_message)
        print("=" * welcome_message_length)
        print(welcome_message)
        print("=" * welcome_message_length)

    def __set_up_logging(self) -> None:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), Constants.LOG_FOLDER_NAME)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, Constants.LOG_FILE_NAME)
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=log_file
        )
        logging.debug("Logging set up")

    def __delete_extracted_folder(self):
        print(f"Deleting contents in {Constants.EXTRACTED_FOLDER_NAME} folder")
        logging.debug(f"Deleting contents in {Constants.EXTRACTED_FOLDER_NAME} folder")
        if os.path.exists(self.contents_location):
            shutil.rmtree(self.contents_location)
            logging.debug(f"{Constants.EXTRACTED_FOLDER_NAME} folder deleted")
        else:
            logging.debug(f"{Constants.EXTRACTED_FOLDER_NAME} folder does not exist")
        logging.info("Deleting complete")


if __name__ == "__main__":
    Main()



