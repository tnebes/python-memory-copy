class SizeCalculator():
    
    def __init__ (self) -> None:
        pass

    def calculate_size_in_mb(self, raw_size) -> int:
        return int(raw_size / 1024 / 1024)