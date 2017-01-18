#!/usr/bin/python
# -*- coding: utf-8 -*-
from cg_graphics_audio import *
from cei2 import *
from DetailsForm import *
from consent_form import ConsentForm
from learning_form import *
from final_form import FinalForm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from curiosity_score import *
from kivy_communication import KL


class CuriosityApp(App):
    sm = None
    cg = None
    cf = None
    qf = None
    lf = None
    df = None
    ff = None
    score = None
    float_layout = None

    cei2 = None
    learn = None

    def build(self):
        # initialize logger
        #KL.start([DataMode.file, DataMode.communication]) #, "/sdcard/curiosity/", the_ip='127.0.0.1')#self.user_data_dir)
        KL.start([DataMode.file, DataMode.communication, DataMode.ros], self.user_data_dir)

        self.cg = CuriosityGame(self)
        self.cf = ConsentForm(self)

        self.cei2 = CEI2()
        self.qf = []
        for p in range(0, len(self.cei2.page_dict)):
            self.qf.append(QuestionsForm(self, self.cei2.page_dict[p]))

        self.learn = Learning(self)
        self.lf = [LearningForm(self), LearningForm(self)]

        self.df = DetailsForm(self)
        self.ff = FinalForm(self)

        self.score = CuriosityScore(self.cg.game_duration,
                                    len(self.cg.items),
                                    self.user_data_dir)

        self.sm = ScreenManager()

        screen = Screen(name='consent')
        screen.add_widget(self.cf)
        self.sm.add_widget(screen)

        screen = Screen(name='thegame')
        screen.add_widget(self.cg.the_widget)
        self.sm.add_widget(screen)

        for kqf in range(0, len(self.qf)):
            screen = Screen(name="question"+str(kqf))
            screen.add_widget(self.qf[kqf])
            self.sm.add_widget(screen)

        screen = Screen(name="learning_0")
        screen.add_widget(self.lf[0])
        screen.bind(on_pre_enter=self.learn.start)
        self.sm.add_widget(screen)

        screen = Screen(name="learning_1")
        screen.add_widget(self.lf[1])
        self.sm.add_widget(screen)

        screen = Screen(name="details")
        screen.add_widget(self.df)
        self.sm.add_widget(screen)

        screen = Screen(name="final")
        screen.bind(on_enter=self.ff.start)
        screen.add_widget(self.ff)
        self.sm.add_widget(screen)

        self.start()
        return self.sm

    def start(self):
        KL.start([DataMode.file, DataMode.communication, DataMode.ros], self.user_data_dir)
        self.cf.start(self)
        for qf in self.qf:
            qf.start()
        self.df.start()
        self.score.init_score()
        self.sm.current = "consent"

    def on_pause(self):
        return True

if __name__ == '__main__':
    CuriosityApp().run()

