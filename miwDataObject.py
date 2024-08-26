class MiwDataClass:
    def __init__(self):
        self.name = ""
        self.wins = 0
        self.kills = 0
        self.finals = 0
        self.witherDamage = 0
        self.witherKills = 0
        self.deaths = 0
        self.arrowsHit = 0
        self.arrowsShot = 0
        self.tkd = 0
        self.kd = 0
        self.fd = 0
        self.wdd = 0
        self.wkd = 0
        self.aa = 0

def get_miw_data(data):
    miwDataObject = MiwDataClass()
    miwDataObject.name = data["player"]["displayname"]
    miwDataObject.wins = data["player"]["stats"]["Arcade"]["wins_mini_walls"]
    miwDataObject.kills = data["player"]["stats"]["Arcade"]["kills_mini_walls"]
    miwDataObject.finals = data["player"]["stats"]["Arcade"]["final_kills_mini_walls"]
    miwDataObject.witherKills = data["player"]["stats"]["Arcade"]["wither_kills_mini_walls"]
    miwDataObject.witherDamage = data["player"]["stats"]["Arcade"]["wither_damage_mini_walls"]
    miwDataObject.deaths = data["player"]["stats"]["Arcade"]["deaths_mini_walls"]
    miwDataObject.arrowsHit = data["player"]["stats"]["Arcade"]["arrows_hit_mini_walls"]
    miwDataObject.arrowsShot = data["player"]["stats"]["Arcade"]["arrows_shot_mini_walls"]

    miwDataObject.tkd = round((miwDataObject.kills + miwDataObject.finals) / miwDataObject.deaths, 2)
    miwDataObject.kd = round(miwDataObject.kills / miwDataObject.deaths, 2)
    miwDataObject.fd = round(miwDataObject.finals / miwDataObject.deaths, 2)
    miwDataObject.wdd = round(miwDataObject.witherDamage / miwDataObject.deaths, 2)
    miwDataObject.wkd = round(miwDataObject.witherKills / miwDataObject.deaths, 2)
    miwDataObject.aa = round(miwDataObject.arrowsHit / miwDataObject.arrowsShot, 2)

    return miwDataObject
