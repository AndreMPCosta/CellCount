from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock

from kivymd.menu import MDDropdownMenu
from kivymd.dialog import MDDialog
from kivymd.theming import ThemeManager
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationLayout
import kivymd.material_resources as m_res

from license import license
from screens import *

class CellCount(App):
    theme_cls = ThemeManager()
    title = "CellCount"


class NavDrawer(MDNavigationDrawer):
    pass


class CellCountRoot(NavigationLayout):
    dots_menu = ObjectProperty()

    def __init__(self, **kwargs):
        super(CellCountRoot, self).__init__(**kwargs)
        Clock.schedule_once(self.my_init)

    def my_init(self, dt):
        self.ids['toolbar'].dots_menu = DotsMenu(self)
        #print self.ids['toolbar']
        #self.ids['toolbar'].right_action_items = [['more-vert', lambda x: self.dots_menu.open(self.ids.right_actions)]]


class ShowLicense(MDDialog):
    link_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(ShowLicense, self).__init__(**kwargs)
        self.title = "License Information"
        self.link_label.text = license
        #self.content.bind(size=self.link_label.setter('text_size'))

    def custom_open(self, menu):
        menu.dismiss()
        self.open()


class DotsMenu(MDDropdownMenu):
    def __init__(self, root, **kwargs):
        super(DotsMenu, self).__init__(**kwargs)
        self.items = [
            {'viewclass': 'MDFlatButton',
             'text': 'Licenses',
             'on_release': lambda: self.menu_license.custom_open(self)},
            {'viewclass': 'MDFlatButton',
             'text': 'Settings',
             'on_release': lambda: app.open_settings()}
        ]
        self.hor_growth = 'left'
        self.ver_growth = 'down'
        self.width_mult = 3
        self.menu_license = ShowLicense()
        self.control_size = (root.width - dp(3), root.top - dp(3))
        root.bind(width=self.adapt_control_width)
        root.bind(height=self.adapt_control_height)

    def adapt_control_width(self, x, y):
        self.control_size = (app.root.width - dp(3), self.control_size[1])
        self.ids['md_menu'].right = self.control_size[0]

    def adapt_control_height(self, x, y):
        self.control_size = (self.control_size[0], app.root.top - dp(3))
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


if __name__ == '__main__':
    app = CellCount()
    app.run()