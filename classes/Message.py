import Stringtools


class Message:

    def __init__(self, title, text):
        hash = Stringtools.Hash(title + text)
        self.Id = str(hash).upper()
        self.Title = title
        self.Text = text

    def getEntriesExpandedBITxt(self):
        title = f"{{{self.Id}_TITLE}}{self.Title}"
        text = f"{{{self.Id}_BODY}}{self.Text}"
        text = text.replace("|", "\\n")
        return f"{title}\n{text}"
