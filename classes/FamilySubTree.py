import random
import Convert


class FamilySubTree:

    _UIDPrefix = "FS"  # Must be unique across all classes!

    def __init__(self, leftparent, rightparent, children=None):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Parent1 = leftparent
        self.Parent2 = rightparent
        self.Children = Convert.List(children)
        self.Children.sort(key=lambda x: x.Age, reverse=True)

    def __str__(self):
        return self.UID

    def getDescrStratEntry(self):
        return "relative\t%s,\t%s,\t%s\tend" % (self.Parent1, self.Parent2, "\t".join(["%s," % c for c in self.Children]))
