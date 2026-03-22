# 🏒 Аэрохоккей для Android

Быстрая игра аэрохоккей для Android устройств.

## 🚀 Быстрый старт

### Для компьютера (тестирование):
```bash
python start.py          # tkinter версия
python android_hockey.py # Kivy версия (если установлен)
```

### Для Android (APK):
```bash
python install_kivy.py   # Установка Kivy
python build_android.py  # Сборка APK
```

## 📱 Создание APK для Android

### Шаг 1: Установка Kivy
```bash
python install_kivy.py
```

### Шаг 2: Сборка APK
```bash
python build_android.py
```

Готовый APK появится в папке `bin/`

## 🎮 Управление

- **На компьютере:** Перетаскивайте ракетку мышью
- **На Android:** Перетаскивайте ракетку пальцем
- Забивайте в красные ворота
- Первый до 7 голов побеждает

## ⚡ Особенности

- Быстрая физика движения
- Активный ИИ соперник  
- Энергичные отскоки
- Кнопки управления игрой
- Оптимизация для сенсорных экранов

## 📁 Файлы

- `android_hockey.py` - Версия для Android (Kivy)
- `fast_hockey.py` - Версия для компьютера (tkinter)
- `start.py` - Быстрый запуск компьютерной версии
- `install_kivy.py` - Установка Kivy
- `build_android.py` - Сборка APK
- `buildozer.spec` - Настройки Android сборки

## 🔧 Требования для APK

- Python 3.8+
- Kivy 2.0+
- Buildozer
- Java JDK
- Android SDK (автоматически загружается)

## 📱 Установка APK

1. Скопируйте APK на Android устройство
2. Включите "Установка из неизвестных источников"
3. Откройте APK файл для установки

Удачи в игре! 🏒