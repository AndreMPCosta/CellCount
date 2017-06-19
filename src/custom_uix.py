from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.lang import Builder
from kivy.properties import StringProperty, BoundedNumericProperty, NumericProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from random import randint
from copy import deepcopy

from kivymd.list import OneLineListItem
from kivymd.menu import MDDropdownMenu
from kivymd.dialog import MDDialog
import kivymd.material_resources as m_res
from kivymd.button import BaseFlatButton, BasePressedButton, BaseButton
from kivymd.ripplebehavior import RectangularRippleBehavior
from kivymd.navigationdrawer import MDNavigationDrawer
from kivymd.selectioncontrols import MDCheckbox

from license import license

Builder.load_string('''
#:import MDLabel kivymd.label.MDLabel
    
<BaseCustomRectangularButton>:
    canvas:
        Clear
        Color:
            rgba: self._current_button_color
        Rectangle:
            size: self.size
            pos: self.pos
    content: content
    height: dp(36)
    width: content.texture_size[0] + dp(32)
    padding: (dp(8), 0)
    theme_text_color: 'Primary'
    MDLabel:
        id: content
        text: root._capitalized_text
        font_style: 'Button'
        size_hint_x: 1
        text_size: (None, root.height)
        font_size: sp(12) if root.grid == 'small' else sp(9)
        height: self.texture_size[1]
        theme_text_color: root.theme_text_color
        text_color: root.text_color
        disabled: root.disabled
        valign: 'middle'
        halign: 'center'
        opposite_colors: root.opposite_colors
            
    Badge:
        canvas:
            Color: 
                rgba: root.theme_cls.accent_color if root._is_empty == False else [1, 1, 1, 0]
            Triangle:
                group: 't'
                points: (root.pos[0] + root.width - root.width/root.badge_divider, root.pos[1] + root.height, root.pos[0] + root.width, root.pos[1] + root.height, root.pos[0] + root.width, root.pos[1] + root.height - root.height/root.badge_divider)
        id: _badge_triangle
        FloatLayout:
            MDLabel:
                id: label_badge
                markup: True
                pos_hint: {'x': 0.925, 'y': 0.4}
                #x: root.right - (_badge_triangle.canvas.get_group('t')[0].points[2] - _badge_triangle.canvas.get_group('t')[0].points[1])         
                #y: root.top - root.height/2 - self.texture_size[1]/2
                text: '[b]' + root.badge_text + '[/b]'
                color: [1, 1, 1, 1]
                font_size: sp(12) if root.grid == 'small' else sp(10)
                opposite_colors: root.opposite_colors         
                                   
<MDAccordionSubItemN>:
    theme_text_color: 'Custom'
''')

class NavDrawer(MDNavigationDrawer):
    pass

class DotsMenu(MDDropdownMenu):
    items = ListProperty()
    def __init__(self, root, **kwargs):
        super(DotsMenu, self).__init__(**kwargs)
        self.items = [
            {'viewclass': 'MDFlatButton',
             'text': 'Licenses',
             'on_release': lambda: self.menu_license.custom_open(self)},
            {'viewclass': 'MDFlatButton',
             'text': 'Clear session'},
            {'viewclass': 'MDFlatButton',
             'text': 'Settings',
             'on_release': lambda: self.change_screen('settings')}
        ]
        self.hor_growth = 'left'
        self.ver_growth = 'down'
        self.width_mult = 3
        self.menu_license = ShowLicense()
        self.root = root
        self.control_size = (self.root.width - dp(3), self.root.top - dp(3))
        self.root.bind(width=self.adapt_control_width)
        self.root.bind(height=self.adapt_control_height)
        self.bind(items=self.ids['md_menu'].refresh_from_data)


    def adapt_control_width(self, x, y):
        self.control_size = (self.root.width - dp(3), self.control_size[1])
        self.ids['md_menu'].right = self.control_size[0]

    def adapt_control_height(self, x, y):
        self.control_size = (self.control_size[0], self.root.top - dp(3))
        self.ids['md_menu'].top = self.control_size[1]

    # Over-ride Open Behaviour
    def open(self, *largs):
        Window.add_widget(self)
        Clock.schedule_once(lambda x: self.display_menu(largs[0]), -1)

    def display_menu(self, caller):
        # We need to pick a starting point, see how big we need to be,
        # and where to grow to.

        # ---ESTABLISH INITIAL TARGET SIZE ESTIMATE---
        target_width = self.width_mult * m_res.STANDARD_INCREMENT
        # If we're wider than the Window...
        if target_width > Window.width:
            # ...reduce our multiplier to max allowed.
            target_width = int(
                Window.width / m_res.STANDARD_INCREMENT) * m_res.STANDARD_INCREMENT

        target_height = sum([dp(48) for i in self.items])
        # If we're over max_height...
        if self.max_height > 0 and target_height > self.max_height:
            target_height = self.max_height

        # ---ESTABLISH VERTICAL GROWTH DIRECTION---
        if self.ver_growth is not None:
            ver_growth = self.ver_growth
        else:
            # If there's enough space below us:
            if target_height <= self.control_size[1] - self.border_margin:
                ver_growth = 'down'
            # if there's enough space above us:
            elif target_height < Window.height - self.control_size[1] - self.border_margin:
                ver_growth = 'up'
            # otherwise, let's pick the one with more space and adjust ourselves
            else:
                # if there's more space below us:
                if self.control_size[1] >= Window.height - self.control_size[1]:
                    ver_growth = 'down'
                    target_height = self.control_size[1] - self.border_margin
                # if there's more space above us:
                else:
                    ver_growth = 'up'
                    target_height = Window.height - self.control_size[1] - self.border_margin

        if self.hor_growth is not None:
            hor_growth = self.hor_growth
        else:
            # If there's enough space to the right:
            if target_width <= Window.width - self.control_size[0] - self.border_margin:
                hor_growth = 'right'
            # if there's enough space to the left:
            elif target_width < self.control_size[0] - self.border_margin:
                hor_growth = 'left'
            # otherwise, let's pick the one with more space and adjust ourselves
            else:
                # if there's more space to the right:
                if Window.width - self.control_size[0] >= self.control_size[0]:
                    hor_growth = 'right'
                    target_width = Window.width - self.control_size[0] - self.border_margin
                # if there's more space to the left:
                else:
                    hor_growth = 'left'
                    target_width = self.control_size[0] - self.border_margin

        if ver_growth == 'down':
            tar_y = self.control_size[1] - target_height
        else:  # should always be 'up'
            tar_y = self.control_size[1]

        if hor_growth == 'right':
            tar_x = self.control_size[0]
        else:  # should always be 'left'
            tar_x = self.control_size[0] - target_width
        anim = Animation(x=tar_x, y=tar_y,
                         width=target_width, height=target_height,
                         duration=.3, transition='out_quint')
        menu = self.ids['md_menu']
        menu.pos = self.control_size
        anim.start(menu)

    def finalize_dismiss(self, anim, menu):
        self.dismiss()
        self.disabled = False
        menu.opacity = 1

    def custom_dismiss(self):
        self.disabled = True
        menu = self.ids['md_menu']
        anim = Animation(opacity=0,
                         duration=.5, transition='out_quint')
        anim.start(menu)
        anim.bind(on_complete=self.finalize_dismiss)

    def change_screen(self, screen):
        self.dismiss()
        setattr(App.get_running_app().root.ids.scr_mngr, 'current', screen)


