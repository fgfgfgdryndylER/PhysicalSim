import pygame
import pymunk
import pymunk.pygame_util
import math
import random
from enum import Enum

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Физическая симуляция: автомобиль, жидкости, взрывы")
clock = pygame.time.Clock()

# ==================== Локализация ====================
LANGUAGES = {
    'ru': {
        'name': 'Русский',
        'font': 'Segoe UI',
        'car': 'Автомобиль',
        'engine_tank': 'Двигатель + бак',
        'fuel_tank': 'Бензобак',
        'soft_body': 'Мягкое тело',
        'water': 'Вода',
        'fuel': 'Топливо',
        'explosive': 'Взрывчатка',
        'clear': 'Очистить всё',
        'info': 'T: цунами | H: ураган | C: автомобиль (мышь) | Передачи: RShift/RCtrl | Клик по объекту – показать параметры',
        'dashboard_title': 'Детали объекта:',
        'speed': 'Скорость: {:.1f}',
        'engine_state_on': 'Заведён',
        'engine_state_off': 'Выключен',
        'rpm': 'Обороты: {:.0f} об/мин',
        'gear': 'Передача: {} (передаточное {:.2f})',
        'torque': 'Крутящий момент: {:.0f} Н·м',
        'engine_temp': 'Температура двигателя: {:.0f}°C',
        'fuel_level': 'Топливо: {:.1f}/{:.0f} л',
        'consumption': 'Расход: {:.1f} л/с',
        'engine_type': 'Тип: Двигатель',
        'fuel_tank_type': 'Тип: Топливный бак',
        'leak': 'Протечка: {}',
        'yes': 'Да',
        'no': 'Нет',
        'engine_on_indicator': 'Engine ON',
        'select_lang': 'Выберите язык / Select language / Seleccione idioma:',
        'press_key': 'Нажмите 1 (RU), 2 (EN), 3 (ES)'
    },
    'en': {
        'name': 'English',
        'font': 'Segoe UI',
        'car': 'Car',
        'engine_tank': 'Engine + tank',
        'fuel_tank': 'Fuel tank',
        'soft_body': 'Soft body',
        'water': 'Water',
        'fuel': 'Fuel',
        'explosive': 'Explosive',
        'clear': 'Clear all',
        'info': 'T: tsunami | H: hurricane | C: car (mouse) | Gears: RShift/RCtrl | Click on object – show parameters',
        'dashboard_title': 'Object details:',
        'speed': 'Speed: {:.1f}',
        'engine_state_on': 'Started',
        'engine_state_off': 'Off',
        'rpm': 'RPM: {:.0f}',
        'gear': 'Gear: {} (ratio {:.2f})',
        'torque': 'Torque: {:.0f} N·m',
        'engine_temp': 'Engine temperature: {:.0f}°C',
        'fuel_level': 'Fuel: {:.1f}/{:.0f} L',
        'consumption': 'Consumption: {:.1f} L/s',
        'engine_type': 'Type: Engine',
        'fuel_tank_type': 'Type: Fuel tank',
        'leak': 'Leak: {}',
        'yes': 'Yes',
        'no': 'No',
        'engine_on_indicator': 'Engine ON',
        'select_lang': 'Select language:',
        'press_key': 'Press 1 (RU), 2 (EN), 3 (ES)'
    },
    'es': {
        'name': 'Español',
        'font': 'Segoe UI',
        'car': 'Coche',
        'engine_tank': 'Motor + tanque',
        'fuel_tank': 'Tanque de combustible',
        'soft_body': 'Cuerpo blando',
        'water': 'Agua',
        'fuel': 'Combustible',
        'explosive': 'Explosivo',
        'clear': 'Borrar todo',
        'info': 'T: tsunami | H: huracán | C: coche (ratón) | Marchas: RShift/RCtrl | Clic en objeto – mostrar parámetros',
        'dashboard_title': 'Detalles del objeto:',
        'speed': 'Velocidad: {:.1f}',
        'engine_state_on': 'Encendido',
        'engine_state_off': 'Apagado',
        'rpm': 'RPM: {:.0f}',
        'gear': 'Marcha: {} (relación {:.2f})',
        'torque': 'Par motor: {:.0f} N·m',
        'engine_temp': 'Temperatura motor: {:.0f}°C',
        'fuel_level': 'Combustible: {:.1f}/{:.0f} L',
        'consumption': 'Consumo: {:.1f} L/s',
        'engine_type': 'Tipo: Motor',
        'fuel_tank_type': 'Tipo: Tanque combustible',
        'leak': 'Fuga: {}',
        'yes': 'Sí',
        'no': 'No',
        'engine_on_indicator': 'Motor ON',
        'select_lang': 'Seleccione idioma:',
        'press_key': 'Presione 1 (RU), 2 (EN), 3 (ES)'
    }
}

