import pygame as pg
from pokeractions import PokerGame, PlayerActions
from settings import Config as cf
from component import *
from datagraph import PokerDataDashboard

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
                        action = self.player_actions.handle_event(event)
                        if action == "quit_to_menu":
                            self.current_screen = "menu"

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
        self.statistics_button = self.create_button(button_x, cf.height / 2 + 50, "Statistics")
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
        self.statistics_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def handle_event(self, event, mouse_pos):
        if self.is_button_clicked(self.start_button, event, mouse_pos):
            return True
        elif self.is_button_clicked(self.quit_button, event, mouse_pos):
            pg.quit()
        elif self.is_button_clicked(self.statistics_button, event, mouse_pos):
            self.open_statistics()
        return False

    def is_button_clicked(self, button, event, mouse_pos):
        return button.is_hovered(mouse_pos) and event.type == pg.MOUSEBUTTONDOWN

    def open_statistics(self):
        def run_dashboard():
            dashboard = PokerDataDashboard(csv_path='data/poker_data.csv')
            dashboard.run()

        statistics_thread = threading.Thread(target=run_dashboard)
        statistics_thread.daemon = True
        statistics_thread.start()

class Game:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.bot_thinking_start_time = pg.time.get_ticks()

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
        # Define button grid layout
        button_width = 160
        button_height = 60
        button_spacing_x = 20
        button_spacing_y = 15

        start_x = 90
        start_y = self.screen_height - (button_height * 2 + button_spacing_y + 60)

        labels = [("FOLD", (255, 0, 0)),
                ("CHECK", (173, 216, 230)),
                ("CALL", cf.button_hover_color),
                ("BET/RAISE", cf.button_hover_color),
                ("ALL IN", (255, 215, 0)),
                ("PEEK", (0, 255, 0))]

        buttons = []
        for index, (text, color) in enumerate(labels):
            col = index % 3
            row = index // 3
            x = start_x + col * (button_width + button_spacing_x)
            y = start_y + row * (button_height + button_spacing_y)

            font = self.font_small if text in ("QUIT") else self.font_body
            button = self.create_button(x, y, button_width, button_height, text, font, color, cf.button_color)
            buttons.append(button)

        (self.fold_button, self.check_button, self.call_button,
        self.raise_button, self.all_in_button, self.peek_button) = buttons

        self.leave_button = self.create_button(30, 40, 80, 40, "QUIT", self.font_small, (230, 0, 0), (0, 0, 0))


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

        if self.game_state.bot_thinking:
            self.display_bot_thinking()

        if self.game_state.isloading:
            self.display_loading_screen()

    def display_turn_text(self):
        stages = ["Pre-Flop", "Flop", "Turn", "River", "Showdown"]
        current_index = stages.index(self.game_state.turn)

        label_font = pg.font.Font(cf.font_body, 28)
        highlight_font = pg.font.Font(cf.font_body, 28)
        rendered_parts = []

        for stage in stages:
            is_current = (stage == self.game_state.turn)
            font = highlight_font if is_current else label_font
            color = (0, 0, 0) if is_current else (160, 160, 160)
            text_surf = font.render(stage, True, color)
            rendered_parts.append(text_surf)

        arrow_font = pg.font.Font(cf.font_body, 28)
        arrow_surf = arrow_font.render("-", True, (100, 100, 100))

        total_width = sum(part.get_width() for part in rendered_parts) + arrow_surf.get_width() * (len(stages) - 1)
        max_height = max(part.get_height() for part in rendered_parts)

        center_x = self.screen.get_width() // 2
        y = 45
        padding_x = 60
        padding_y = 20
        bg_rect = pg.Rect(center_x - total_width // 2 - padding_x, y - padding_y,
                        total_width + padding_x * 2, max_height + padding_y * 2)

        pg.draw.rect(self.screen, (255, 255, 255), bg_rect, border_radius=12)

        pg.draw.rect(self.screen, (0, 0, 0), bg_rect, width=2, border_radius=12)

        # Draw sequence
        x = center_x - total_width // 2
        for i, surf in enumerate(rendered_parts):
            self.screen.blit(surf, (x, y))
            x += surf.get_width()
            if i < len(stages) - 1:
                self.screen.blit(arrow_surf, (x, y + 5))
                x += arrow_surf.get_width()


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
        card_width, card_height = 80, 120
        hand_spacing = 20
        num_cards = len(players[0].hand)

        hand_width = num_cards * (card_width + hand_spacing) - hand_spacing
        hand_height = card_height + 40

        center_x = self.screen_width // 2
        x_centered = center_x - hand_width // 2 - 20
        y_bottom = self.screen_height - 200

        self.draw_hand(players[0], x_centered, y_bottom, 100, 150, hand_width, hand_height)

        top_y = 140
        self.bot_hand(players[1], self.screen_width - 275, top_y, 100, 150, hand_width, hand_height)


    def draw_hand(self, player, x_right, y_bottom, card_width, card_height, hand_width, hand_height):
        total_card_width = len(player.hand) * card_width + (len(player.hand) - 1) * 20
        x_start = x_right - total_card_width + 500

        label_font = pg.font.Font(cf.font_body, 25)
        label_text = "YOUR HAND"
        label_surface = label_font.render(label_text, True, (255, 255, 255))

        label_rect = label_surface.get_rect(center=(x_start + total_card_width // 2, y_bottom - 30))
        self.screen.blit(label_surface, label_rect)

        for card in player.hand:
            card_name = PokerGame.convert_name(card)
            card_image = pg.image.load(f"./picture/PNG-cards-1.3/{card_name}")
            card_image = pg.transform.scale(card_image, (card_width, card_height))
            self.screen.blit(card_image, (x_start, y_bottom))
            x_start += card_width + 20
    
    def bot_hand(self, player, x_right, y_bottom, card_width, card_height, hand_width, hand_height):
        total_card_width = len(player.hand) * card_width + (len(player.hand) - 1) * 20
        x_start = x_right - total_card_width + 170

        label_font = pg.font.Font(cf.font_body, 25)
        label_text = "BOT HAND"
        label_surface = label_font.render(label_text, True, (255, 255, 255))

        label_rect = label_surface.get_rect(center=(x_start + total_card_width // 2, y_bottom - 10))
        self.screen.blit(label_surface, label_rect)

        for card in player.hand:
            card_name = PokerGame.convert_name(card)
            if self.game_state.showcard:
                card_image = pg.image.load(f"./picture/PNG-cards-1.3/{card_name}")
            else:
                card_image = pg.image.load(f"./picture/scene/cardback.png")

            card_image = pg.transform.scale(card_image, (card_width, card_height))
            self.screen.blit(card_image, (x_start, y_bottom + 20))
            x_start += card_width + 20

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
        overlay.fill((0, 0, 0, 128))

        elapsed_ms = pg.time.get_ticks() - self.bot_thinking_start_time
        dot_count = (elapsed_ms // 500) % 4  # Changes every 500ms: 0 to 3 dots
        dots = "." * dot_count

        font = pg.font.Font(cf.font_body, 50)
        text_surface = font.render(f"Bot is Thinking{dots}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text_surface, text_rect)


    def display_loading_screen(self):
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))

        elapsed_ms = pg.time.get_ticks() - self.bot_thinking_start_time
        dot_count = (elapsed_ms // 500) % 4
        dots = "." * dot_count

        font = pg.font.Font(cf.font_body, 50)
        text_surface = font.render(f"Loading{dots}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text_surface, text_rect)

    def display_players(self):
        players = self.game_state.get_all_players()
        y_offset = 140
        panel_width = 260
        panel_height = 75
        padding = 10
        avatar_size = 40

        label_font = pg.font.Font(cf.font_body, 18)
        chips_font = pg.font.Font(cf.font_body, 16)
        action_font = pg.font.Font(cf.font_body, 14)

        for player in players:
            is_turn = self.game_state.turn == player.name
            is_bot = player.name.lower() == "bot"

            panel_rect = pg.Rect(40, y_offset, panel_width, panel_height)
            bg_color = (245, 245, 245) if not is_turn else (255, 255, 255)
            border_color = (200, 200, 200) if not is_turn else (120, 120, 120)
            pg.draw.rect(self.screen, bg_color, panel_rect, border_radius=12)
            pg.draw.rect(self.screen, border_color, panel_rect, width=2, border_radius=12)

            # Avatar
            avatar_img = getattr(player, 'avatar', pg.Surface((avatar_size, avatar_size)))
            avatar_img.fill((180, 180, 180))  # Light grey avatar placeholder
            avatar_img = pg.transform.scale(avatar_img, (avatar_size, avatar_size))
            self.screen.blit(avatar_img, (panel_rect.left + padding, panel_rect.top + (panel_height - avatar_size) // 2))

            # Text
            text_x = panel_rect.left + padding + avatar_size + 10
            text_y = panel_rect.top + padding + 5
            self.screen.blit(label_font.render(player.name.upper(), True, (0, 0, 0)), (text_x, text_y))
            self.screen.blit(chips_font.render(f"Chips: {player.chips}", True, (50, 50, 50)), (text_x, text_y + 20))

            # Bot action
            if is_bot:
                action = self.game_state.get_bot_actions()
                action_text = f"{action.upper()}!" if action else "THINKING..."

                badge_font = pg.font.Font(cf.font_body, 22)
                badge_surf = badge_font.render(action_text, True, (0, 0, 0))
                badge_rect = badge_surf.get_rect()
                badge_rect.centerx = panel_rect.centerx + 60
                badge_rect.centery = panel_rect.top + panel_height // 2
                self.screen.blit(badge_surf, badge_rect)

            y_offset += panel_height + 12


    def display_pot(self):
        pot = self.game_state.get_pot()
        label_font = pg.font.Font(cf.font_body, 24)
        label_surface = label_font.render(f"Pot Total: {pot}", True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(self.screen.get_width() / 2, 300))

        self.screen.blit(label_surface, label_rect)
        
    # ไม่ได้ใช้
    def display_log(self):
        log = self.game_state.get_log()
        latest_logs = log[-10:]

        box_width = 250
        line_height = 18
        padding = 10
        total_lines = len(latest_logs)
        box_height = line_height * 10 + 2 * padding

        x = 10
        y = self.screen.get_height() - box_height - 470

        # Draw chat box background
        chat_box_rect = pg.Rect(x, y, box_width, box_height)
        pg.draw.rect(self.screen, (50, 50, 50), chat_box_rect, border_radius=12)
        pg.draw.rect(self.screen, (100, 100, 100), chat_box_rect, 2, border_radius=12)

        # Render text lines
        label_font = pg.font.Font(cf.font_log, 16)
        for i, message in enumerate(reversed(latest_logs)):
            label_surface = label_font.render(message, True, (255, 255, 255))
            self.screen.blit(label_surface, (x + padding, y + padding + i * line_height))


