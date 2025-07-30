import pygame
import time
from enum import Enum

class Trades(Enum):
    NONE = 0
    BINOCULARS = 1
    HEALTH = 2
    GUN = 3
    BOATPART = 4

class NPC:
    def __init__(self, x, y, hud):
        self.sprite_scale = 100
        self.originalImage = pygame.image.load("assets/Entities/Trader/Trader.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.sprite_scale, self.sprite_scale))
        self.image = self.originalImage
        self.OpenTradeMenu = False
        self.PlayerHud = hud
        self.BinocularsColor = (200, 255, 255)
        self.HealthColor = (200, 255, 255)
        self.PartColor = (200, 255, 255)
        self.GunColor = (200, 255, 255)
        self.current = Trades.NONE
        self.x = x
        self.y = y

    def get_pos(self):
        return [self.x, self.y]

    def distance_from_player(self, player):
        px, py = player.get_pos()
        dx = px - self.x
        dy = py - self.y
        return (dx ** 2 + dy ** 2) ** 0.5
    
    def render_trade_options(self, screen, TradingMenuMargin, BinocularsPrice, HealthPrice, GunPrice, PartPrice):
        BinocularsStr = "Binoculars"
        BinocularsTxt = self.PlayerHud.font.render(BinocularsStr, True, (0, 0, 0))
        screen.blit(BinocularsTxt, (150 + TradingMenuMargin + 15, 260 + TradingMenuMargin + 30))
        
        BinocularsPriceStr = f"Wood x{BinocularsPrice}"
        BinocularsPriceTxt = self.PlayerHud.font.render(BinocularsPriceStr, True, (0, 0, 0))
        screen.blit(BinocularsPriceTxt, (550 + TradingMenuMargin - 20, 260 + TradingMenuMargin + 30))

        HealthStr = "+10 Health"
        HealthTxt = self.PlayerHud.font.render(HealthStr, True, (0, 0, 0))
        screen.blit(HealthTxt, (150 + TradingMenuMargin + 15, 260 + TradingMenuMargin + 30 + 80))
       
        HealthPriceStr = f"Wood x{HealthPrice}"
        HealthPriceTxt = self.PlayerHud.font.render(HealthPriceStr, True, (0, 0, 0))
        screen.blit(HealthPriceTxt, (550 + TradingMenuMargin - 20, 260 + TradingMenuMargin + 30 + 80))

        GunStr = "Boat Part"
        GunTxt = self.PlayerHud.font.render(GunStr, True, (0, 0, 0))
        screen.blit(GunTxt, (150 + TradingMenuMargin + 15, 260 + TradingMenuMargin + 30 + 160 + 80))
        
        GunPriceStr = f"Coin x{GunPrice}"
        GunPriceTxt = self.PlayerHud.font.render(GunPriceStr, True, (0, 0, 0))
        screen.blit(GunPriceTxt, (550 + TradingMenuMargin - 30, 260 + TradingMenuMargin + 30 + 160 + 80))  

        PartStr = "Boat Part"
        PartTxt = self.PlayerHud.font.render(PartStr, True, (0, 0, 0))
        screen.blit(PartTxt, (150 + TradingMenuMargin + 15, 260 + TradingMenuMargin + 30 + 160 + 80))
        
        PartPriceStr = f"Coin x{PartPrice}"
        PartPriceTxt = self.PlayerHud.font.render(PartPriceStr, True, (0, 0, 0))
        screen.blit(PartPriceTxt, (550 + TradingMenuMargin - 30, 260 + TradingMenuMargin + 30 + 160 + 80))    

    def get_selected_trade(self, mx, my, TradingMenuMargin, player, MB1DOWN):
        if (mx <= 150 + TradingMenuMargin + 70) and (mx >= 150 + TradingMenuMargin) and (my >= 200 + TradingMenuMargin) and (my <= 200 + TradingMenuMargin + 40):
            player.EntityInCrosshair = True

            if MB1DOWN:
                player.IsTrading = False
                self.OpenTradeMenu = False

        elif (mx <= 150 + TradingMenuMargin + 480) and (mx >= 150 + TradingMenuMargin) and (my >= 260 + TradingMenuMargin + 5) and (my <= 260 + TradingMenuMargin + 5 + 70):
            if MB1DOWN:
                self.BinocularsColor = (100, 255, 255)
                self.HealthColor = (200, 255, 255)
                self.GunColor = (200, 255, 255)
                self.PartColor = (200, 255, 255)
                self.current = Trades.BINOCULARS
            
            player.EntityInCrosshair = True
        elif (mx <= 150 + TradingMenuMargin + 480) and (mx >= 150 + TradingMenuMargin) and (my >= 260 + TradingMenuMargin + 5) and (my <= 340 + TradingMenuMargin + 5 + 70):
            if MB1DOWN:
                self.BinocularsColor = (200, 255, 255)
                self.HealthColor = (100, 255, 255)
                self.GunColor = (200, 255, 255)
                self.PartColor = (200, 255, 255)
                self.current = Trades.HEALTH
            
            player.EntityInCrosshair = True
        elif (mx <= 150 + TradingMenuMargin + 480) and (mx >= 150 + TradingMenuMargin) and (my >= 260 + TradingMenuMargin + 5) and (my <= 420 + TradingMenuMargin + 5 + 70):
            if MB1DOWN:
                self.BinocularsColor = (200, 255, 255)
                self.HealthColor = (200, 255, 255)
                self.GunColor = (100, 255, 255)
                self.PartColor = (200, 255, 255)
                self.current = Trades.GUN
            player.EntityInCrosshair = True
        elif (mx <= 150 + TradingMenuMargin + 480) and (mx >= 150 + TradingMenuMargin) and (my >= 260 + TradingMenuMargin + 5) and (my <= 500 + TradingMenuMargin + 5 + 70):
            if MB1DOWN:
                self.BinocularsColor = (200, 255, 255)
                self.HealthColor = (200, 255, 255)
                self.GunColor = (200, 255, 255)
                self.PartColor = (100, 255, 255)
                self.current = Trades.BOATPART
            
            player.EntityInCrosshair = True    

    def make_trade(self, mx, my, TradingMenuMargin, player, MB1DOWN, current, BinocularsPrice, HealthPrice, PartPrice):
        if (mx <= 550 + TradingMenuMargin + 77) and (mx >= 550 + TradingMenuMargin) and (my >= 200 + TradingMenuMargin) and (my <= 200 + TradingMenuMargin + 40):
            player.EntityInCrosshair = True

            if MB1DOWN:
                match current:
                    case Trades.BINOCULARS:
                        if (not player.HasBinoculars) and (player.Logs >= BinocularsPrice):
                            player.Logs -= BinocularsPrice
                            player.HasBinoculars = True
                    case Trades.HEALTH:
                        if (player.get_health() < player.get_max_health()) and (player.Logs >= HealthPrice):
                            player.Logs -= HealthPrice
                            player.heal(0.1)
                            time.sleep(0.1)
                    case Trades.BOATPART:
                        if (not player.HasPart) and (player.Coins >= PartPrice):
                            player.Coins -= PartPrice
                            player.HasPart = True
                    case _:
                        pass

    def render_trade_ui(self, TradingMenuMargin, screen):
        TradeBtnStr = "Trade!"
        TradeBtnTxt = self.PlayerHud.font.render(TradeBtnStr, True, (255, 255, 255))

        ExitBtnStr = "Exit!"
        ExitBtnTxt = self.PlayerHud.font.render(ExitBtnStr, True, (255, 255, 255))

        YouStr = "You get"
        YouTxt = self.PlayerHud.font.render(YouStr, True, (0, 0, 0))

        PayStr = "You pay"
        PayTxt = self.PlayerHud.font.render(PayStr, True, (0, 0, 0))

        pygame.draw.rect(screen, (155, 255, 255), (150 , 200, 500, 400 + 80 - 70)) 

        pygame.draw.rect(screen, (255, 0, 0), (150 + TradingMenuMargin, 200 + TradingMenuMargin, 70, 40))
        screen.blit(ExitBtnTxt, (150 + TradingMenuMargin + 9, 200 + TradingMenuMargin + 12))


        pygame.draw.rect(screen, (0, 0, 255), (550 + TradingMenuMargin, 200 + TradingMenuMargin, 77, 40))
        screen.blit(TradeBtnTxt, ((550 + TradingMenuMargin + 5, 200 + TradingMenuMargin + 12)))

        screen.blit(YouTxt, ((150 + TradingMenuMargin + 5, 247 + TradingMenuMargin)))
        screen.blit(PayTxt, ((550 + TradingMenuMargin - 11, 247 + TradingMenuMargin)))

        pygame.draw.rect(screen, self.BinocularsColor, (150 + TradingMenuMargin, 260 + TradingMenuMargin + 5, 480, 70))
        pygame.draw.rect(screen, self.HealthColor, (150 + TradingMenuMargin, 340 + TradingMenuMargin + 5, 480, 70))
        pygame.draw.rect(screen, self.GunColor, (150 + TradingMenuMargin, 420 + TradingMenuMargin + 5, 480, 70))
        pygame.draw.rect(screen, self.PartColor, (150 + TradingMenuMargin, 500 + TradingMenuMargin + 5, 480, 70))

    def Open_Trade_Menu(self, screen, mousePos, player, MB1DOWN):
        TradingMenuMargin = 10

        BinocularsPrice = 10
        HealthPrice = 15
        GunPrice = 5
        PartPrice = 10

        mx, my = mousePos

        self.render_trade_ui(TradingMenuMargin, screen)
        self.render_trade_options(screen, TradingMenuMargin, BinocularsPrice, HealthPrice, GunPrice, PartPrice)
        self.get_selected_trade(mx, my, TradingMenuMargin, player, MB1DOWN)
        self.make_trade(mx, my, TradingMenuMargin, player, MB1DOWN, self.current, BinocularsPrice, HealthPrice, GunPrice, PartPrice)
    
    def check_click(self, mouse_pos, cx, cy, player):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))

        if (self.distance_from_player(player) < player.get_melee_reach()):
            if rect.collidepoint(mouse_pos):
                player.EntityInCrosshair = True

                if player.is_melee_attacking():
                    player.IsTrading = True
                    self.OpenTradeMenu = True
        else:
            player.IsTrading = False
            self.OpenTradeMenu = False

    def render(self, screen, cx, cy):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))
        screen.blit(self.image, rect.topleft)

    def update(self, screen, player, cx, cy, mp, MB1DOWN):
        self.render(screen, cx, cy)
        self.check_click(mp, cx, cy, player)

        if self.OpenTradeMenu:
            self.Open_Trade_Menu(screen, mp, player, MB1DOWN)