# Глобальная переменная для текущего языка
current_lang = None
lang_data = None
font = None
big_font = None
mono_font = None

def select_language():
    """Меню выбора языка перед запуском симуляции"""
    lang_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Выбор языка / Language selection")
    font_large = pygame.font.SysFont("Segoe UI", 48)
    font_medium = pygame.font.SysFont("Segoe UI", 32)
    
    waiting = True
    selected = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = 'ru'
                    waiting = False
                elif event.key == pygame.K_2:
                    selected = 'en'
                    waiting = False
                elif event.key == pygame.K_3:
                    selected = 'es'
                    waiting = False
        
        lang_screen.fill((1, 92, 153))  # BACKGROUND
        # Заголовок на трёх языках
        title_ru = font_large.render(LANGUAGES['ru']['select_lang'], True, (255,255,255))
        title_en = font_large.render(LANGUAGES['en']['select_lang'], True, (255,255,255))
        title_es = font_large.render(LANGUAGES['es']['select_lang'], True, (255,255,255))
        lang_screen.blit(title_ru, (WIDTH//2 - title_ru.get_width()//2, HEIGHT//2 - 100))
        lang_screen.blit(title_en, (WIDTH//2 - title_en.get_width()//2, HEIGHT//2 - 50))
        lang_screen.blit(title_es, (WIDTH//2 - title_es.get_width()//2, HEIGHT//2))
        
        # Подсказка
        prompt = font_medium.render(LANGUAGES['ru']['press_key'], True, (255,255,255))
        lang_screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 50))
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    return selected

# ==================== Остальной код (классы, функции) ====================
# Здесь должны быть все классы (LiquidParticle, SoftBody, Engine, FuelTank, Gearbox, Car) и функции,
# но без текстовых строк, которые зависят от языка. Тексты для отображения будут браться из lang_data.
# Для краткости я перечислю только изменённые части (кнопки, дашборд, info), а полный код можно восстановить из предыдущего ответа.

# Цвета
BACKGROUND = (1, 92, 153)      # #015C99
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)

# Пространство Pymunk
space = pymunk.Space()
space.gravity = (0, 900)

# Глобальные списки объектов
liquid_particles = []   # все частицы жидкости
soft_bodies = []        # мягкие тела
cars = []               # автомобили
engines = []            # отдельные двигатели (не в машине)
fuel_tanks = []         # отдельные баки

# Переменная для хранения выбранного объекта для отображения параметров
selected_object = None   # может быть Car, Engine, FuelTank

# Типы жидкостей
class LiquidType(Enum):
    WATER = 0
    FUEL = 1
    EXPLOSIVE = 2

# ========== Класс LiquidParticle (без изменений) ==========
class LiquidParticle:
    def __init__(self, x, y, ltype=LiquidType.WATER):
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 3))
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 3)
        self.shape.elasticity = 0.1
        self.shape.friction = 0.3
        self.ltype = ltype
        self.color = {
            LiquidType.WATER: BLUE,
            LiquidType.FUEL: YELLOW,
            LiquidType.EXPLOSIVE: ORANGE
        }[ltype]
        self.on_fire = False
        self.fire_timer = 0
        space.add(self.body, self.shape)
        liquid_particles.append(self)

    def ignite(self):
        if not self.on_fire and self.ltype in (LiquidType.FUEL, LiquidType.EXPLOSIVE):
            self.on_fire = True
            self.fire_timer = 2.0
            self.color = RED

    def update(self, dt):
        if self.on_fire:
            self.fire_timer -= dt
            if self.fire_timer <= 0:
                if self.ltype == LiquidType.EXPLOSIVE:
                    explode_at(self.body.position, 200)
                space.remove(self.body, self.shape)
                liquid_particles.remove(self)
                return False
            for body in space.bodies:
                if body.body_type != pymunk.Body.STATIC:
                    dx = body.position.x - self.body.position.x
                    dy = body.position.y - self.body.position.y
                    dist = math.hypot(dx, dy)
                    if dist < 40:
                        force = 100 / (dist + 1)
                        direction = (dx/dist, dy/dist) if dist > 0 else (0,0)
                        body.apply_impulse_at_local_point((direction[0]*force, direction[1]*force))
        return True

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.body.position.x), int(self.body.position.y)), 3)