class ShowLicense(MDDialog):
    link_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(ShowLicense, self).__init__(**kwargs)
        self.title = "License Information"
        self.link_label.text = license
        # self.content.bind(size=self.link_label.setter('text_size'))

    def custom_open(self, menu):
        menu.dismiss()
        self.open()


class BaseCustomRectangularButton(RectangularRippleBehavior, BaseButton):
    '''
    Abstract base class for all rectangular buttons, bringing in the
    appropriate on-touch behavior. Also maintains the correct minimum width
    as stated in guidelines.
    '''
    width = BoundedNumericProperty(dp(88), min=dp(88), max=None,
                                   errorhandler=lambda x: dp(88))
    text = StringProperty('')
    _capitalized_text = StringProperty('')

    def on_text(self, instance, value):
        self._capitalized_text = value.upper()


class MDColorFlatButton(BaseCustomRectangularButton, BaseFlatButton, BasePressedButton):
    counter = NumericProperty(0)
    badge_divider = NumericProperty(3)
    badge_text = StringProperty('')
    _is_empty = BooleanProperty(True)
    grid = StringProperty('small')
    def __init__(self, **kwargs):
        super(MDColorFlatButton, self).__init__(**kwargs)
        self.md_bg_color = (0., 0., 0., 0.)
        # self.bind(pos=self.set_drag_rectangle, size=self.set_drag_rectangle, on_touch_move=self.bring_to_front)
        # self.drag_timeout = 10000000
        # self.drag_distance = 0

    def bring_to_front(self, instance, value):
        print 'bringing to front'
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(self)

    def set_drag_rectangle(self, instance, value):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def set_bg_color(self, color):
        self.md_bg_color = color

    def set_is_empty(self, boolean):
        if boolean:
            self._is_empty = True
        else:
            self._is_empty = False


    def increment_counter(self):
        self.counter += 1
        if self.counter > 9:
            if self.ids.label_badge.pos_hint['x'] != 0.9:
                self.ids.label_badge.pos_hint = {'x':0.9, 'y': 0.4}
        self.badge_text = str(self.counter) # "%02d" % self.counter

class ColorManager(object):
    def __init__(self, color_array, **kwargs):
        super(ColorManager, self).__init__(**kwargs)
        self.saved_colors = deepcopy(color_array)
        self.colors = deepcopy(color_array)
        self.size = len(self.colors)

    def update_size(self):
        self.size = len(self.colors)
        if self.size == 0:
            self.reset()

    def pop(self):
        temp_pop = self.colors.pop(randint(0, len(self.colors) - 1))
        self.update_size()
        return temp_pop

    def reset(self):
        self.colors = deepcopy(self.saved_colors)

class Badge(BoxLayout):
    pass

class MDResetCheckbox(MDCheckbox):
    pass_text = StringProperty()
    def __init__(self, **kwargs):
        super(MDResetCheckbox, self).__init__(**kwargs)

    def set_active_false(self, instance, value):
        self.active = False
        #print instance, value

class MDAccordionSubItemN(OneLineListItem):
    parent_item = ObjectProperty()
    def __init__(self, **kwargs):
        super(MDAccordionSubItemN, self).__init__(**kwargs)
        if self.parent is not None:
            self.text_color = self.parent_item.parent.specific_text_color
