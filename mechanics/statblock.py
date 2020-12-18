from random import random as rnd

dice = lambda d: int(rnd() * d) + 1
mod = lambda stat: int((stat-10)/2)

class StatBlock:

    def __init__(self, Str, Agi, Vit, Mnd, Spi, hit_die, level=1):
    
        self.level = level
        self.Str = Str # Strength
        self.Agi = Agi # Agility
        self.Vit = Vit # Vitality
        self.Mnd = Mnd # Mind
        self.Spi = Spi # Spirit
        
        self.hit_die = hit_die
        
        self.max_hp = self.hit_die
        for lvl in range(level-1):
            self.max_hp += dice(self.hit_die)
        self.cur_hp = self.max_hp
        
        self.evade = 10 + mod(self.Agi) + int(self.level / 3) # + self.armour + self.buffs + self.nerfs
                
        self.exp = 0
        self.next = 500
        
    def melee_hit(self, target):
        return dice(20) + mod(self.Str) + int(self.level / 2) >= target.evade
    
    def ranged_hit(self, target):
        return dice(20) + mod(self.Agi) + int(self.level / 2) >= target.evade
        
    def level_up(self):
    
        self.level += 1
        
        # can you take a stat boost?
        if self.level % 3 == 0:
            print("Which stat would you like to boost?")
        if self.level % 4 == 0:
            print("Which new special skill would you like?")
                
        #self.fortitude = int((self.body+self.spirit) / 2)
        #self.reflex = int((self.mind+self.body) / 2)
        #self.will = int((self.spirit+self.mind) / 2)
        
        self.max_hp += dice(self.hit_die) + mod(self.Vit) # body
        self.cur_hp = self.max_hp
        self.evade = 10 + self.reflex + int(self.level / 3)
        
        self.exp = 0
        self.next = self.level * 500
        
    def add_exp(self, amount):
    
        self.exp += amount
        
        if self.exp >= self.next: self.level_up()

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
