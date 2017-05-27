from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.app import App

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        # self.transition = SlideTransition()
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