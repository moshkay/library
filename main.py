import kivy
kivy.require("1.9.1")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen 
from kivy.clock import Clock 
from kivymd.theming import ThemeManager
from kivy.properties import StringProperty,ListProperty,ObjectProperty
from kivymd.card import MDCard
from kivymd.dialog import MDDialog
from kivymd.button import MDFlatButton
from kivymd.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.button import MDRaisedButton
from kivymd.list import OneLineListItem
from kivy.storage.jsonstore import JsonStore
from random import random

class Manager(ScreenManager):
	def __init__(self,**opt):
		super(Manager,self).__init__(**opt)
		Clock.schedule_once(self.move,4)
	def move(self,*args):
		self.switch_to(Home(),direction="right")

class ToolbarScreen(Screen):
	page_title=StringProperty("")

	#these store the action items
	left=ListProperty([])
	right=ListProperty([])
	next_page=StringProperty("")#stores the next name of the next page
	def __init__(self,**opt):
		super(ToolbarScreen,self).__init__(**opt)
	def move(self,*args):
		app.root.current=self.next_page



class UserCard(MDCard):
	sex=StringProperty()
	accesscode=StringProperty()
	surname=StringProperty()
	lastname=StringProperty()
	age=StringProperty()
	password=StringProperty()
	def __init__(self,**opt):
		super(UserCard,self).__init__(**opt)

class MaterialStatus(MDCard):
	userid=StringProperty("")
	username=StringProperty("")
	material=StringProperty("")
	date=StringProperty("")
	status=StringProperty("")
	def __init__(self,**opt):
		super(MaterialStatus,self).__init__(**opt)

class Dialog(MDDialog):
	label=ObjectProperty()
	def __init__(self,**opt):
		super(Dialog,self).__init__(**opt)
		self.title="Actions Performed:"

	def display_mat(self,material,mat_id,status):
		self.label.text="%s with the id %s has been %s "%(material,mat_id,status)
		self.createBox()
		self.open()
	def display_user(self,accesscode,status):
		self.label.text="the user with %s has been %s"%(accesscode,status)
		self.createBox()
		self.open()
	def no_display_user(self,accesscode,status):
		self.label.text="the user with %s %s"%(accesscode,status)
		self.createBox()
		self.open()
	def createBox(self):
		self.add_action_button("Dismiss", action=lambda x: self.dismiss())
		

###########################################
#the screens on the application           #
###########################################

#the main screens
class Home(Screen):
	def __init__(self,**opt):
		super(Home,self).__init__(**opt)

class Splash(Screen):
	def __init__(self,**opt):
		super(Splash,self).__init__(**opt)

#screens related to the admin
class Admin(ToolbarScreen):
	
	def __init__(self,**opt):
		super(Admin,self).__init__(**opt)

class AdminLogin(ToolbarScreen):
	username=ObjectProperty(None)
	password=ObjectProperty(None)
	def __init__(self,**opt):
		super(AdminLogin,self).__init__(**opt)
	def login(self,*args):
		admin=JsonStore("jsondb/admin.json")
		if (self.username.text != "" and self.password.text != ""):
			if admin.exists(self.username.text):
				if self.password.text==admin.get(self.username.text)["password"]:
					app.root.current="admin"
			else:
				Dialog().no_display_user("admin username and password","does not exist")
			

class ManageAccount(ToolbarScreen):
	def __init__(self,**opt):
		super(ManageAccount,self).__init__(**opt)


#the status screen
class Status(ToolbarScreen):
	status_layout=ObjectProperty()
	def __init__(self,**opt):
		super(Status,self).__init__(**opt)


class UserData(ToolbarScreen):
	librarian=ObjectProperty()
	patron=ObjectProperty()
	def __init__(self,**opt):
		super(UserData,self).__init__(**opt)
		self.bind(on_pre_enter=self.update)
	def update(self,*args):
		self.patron.clear_widgets()
		self.librarian.clear_widgets()
		lib=JsonStore("jsondb/librarian.json")
		pat=JsonStore("jsondb/patron.json")
		for i in pat:
			user=pat.get(i)
			detail=UserCard()
			detail.sex=user["sex"]
			detail.accesscode=user["accesscode"]
			detail.age=user["age"]
			detail.surname=user["surname"]
			detail.lastname=user["lastname"]
			self.patron.add_widget(detail)
		for i in lib:
			user=lib.get(i)
			detail=UserCard()
			detail.sex=user["sex"]
			detail.accesscode=user["accesscode"]
			detail.age=user["age"]
			detail.surname=user["surname"]
			detail.lastname=user["lastname"]
			self.librarian.add_widget(detail)

			
			