# ========== Класс SoftBody (без изменений) ==========
class SoftBody:
    def __init__(self, x, y, width, height, rows, cols):
        self.particles = []
        self.springs = []
        self.rows = rows
        self.cols = cols
        spacing_x = width / (cols - 1)
        spacing_y = height / (rows - 1)
        for i in range(rows):
            for j in range(cols):
                px = x + j * spacing_x
                py = y + i * spacing_y
                body = pymunk.Body(0.5, pymunk.moment_for_circle(0.5, 0, 4))
                body.position = px, py
                shape = pymunk.Circle(body, 4)
                shape.elasticity = 0.3
                shape.friction = 0.5
                space.add(body, shape)
                self.particles.append(body)
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                if j < cols - 1:
                    self.add_spring(idx, idx + 1)
                if i < rows - 1:
                    self.add_spring(idx, idx + cols)
                if i < rows - 1 and j < cols - 1:
                    self.add_spring(idx, idx + cols + 1)
                if i < rows - 1 and j > 0:
                    self.add_spring(idx, idx + cols - 1)
        soft_bodies.append(self)

    def add_spring(self, a, b):
        spring = pymunk.constraints.DampedSpring(self.particles[a], self.particles[b],
                                                 (0,0), (0,0), 30, 100, 1)
        space.add(spring)
        self.springs.append(spring)

    def draw(self):
        for p in self.particles:
            pygame.draw.circle(screen, GREEN, (int(p.position.x), int(p.position.y)), 4)
        for s in self.springs:
            a = s.a.position
            b = s.b.position
            pygame.draw.line(screen, GREEN, (int(a.x), int(a.y)), (int(b.x), int(b.y)), 1)

# ========== Класс Engine (без изменений) ==========
class Engine:
    def __init__(self, x, y, fuel_tank):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.sensor = True
        space.add(self.body, self.shape)
        self.fuel_tank = fuel_tank
        self.active = False
        self.force_magnitude = 0
        self.explosion_radius = 30
        self.cooldown = 0
        self.temperature = 20.0
        self.rpm = 0

    def update(self, throttle):
        if self.cooldown > 0:
            self.cooldown -= 1
        if throttle > 0 and self.fuel_tank.has_fuel() and self.cooldown == 0:
            fuel_used = self.fuel_tank.use_fuel(throttle * 0.01)
            if fuel_used > 0:
                self.force_magnitude = throttle * 5
                self.rpm = throttle * 3000
                self.temperature += throttle * 2
                for body in space.bodies:
                    if body.body_type != pymunk.Body.STATIC:
                        dx = body.position.x - self.body.position.x
                        dy = body.position.y - self.body.position.y
                        dist = math.hypot(dx, dy)
                        if dist < self.explosion_radius and dist > 0:
                            force_dir = (dx/dist, dy/dist)
                            force = self.force_magnitude * 50 / (dist + 1)
                            body.apply_impulse_at_local_point((force_dir[0]*force, force_dir[1]*force))
                self.cooldown = 5
        else:
            self.rpm = 0
        self.temperature -= 1
        self.temperature = max(20, min(200, self.temperature))

    def draw(self):
        color = RED if self.active else GRAY
        pygame.draw.circle(screen, color, (int(self.body.position.x), int(self.body.position.y)), 15)
        pygame.draw.circle(screen, BLACK, (int(self.body.position.x), int(self.body.position.y)), 15, 2)

