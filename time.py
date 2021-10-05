from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.uix.widget import Widget
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDTextButton

import datetime 
import pygame

Window.size = (350, 600)



class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
	pass




class MyMainApp(MDApp):
	pygame.init()
	sound = pygame.mixer.Sound("alarm.mp3")
	volume = 0
	showAnswers = True


	def build(self):
		return Builder.load_file("time.kv")
	def time_picker(self):
		time_dialouge = MDTimePicker()
		time_dialouge.bind(time=self.get_time, on_save=self.schedule)
		time_dialouge.open()
	def get_time(self, instance, time):
		self.root.ids.alarm_time.text = str(time)
	def schedule(self, *args):
		Clock.schedule_once(self.alarm, 1)
	def alarm(self, *args):
		while True:
			current_time = datetime.datetime.now().strftime("%H:%M:%S")
			if self.root.ids.alarm_time.text == str(current_time):
				self.start()
				break
	def set_volume(self, *args):
		self.volume += 0.05

		if self.volume < 1.0:
			Clock.schedule_interval(self.set_volume, 10)
			self.sound.set_volume(self.volume)
			print(self.volume)
		else:
			self.sound.set_volume(1)
			print("Reached Max volume")

	def start(self, *args):
		self.sound.play(-1)
		self.set_volume()
	def stop(self):
		self.sound.stop()
		Clock.unschedule(self.set_volume)
		self.volume = 0
	def change_color(self, instance):
		if instance in self.root.ids.values():
			current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
			for i in range(2):
				if f"nav_icon{i+1}" == current_id:
					self.root.ids[f"nav_icon{i+1}"].text_color = 1, 0, 0, 1
				else:
					self.root.ids[f"nav_icon{i+1}"].text_color = 0, 0, 0, 1

	def select(self, instance):
		if instance in self.root.ids.values():
			current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
			for i in range(12):
				if f"bottom_note{i+1}" == current_id:
					self.root.ids[f"bottom_note{i+1}"].disabled = False
				else:
					self.root.ids[f"bottom_note{i+1}"].disabled = True
	def createLabels(self, instance):
		for i in range(78): 
			txt = "{0}".format(i) if self.showAnswers else ""
			label = MDLabel(
                    text=txt,
                    halign="center",
					font_size= "30sp",
                )
			instance.ids[f"fret_label{i+1}"] = label

			instance.add_widget(label)

if __name__ == '__main__':
	MyMainApp().run()