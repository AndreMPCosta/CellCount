from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock, mainthread
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty

from kivymd.navigationdrawer import NavigationLayout
from custom_uix import DotsMenu, MDColorFlatButton, ColorManager

from config import md_colors

dev = 0

class Workspace(Screen):
    def __init__(self, **kwargs):
        super(Workspace, self).__init__(**kwargs)
        pass


    @staticmethod
    def j(x):
        print x
        print 'click'


class Theming(Screen):
    def __init__(self, **kwargs):
        super(Theming, self).__init__(**kwargs)
        pass


class CellCountRoot(NavigationLayout):
    def __init__(self, **kwargs):
        super(CellCountRoot, self).__init__(**kwargs)
        Clock.schedule_once(self.my_init)

    def my_init(self, dt):
        print self.ids
        self.ids['toolbar'].dots_menu = DotsMenu(self)


class CurrentSession(Screen):
    working_layout = ObjectProperty()
    s_layout = ObjectProperty()
    def __init__(self, **kwargs):
        super(CurrentSession, self).__init__(**kwargs)
        #self.snack = Snackbar(text="Current session updated", duration=2)
        self.working_layout.bind(minimum_height=self.working_layout.setter('height'))
        self.buttons = {}

    @mainthread
    def on_enter(self, *args):
        if not self.parent.has_screen('workspace'):
            self.parent.add_widget(self.parent.saved_screens['workspace']())


    def populate_current_session(self, _widget, app, color_manager):
        if _widget.active:
            if not self.buttons.has_key(_widget.pass_text) or dev:
                print 'Adding ' + _widget.pass_text + ' to current session'
                button = MDColorFlatButton(text=_widget.pass_text, id=_widget.pass_text,
                                           size_hint=(1,1), on_release=self.test)
                #button.ids.content.font_size = 11
                #print button.ids.content.font_size
                self.buttons[_widget.pass_text] = button
                button.set_bg_color(get_color_from_hex(color_manager.pop()))
                self.working_layout.add_widget(button)
                #self.s_layout.add_widget(button)
                # r = RelativeLayout()
                # button.badge_label = MDLabel(text='50', pos=(button.pos[0] + button.width - button.width / 7,
                #                             button.height / 2 - button.height / 7))
                # r.add_widget(button.badge_label)
                # button.add_widget(r)


        else:
            if self.buttons.has_key(_widget.pass_text):
                self.working_layout.remove_widget(self.buttons[_widget.pass_text])
                del self.buttons[_widget.pass_text]

    def test(self, button):
        button.set_is_empty(False)
        button.increment_counter()



class Erithroblast(Screen):
    def __init__(self, **kwargs):
        super(Erithroblast, self).__init__(**kwargs)

    def j(self, widget, state):
        print widget, state
        print 'click'


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.saved_screens = {'theming': Theming, 'current_session': CurrentSession,
                              'workspace': Workspace}
        # self.transition = FallOutTransition()
        self.add_widget(CurrentSession())
        self.add_widget(Theming())
        self.bind(current_screen=self.update_nav_drawer)
        # print Window
        # if platform == 'android':
        #     import android
        #     android.map_key(android.KEYCODE_BACK, 1001)
        Window.bind(on_keyboard=self.android_back_click)
        # print self.screens

    def update_nav_drawer(self, screen_manager, screen):
        nav_drawer = self.parent.parent.parent.ids.nav_drawer
        nav_drawer.ids[screen.name]._set_active(True, list=nav_drawer)

    def android_back_click(self, window, key, *largs):
        if key in [27, 1001, 1073742094, 4]:  # 1073742094:
            print self.current_screen
            if self.current_screen.tree == 1:
                self.current = 'current_session'
            # print (type(self.current_screen))
            # if self.has_screen('SingleNews') :
            #     if self.current_screen == self.get_screen('SingleNews'):
            #         self.current = 'News'
            # else:
            #     if self.current_screen == self.get_screen('News'):
            #         App.get_running_app().stop()
            return True

    def change_screen(self, screen_name):
        if not self.has_screen(screen_name):
            # print self.saved_screens[screen_name]
            self.add_widget(self.saved_screens[screen_name]())
        self.current = screen_name


class SecondScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(SecondScreenManagement, self).__init__(**kwargs)
        self.color_manager = ColorManager(md_colors)

        # print [x for x in _widget.ids['pick_layout'].walk()]
