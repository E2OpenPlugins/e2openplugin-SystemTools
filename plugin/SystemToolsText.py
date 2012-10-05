from Screens.Screen import Screen

from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.ScrollLabel import ScrollLabel
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Button import Button

class SystemToolsTextBox(Screen):
	skin = """
	<screen name="SystemToolsTextBox" position="center,center" size="700,576" title="System Tools Text Box">
		<widget name="text" position="10,10" font="Console;20" size="680,520" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="140,536" size="140,40" alphatest="on" />
		<widget name="key_red" position="140,536" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="420,536" size="140,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="420,536" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""
	def __init__(self, session, text = "", title = ""):
		Screen.__init__(self, session)
		
		self.text = text
		self.title = title
		if title != "":
			self.onShown.append(self.setWindowTitle)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("OK"))
		self["text"] = ScrollLabel(self.text)
		
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"], 
				{
					"cancel": self.cancel,
					"ok": self.ok,
					"up": self["text"].pageUp,
					"down": self["text"].pageDown,
					"red": self.cancel,
					"green": self.ok
				}, -1)


	def setWindowTitle(self):
		self.setTitle(self.title)
		
	def ok(self):
		self.close()
	
	def cancel(self):
		self.close()

class SystemToolsTextBox2(Screen):
	skin = """
	<screen name="SystemToolsTextBox2" position="center,center" size="1024,576" title="System Tools Text Box">
		<widget name="text" position="10,10" size="1004,520" font="Console;22" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="248,536" size="140,40" alphatest="on" />
		<widget name="key_red" position="248,536" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="636,536" size="140,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="636,536" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""
	def __init__(self, session, text = "", title = ""):
		Screen.__init__(self, session)
		
		self.text = text
		self.title = title
		if title != "":
			self.onShown.append(self.setWindowTitle)
		self["key_red"] = Label(_("Close"))
		self["key_green"] = Label(_("Close"))
		self["text"] = ScrollLabel(self.text)
		
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"], 
				{
					"cancel": self.cancel,
					"ok": self.ok,
					"up": self["text"].pageUp,
					"down": self["text"].pageDown,
					"red": self.cancel,
					"green": self.ok,
				}, -1)

	def setWindowTitle(self):
		self.setTitle(self.title)
		
	def ok(self):
		self.close()
	
	def cancel(self):
		self.close()

class SystemToolsTextBoxEcm(Screen):
	skin = """
	<screen name="SystemToolsTextBox" position="810,40" size="410,288" title="System Tools Text Box">
		<widget name="text" position="10,10" size="390,268" font="Console;20" />
	</screen>"""
	def __init__(self, session, text = "", title = ""):
		Screen.__init__(self, session)
		
		self.text = text
		self.title = title
		if title != "":
			self.onShown.append(self.setWindowTitle)
		self["text"] = ScrollLabel(self.text)
		
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"], 
				{
					"cancel": self.cancel,
					"ok": self.ok,
					"up": self["text"].pageUp,
					"down": self["text"].pageDown,
					"red": self.cancel,
					"green": self.ok,
				}, -1)

	def setWindowTitle(self):
		self.setTitle(self.title)
		
	def ok(self):
		self.close()
	
	def cancel(self):
		self.close()
