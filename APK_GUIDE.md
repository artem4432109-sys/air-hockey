# 📱 Создание APK без установки Kivy

Если Kivy не устанавливается на вашем компьютере, используйте онлайн-сервисы.

## 🌐 Способ 1: Replit (Рекомендуется)

1. Зайдите на [replit.com](https://replit.com)
2. Создайте новый Python проект
3. Загрузите файлы:
   - `simple_android.py`
   - `buildozer.spec`
4. В терминале Replit выполните:
```bash
pip install kivy buildozer
python simple_android.py  # тест
buildozer android debug   # сборка APK
```

## 🌐 Способ 2: Google Colab

1. Откройте [colab.research.google.com](https://colab.research.google.com)
2. Создайте новый блокнот
3. Выполните код:

```python
# Установка зависимостей
!pip install kivy buildozer

# Загрузка файлов игры
from google.colab import files
uploaded = files.upload()  # Загрузите simple_android.py и buildozer.spec

# Сборка APK
!buildozer android debug

# Скачивание APK
from google.colab import files
files.download('bin/airhockey-0.1-armeabi-v7a-debug.apk')
```

## 🌐 Способ 3: GitHub Actions (Автоматический)

1. Создайте репозиторий на GitHub
2. Загрузите файлы игры
3. Создайте файл `.github/workflows/build.yml`:

```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install kivy buildozer
    - name: Build APK
      run: buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: apk
        path: bin/*.apk
```

## 🔧 Способ 4: Локальная установка Kivy (альтернативы)

Если хотите попробовать еще раз на своем компьютере:

```cmd
# Через conda (если установлен)
conda install kivy

# Или через wheel файлы
pip install --only-binary=all kivy

# Или dev версия
pip install https://github.com/kivy/kivy/archive/master.zip
```

## 📱 Способ 5: Использование готового APK

Если ничего не работает, можете:
1. Попросить кого-то собрать APK
2. Использовать компьютерную версию: `python fast_hockey.py`
3. Играть в браузерную версию (если создам)

## 🎯 Рекомендация

**Самый простой способ:** Используйте Replit - там уже все настроено для Python разработки и сборки APK.

1. Зарегистрируйтесь на replit.com
2. Создайте Python проект
3. Загрузите файлы игры
4. Соберите APK в облаке

Готовый APK можно будет скачать и установить на телефон!