# ========== Класс FuelTank (без изменений) ==========
class FuelTank:
    def __init__(self, x, y, capacity=100):
        self.body = pymunk.Body(5, pymunk.moment_for_box(5, (30, 30)))
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (30, 30))
        self.shape.elasticity = 0.2
        space.add(self.body, self.shape)
        self.capacity = capacity
        self.fuel = capacity
        self.leaking = False

    def has_fuel(self):
        return self.fuel > 0

    def use_fuel(self, amount):
        used = min(amount, self.fuel)
        self.fuel -= used
        if self.fuel <= 0:
            self.leaking = True
        return used

    def draw(self):
        color = YELLOW if self.fuel > 0 else GRAY
        pygame.draw.rect(screen, color, (int(self.body.position.x-15), int(self.body.position.y-15), 30, 30))
        pygame.draw.rect(screen, BLACK, (int(self.body.position.x-15), int(self.body.position.y-15), 30, 30), 2)
        fuel_height = int(30 * (self.fuel / self.capacity))
        pygame.draw.rect(screen, GREEN, (int(self.body.position.x-15), int(self.body.position.y+15-fuel_height), 30, fuel_height))

# ========== Класс Gearbox (без изменений) ==========
class Gearbox:
    def __init__(self, x, y):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.gear = 1
        self.ratios = {1: 3.0, 2: 2.0, 3: 1.5, 4: 1.0, 5: 0.8}
        self.max_gear = 5
        self.gear_change_time = 0

    def shift_up(self):
        if self.gear < self.max_gear:
            self.gear += 1
            self.gear_change_time = 0.2

    def shift_down(self):
        if self.gear > 1:
            self.gear -= 1
            self.gear_change_time = 0.2

    def get_ratio(self):
        return self.ratios[self.gear]

    def update(self, dt):
        if self.gear_change_time > 0:
            self.gear_change_time -= dt

    def draw(self):
        pygame.draw.rect(screen, GRAY, (int(self.body.position.x-20), int(self.body.position.y-20), 40, 40))
        text = font.render(f"G{self.gear}", True, BLACK)
        screen.blit(text, (self.body.position.x-10, self.body.position.y-10))

# ========== Класс Car (без изменений) ==========
class Car:
    def __init__(self, x, y):
        self.chassis = pymunk.Body(20, pymunk.moment_for_box(20, (60, 30)))
        self.chassis.position = x, y
        self.chassis_shape = pymunk.Poly.create_box(self.chassis, (60, 30))
        self.chassis_shape.elasticity = 0.3
        self.chassis_shape.friction = 0.7
        space.add(self.chassis, self.chassis_shape)

        self.wheels = []
        wheel_positions = [(-25, -15), (25, -15), (-25, 15), (25, 15)]
        for wx, wy in wheel_positions:
            body = pymunk.Body(2, pymunk.moment_for_circle(2, 0, 8))
            body.position = x + wx, y + wy
            shape = pymunk.Circle(body, 8)
            shape.elasticity = 0.5
            shape.friction = 1.0
            space.add(body, shape)
            self.wheels.append(body)
            joint = pymunk.constraints.PinJoint(self.chassis, body, (wx, wy), (0,0))
            space.add(joint)

        self.fuel_tank = FuelTank(x-20, y+20)
        self.engine = Engine(x, y+10, self.fuel_tank)
        self.gearbox = Gearbox(x+20, y-10)

        self.engine_started = False
        self.throttle = 0
        self.brake = 0
        self.steering = 0
        self.velocity_threshold = 200

        self.torque = 0
        self.fuel_consumption = 0
        self.speed = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.throttle = 0
        self.brake = 0
        self.steering = 0

        if self.engine_started:
            if keys[pygame.K_UP]:
                self.throttle = 1
            if keys[pygame.K_DOWN]:
                self.brake = 1
            if keys[pygame.K_LEFT]:
                self.steering = -1
            if keys[pygame.K_RIGHT]:
                self.steering = 1
            if keys[pygame.K_RSHIFT]:
                self.gearbox.shift_up()
            if keys[pygame.K_RCTRL]:
                self.gearbox.shift_down()

        self.speed = math.hypot(self.chassis.velocity.x, self.chassis.velocity.y)
        if not self.engine_started and self.speed > self.velocity_threshold:
            self.engine_started = True

        ratio = self.gearbox.get_ratio()
        engine_force = self.throttle * 500 * ratio
        self.torque = engine_force
        if self.brake:
            engine_force = 0
            for wheel in self.wheels:
                wheel.velocity = (wheel.velocity.x * 0.95, wheel.velocity.y * 0.95)

        if self.engine_started and engine_force > 0:
            for i in [2,3]:
                wheel = self.wheels[i]
                direction = (math.cos(self.chassis.angle), math.sin(self.chassis.angle))
                wheel.apply_impulse_at_local_point((direction[0]*engine_force*dt, direction[1]*engine_force*dt))

        if self.steering != 0:
            torque = self.steering * 200
            self.chassis.apply_impulse_at_local_point((torque, 0))

        self.engine.update(self.throttle if self.engine_started else 0)
        self.gearbox.update(dt)

        if self.engine_started and self.throttle > 0:
            self.fuel_consumption = self.throttle * 0.2 * ratio
        else:
            self.fuel_consumption = 0

    def draw(self):
        points = self.chassis_shape.get_vertices()
        rotated = [self.chassis.position + p.rotated(self.chassis.angle) for p in points]
        pygame.draw.polygon(screen, RED, [(int(p.x), int(p.y)) for p in rotated])
        for w in self.wheels:
            pygame.draw.circle(screen, BLACK, (int(w.position.x), int(w.position.y)), 8)
        self.fuel_tank.draw()
        self.engine.draw()
        self.gearbox.draw()
        if self.engine_started:
            text = font.render(lang_data['engine_on_indicator'], True, GREEN)
            screen.blit(text, (self.chassis.position.x-20, self.chassis.position.y-30))

