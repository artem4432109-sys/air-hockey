[app]

# (str) Title of your application
title = AirHockey

# (str) Package name
package.name = airhockey

# (str) Package domain (needed for android/ios packaging)
package.domain = com.airhockey

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (leave empty to not exclude anything)
source.exclude_exts = spec,md,txt,yml

# (list) List of directory to exclude (leave empty to not exclude anything)
source.exclude_dirs = .git,.vscode,__pycache__,.buildozer,bin

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse, landscape-reverse, or all
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
