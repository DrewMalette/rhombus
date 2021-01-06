from random import random as rnd

dice = lambda d: int(rnd() * d) + 1
mod = lambda stat: int((stat-10)/2)

class StatBlock:

    def __init__(self, Str, Agi, Vit, Mind): # Based on a Rogue for some reason
        self.Str = Str # Strength
        self.Agi = Agi # Agility
        self.Vit = Vit # Vitality
        self.Mnd = Mnd # Mind; Intellect and Wisdom rolled into one
        
        self.max_hp = self.cur_hp = 100
        
        self.evade = 10 + mod(self.Agi) + int(self.evade_level / 3) # + self.armour + self.buffs + self.nerfs
        
        self.reflex = 2 * mod(self.Agi)
        self.fortitude = 2 * mod(self.Vit)
        self.will = 2 * mod(self.Mnd)
        
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
        
    def melee_hit(self, target):
        return dice(20) + mod(self.Str) + int(self.level / 2) >= target.evade
    
    def ranged_hit(self, target):
        return dice(20) + mod(self.Agi) + int(self.level / 2) >= target.evade
        
    #def add_exp(self, amount, exp_type): # (self, int, str)
    #    self.__setattr__(exp_type, amount)

if __name__ == "__main__":

    player = StatBlock(13,10,12,12,10,10)
    wolf = StatBlock(14,12,12,5,12,8)

    hit = 0
    miss = 0

    for i in range(100):
        result = wolf.melee_hit(player)
        if result == True:
            hit += 1
        else:
            miss += 1
    print(hit)
    print(miss)
