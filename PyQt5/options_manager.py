class OptionsManager:
    def __init__(self):
        self.options = {
            "recursive_search": True,
            "search_by": "Content",
            "algorithm": "aHash",
            "limit_size": False,
            "limit_creation_date": False,
            "limit_changing_date": False
        }

    def set_option(self, option_name, value):
        if option_name in self.options:
            self.options[option_name] = value
            print(self.options)
        else:
            print(f"Option '{option_name}' does not exist")

    def get_option(self, option_name):
        return self.options.get(option_name, None)
