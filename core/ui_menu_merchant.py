
# software spec:
# 3 panes
# Selector Dialogue, Buy/Sell
# Main pane; works similar to inventory (child pane changes based on Selector position)
# Label for currency (player.money = { "gold": 0, "silver": 0, "copper": 0 })
# Child pane displays what goods are for sale ("Buy") or what goods you have for sale ("Sell").
#   'item name' $price
#   as well, not all buyers buy all products. a potion seller won't buy swords, etc.,
#
# Game.ui_settings
# UI_Group (a collection of UI elements)
#
#
#

class Game:
    def __init__(self):
        self.ui_settings = None

class UI_Theme: # Game.ui_settings
    def __init__(self, game, data):
        self.game = game
        self.font = data["ui-font"]

class UI_Group:
    def __init__(self, game):
        self.game = game
        self.settings = self.game.ui_settings

class UI_Merchant(UI_Group):
    def __init__(self, game):
        UI_Group.__init__(self, game)
        
        self.selector = UI_Selector(self.game)
        self.currency_display = UI_CurrencyDisplay(self.game)
        self.buy_display = UI_BuyDisplay(self.game)
        self.sell_display = UI_SellDisplay(self.game)
        
    def update(self):
        self.selector.update()
        self.merc_display.update()
        # after each transaction: self.currency_display.update()
