#!/usr/bin/python
# -*- coding: utf-8 -*-
from cg_graphics_audio import *
from cei2 import *
from DetailsForm import *
from consent_form import ConsentForm
from framing_form import FramingForm
from learning_form import *
from final_form import FinalForm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from curiosity_score import *
from kivy_communication import KL


# version 2.0

conditions = ['no_framing/no_stop', 'framing/no_stop', 'no_framing/stop', 'framing/stop']


class CuriosityApp(App):
    sm = None
    cg = None
    cf = None
    qf = None
    lf = None
    df = None
    ff = None
    framing_form = None
    score = None
    float_layout = None

    cei2 = None
    bfi = None
    learn = None

    the_condition = ''

    def build(self):
        # initialize logger
        #KL.start([DataMode.file, DataMode.communication]) #, "/sdcard/curiosity/", the_ip='127.0.0.1')#self.user_data_dir)
        KL.start([DataMode.file, DataMode.communication, DataMode.ros], self.user_data_dir)

        self.cg = CuriosityGame(self)
        self.cf = ConsentForm(self)
        self.framing_form = FramingForm(self)

        self.cei2 = CEI2('questions.json')
        self.bfi  = CEI2('more_questions.json')
        self.qf = []
        for p in range(0, len(self.cei2.page_dict)):
            self.qf.append(QuestionsForm(self, self.cei2.page_dict[p]))
        for p in range(0, len(self.bfi.page_dict)):
            self.qf.append(QuestionsForm(self, self.bfi.page_dict[p]))

        self.learn = Learning(self)
        self.lf = [LearningForm(self)]
        for i in range(1, self.learn.max_number_questions / self.lf[0].q_per_page):
            self.lf.append(LearningForm(self))

        self.df = DetailsForm(self)
        self.ff = FinalForm(self)

        self.score = CuriosityScore(self.cg.game_duration,
                                    len(self.cg.items),
                                    self.user_data_dir)

        self.sm = ScreenManager()

        screen = Screen(name='consent')
        screen.add_widget(self.cf)
        self.sm.add_widget(screen)

        screen = Screen(name='framing')
        screen.add_widget(self.framing_form)
        self.sm.add_widget(screen)

        screen = Screen(name='thegame')
        screen.add_widget(self.cg.the_widget)
        self.sm.add_widget(screen)

        for kqf in range(0, len(self.qf)):
            screen = Screen(name="question"+str(kqf))
            screen.add_widget(self.qf[kqf])
            self.sm.add_widget(screen)

        for i, ilf in enumerate(self.lf):
            screen = Screen(name="learning_" + str(i))
            screen.add_widget(ilf)
            screen.bind(on_pre_enter=self.learn.start)
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

        self.choose_condition()

        self.sm.current = "consent"

    def choose_condition(self):
        self.the_condition = random.choice(conditions)
        KL.log.insert(action=LogAction.data, obj='condition', comment=self.the_condition)

        if 'no_framing' in self.the_condition:
            self.framing_form.framing_text.text = ''
        else:
            self.framing_form.framing_text.text = u'תונרקס קחשמ וניה אבה ךסמה'


    def on_pause(self):
        return True

if __name__ == '__main__':
    CuriosityApp().run()

