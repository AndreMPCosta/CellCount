from kivy.core.window import Window
from kivy.animation import Animation
from kivy.gesture import Gesture, GestureDatabase
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock, mainthread
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, DictProperty, BooleanProperty
from kivy.utils import platform

from kivymd.label import MDLabel
from kivymd.navigationdrawer import NavigationLayout
from kivymd.textfields import MDTextField

from custom_uix import DotsMenu, MDColorFlatButton, ColorManager, MDResetCheckbox

from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem
from config import animation_type
from config import md_colors, number_of_cols, group_cells, items
from my_gestures import left_to_right

if platform == 'android' or platform == 'ios':
    from plyer import vibrator

dev = 0

def vibrate(seconds):
    vibrator.vibrate(seconds)

class Workspace(Screen):
    def __init__(self, **kwargs):
        super(Workspace, self).__init__(**kwargs)
        self.secondary_screen_manager = SecondScreenManagement()
        Clock.schedule_once(self.my_init)

    def my_init(self, dt):
        main_container = BoxLayout()
        accordion = MDAccordion(id='accordion', orientation='vertical', size_hint_x= None,
        width='185dp')
        for group in self._app.group_cells:
            accordion_item = MDAccordionItem(title=group, icon='checkbox-blank-circle')
            accordion.add_widget(accordion_item)
            for c in self._app.items[group]:
                if type(c) == dict:
                    print c.keys()[0]
                    accordion_sub_item =  MDAccordionSubItem(text=c.keys()[0], parent_item=accordion_item,
                                                             on_release=self.change_screen)
                else:
                    accordion_sub_item = MDAccordionSubItem(text=c, parent_item=accordion_item,
                                                            on_release=self.change_screen)
                accordion_item.add_widget(accordion_sub_item)
        main_container.add_widget(accordion)
        main_container.add_widget(self.secondary_screen_manager)
        self.add_widget(main_container)

    def change_screen(self, value):
        self.secondary_screen_manager.current = value.text

class Theming(Screen):
    def __init__(self, **kwargs):
        super(Theming, self).__init__(**kwargs)
        pass


class CellCountRoot(NavigationLayout):
    toolbar = ObjectProperty()
    def __init__(self, **kwargs):
        super(CellCountRoot, self).__init__(**kwargs)
        Clock.schedule_once(self.my_init)

    def my_init(self, dt):
        #self.toolbar.dots_menu = DotsMenu(self)
        self.ids['toolbar'].dots_menu = DotsMenu(self)


