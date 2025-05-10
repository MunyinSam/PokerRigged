import pygame as pg
from pokeractions import PokerGame, PlayerActions
from settings import Config as cf
from component import *

class GameRunner:
    def __init__(self):
        self.pygameInit()
        self.running = True
        self.gameInit()

    def pygameInit(self):
        pg.init()
        pg.display.set_caption("Poker Rigged")
        self.screen = pg.display.set_mode((cf.width, cf.height))

    def gameInit(self):
        self.current_screen = "menu"
        self.menu = Menu(self.screen)
        self.game_state = PokerGame(self.screen)
        self.game = Game(self.screen, self.game_state)
        self.display_obj = Display(self.screen)
        self.player_actions = PlayerActions(self.game, self.screen, self.game_state)

    def run(self):
        while self.running:
            self.screen.fill((6, 64, 43))
            self.mouse_pos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.current_screen == "menu" and self.menu.handle_event(event, self.mouse_pos):
                        self.current_screen = "game"
                    elif self.current_screen == "game" and self.player_actions:
                        self.player_actions.handle_event(event)

            if self.current_screen == "menu":
                self.menu.display()
            elif self.current_screen == "game":
                self.game.display()

            pg.display.flip()

        pg.quit()

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.load_fonts()
        self.create_buttons()
        self.load_title_image()

    def load_fonts(self):
        self.font_title = pg.font.Font(cf.font_title, cf.font_title_size)
        self.font_body = pg.font.Font(cf.font_body, cf.font_body_size)

    def create_buttons(self):
        button_x = cf.width / 2 - 100
        self.start_button = self.create_button(button_x, cf.height / 2, "Start Game")
        self.setting_button = self.create_button(button_x, cf.height / 2 + 50, "Setting")
        self.quit_button = self.create_button(button_x, cf.height / 2 + 100, "Quit")

    def create_button(self, x, y, text):
        return Button(
            x, y,
            cf.button_width, cf.button_height, text,
            self.font_body, cf.button_text_color,
            cf.button_hover_color, cf.button_color, True
        )

    def load_title_image(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.title = pg.image.load(cf.title_image_path)
        image_width, image_height = self.title.get_size()

        scale_factor = screen_height / image_height
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)

        self.title = pg.transform.scale(self.title, (new_width, new_height))
        self.title_x = (screen_width - new_width) // 2
        self.title_y = 0

    def display(self):
        self.screen.blit(self.title, (self.title_x, self.title_y))
        self.start_button.draw(self.screen)
        self.setting_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def handle_event(self, event, mouse_pos):
        if self.is_button_clicked(self.start_button, event, mouse_pos):
            return True
        elif self.is_button_clicked(self.quit_button, event, mouse_pos):
            pg.quit()
        return False

    def is_button_clicked(self, button, event, mouse_pos):
        return button.is_hovered(mouse_pos) and event.type == pg.MOUSEBUTTONDOWN