class AddUser(ToolbarScreen):
	sex="Male"
	user="Pat"
	surname=ObjectProperty()
	lastname=ObjectProperty()
	age=ObjectProperty()
	def __init__(self,**opt):
		super(AddUser,self).__init__(**opt)
	def sex_change(self,widget):
		if widget.state=="down":
			if widget.group=="sex":
				self.sex=widget.value
			elif widget.group=="users":
				self.user=widget.value
				
	def add_user(self,*args):
		#getting the last 4 digit of a random number
		value=str(random())[-1:-5:-1]

		if (self.surname.text!="" and self.lastname.text!="" and self.age.text!=""):
			accesscode=self.user+value
			if (self.user=="Pat"):
				patron=JsonStore("jsondb/patron.json")
				patron.put(accesscode,surname=self.surname.text,lastname=self.lastname.text,age=self.age.text,accesscode=accesscode,sex=self.sex)
			else:
				librarian=JsonStore("jsondb/librarian.json")

				librarian.put(accesscode,surname=self.surname.text,lastname=self.lastname.text,age=self.age.text,
					accesscode=accesscode,sex=self.sex)
			Dialog().display_user(accesscode,"added")

							
class DeleteUser(ToolbarScreen):
	accesscode=ObjectProperty()
	user="Pat"
	def __init__(self,**opt):
		super(DeleteUser,self).__init__(**opt)
	def sex_change(self,widget):
		if widget.state=="down":
			self.user=widget.value
			print(self.user)
	def delete(self,*args):
		if self.user=="Pat":
			User=JsonStore("jsondb/patron.json")
		else:
			User=JsonStore("jsondb/librarian.json")
		if self.accesscode.text!="":
			if User.exists(self.accesscode.text):
				User.delete(self.accesscode.text)
				Dialog().display_user(self.accesscode,"deleted")

		

class Librarian(ToolbarScreen):
	def __init__(self,**opt):
		super(Librarian,self).__init__(**opt)


class Borrow(ToolbarScreen):
	mat_name=ObjectProperty()
	searchdisplay=ObjectProperty(None)
	def __init__(self,**opt):
		super(Borrow,self).__init__(**opt)
		
	def search(self,*args):
		self.searchdisplay.clear_widgets()
		self.mat=JsonStore("jsondb/material.json")

		if self.mat.exists(self.mat_name.text):
			info=self.mat.get(self.mat_name.text)
			text="Mat_id: %s  Material type: %s  Author: %s  "%(info["mat_id"],info["material"],info["author"])
			material=OneLineListItem(size_hint=(1,None),text=text)
			self.searchdisplay.add_widget(material)
		
	def borrow(self,*args):
		pass


		

class Return(ToolbarScreen):
	def __init__(self,**opt):
		super(Return,self).__init__(**opt)
		

class Patron(ToolbarScreen):
	
	def __init__(self,**opt):
		super(Patron,self).__init__(**opt)
	def show_dialog(self,*args):
		button=MDFlatButton(text='OK')
		self.dialog=MDDialog(size_hint=(0.5,0.4),
			auto_dismiss=False,
			pos_hint={"center_x":0.5},
			title="Material to be returned",
			content=button)
		button.bind(on_press=self.dialog.dismiss)
		self.dialog.open()

class PatronLogin(ToolbarScreen):
	accesscode=ObjectProperty()
	def __init__(self,**opt):
		super(PatronLogin,self).__init__(**opt)
	def login(self,*args):
		if self.accesscode.text!="":
			patron=JsonStore("jsondb/patron.json")
			if patron.exists(self.accesscode.text):
				app.root.current="patron"
			else:
				Dialog().no_display_user("the user with accesscode %s"%self.accesscode.text,
					"does not exist")


class LibrarianLogin(ToolbarScreen):
	accesscode=ObjectProperty()
	def __init__(self,**opt):
		super(LibrarianLogin,self).__init__(**opt)
	def login(self,*args):
		if self.accesscode.text!="":
			librarian=JsonStore("jsondb/librarian.json")
			if librarian.exists(self.accesscode.text):
				app.root.current="librarian"
			else:
				Dialog().no_display_user("the user with accesscode %s"%self.accesscode.text,
					"does not exist")

class AddMaterial(ToolbarScreen):
	material=ObjectProperty()
	mat_id=ObjectProperty()
	author=ObjectProperty()
	def __init__(self,**opt):
		super(AddMaterial,self).__init__(**opt)
	def add_mat(self,*args):
		mat=JsonStore("jsondb/material.json")
		if self.mat_id.text!="" and self.author.text!="":
			if mat.exists(self.mat_id.text):
				Dialog().no_display_user("the material with the id %s"%self.mat_id.text,
				"already exists")
			else:
				mat.put(self.mat_id.text,material=self.material.text,author=self.author.text,mat_id=self.mat_id.text)
				print("added")
				Dialog().display_mat(self.material.text,self.mat_id.text,"added")


class DeleteMaterial(ToolbarScreen):
	mat_id=ObjectProperty()
	def __init__(self,**opt):
		super(DeleteMaterial,self).__init__(**opt)
	def delete(self,*args):
		mat=JsonStore("jsondb/material.json")
		if self.mat_id.text!="":
			if mat.exists(self.mat_id.text):
				mat.delete(self.mat_id.text)
				Dialog().display_mat("Material",self.mat_id.text,"deleted")
			else:
				Dialog().no_display_user("the material with the id %s"%self.mat_id.text,
				"does not exist")

				


class LibraryApp(App):
	"""docstring for LibraryApp"""
	theme_cls=ThemeManager()
	use_kivy_settings=False
	def build(self):
		return Manager()
app=LibraryApp()
app.run()