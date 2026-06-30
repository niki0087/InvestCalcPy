"""
InvestCalcPy - Инвестиционный калькулятор для Android
Точка входа в приложение KivyMD.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from kivy.config import Config
from kivy.logger import Logger

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Config.set('kivy', 'log_level', 'debug')
# Отключаем cutbuffer ошибки
Config.set('kivy', 'cutbuffer', 'sdl2')
Config.set('kivy', 'clipboard', 'sdl2')


def main():
    try:
        Logger.info("InvestCalcPy: Starting application...")
        from presentation.app import InvestCalcApp
        app = InvestCalcApp()
        app.run()
    except Exception as e:
        Logger.critical(f"InvestCalcPy: Application crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()