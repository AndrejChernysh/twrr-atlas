
class AIProfile:

    def __init__(self, id, aihostility: int):
        self.Id: str = id
        self.AIHostility: int = aihostility
        self.Mass: int = 1
        self.InfantryLight: int = 90
        self.InfantryHeavy: int = 70
        self.InfantryMissile: int = 60
        self.InfantrySpearmen: int = 80
        self.CavalryLight: int = 40
        self.CavalryHeavy: int = 50
        self.CavalryMissile: int = 30
        self.SiegeArtillery: int = 20
        self.Special: int = 1
        self.SallyAgression: int = 1
        self.SallyDesperate: int = 100
        self.AttackRiskTaker: int = 2 if self.AIHostility > 66 else 3
        self.SubterfugeRiskTaker: int = max(round((self.AIHostility - 30) / 10), 1)
        self.BuildingPrioritiesId: str = "DoNotCareAboutRevolts"

    def __str__(self):
        return self.Id

    def getDescrAIPersonalityTXTMilitaryPriorityEntry(self):
        code = f"""
            military_priority mp_{self.Id}
            mass {self.Mass}
            infantry_light {self.InfantryLight}
            infantry_heavy {self.InfantryHeavy}
            infantry_missile {self.InfantryMissile}
            infantry_spearmen {self.InfantrySpearmen}
            cavalry_light {self.CavalryLight}
            cavalry_heavy {self.CavalryHeavy}
            cavalry_missile {self.CavalryMissile}
            siege_artillery {self.SiegeArtillery}
            special {self.Special}
            sally_agression {self.SallyAgression}
            sally_desperate {self.SallyDesperate}
            attack_risk_taker {self.AttackRiskTaker}
            subterfuge_risk_taker {self.SubterfugeRiskTaker}
        """
        return "\n".join([line.strip() for line in code.split("\n")])

    def getDescrAIPersonalityTXTDiplomaticPriorityEntry(self):
        code = f"""
            diplomatic_priority dp_{self.Id}
            aggresiveness {self.AIHostility}
        """
        return "\n".join([line.strip() for line in code.split("\n")])

    def getDescrAIPersonalityTXTPersonalitiesEntry(self):
        code = f"""
            personality ai_personality_{self.Id}
            building_priority {self.BuildingPrioritiesId}
            military_priority mp_{self.Id}
            diplomatic_priority dp_{self.Id}
        """
        return "\n".join([line.strip() for line in code.split("\n")])
