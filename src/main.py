from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
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


# class CellCountRoot(NavigationLayout):
#     dots_menu = ObjectProperty()
#
#     def __init__(self, **kwargs):
#         super(CellCountRoot, self).__init__(**kwargs)
#         Clock.schedule_once(self.my_init)
#
#     def my_init(self, dt):
#         print self.ids['scr_mngr'].get_screen('current_session').ids['toolbar']
#
#         #print self.ids['toolbar']
#         #self.ids['toolbar'].right_action_items = [['more-vert', lambda x: self.dots_menu.open(self.ids.right_actions)]]


if __name__ == '__main__':
    app = CellCount()
    app.run()