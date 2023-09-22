import sys
sys.path.append('../src')

import logging
import os
from validator import File_Directory_Validator
from validator import Slice_Size_Validator
from constants import Constants
from extractor import Extractor
from slicer import Slicer

class Main():

    def __init__(self) -> None:
        self.__set_up_logging()
        logging.info("Starting program")
        self.__run()

    def __run(self) -> None:
        try:
            path = self.__get_path()
            max_size = self.__get_max_size()
            logging.debug(f"Path: {path}, Max Size: {max_size}MB")
            contents_location = Extractor(path).extract()
            print("Extraction complete")
        except Exception as e:
            logging.error(e)
            print(e)
            return

        print("Done!")
        
    def __get_path(self) -> str:
        print("Enter the absolute path to a compressed file that you wish to slice:")
        # path = input()
        path = r"C:\Users\tnebes\Desktop\dev\git\python-memory-copy\MechJeb2-2.14.0.0.zip"
        try:
            file_validator = File_Directory_Validator(path)
            if file_validator.validate_zip():
                return path            
        except Exception as e:
            logging.error(e)
            print(e)
            return self.__get_path()

    def __get_max_size(self) -> int:
        print("Enter the maximum size of each uncompressed slice in MB:")
        max_size = input()
        try:
            size_validator = Slice_Size_Validator(max_size)
            if size_validator.validate_number():
                return int(max_size)
        except Exception as e:
            logging.error(e)
            print(e)
            return self.__get_max_size
        
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

if __name__ == "__main__":
    Main()



