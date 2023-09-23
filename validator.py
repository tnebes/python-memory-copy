import os
from exceptions import NotFileError
from constants import Constants

class FileDirectoryValidator:

    def __init__(self, path) -> None:
        self.path = path

    def validate_file(self) -> bool:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File {self.path} not found")

        if not os.path.isfile(self.path):
            raise NotFileError(f"{self.path} is not a file")

        if not os.access(self.path, os.R_OK):
            raise PermissionError(f"File {self.path} is not readable")

        return True
    
    def validate_dir(self) -> bool:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Directory {self.path} not found")

        if not os.path.isdir(self.path):
            raise NotFileError(f"{self.path} is not a directory")

        if not os.access(self.path, os.R_OK):
            raise PermissionError(f"Directory {self.path} is not readable")

        return True
    
    def validate_zip(self) -> bool:
        if not self.validate_file():
            return False
        if self.path.endswith(Constants.ZIP_EXTENSION):
            return True
        raise NotFileError(f"{self.path} is not a zip file")
    

class SliceSizeValidator:

    def __init__(self, number) -> None:
        self.number = number

    def validate_number(self) -> bool:
        try:
            number = int(self.number)
        except ValueError:
            raise ValueError(f"{self.number} is not a valid number")
        if number < Constants.MINIMUM_FILE_SIZE:
            raise ValueError(f"{self.number} must be greater than 0")
        if number > Constants.MAXIMUM_FILE_SIZE:
            raise ValueError(f"{self.number} must be less than 1000")
        return True


    
