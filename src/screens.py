from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivymd.tabs import MDTab

from config import group_cells

class Workspace(Screen):
    def __init__(self, **kwargs):
        super(Workspace, self).__init__(**kwargs)
        pass

class Theming(Screen):
    def __init__(self, **kwargs):
        super(Theming, self).__init__(**kwargs)
        pass

class Pickspace(Screen):
    tab_panel = ObjectProperty()
    def __init__(self, **kwargs):
        super(Pickspace, self).__init__(**kwargs)
        for group in group_cells:
            tab = MDTab(name=group.lower(), text=group, id=group.lower())
            #TODO create items in tab
            #tab.add_widget()
            self.tab_panel.add_widget(tab)
        self.tab_panel.bind(width=self.print_width)

    def print_width(self,x,y):
        #print x,y
        #print self.tab_panel.width
        #print self.ids['tab_panel'].ids
        print [type(widget) for widget in self.walk()]
        print dir(self.ids['tab_panel'])


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        screens = {'theming': Theming(),
                   'pickspace': Pickspace()}
        #self.transition = FallOutTransition()
        self.add_widget(Workspace())
        for screen in screens.values():
            print screen
            self.add_widget(screen)
        # print Window
        # if platform == 'android':
        #     import android
        #     android.map_key(android.KEYCODE_BACK, 1001)
        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        print key
        if key in [27, 1001, 1073742094, 4]: #1073742094:
            # print (type(self.current_screen))
            # if self.has_screen('SingleNews') :
            #     if self.current_screen == self.get_screen('SingleNews'):
            #         self.current = 'News'
            # else:
            #     if self.current_screen == self.get_screen('News'):
            #         App.get_running_app().stop()
            return True

    def change_screen(self, screen_name):
        self.current = screen_name