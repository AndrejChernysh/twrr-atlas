import math

import Stringtools
import Convert
import classes.Position as Position
import classes.ResourcePosition as ResourcePosition
import classes.SettlementLevel as SettlementLevel
import random
import Log
import singletons.Get as Get


class MercPool:

    _UIDPrefix = "MP"  # Must be unique across all classes!

    def __init__(self, uid, id: str, unit: str, exp: int, replenishmin: int, replenishmax: int, cap: int, initial: int):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        Log.ErrorIf(id is None, f"MercPool {uid} has no Id")
        Log.ErrorIf(unit is None, f"MercPool {uid} has no UnitId")
        Log.ErrorIf(exp is None, f"MercPool {uid} has no Exp")
        Log.ErrorIf(replenishmin is None, f"MercPool {uid} has no ReplenishMin")
        Log.ErrorIf(replenishmax is None, f"MercPool {uid} has no ReplenishMax")
        Log.ErrorIf(cap is None, f"MercPool {uid} has no Cap")
        Log.ErrorIf(initial is None, f"MercPool {uid} has no Initial")
        self.Id: str = id
        self.UnitId: str = unit
        self.Exp: int = exp
        self.ReplenishMin: int = replenishmin
        self.ReplenishMax: int = replenishmax
        self.Cap: int = cap
        self.Initial: int = initial

    def __str__(self):
        return self.UID

    def __eq__(self, other):
        return self.UID == other.UID
