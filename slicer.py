from util import SizeCalculator
from constants import Constants

import logging
import os
import shutil
import zipfile
import io

class Slicer:
    
    def __init__(self) -> None:
        self.current_slice_size = 0
        self.save_location = ""
        self.collected_files = {}

    def slice(self, path, max_size) -> None:
        logging.debug(f"Slicing {path} into {max_size}MB slices")
        print(f"Slicing {path} into {max_size}MB slices")
        package_name = os.path.basename(path)
        self.save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), Constants.OUTPUT_FOLDER_NAME, package_name)
        try:
            iteration = 0
            for file_directory, _, files in os.walk(path):
                for file in files:
                    relative_path = ""
                    if (len(file_directory) == len(path)):
                        relative_path = file
                    else:
                        relative_path = fr"{file_directory[len(path) + 1:]}\{file}"

                    with open(os.path.join(file_directory, file), "rb") as file:
                        file_contents = io.BytesIO(file.read())
                        self.collected_files[relative_path] = file_contents
                        self.current_slice_size += SizeCalculator().calculate_size_in_mb(file_contents.getbuffer().nbytes)

                    if self.current_slice_size >= max_size:
                        new_package_name = self.__generate_package_name(package_name, iteration)
                        logging.info(f"\tReached maximum slice size of {max_size}MB. Creating {new_package_name}")
                        print(f"\tReached maximum slice size of {max_size}MB. Creating {new_package_name}")
                        self.__save_as_package(package_name, iteration, self.collected_files)
                        iteration += 1
                        self.current_slice_size = 0
                        self.collected_files = {}
                        
        except Exception as e:
            logging.error(f"Error while slicing {path}", e)
            print(e)
            raise e

    def __save_as_package(self, package_name, iteration, files) -> None:
        try:
            package_name = self.__generate_package_name(package_name, iteration)
            save_file_path = os.path.join(self.save_location, package_name)

            if not os.path.exists(self.save_location):
                os.makedirs(self.save_location)

            logging.info(f"\t\tSaving package {package_name} to {save_file_path}")

            with zipfile.ZipFile(save_file_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
                for file_name, file_contents in files.items():
                    zip_file.writestr(file_name, file_contents.getbuffer())

            logging.info(f"\t\tPackage {package_name} saved successfully at {save_file_path}")
        except Exception as e:
            logging.error(f"\t\tError while saving package {package_name}", e)
            print(e)
            raise e

    def __generate_package_name(self, package_name, iteration) -> str:
        return f"{package_name}_{iteration}.zip"
        

        

