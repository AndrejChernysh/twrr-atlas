class CustomCapability:

    def __init__(self, label):
        self.Label = label
        self.Id = label.replace("%", "percent").replace("+", "plus").replace("-", "minus").replace(" ", "").replace(",", "").replace(".", "").replace("-", "").upper()

    def __str__(self):
        return self.Label
