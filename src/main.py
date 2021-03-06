from kivy.app import App
from screens import CellCountRoot

from kivymd.theming import ThemeManager
from config import main_colors, languages

try:
    import cPickle as pickle
except:
    import pickle

#Window.size = (1080/3, 1920/3)

class CellCount(App):
    def __init__(self, **kwargs):
        super(CellCount, self).__init__(**kwargs)
        # self.root = CellCountRoot()
    theme_cls = ThemeManager()
    title = "CellCount"
    theme_cls.primary_palette = main_colors['primary']
    theme_cls.accent_palette = main_colors['accent']
    language = 'en'
    items = languages[language]['items']
    group_cells = languages[language]['group_cells']


    # def build(self):
    #     return self.root


    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def on_stop(self):
        pass


    # def build(self):
    #     with open('cell_count.kv'.decode('utf8')) as f:
    #         Builder.load_string(f.read())



if __name__ == '__main__':
    app = CellCount()
    app.run()