# ========== Вспомогательные функции ==========
def explode_at(pos, force):
    for body in space.bodies:
        if body.body_type != pymunk.Body.STATIC:
            dx = body.position.x - pos.x
            dy = body.position.y - pos.y
            dist = math.hypot(dx, dy)
            if dist < 100:
                direction = (dx/dist, dy/dist) if dist > 0 else (0,0)
                imp = force * 200 / (dist + 1)
                body.apply_impulse_at_local_point((direction[0]*imp, direction[1]*imp))

def create_tsunami(x, y):
    for _ in range(300):
        LiquidParticle(x + random.uniform(-150,150), y + random.uniform(-80,80), LiquidType.WATER)

def hurricane_force():
    center = (WIDTH//2, HEIGHT//2)
    for body in space.bodies:
        if body.body_type != pymunk.Body.STATIC:
            dx = body.position.x - center[0]
            dy = body.position.y - center[1]
            dist = math.hypot(dx, dy)
            if dist > 0:
                force = 5000 / (dist + 1)
                direction = (dx/dist, dy/dist)
                perp = (-direction[1], direction[0])
                force_vec = (direction[0]*force*0.3 + perp[0]*force*0.7,
                             direction[1]*force*0.3 + perp[1]*force*0.7)
                body.apply_impulse_at_local_point(force_vec)

def check_ignitions(dt):
    for body in space.bodies:
        if body.body_type == pymunk.Body.STATIC:
            continue
        speed = math.hypot(body.velocity.x, body.velocity.y)
        if speed < 150:
            continue
        for part in liquid_particles:
            if part.on_fire:
                continue
            if part.ltype in (LiquidType.FUEL, LiquidType.EXPLOSIVE):
                dist = (body.position - part.body.position).length
                if dist < 5 + 3:
                    part.ignite()

def select_object_at(pos):
    for car in cars:
        x, y = pos
        dx = car.chassis.position.x - x
        dy = car.chassis.position.y - y
        if abs(dx) < 40 and abs(dy) < 30:
            return car
    for eng in engines:
        x, y = pos
        dx = eng.body.position.x - x
        dy = eng.body.position.y - y
        if abs(dx) < 20 and abs(dy) < 20:
            return eng
    for tank in fuel_tanks:
        x, y = pos
        dx = tank.body.position.x - x
        dy = tank.body.position.y - y
        if abs(dx) < 20 and abs(dy) < 20:
            return tank
    return None

def draw_dashboard(obj):
    if obj is None:
        return
    x_start = WIDTH - 280
    y_start = 20
    panel_width = 260
    panel_height = 200
    pygame.draw.rect(screen, (0,0,0,180), (x_start, y_start, panel_width, panel_height))
    pygame.draw.rect(screen, WHITE, (x_start, y_start, panel_width, panel_height), 2)
    title = mono_font.render(lang_data['dashboard_title'], True, WHITE)
    screen.blit(title, (x_start+10, y_start+5))

    if isinstance(obj, Car):
        lines = [
            lang_data['speed'].format(obj.speed),
            f"{lang_data['engine_state_on'] if obj.engine_started else lang_data['engine_state_off']}",
            lang_data['rpm'].format(obj.engine.rpm),
            lang_data['gear'].format(obj.gearbox.gear, obj.gearbox.get_ratio()),
            lang_data['torque'].format(obj.torque),
            lang_data['engine_temp'].format(obj.engine.temperature),
            lang_data['fuel_level'].format(obj.fuel_tank.fuel, obj.fuel_tank.capacity),
            lang_data['consumption'].format(obj.fuel_consumption)
        ]
        for i, line in enumerate(lines):
            text = mono_font.render(line, True, WHITE)
            screen.blit(text, (x_start+10, y_start+30 + i*20))
    elif isinstance(obj, Engine):
        lines = [
            lang_data['engine_type'],
            lang_data['rpm'].format(obj.rpm),
            lang_data['engine_temp'].format(obj.temperature),
            lang_data['fuel_level'].format(obj.fuel_tank.fuel, obj.fuel_tank.capacity)
        ]
        for i, line in enumerate(lines):
            text = mono_font.render(line, True, WHITE)
            screen.blit(text, (x_start+10, y_start+30 + i*20))
    elif isinstance(obj, FuelTank):
        leak_text = lang_data['yes'] if obj.leaking else lang_data['no']
        lines = [
            lang_data['fuel_tank_type'],
            lang_data['fuel_level'].format(obj.fuel, obj.capacity),
            lang_data['leak'].format(leak_text)
        ]
        for i, line in enumerate(lines):
            text = mono_font.render(line, True, WHITE)
            screen.blit(text, (x_start+10, y_start+30 + i*20))

# ========== Меню (кнопки) ==========
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.color = GRAY
        self.hover = False

    def draw(self, surf):
        color = (100,100,100) if self.hover else self.color
        pygame.draw.rect(surf, color, self.rect)
        pygame.draw.rect(surf, BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

def create_car_at_mouse():
    x, y = pygame.mouse.get_pos()
    cars.append(Car(x, y))

def create_engine_at_mouse():
    x, y = pygame.mouse.get_pos()
    tank = FuelTank(x-30, y)
    engine = Engine(x, y, tank)
    engines.append(engine)
    fuel_tanks.append(tank)

def create_fuel_tank_at_mouse():
    x, y = pygame.mouse.get_pos()
    fuel_tanks.append(FuelTank(x, y))

def create_soft_body_at_mouse():
    x, y = pygame.mouse.get_pos()
    SoftBody(x, y, 100, 80, 5, 7)

def create_water_at_mouse():
    x, y = pygame.mouse.get_pos()
    for _ in range(20):
        LiquidParticle(x + random.randint(-20,20), y + random.randint(-20,20), LiquidType.WATER)

def create_fuel_at_mouse():
    x, y = pygame.mouse.get_pos()
    for _ in range(15):
        LiquidParticle(x + random.randint(-20,20), y + random.randint(-20,20), LiquidType.FUEL)

def create_explosive_at_mouse():
    x, y = pygame.mouse.get_pos()
    for _ in range(10):
        LiquidParticle(x + random.randint(-20,20), y + random.randint(-20,20), LiquidType.EXPLOSIVE)

def clear_all():
    global liquid_particles, soft_bodies, cars, engines, fuel_tanks, selected_object
    for body in space.bodies[:]:
        if body.body_type != pymunk.Body.STATIC:
            space.remove(body)
    liquid_particles.clear()
    soft_bodies.clear()
    cars.clear()
    engines.clear()
    fuel_tanks.clear()
    selected_object = None
    add_boundaries()

def add_boundaries():
    static_lines = [
        pymunk.Segment(space.static_body, (0, HEIGHT-50), (WIDTH, HEIGHT-50), 5),
        pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5),
        pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5),
        pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 5),
    ]
    for line in static_lines:
        line.elasticity = 0.5
        line.friction = 0.5
        space.add(line)
    ground_block = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground_block.position = WIDTH//2, HEIGHT-100
    block_shape = pymunk.Poly.create_box(ground_block, (200, 20))
    space.add(ground_block, block_shape)