class Game:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.setup_fonts()
        self.load_background()
        self.create_buttons()

    def setup_fonts(self):
        self.font_body = pg.font.Font(cf.font_body, cf.font_body_size)
        self.font_small = pg.font.Font(cf.font_body, 20)

    def load_background(self):
        self.background = pg.image.load(cf.background_image_path)
        img_w, img_h = self.background.get_size()
        scale_factor = self.screen_height / img_h

        new_width = int(img_w * scale_factor)
        new_height = int(img_h * scale_factor)

        self.background = pg.transform.scale(self.background, (new_width, new_height))
        self.background_x = (self.screen_width - new_width) // 2
        self.background_y = 0

    def create_buttons(self):
        num_buttons = 4
        spacing = (self.screen_width - (cf.button_width * num_buttons)) // (num_buttons + 1)
        button_y = self.screen_height - 110
        left_space = 180

        half_w = cf.button_width2 // 2
        half_h = cf.button_height2 // 2
        raise_x = left_space + spacing * 4 + cf.button_width2 * 3
        raise_y = button_y

        # Main action buttons
        self.fold_button = self.create_button(
            left_space + spacing * 2 + cf.button_width2, button_y,
            cf.button_width2, cf.button_height2, "FOLD",
            self.font_body, (255, 0, 0), cf.button_color
        )

        self.call_button = self.create_button(
            left_space + spacing * 3 + cf.button_width2 * 2, button_y,
            cf.button_width2, cf.button_height2, "CALL",
            self.font_body, cf.button_hover_color, cf.button_color
        )

        self.raise_button = self.create_button(
            raise_x, raise_y,
            cf.button_width2, cf.button_height2, "BET/RAISE",
            self.font_body, cf.button_hover_color, cf.button_color
        )

        # Smaller action buttons
        self.check_button = self.create_button(
            left_space + spacing * 3 + cf.button_width2 * 2, button_y - half_h,
            cf.button_width2, half_h, "CHECK",
            self.font_small, (173, 216, 230), (0, 0, 0)
        )

        self.all_in_button = self.create_button(
            raise_x, raise_y - half_h,
            half_w, half_h, "ALL IN",
            self.font_small, (255, 215, 0), (0, 0, 0)
        )

        self.peek_button = self.create_button(
            raise_x + half_w, raise_y - half_h,
            half_w, half_h, "PEEK",
            self.font_small, (0, 255, 0), (0, 0, 0)
        )

        self.leave_button = self.create_button(
            10, 10,
            half_w, half_h, "QUIT",
            self.font_small, (230, 0, 0), (0, 0, 0)
        )

    def create_button(self, x, y, w, h, text, font, hover_color, bg_color):
        return Button(
            x, y, w, h, text,
            font, cf.button_text_color,
            hover_color, bg_color, True
        )

    def display(self):
        # Display Background
        self.screen.blit(self.background, (self.background_x, self.background_y))
        
        # Display Turn Text
        self.display_turn_text()

        # Display Buttons
        self.display_buttons()

        # Display Game State
        self.display_player_hands()
        self.display_community_cards()
        self.display_players()
        self.display_pot()
        # self.display_log()

        self.display_bot_actions()

        if self.game_state.bot_thinking:
            self.display_bot_thinking()

        if self.game_state.isloading:
            self.display_loading_screen()

    def display_turn_text(self):
        label_font = pg.font.Font(cf.font_body, 40)
        turn_text = label_font.render(f"{self.game_state.turn}", True, (255, 255, 255))
        label_rect = turn_text.get_rect(center=(self.screen.get_width() / 2, 50))
        
        padding_height = 10
        padding_width = 40
        bg_rect = pg.Rect(
            label_rect.left - padding_width,
            label_rect.top - padding_height,
            label_rect.width + 2 * padding_width,
            label_rect.height + 2 * padding_height
        )
        
        pg.draw.rect(self.screen, (50, 50, 50), bg_rect, border_radius=12)
        self.screen.blit(turn_text, label_rect)

    def display_buttons(self):
        # Buttons related to game actions
        buttons = [
            self.check_button, self.call_button, self.raise_button,
            self.fold_button, self.all_in_button, self.peek_button,
            self.leave_button
        ]
        for button in buttons:
            button.draw(self.screen)

    def display_player_hands(self):
        players = self.game_state.get_all_players()
        x_left, y_bottom1 = 125, cf.height - 200
        card_width, card_height = 80, 120
        hand_width = len(players[0].hand) * (card_width + 20) - 20
        hand_height = card_height + 40

        self.draw_hand(players[0], x_left, y_bottom1, card_width, card_height, hand_width, hand_height)

        center_x = self.screen_width // 2
        top_y = 140
        self.bot_hand(players[1], self.screen_width - 250, top_y, card_width, card_height, hand_width, hand_height)

    def draw_hand(self, player, x_left, y_bottom, card_width, card_height, hand_width, hand_height):
        border_padding_x, border_padding_y = 50, 20
        border_rect = pg.Rect(
            x_left - border_padding_x, y_bottom - border_padding_y,
            hand_width + border_padding_x * 2, hand_height + border_padding_y
        )
        pg.draw.rect(self.screen, (80, 80, 80), border_rect, border_radius=12)
        pg.draw.rect(self.screen, (255, 255, 255), border_rect, 2, border_radius=12)

        for card in player.hand:
            card_name = PokerGame.convert_name(card)
            card_image = pg.image.load(f"./picture/PNG-cards-1.3/{card_name}")
            card_image = pg.transform.scale(card_image, (card_width, card_height))
            self.screen.blit(card_image, (x_left, y_bottom))
            x_left += card_width + 20

        label_font = pg.font.Font(cf.font_body, 20)
        label_text = f"{player.name} Chips: {player.chips}"
        label_surface = label_font.render(label_text, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(border_rect.centerx, border_rect.bottom - 20))

        padding = 8
        bg_rect = pg.Rect(
            label_rect.left - padding,
            label_rect.top - padding,
            label_rect.width + 2 * padding,
            label_rect.height + 2 * padding
        )
        pg.draw.rect(self.screen, (80, 80, 80), bg_rect, border_radius=10)
        self.screen.blit(label_surface, label_rect)

    
    def bot_hand(self, player, x_left, y_bottom, card_width, card_height, hand_width, hand_height):
        border_padding_x, border_padding_y = 50, 20
        border_rect = pg.Rect(
            x_left - border_padding_x, y_bottom - border_padding_y,
            hand_width + border_padding_x * 2, hand_height + border_padding_y
        )
        pg.draw.rect(self.screen, (80, 80, 80), border_rect, border_radius=12)
        pg.draw.rect(self.screen, (255, 255, 255), border_rect, 2, border_radius=12)

        for card in player.hand:
            card_name = PokerGame.convert_name(card)

            if self.game_state.showcard:
                 card_image = pg.image.load(f"./picture/PNG-cards-1.3/{card_name}")
            else:
                card_image = pg.image.load(f"./picture/scene/cardback.png")
            card_image = pg.transform.scale(card_image, (card_width, card_height))
            self.screen.blit(card_image, (x_left, y_bottom))
            x_left += card_width + 20

        # Draw label for player's hand
        label_font = pg.font.Font(cf.font_body, 20)
        label_text = f"{player.name} Chips: {player.chips}"
        label_surface = label_font.render(label_text, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(border_rect.centerx, border_rect.bottom - 20))

        padding = 8
        bg_rect = pg.Rect(
            label_rect.left - padding,
            label_rect.top - padding,
            label_rect.width + 2 * padding,
            label_rect.height + 2 * padding
        )
        pg.draw.rect(self.screen, (80, 80, 80), bg_rect, border_radius=10)
        self.screen.blit(label_surface, label_rect)

    def display_community_cards(self):
        self.community_cards = self.game_state.get_community_cards()
        if self.game_state.turn == "Pre-Flop":
            return
        if len(self.community_cards) != 0:
            x, y = 197, 352
            for card in self.community_cards:
                card_name = PokerGame.convert_name(card)
                card_image = pg.image.load(f"./picture/PNG-cards-1.3/{card_name}")
                card_image = pg.transform.scale(card_image, (100, 150))
                self.screen.blit(card_image, (x, y))
                x += 126

    def display_bot_thinking(self):
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency

        font = pg.font.Font(cf.font_body, 74)  # Large font size
        text_surface = font.render("Bot is Thinking...", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text_surface, text_rect)

    def display_loading_screen(self):
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency

        font = pg.font.Font(cf.font_body, 74)
        text_surface = font.render("Loading...", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text_surface, text_rect)

    def display_players(self):
        players = self.game_state.get_all_players()
        y_offset = 60
        
        for player in players:
            label_font = pg.font.Font(cf.font_body, 20)
            player_info = f"{player.name} - Chips: {player.chips}"
            player_text = label_font.render(player_info, True, (255, 255, 255))
            self.screen.blit(player_text, (10, y_offset))
            
            y_offset += 30

    def display_pot(self):
        pot = self.game_state.get_pot()
        label_font = pg.font.Font(cf.font_body, 24)
        label_surface = label_font.render(f"Pot Total: {pot}", True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(self.screen.get_width() / 2, 300))

        padding = 10
        bg_rect = pg.Rect(
            label_rect.left - padding,
            label_rect.top - padding,
            label_rect.width + 2 * padding,
            label_rect.height + 2 * padding
        )

        pg.draw.rect(self.screen, (50, 50, 50), bg_rect, border_radius=12)
        self.screen.blit(label_surface, label_rect)

    def display_log(self):
        log = self.game_state.get_log()
        latest_logs = log[-10:]  # Show only the last 10 messages

        # Chat box dimensions
        box_width = 250
        line_height = 18
        padding = 10
        total_lines = len(latest_logs)
        box_height = line_height * 10 + 2 * padding

        x = 10
        y = self.screen.get_height() - box_height - 470  # 20px above bottom

        # Draw chat box background
        chat_box_rect = pg.Rect(x, y, box_width, box_height)
        pg.draw.rect(self.screen, (50, 50, 50), chat_box_rect, border_radius=12)
        pg.draw.rect(self.screen, (100, 100, 100), chat_box_rect, 2, border_radius=12)

        # Render text lines
        label_font = pg.font.Font(cf.font_log, 16)
        for i, message in enumerate(reversed(latest_logs)):
            label_surface = label_font.render(message, True, (255, 255, 255))
            self.screen.blit(label_surface, (x + padding, y + padding + i * line_height))

    def display_bot_actions(self):
        bot_actions = self.game_state.get_bot_actions()

        # Set the position for the text bubble
        bubble_x = 700
        bubble_y = 45  # Below the "QUIT" button
        bubble_width = 280
        bubble_height = 50

        # Render the bot's action text
        font = pg.font.Font(cf.font_body, 20)  # Use a small font size
        action_text = f"Bot chooses to {bot_actions}!" if bot_actions else ". . ."
        text_surface = font.render(action_text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + bubble_height // 2))

        # Draw the text bubble (rounded rectangle)
        bubble_rect = pg.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        pg.draw.rect(self.screen, (50, 50, 50), bubble_rect, border_radius=12)  # Background color
        pg.draw.rect(self.screen, (255, 255, 255), bubble_rect, 2, border_radius=12)  # Border color

        # Draw the text inside the bubble
        self.screen.blit(text_surface, text_rect)

