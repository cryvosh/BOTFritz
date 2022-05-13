Fritz is an experimental Python-based bot designed to eventually rival the existing bots within Counter-Strike: Global Offensive.

At present, he has some basic aiming/hearing/movement capabilities and can automatically buy weapons at the start of a round, shoot at the enemy team, roam around in deathmatch, and look towards gunfire using sound.

Improved logic, pathfinding, audio analysis, and object detection are in the works.

**Controls:**
- Press 'HOME' to pause/unpause Fritz.
- Press 'END' to close Fritz.

**Required CS:GO Commands:**
- cl_showpos 1
- safezonex 0.85
- safezoney 0.85
- hud_scaling 0.85
- cl_hud_background_alpha 1
- mat_setvideomode 1152 864 1

**Dependencies:**
- Python 3.9.7
- pip install pywin32
- pip install tensorflow
- pip install opencv-python
- pip install mss
- pip install Pillow
- pip install pytesseract + https://github.com/UB-Mannheim/tesseract/wiki
- pip install tesseract-ocr
- pip install tesseract
- PyAudio, which can be installed using the included .whl file or from the [repo](https://github.com/intxcc/pyaudio_portaudio).

**Notes:**
- Fritz automatically pauses if the game loses focus, press HOME to unpause.
- You can configure your CS:GO sensitivity and m_yaw on lines 9 and 10 of logic.py.
- Roaming/sound seeking movement and defuse/deathmatch logic is set on line 28 of main.py.
- Fritz hears better with HRTF disabled.
- The current detection model was trained for de_dust2. A significantly improved detection model is in the works.

Fritz is ultimately intended for offline use, so be sure to **add -insecure and +sv_lan 1 to the CS:GO launch options** before testing Fritz to avoid any complications.
