import random
import classes.Position as Position
import classes.Resource as Resource
import singletons.Get as Get


class ResourcePosition:

    _UIDPrefix = "RP"  # Must be unique across all classes!

    def __init__(self, resource: Resource, position: Position):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Resource = resource
        self.Position = position
        self.Quantity = random.randint(1, Get.Setting("ResourceQuantityMax"))

    def __str__(self):
        return self.UID
