from duplicates_finder.comparisonMethod import ComparisonMethod
from duplicates_finder.find_funcs import get_data

class ComparisonObject:
    def __init__(self, file_path: str, comparison_method: ComparisonMethod):
        self.file_path = file_path
        self.object, self.comparison_data = get_data(file_path, comparison_method)
