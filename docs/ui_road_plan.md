# Car Racing – UI & Road Module Plan

## 1. Мета

Реалізувати модулі:
- Road (малювання дороги та анімація розмітки)
- UI (HUD, Menu, Pause, Game Over, Flash effect)

Ці модулі відповідають лише за відображення (rendering) і не містять логіки руху авто чи обробки колізій.

---

## 2. Game State 

UI та Road працюють на основі стану гри:

GameState:
- MENU
- PLAYING
- PAUSED
- GAME_OVER

Логіка оновлення світу виконується тільки у стані PLAYING.
UI та Road рендеряться залежно від state.

---

## 3. Road Module

### Відповідальність:
- Малювання фону (трава)
- Малювання дороги (асфальт)
- Малювання меж дороги
- Малювання смуг
- Анімація руху пунктирної розмітки (scroll)

### Інтерфейс:
- Road.update(dt, speed)
- Road.draw(surface)

### Параметри:
- screen_w
- screen_h
- lane_count
- dash_len
- dash_gap
- scroll_multiplier

---

## 4. UI Module

### Відповідальність:
- Відображення HUD (score, speed, level)
- Головне меню
- Екран паузи
- Екран завершення гри
- Flash-ефект при зіткненні

### Інтерфейс:
- UI.handle_event(event, game)
- UI.update(dt, game)
- UI.draw(surface, game)

### Дані, які UI читає з game:
- game.state
- game.score
- game.speed
- game.level (optional)
- game.collision_flash (optional)

---

## 5. Управління клавішами

MENU:
- Enter → START
- Esc → QUIT

PLAYING:
- P → PAUSE
- Esc → MENU

PAUSED:
- P → CONTINUE
- Esc → MENU

GAME_OVER:
- R → RESTART
- Esc → MENU

---

## 6. Flash Effect

При зіткненні:
- UI встановлює flash_alpha = 200–255
- На кожному кадрі alpha зменшується
- Поверх екрану малюється напівпрозорий білий overlay