# ========== Основной цикл ==========
def main():
    global selected_object, font, mono_font, big_font, lang_data, current_lang
    current_lang = select_language()
    lang_data = LANGUAGES[current_lang]
    
    # Загружаем шрифты
    try:
        font = pygame.font.SysFont(lang_data['font'], 24)
        big_font = pygame.font.SysFont(lang_data['font'], 36)
        mono_font = pygame.font.SysFont("Courier New", 20)
    except:
        font = pygame.font.Font(None, 24)
        big_font = pygame.font.Font(None, 36)
        mono_font = pygame.font.Font(None, 20)
    
    # Устанавливаем окно обратно
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Физическая симуляция: автомобиль, жидкости, взрывы")
    
    add_boundaries()

    # Меню (кнопки)
    menu_width = 200
    menu_x = WIDTH - menu_width - 20
    button_y = 80
    buttons = [
        Button(menu_x, button_y, menu_width, 40, lang_data['car'], create_car_at_mouse),
        Button(menu_x, button_y+50, menu_width, 40, lang_data['engine_tank'], create_engine_at_mouse),
        Button(menu_x, button_y+100, menu_width, 40, lang_data['fuel_tank'], create_fuel_tank_at_mouse),
        Button(menu_x, button_y+150, menu_width, 40, lang_data['soft_body'], create_soft_body_at_mouse),
        Button(menu_x, button_y+200, menu_width, 40, lang_data['water'], create_water_at_mouse),
        Button(menu_x, button_y+250, menu_width, 40, lang_data['fuel'], create_fuel_at_mouse),
        Button(menu_x, button_y+300, menu_width, 40, lang_data['explosive'], create_explosive_at_mouse),
        Button(menu_x, button_y+350, menu_width, 40, lang_data['clear'], clear_all),
    ]

    running = True
    while running:
        dt = 1/60.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    create_tsunami(WIDTH//2, 100)
                elif event.key == pygame.K_h:
                    hurricane_force()
                elif event.key == pygame.K_c:
                    create_car_at_mouse()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selected_object = select_object_at(event.pos)
            for btn in buttons:
                btn.handle_event(event)

        # Обновление частиц
        for p in liquid_particles[:]:
            if not p.update(dt):
                continue

        check_ignitions(dt)

        space.step(dt)
        for car in cars:
            car.update(dt)

        # Отрисовка
        screen.fill(BACKGROUND)

        # Статические объекты (границы, земля)
        for shape in space.static_body.shapes:
            if isinstance(shape, pymunk.Segment):
                pygame.draw.line(screen, BLACK, (int(shape.a.x), int(shape.a.y)), (int(shape.b.x), int(shape.b.y)), 2)
            elif isinstance(shape, pymunk.Poly):
                points = shape.get_vertices()
                pts = [(int(p.x), int(p.y)) for p in points]
                pygame.draw.polygon(screen, BROWN, pts)

        # Мягкие тела
        for soft in soft_bodies:
            soft.draw()

        # Автомобили
        for car in cars:
            car.draw()

        # Отдельные двигатели и баки
        for eng in engines:
            eng.draw()
        for tank in fuel_tanks:
            tank.draw()

        # Частицы жидкости
        for p in liquid_particles:
            p.draw()

        # Меню
        pygame.draw.rect(screen, (200,200,200,180), (menu_x-5, 20, menu_width+10, 450))
        for btn in buttons:
            btn.draw(screen)

        # Подсказки
        info_text = font.render(lang_data['info'], True, WHITE)
        screen.blit(info_text, (10, 10))

        # Дашборд
        draw_dashboard(selected_object)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()