import math
import struct

import pygame
from .marble import Marble
from .wall import Wall

# Game Engine

WHITE = (255, 255, 255)
DARK = (40, 40, 50)
WALL_COLOR = (90, 90, 110)
GOAL_COLOR = (60, 200, 120)

DIFFICULTIES = {
    "Easy": (0.4, 0.03, 60000),
    "Medium": (0.6, 0.02, 45000),
    "Hard": (0.85, 0.01, 30000),
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.marble = Marble(50, 50)
        self.difficulty = "Medium"
        self.tilt_strength, self.friction, self.time_limit_ms = DIFFICULTIES[self.difficulty]
        self.max_speed = 9

        self.walls = self._build_maze()
        self.goal_x, self.goal_y, self.goal_radius = width - 60, height - 60, 22

        self.start_ticks = pygame.time.get_ticks()

        self.font = pygame.font.SysFont("Arial", 26)
        self.game_over_font = pygame.font.SysFont("Arial", 42)
        self.game_over = False
        self.result = None  # "solved" or "timeout"
        self.finish_time_ms = None
        self.quit_requested = False
        self.menu_state = "result"
        self.goal_sound_played = False
        self.timeout_sound_played = False
        self.sounds = self._initialize_sounds()

    def _initialize_sounds(self):
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            mixer_settings = pygame.mixer.get_init()
        except pygame.error as error:
            print(f"Audio unavailable: {error}")
            return {}

        if mixer_settings is None:
            print("Audio unavailable: the mixer did not initialize.")
            return {}

        sample_rate, sample_format, channels = mixer_settings
        sound_settings = {
            "wall": (180, 0.08),
            "goal": (880, 0.28),
            "timeout": (280, 0.42),
        }
        sounds = {}

        for name, (frequency, duration) in sound_settings.items():
            try:
                buffer = self._create_tone(frequency, duration, sample_rate, sample_format, channels)
                if buffer is None:
                    print(f"Could not create the {name} sound: unsupported mixer format.")
                    continue
                sounds[name] = pygame.mixer.Sound(buffer=buffer)
            except pygame.error as error:
                print(f"Could not load the {name} sound: {error}")
                continue

        return sounds

    @staticmethod
    def _create_tone(frequency, duration, sample_rate, sample_format, channels):
        formats = {
            -8: ("b", -(1 << 7), (1 << 7) - 1, 0),
            8: ("B", 0, (1 << 8) - 1, 1 << 7),
            -16: ("h", -(1 << 15), (1 << 15) - 1, 0),
            16: ("H", 0, (1 << 16) - 1, 1 << 15),
            -32: ("i", -(1 << 31), (1 << 31) - 1, 0),
            32: ("I", 0, (1 << 32) - 1, 1 << 31),
        }
        sample_format_info = formats.get(sample_format)
        if sample_format_info is None:
            return None

        pack_format, minimum, maximum, midpoint = sample_format_info
        sample_count = int(sample_rate * duration)
        amplitude = min(maximum - midpoint, midpoint - minimum) * 0.25
        samples = []

        for index in range(sample_count):
            envelope = min(1, index / (sample_rate * 0.005), (sample_count - index) / (sample_rate * 0.025))
            value = math.sin(2 * math.pi * frequency * index / sample_rate)
            sample = round(midpoint + value * amplitude * envelope)
            samples.extend([sample] * channels)

        return struct.pack(f"<{pack_format * len(samples)}", *samples)

    def _play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is None:
            return

        try:
            sound.play()
        except pygame.error as error:
            print(f"Could not play the {name} sound: {error}")
            self.sounds[name] = None

    def _build_maze(self):
        walls = []
        t = 16  # wall thickness

        # outer boundary
        walls.append(Wall(0, 0, self.width, t))
        walls.append(Wall(0, self.height - t, self.width, t))
        walls.append(Wall(0, 0, t, self.height))
        walls.append(Wall(self.width - t, 0, t, self.height))

        # a few internal walls forming a simple winding path
        walls.append(Wall(0, 140, self.width - 140, t))
        walls.append(Wall(140, 260, self.width - 140, t))
        walls.append(Wall(0, 380, self.width - 140, t))

        return walls

    def handle_event(self, event):
        if not self.game_over or event.type != pygame.KEYDOWN:
            return

        if self.menu_state == "result":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.menu_state = "difficulty"
            elif event.key == pygame.K_ESCAPE:
                self.quit_requested = True
        elif self.menu_state == "difficulty":
            if event.key == pygame.K_ESCAPE:
                self.menu_state = "result"
            else:
                difficulty_keys = {
                    pygame.K_1: "Easy",
                    pygame.K_2: "Medium",
                    pygame.K_3: "Hard",
                }
                difficulty = difficulty_keys.get(event.key)
                if difficulty is not None:
                    self._start_new_game(difficulty)

    def _start_new_game(self, difficulty):
        self.difficulty = difficulty
        self.tilt_strength, self.friction, self.time_limit_ms = DIFFICULTIES[difficulty]
        self.marble = Marble(50, 50)
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.result = None
        self.finish_time_ms = None
        self.quit_requested = False
        self.menu_state = "result"
        self.goal_sound_played = False
        self.timeout_sound_played = False

    def handle_input(self):
        if self.game_over:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.width // 2
        dy = mouse_y - self.height // 2
        dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        ax = (dx / dist) * self.tilt_strength
        ay = (dy / dist) * self.tilt_strength
        self.marble.vx += ax
        self.marble.vy += ay

    def update(self):
        if self.game_over:
            return

        elapsed = pygame.time.get_ticks() - self.start_ticks
        if elapsed >= self.time_limit_ms:
            self.game_over = True
            self.result = "timeout"
            if not self.timeout_sound_played:
                self._play_sound("timeout")
                self.timeout_sound_played = True
            return

        self.marble.vx *= (1 - self.friction)
        self.marble.vy *= (1 - self.friction)

        speed = (self.marble.vx ** 2 + self.marble.vy ** 2) ** 0.5
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.marble.vx *= scale
            self.marble.vy *= scale

        self.marble.x += self.marble.vx
        self.marble.y += self.marble.vy

        if self._resolve_wall_collisions():
            self._play_sound("wall")

        gx = self.goal_x - self.marble.x
        gy = self.goal_y - self.marble.y
        if (gx ** 2 + gy ** 2) ** 0.5 <= self.goal_radius:
            self.game_over = True
            self.result = "solved"
            self.finish_time_ms = elapsed
            if not self.goal_sound_played:
                self._play_sound("goal")
                self.goal_sound_played = True

    def _resolve_wall_collisions(self):
        bounce_factor = 0.3
        collided = False

        for wall in self.walls:
            wall_rect = wall.rect()
            closest_x = max(wall_rect.left, min(self.marble.x, wall_rect.right))
            closest_y = max(wall_rect.top, min(self.marble.y, wall_rect.bottom))
            dx = self.marble.x - closest_x
            dy = self.marble.y - closest_y
            distance_squared = dx * dx + dy * dy
            radius = self.marble.radius

            if distance_squared >= radius * radius:
                continue

            if distance_squared > 0:
                distance = distance_squared ** 0.5
                normal_x = dx / distance
                normal_y = dy / distance
                penetration = radius - distance
            else:
                is_horizontal = wall_rect.width > wall_rect.height
                is_vertical = wall_rect.height > wall_rect.width

                if is_horizontal and wall_rect.width == self.width and wall_rect.top == 0:
                    normal_x, normal_y = 0, 1
                    penetration = wall_rect.bottom - self.marble.y + radius
                elif is_horizontal and wall_rect.width == self.width and wall_rect.bottom == self.height:
                    normal_x, normal_y = 0, -1
                    penetration = self.marble.y - wall_rect.top + radius
                elif is_vertical and wall_rect.height == self.height and wall_rect.left == 0:
                    normal_x, normal_y = 1, 0
                    penetration = wall_rect.right - self.marble.x + radius
                elif is_vertical and wall_rect.height == self.height and wall_rect.right == self.width:
                    normal_x, normal_y = -1, 0
                    penetration = self.marble.x - wall_rect.left + radius
                else:
                    exits = (
                        (self.marble.x - wall_rect.left, -1, 0),
                        (wall_rect.right - self.marble.x, 1, 0),
                        (self.marble.y - wall_rect.top, 0, -1),
                        (wall_rect.bottom - self.marble.y, 0, 1),
                    )
                    edge_distance, normal_x, normal_y = min(exits, key=lambda exit: exit[0])
                    penetration = radius + edge_distance

            self.marble.x += normal_x * penetration
            self.marble.y += normal_y * penetration

            normal_velocity = self.marble.vx * normal_x + self.marble.vy * normal_y
            if normal_velocity < 0:
                collided = True
                self.marble.vx -= (1 + bounce_factor) * normal_velocity * normal_x
                self.marble.vy -= (1 + bounce_factor) * normal_velocity * normal_y

        return collided

    def render(self, screen):
        screen.fill(DARK)

        if self.game_over:
            if self.result == "solved":
                title = "Maze Solved!"
                detail = f"Finished in {self.finish_time_ms / 1000:.1f} seconds"
            else:
                title = "Time's Up!"
                detail = ""

            title_surface = self.game_over_font.render(title, True, WHITE)
            screen.blit(title_surface, title_surface.get_rect(center=(self.width // 2, self.height // 2 - 75)))

            if detail:
                detail_surface = self.font.render(detail, True, WHITE)
                screen.blit(detail_surface, detail_surface.get_rect(center=(self.width // 2, self.height // 2 - 30)))

            if self.menu_state == "result":
                options = ("Enter: Play Again", "Esc: Exit")
            else:
                options = ("Choose difficulty:", "1: Easy", "2: Medium", "3: Hard", "Esc: Back")

            for index, text in enumerate(options):
                option_surface = self.font.render(text, True, WHITE)
                y = self.height // 2 + 15 + index * 35
                screen.blit(option_surface, option_surface.get_rect(center=(self.width // 2, y)))
            return

        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall.rect())

        pygame.draw.circle(screen, GOAL_COLOR, (self.goal_x, self.goal_y), self.goal_radius)
        pygame.draw.circle(screen, WHITE, (int(self.marble.x), int(self.marble.y)), self.marble.radius)

        elapsed = pygame.time.get_ticks() - self.start_ticks
        seconds_left = max(0, (self.time_limit_ms - elapsed) // 1000)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (10, 10))
