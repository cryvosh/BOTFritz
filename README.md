Fritz is an experimental Python-based bot designed to eventually rival the existing bots within Counter-Strike: Global Offensive.

At present, he has some primitive vision/aiming/movement capabilities and can automatically buy weapons at the start of a round.

Improved logic, pathfinding, and object detection are in the works.

**Controls:** Hold ENTER/RETURN to enable Fritz. Press DELETE to close Fritz.

**Note:** m_rawinput must be disabled so Fritz can aim. Playing in fullscreen-windowed mode is also recommended.

**Requirements:** Currently requires python 3, win32api, tensorflow, opencv, pyautogui, mss, numpy, and pytesseract, which further requires the installation of [tesseract 3.05](https://github.com/UB-Mannheim/tesseract/wiki).

Fritz is ultimately intended for offline use, so be sure to add -insecure and +sv_lan 1 to the CS:GO launch options before testing Fritz to avoid any complications.