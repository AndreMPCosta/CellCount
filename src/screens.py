from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock, mainthread
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.metrics import sp

from kivymd.navigationdrawer import NavigationLayout
from custom_uix import DotsMenu, MDColorFlatButton, ColorManager

from config import md_colors, number_of_cols

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
        # print self.ids
        self.ids['toolbar'].dots_menu = DotsMenu(self)


class CurrentSession(Screen):
    working_layout = ObjectProperty()
    grid = StringProperty('small')
    n_of_cols = NumericProperty(number_of_cols)

    def __init__(self, **kwargs):
        super(CurrentSession, self).__init__(**kwargs)
        #self.snack = Snackbar(text="Current session updated", duration=2)
        self.working_layout.bind(minimum_height=self.working_layout.setter('height'))
        self.buttons = {}
        self.available_grid_sizes = ['small', 'large']
        self.bind(grid=self.refresh_menu_text)
        self.menu_item = {'viewclass': 'MDFlatButton',
                          'text': 'Show %s grid' % self.grid,
                          'on_release': lambda: self.change_grid_size()}
        Clock.schedule_once(self.my_init)

    def my_init(self, dt):
        self.root = self.parent.parent.parent.parent

    @mainthread
    def on_enter(self, *args):
        if not self.parent.has_screen('workspace'):
            self.parent.add_widget(self.parent.saved_screens['workspace']())
        self.update_dots_menu()

    @mainthread
    def on_leave(self, *args):
        if len(self.root.ids['toolbar'].dots_menu.items) > 2:
            del self.root.ids['toolbar'].dots_menu.items[2]

    def update_dots_menu(self):
        self.root.ids['toolbar'].dots_menu.items.append(self.menu_item)

    def refresh_menu_text(self, widget, value):
        self.menu_item['text'] = 'Show %s grid' % value

    def change_grid_size(self):
        if self.grid != self.available_grid_sizes[0]:
            self.grid = self.available_grid_sizes[0]
            self.n_of_cols = number_of_cols
        else:
            self.grid = self.available_grid_sizes[1]
            self.n_of_cols = number_of_cols + 1
        self.root.ids['toolbar'].dots_menu.items[2]=self.menu_item
        self.root.ids['toolbar'].dots_menu.custom_dismiss()


    def populate_current_session(self, _widget, app, color_manager):
        if _widget.active:
            if not self.buttons.has_key(_widget.pass_text) or dev:
                print 'Adding ' + _widget.pass_text + ' to current session'
                new_text = _widget.pass_text.replace(' ', '\n')
                button = MDColorFlatButton(text=new_text, id=_widget.pass_text,
                                           size_hint=(1,1), on_release=self.add)
                button.ids.content.font_size = sp(12)
                #print button.ids.content.font_size
                self.buttons[_widget.pass_text] = button
                button.set_bg_color(get_color_from_hex(color_manager.pop()))
                self.working_layout.add_widget(button)
        else:
            if self.buttons.has_key(_widget.pass_text):
                self.working_layout.remove_widget(self.buttons[_widget.pass_text])
                del self.buttons[_widget.pass_text]

    def add(self, button):
        button.set_is_empty(False)
        button.increment_counter()
        # print button.ids.label_badge.texture_size[0]
        # print button.ids._badge_triangle.right - (button.ids._badge_triangle.canvas.get_group('t')[0].points[2] - button.ids._badge_triangle.canvas.get_group('t')[0].points[1])
        #print button.ids._badge_triangle.top


class Erithroblast(Screen):
    def __init__(self, **kwargs):
        super(Erithroblast, self).__init__(**kwargs)

class Reticulocyte(Screen):
    def __init__(self, **kwargs):
        super(Reticulocyte, self).__init__(**kwargs)

class Myeloblast(Screen):
    def __init__(self, **kwargs):
        super(Myeloblast, self).__init__(**kwargs)

class Promyelocyte(Screen):
    def __init__(self, **kwargs):
        super(Promyelocyte, self).__init__(**kwargs)

class Myelocyte(Screen):
    def __init__(self, **kwargs):
        super(Myelocyte, self).__init__(**kwargs)

class Metamyelocyte(Screen):
    def __init__(self, **kwargs):
        super(Metamyelocyte, self).__init__(**kwargs)

class Band(Screen):
    def __init__(self, **kwargs):
        super(Band, self).__init__(**kwargs)

class Immature_forms(Screen):
    def __init__(self, **kwargs):
        super(Immature_forms, self).__init__(**kwargs)

class Mature_forms(Screen):
    def __init__(self, **kwargs):
        super(Mature_forms, self).__init__(**kwargs)

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.saved_screens = {'theming': Theming, 'current_session': CurrentSession,
                              'workspace': Workspace}
        # self.transition = FallOutTransition()
        self.add_widget(CurrentSession())
        self.add_widget(Theming())
        self.bind(current_screen=self.update)
        # print Window
        # if platform == 'android':
        #     import android
        #     android.map_key(android.KEYCODE_BACK, 1001)
        Window.bind(on_keyboard=self.android_back_click)
        # print self.screens

    def update(self, screen_manager, screen):
        nav_drawer = self.parent.parent.parent.ids.nav_drawer
        nav_drawer.ids[screen.name]._set_active(True, list=nav_drawer)

    def android_back_click(self, window, key, *largs):
        if key in [27, 1001, 1073742094, 4]:  # 1073742094:
            # print self.current_screen
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
