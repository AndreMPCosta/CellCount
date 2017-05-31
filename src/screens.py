from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock, mainthread

from kivymd.navigationdrawer import NavigationLayout
from kivymd.snackbar import Snackbar
from custom_uix import DotsMenu

class Workspace(Screen):
    def __init__(self, **kwargs):
        super(Workspace, self).__init__(**kwargs)
        pass
        # for group in group_cells:
        #     first_level = MDAccordionItem(title=group, icon='checkbox-blank-circle', id=group[0].lower() + group[1:])
        #     self.accordion.add_widget(first_level)
        #     for item in items[group]:
        #         if type(item) == dict:
        #             print item.keys()[0]
        #             first_level.add_widget(MDAccordionSubItem(text=item.keys()[0]))
        #         print type(item)

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
    def __init__(self, **kwargs):
        super(CurrentSession, self).__init__(**kwargs)

    @mainthread
    def on_enter(self, *args):
        if not self.parent.has_screen('workspace'):
            self.parent.add_widget(self.parent.saved_screens['workspace']())


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
        # print Window
        # if platform == 'android':
        #     import android
        #     android.map_key(android.KEYCODE_BACK, 1001)
        Window.bind(on_keyboard=self.android_back_click)
        # print self.screens

    @staticmethod
    def android_back_click(window, key, *largs):
        print key
        if key in [27, 1001, 1073742094, 4]:  # 1073742094:
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
        self.snack = Snackbar(text="Added to current session", duration=2)

    def populate_current_session(self, _widget, app):
        #print _widget.ids
        self.snack.show()
        for cells in app.items[_widget.main][_widget.index][_widget.name]:
            #print cells
            if _widget.ids[cells].active:
                print 'Adding ' + cells + ' to current session'
        # print [x for x in _widget.ids['pick_layout'].walk()]
