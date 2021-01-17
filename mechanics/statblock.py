from random import random as rnd

dice = lambda d: int(rnd() * d) + 1
mod = lambda stat: int((stat-10)/2)

class StatBlock:
    def __init__(self, Str, Agi, Vit, Mnd): # Based on a Rogue for some reason
        self.combat_exp = 0
        self.craft_exp = 0
        
        self.axe_level = 0 # level += 1 * (level != 9)
        self.blade_level = 0
        self.firearm_level = 0
        self.spear_level = 0
        self.evade_level = 0
        
        self.axe_exp = 0
        self.blade_exp = 0
        self.firearm_exp = 0
        self.spear_exp = 0
        self.eva_exp = 0
        
        self.max_hp = 100
        
        self.stats = {}
        self.stats["hp"] = self.max_hp
        self.stats["str"] = Str # Strength
        self.stats["agi"] = Agi # Agility
        self.stats["vit"] = Vit # Vitality
        self.stats["mnd"] = Mnd # Mind; Intellect and Wisdom rolled into one
                
        self.stats["evade"] = 10 + mod(self.stats["agi"]) + int(self.evade_level / 3) # + self.armour + self.buffs + self.nerfs
        self.stats["immunity"] = 2 + mod(self.stats["vit"])
        self.stats["will"] = 2 + mod(self.stats["mnd"])
                
    def melee_hit(self, target):
        return dice(20) + mod(self.Str) + int(self.level / 2) >= target.evade
    
    def ranged_hit(self, target):
        return dice(20) + mod(self.Agi) + int(self.level / 2) >= target.evade
        
    #def add_exp(self, amount, exp_type): # (self, int, str)
    #    self.__setattr__(exp_type, amount)

