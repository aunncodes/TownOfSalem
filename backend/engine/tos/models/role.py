class Role:
    def __init__(self, key, name, faction, subfaction, tags, data, abilities):
        self.key = key
        self.name = name
        self.faction = faction
        self.subfaction = subfaction
        self.tags = set(tags)
        self.data = data
        self.abilities = list(abilities)

class RoleData:
    def __init__(self, investigator_result):
        self.investigator_result = investigator_result