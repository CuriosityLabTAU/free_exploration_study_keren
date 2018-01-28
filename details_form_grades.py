#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy_communication.logged_widgets import *
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen


class DetailsScreenGrades(Screen):

    def add_widget(self, widget, index=0):
        super(Screen, self).add_widget(widget, index)
        self.bind(on_enter=widget.on_enter)


class DetailsFormGrades(BoxLayout):
    details = {}
    the_app = None
    SAT_text = None
    bagrut_text = None

    def __init__(self, the_app):
        super(DetailsFormGrades, self).__init__()
        self.the_app = the_app

        with self.canvas.before:
            self.rect = Rectangle(source='back3.png')
            self.bind(size=self._update_rect, pos=self._update_rect)

        dict = {}
        self.answers = {}
        store = JsonStore('details.json').get('details')

        for key, value in store.items():
            if key in ['FirstName', 'LastName', 'Email', 'end_button','details_title','Age', 'SAT', 'bagrut']:
                dict[key] = value[::-1]
            if key in ['Gender']:
                dict[key] = {}
                for kqa, qa in value.items():
                    if kqa=='text':
                        dict[key][kqa] = qa[::-1]
                    elif kqa == 'default':
                        dict[key][kqa] = qa[::-1]
                    elif kqa != 'ages':
                        dict[key][kqa]=[]
                        for k,v in value[kqa].items():
                           dict[key][kqa].append(v[::-1])
                    else:
                        dict[key][kqa]=[]
                        age=10
                        while age<100:
                            dict[key][kqa].append(str(age))
                            age += 1

        # definitions of all the GUI
        y_size = 0.2

        self.SAT_text = LoggedTextInput(size_hint_x=0.5, font_size=40, input_filter='int', size_hint_y=y_size)
        self.SAT_text.bind(text=self.SAT_text.on_text_change)
        self.SAT_text.name = 'SAT'

        self.bagrut_text = LoggedTextInput(size_hint_x=2, font_size=32, input_filter='float', size_hint_y=y_size)
        self.bagrut_text.bind(text=self.bagrut_text.on_text_change)
        self.bagrut_text.name = 'email'

        end_button = Button(background_color=[0, 0.71, 1, 1],
                            background_normal="",
                            text=dict['end_button'], font_size=30,
                            font_name="fonts/the_font.ttf",
                            halign='right', on_press=self.next)

        end_button.bind(on_press=self.save)  # layout of the GUI

        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(BoxLayout(size_hint_y=y_size))
        layoutup.add_widget(
             Label(text=dict['details_title'], 
                   font_size=50, font_name="fonts/the_font.ttf",
                   halign='right', size_hint_y=y_size,
                   color=[0,0,0,1]))

        layout = GridLayout(cols=8, rows=6)

        # === first line ===
        layout.add_widget(end_button)
        layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=y_size))

        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout(size_hint_y=y_size))

        layout.add_widget(self.bagrut_text)
        layout.add_widget(
            Label(text=dict['bagrut'], font_size=30,
                  font_name="fonts/the_font.ttf", halign='right',
                  size_hint_y=y_size,
                  color=[0,0,0,1]))

        layout.add_widget(self.SAT_text)
        layout.add_widget(
            Label(text=dict['SAT'], font_size=30,
                  font_name="fonts/the_font.ttf", halign='right',
                  size_hint_y=y_size,
                  color=[0, 0, 0, 1]))

    # === second line ===
        layout.add_widget(BoxLayout(size_hint_y=y_size))
        layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=y_size))
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout(size_hint_y=y_size))

        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout(size_hint_x=1.5))
        layout.add_widget(BoxLayout(size_hint_x=1.5))

        # === space lines ===
        for lines in range(2):
            for space_line in range(8):
                layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=1))
                # layout.add_widget(BoxLayout(size_hint_y=1))

        # === last line ===
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=y_size))
        layout.add_widget(BoxLayout())

        layout.add_widget(BoxLayout(size_hint_x=0.2))

        layout.add_widget(
            Label(text="ךתופתתשה לע הדות", font_size=36,
                  color=[0, 0, 0, 1],
                  font_name="fonts/the_font.ttf", halign='right', size_hint_x=1.5))

        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())

        # === space lines ===
        for lines in range(1):
            for space_line in range(7):
                layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=1))
                # layout.add_widget(BoxLayout(size_hint_y=1))
        # ======= end =======

        layoutup.add_widget(layout)
        self.add_widget(layoutup)
        self.start()

    def start(self):
        pass

    def on_enter(self, *args):
        self.SAT_text.text = ""
        self.bagrut_text.text = ""

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def justify_hebrew(self, instance, value):
        print("justify hebrew", instance, value)
        if len(value) > 0:
            if len(instance.the_text) != len(value):
                instance.the_text = value
                instance.text = value[-1] + instance.the_text[:-1]

    def save(self, instance):
        details = {'SAT': self.SAT_text.text,
                   'bagrut': self.bagrut_text.text}
        self.the_app.score.add_details(details)

    def next(self, pars):
        self.the_app.sm.current = self.the_app.sm.next()