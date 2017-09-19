Fritz is an experimental Python-based bot designed to eventually rival the existing bots within Counter-Strike: Global Offensive.

At present, he has some basic vision/aiming/movement capabilities and can automatically buy weapons at the start of a round/shoot at the enemy team/roam around in deathmatch.

Improved logic, pathfinding, and object detection are in the works.

**Controls:** Press ENTER/RETURN to toggle Fritz. Press DELETE to close Fritz.

**Required CS:GO Commands:** cl_showpos 1, safezonex 0.85, safezoney 0.85, hud_scaling 0.85, cl_hud_background_alpha 1, mat_setvideomode 1152 864 1

**Dependencies:** Python 3, win32api, tensorflow, opencv, mss, numpy, PIL, and pytesseract, which further requires the installation of [tesseract 3.05](https://github.com/UB-Mannheim/tesseract/wiki).

**Note:** Roaming movement and 'defuse'/'deathmatch' gamemode are set on line 26 of main.py.

Fritz is ultimately intended for offline use, so be sure to **add -insecure and +sv_lan 1 to the CS:GO launch options** before testing Fritz to avoid any complications.