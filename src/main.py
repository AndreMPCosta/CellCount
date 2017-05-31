from kivy.app import App
from kivy.core.window import Window
from screens import CellCountRoot

from kivymd.theming import ThemeManager
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationLayout

from config import main_colors, languages

Window.size = (1080/3, 1920/3)

class CellCount(App):
    theme_cls = ThemeManager()
    title = "CellCount"
    theme_cls.primary_palette = main_colors['primary']
    theme_cls.accent_palette = main_colors['accent']
    language = 'en'
    items = languages[language]['items']
    group_cells = languages[language]['group_cells']

    # def build(self):
    #     #self.root = CellCountRoot()
    #     # Builder.load_file('cell_count.kv')
    # #     return CellCountRoot()

class NavDrawer(MDNavigationDrawer):
    pass


if __name__ == '__main__':
    app = CellCount()
    app.run()