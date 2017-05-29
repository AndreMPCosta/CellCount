from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.clock import Clock, mainthread

from kivymd.button import MDRaisedButton
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, IRightBody
from kivymd.selectioncontrols import MDCheckbox

from functools import partial

from config import group_cells


class CellLine(ILeftBody, MDCheckbox):
    pass

class Workspace(Screen):
    def __init__(self, **kwargs):
        super(Workspace, self).__init__(**kwargs)
        pass

class Theming(Screen):
    def __init__(self, **kwargs):
        super(Theming, self).__init__(**kwargs)
        pass

class Pickspace(Screen):
    pick_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super(Pickspace, self).__init__(**kwargs)
        for group in group_cells:
            boxlayout = BoxLayout(size_hint_y=None, height= dp(120), id=group.lower(), orientation='vertical')
            self.pick_layout.add_widget(boxlayout)
            button = MDRaisedButton(id=group.lower(), text=group, pos_hint = {'center_x': 0.5},
                                    on_release=self.test)
            boxlayout.add_widget(button)

    def test(self, x):
        print x.center_x
        self.parent.change_screen(x.id)
        # print x.parent
        # x.center_x = x.parent.center_x
        # print button.center_x


class Erythroid(Screen):
    #teste = ObjectProperty()
    def __init__(self, **kwargs):
        super(Erythroid, self).__init__(**kwargs)
        #self.teste.bind(active=self.j)
    def j(self, widget, state):
        print widget, state
        print 'click'


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.saved_screens = {'theming': Theming, 'pickspace': Pickspace,
                              'erythroid': Erythroid}
        #self.transition = FallOutTransition()
        self.add_widget(Workspace())
        self.add_widget(Theming())
        # print Window
        # if platform == 'android':
        #     import android
        #     android.map_key(android.KEYCODE_BACK, 1001)
        Window.bind(on_keyboard=self.android_back_click)
        #print self.screens

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
        if self.has_screen(screen_name) == False:
            #print self.saved_screens[screen_name]
            self.add_widget(self.saved_screens[screen_name]())
        self.current = screen_name