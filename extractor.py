import shutil
import logging
import os
from constants import Constants

class Extractor:

    def __init__(self, path) -> None:
        self.path = path
        self.file_name = os.path.basename(self.path).replace(Constants.ZIP_EXTENSION, "")
        self.extraction_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             Constants.EXTRACTED_FOLDER_NAME, self.file_name)

    def extract(self) -> str:
        try:
            print(f"Extracting {self.path} to {self.extraction_path}")
            logging.info(f"Extracting {self.path} to {self.extraction_path}")
            shutil.unpack_archive(self.path, self.extraction_path)
            logging.info("Extraction complete")
            print (f"Extraction complete. Extracted files are in {self.extraction_path}")
            return self.extraction_path
        except Exception as e:
            logging.error(e)
            print(e)
            raise e