class CurrentSession(Screen):
    _app = ObjectProperty()
    working_layout = ObjectProperty()
    buttons = DictProperty()
    grid = StringProperty('small')
    n_of_cols = NumericProperty(number_of_cols)
    color_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super(CurrentSession, self).__init__(**kwargs)
        #self.snack = Snackbar(text="Current session updated", duration=2)
        self.ssm = None
        self.buttons = {}
        self.available_grid_sizes = ['small', 'large']
        self.bind(grid=self.refresh_menu_text, buttons=self.refresh_screen)
        self.working_layout.bind(minimum_height=self.working_layout.setter('height'))
        self.menu_items = [{'viewclass': 'MDFlatButton',
                          'text': 'Show %s grid' % self.grid,
                          'on_release': lambda: self.change_grid_size()}
                           ]
        self.color_manager = ColorManager(md_colors)
        self.clear_anim = Animation(x=self.width,
                                    duration=.5, transition=animation_type)
        self.bind(width=self.update_anim, size=self.adjust_height)
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(left_to_right)
        Clock.schedule_once(self.my_init)

    def my_init(self, dt):
        self.manager = self.parent
        self.root = self.parent.parent.parent.parent
        self.working_layout.parent.bind(minimum_height=self.working_layout.parent.setter('height'))
        self.init_button = self.ids.add_cells

    def animate_action_button(self, instance):
        # print instance.content
        # anim = Animation(size=(0,0), center_x=instance.center_x, duration=1, transition='in_out_quad')
        # anim2 = Animation(opacity=0, center_x=instance.center_x, duration=1, transition='in_out_quad')
        # print instance.center_x, instance.center_y
        # anim.bind(on_complete= self.teste)
        # anim.start(instance)
        # anim2.start(instance.content)
        self.parent.current = 'workspace'

    def teste(self, x, y):
        print x, y

    def update_anim(self, instance, value):
        self.clear_anim._animated_properties['x'] = self.width

    def refresh_screen(self, instance, value):
        if bool(self.buttons):
            if self.ids.plus_layout.children:
                self.ids.plus_layout.remove_widget(self.ids.add_cells)
        else:
            self.ids.plus_layout.add_widget(self.init_button)


    def on_touch_down(self, touch):
        # create an user defined variable and add the touch coordinates
        touch.ud['gesture_path'] = [(touch.x, touch.y)]
        super(CurrentSession, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if 'gesture_path' in touch.ud:
            touch.ud['gesture_path'].append((touch.x, touch.y))
        super(CurrentSession, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if 'gesture_path' in touch.ud:
            # create a gesture object
            gesture = Gesture()
            # add the movement coordinates
            gesture.add_stroke(touch.ud['gesture_path'])
            # normalize so thwu willtolerate size variations
            gesture.normalize()
            # minscore to be attained for a match to be true, default 0.3
            g2 = self.gdb.find(gesture, minscore=0.70)
            if g2:
                print 'swipe left'


        #print("gesture representation:", self.gdb.gesture_to_str(gesture))

    def finish(self):
        print 'finishing'
        self.clear()


    def adjust_height(self, instance, value):
        # TODO Analysis
        pass
        # print self.width, self.height
        # print self.ids.add_cells.pos
        #print self.height
        #self.ids.plus_layout.height = self.height - self.ids.add_cells.height - self.root.ids.toolbar.height
        #print self.ids.plus_layout.height
        # print [x for x in instance.walk()]
        # print self.buttons
        #print type(instance) == GridLayout
        # if type(instance) == GridLayout:
        #     self.ids.plus_layout.height = self.working_layout.row_default_height
        #     self.ids.add_cells.y = self.buttons[sorted(self.buttons.keys())[-1]].y

    # def on_touch_down(self, touch):
    #     print touch

    @mainthread
    def on_enter(self, *args):
        if not self.parent.has_screen('workspace'):
            self.parent.add_widget(self.parent.saved_screens['workspace']())
            self.ssm = self.parent.get_screen('workspace').secondary_screen_manager
        self.update_dots_menu()

    @mainthread
    def on_leave(self, *args):
        if len(self.root.ids['toolbar'].dots_menu.items) > 3:
            del self.root.ids['toolbar'].dots_menu.items[1]

    def update_dots_menu(self):
        self.root.ids['toolbar'].dots_menu.items.insert(1, self.menu_items[0])

    def refresh_menu_text(self, widget, value):
        self.menu_items[0]['text'] = 'Show %s grid' % value

    def change_grid_size(self):
        if self.grid != self.available_grid_sizes[0]:
            self.grid = self.available_grid_sizes[0]
            self.n_of_cols = number_of_cols
        else:
            self.grid = self.available_grid_sizes[1]
            self.n_of_cols = number_of_cols + 1
        self.root.ids['toolbar'].dots_menu.items[1]=self.menu_items[0]
        self.root.ids['toolbar'].dots_menu.custom_dismiss()


    def populate_current_session(self, _widget):
        if _widget.active:
            if not self.buttons.has_key(_widget.pass_text) or dev:
                print 'Adding ' + _widget.pass_text + ' to current session'
                new_text = _widget.pass_text.replace(' ', '\n')
                button = MDColorFlatButton(text=new_text, id=_widget.pass_text,
                                           size_hint=(1,1), on_release=self.add)
                self.bind(grid=button.setter('grid'))
                self.buttons[_widget.pass_text] = button
                button.set_bg_color(get_color_from_hex(self.color_manager.pop()))
                self.working_layout.add_widget(button)
        else:
            if self.buttons.has_key(_widget.pass_text):
                self.working_layout.remove_widget(self.buttons[_widget.pass_text])
                del self.buttons[_widget.pass_text]

    def add(self, button):
        button.set_is_empty(False)
        button.increment_counter()
        if self.parent.get_screen('settings').ids.vibration.active:
            print "I'm vibratin'!"
        if (platform == 'android' or platform == 'ios') and self.parent.get_screen('settings').ids.vibration.active:
            #print platform
            # try:
            vibrate(0.1)
            # except NotImplementedError:
            #     print "Can't access the vibrate function"

    def clear(self):
        if self.manager.current_screen.name == self.name:
            for i, button in enumerate(self.buttons.values()):
                self.clear_anim.start(button)
                if i == len(self.buttons) - 1:
                    self.clear_anim.bind(on_complete=self.clear_complete)
        else:
            self.ssm.reset = not self.ssm.reset

    def clear_complete(self, instance, value):
        # sm = self.parent.get_screen('workspace').ids.secondary_screen_manager
        # sm.reset = not sm.reset
        self.ssm.reset = not self.ssm.reset
        # print button.ids.label_badge.texture_size[0]
        # print button.ids._badge_triangle.right - (button.ids._badge_triangle.canvas.get_group('t')[0].points[2] - button.ids._badge_triangle.canvas.get_group('t')[0].points[1])
        #print button.ids._badge_triangle.top


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.saved_screens = {'theming': Theming, 'current_session': CurrentSession,
                              'workspace': Workspace, 'settings': SettingsScreen}
        # self.transition = FallOutTransition()
        self.add_widget(CurrentSession())
        self.add_widget(Theming())
        self.add_widget(SettingsScreen())
        self.bind(current_screen=self.update)
        Clock.schedule_once(self.my_init)
        # print Window
        # if platform == 'android':
        #     import android
        #     android.map_key(android.KEYCODE_BACK, 1001)
        Window.bind(on_keyboard=self.android_back_click)
        # print self.screens

    def my_init(self, dt):
        self.root = self.parent.parent.parent
        self.root.ids['toolbar'].dots_menu.items[2]['on_release'] = lambda: self.clear()

    def update(self, screen_manager, screen):
        nav_drawer = self.parent.parent.parent.ids.nav_drawer
        if screen.name != 'settings':
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

    def clear(self):
        #print self.get_screen('workspace').ids.secondary_screen_manager
        self.get_screen('current_session').clear()
        # for screen in sm:
        #     temp_widgets = [x for x in screen.walk()]
        #     for temp_widget in temp_widgets:
        #         if type(temp_widget) == MDCheckbox:
        #             temp_widget.active = False
        self.root.ids['toolbar'].dots_menu.custom_dismiss()


class SecondScreenManagement(ScreenManager):
    reset = BooleanProperty(True)
    _app = ObjectProperty()
    _app_root = ObjectProperty()

    def __init__(self, **kwargs):
        super(SecondScreenManagement, self).__init__(**kwargs)
        # self.color_manager = ColorManager(md_colors)
        Clock.schedule_once(self.my_init)

    def my_init(self, dt):
        self.generate_screens()

    def generate_screens(self):
        for group in group_cells:
            for c in items[group]:
                if type(c) == dict:
                    temp_screen = Screen(name=c.keys()[0])
                    temp_items = c[c.keys()[0]]
                else:
                    temp_screen = Screen(name=c)
                    temp_items = c
                main_container = BoxLayout(id='main_container', orientation='vertical',
                                                 padding=[dp(10), 0, 0, 0], spacing=dp(20))
                if not type(temp_items) == str:
                    for i, value in enumerate(temp_items):
                        #print value
                        temp_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
                        temp_label = MDLabel(id='label' + str(i), font_style="Caption", halign="left",
                                             text=value,
                                             theme_text_color='Secondary'
                                             if self._app.theme_cls.theme_style == 'Light' else 'Primary')
                        temp_checkbox = MDResetCheckbox(pass_text=value, size_hint=(None, None), size=(dp(48), dp(48)),
                                                        pos_hint={'center_x': 0.25, 'center_y': 0.5})
                        temp_checkbox.bind(state=self.aux_populate)
                        self.bind(reset=temp_checkbox.set_active_false)
                        temp_box.add_widget(temp_label)
                        temp_box.add_widget(temp_checkbox)
                        main_container.add_widget(temp_box)
                else:
                    temp_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
                    if temp_items == 'Create other type':
                        temp_checkbox = MDResetCheckbox(size_hint=(None, None),
                                                        size=(dp(48), dp(48)),
                                                        pos_hint={'center_x': 0.25, 'center_y': 0.5})
                        temp_text_field = MDTextField(color_mode='accent')
                        temp_text_field.bind(text=temp_checkbox.setter('pass_text'))
                        temp_box.add_widget(temp_text_field)
                    else:
                        temp_label = MDLabel(id='label1', font_style="Caption", halign="left",
                                             text=temp_items,
                                             theme_text_color=
                                             'Secondary' if self._app.theme_cls.theme_style == 'Light' else 'Primary')
                        temp_box.add_widget(temp_label)
                        temp_checkbox = MDResetCheckbox(pass_text=temp_items, size_hint=(None, None), size=(dp(48), dp(48)),
                                                        pos_hint={'center_x': 0.25, 'center_y': 0.5})
                    temp_checkbox.bind(state=self.aux_populate)
                    self.bind(reset=temp_checkbox.set_active_false)
                    temp_box.add_widget(temp_checkbox)
                    main_container.add_widget(temp_box)
                main_container.add_widget(BoxLayout())
                temp_screen.add_widget(main_container)
                self.add_widget(temp_screen)

    def aux_populate(self, instance, value):
        #print instance, value
        #self._app_root.ids.scr_mngr.get_screen('current_s')
        self._app_root.ids['scr_mngr'].get_screen('current_session').populate_current_session(instance)
        #print self.reset

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)