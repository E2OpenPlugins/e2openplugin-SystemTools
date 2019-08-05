# System Tools e2plugin
# This Tools are made To have system tools Integrated into skin.
# For prober skin integration, skin.xml needs to be adapted to have the screens fit into it.
# I added an info.txt file, there You find the openpli-hd skin integration example.
# I used A part of the Tools v0.81 from Rob van der Does
# If someone can find him may I ask to send this tools to him ?
# Feel free to add comments and pas extra stuff You would have fitted in.
# stefansat#telenet.be
# Christophe Van Reusel
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.TextBox import TextBox
from SystemToolsText import SystemToolsTextBox, SystemToolsTextBox2, SystemToolsTextBoxEcm
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigInteger, ConfigYesNo, ConfigText, ConfigElement
from Components.ConfigList import ConfigList
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, pathExists
from SystemToolsConsole import ConsoleBox, SystemToolsConsole
from Components.MultiContent import MultiContentEntryText
import os
from enigma import eTimer, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, gFont, gRGB, eListboxPythonMultiContent

##############################################################################
config.SystemTools = ConfigSubsection()
config.SystemTools.mainmenu = ConfigYesNo(default=False)
config.SystemTools.systemmenu = ConfigYesNo(default=False)
config.SystemTools.applicationmenu = ConfigYesNo(default=False)
config.SystemTools.setupmenu = ConfigYesNo(default=False)

#global vars#################################################################
entrylist = []
lengthList = [0,0,0,0]


###########################################################################


class SystemToolsConfig(Screen, ConfigListScreen):
	skin = """
	<screen name="SystemToolsConfig" position="center,center" size="670,522" title="SystemToolsConfig to activate some changes restart enigma">
		<widget name="config" position="10,10" size="650,466" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="buttons/red.png" position="130,482" size="140,40" alphatest="on" />
		<widget name="key_red" position="130,482" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="400,482" size="140,40" pixmap="buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="400,482" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""

	def __init__(self, session):
		self.skin = SystemToolsConfig.skin			
		Screen.__init__(self, session)
		self.list = []

		ConfigListScreen.__init__(self, self.list)
		self.name = "SystemToolsConfig to activate some changes restart enigma"
		self.onShown.append(self.setWindowTitle)
	
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.keyCancel,
			"back": self.keyCancel,
			"green": self.keySave,

		}, -2)

		self.list.append(getConfigListEntry(_("Show SystemTools in Main menu"), config.SystemTools.mainmenu))
		self.list.append(getConfigListEntry(_("Show SystemTools in System menu"), config.SystemTools.systemmenu))
		self.list.append(getConfigListEntry(_("Show SystemTools in Setup menu"), config.SystemTools.setupmenu))
		self.list.append(getConfigListEntry(_("Show SystemTools in Plugin menu restart enigma to activate"), config.SystemTools.applicationmenu))
	
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def setWindowTitle(self):
		self.setTitle(self.name)

	def keySave(self):
		for x in self["config"].list:
			x[1].save()
		self.close()
		
	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()	


class SystemToolsSc(Screen):
	skin = """
	<screen name="SystemToolsSc" position="center,center" size="670,522" title="System Tools Main Menu">
		<widget name="entries" position="10,10" size="650,466" itemHeight="45" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="buttons/red.png" position="62,482" size="140,40" alphatest="on" />
		<widget name="key_red" position="62,482" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="265,482" size="140,40" pixmap="buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="265,482" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
		<ePixmap position="468,482" size="140,40" pixmap="buttons/yellow.png" alphatest="on" zPosition="1" />
		<widget name="key_yellow" position="468,482" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="yellow" transparent="1" />
	</screen>"""

	def __init__(self, session):
		self.skin = SystemToolsSc.skin
		Screen.__init__(self, session)
		#self.ListEntry = []
		self.list = []
						
		self.name = "System Tools Main Menu"
		self.onShown.append(self.setWindowTitle)
			
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("OK"))
		self["key_yellow"] = Label(_("Configure"))
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"ok": self.go,
			"cancel": self.cancel,
			"red": self.cancel,			
			"green": self.go,
			"yellow": self.KeyConfig,
		}, -1)

		self.list.append(("Restart active Softcam", "com_one"))
		self.list.append(("Restart enigma2", "com_eight"))
		self.list.append(("Ecm Info ", "com_two"))
		self.list.append(("Clean Memory", "com_seven"))
		self.list.append(("Delete Epg data CAUTION RESTARTS ENIGMA2 ", "com_six"))
		self.list.append(("Menu Swap File Tools", "com_four"))
		self.list.append(("Menu System Information Tools ", "com_five"))
		self.list.append((_("Exit"), "exit"))
					
		self["entries"] = MenuList(self.list)
		
						
	def setWindowTitle(self):
		self.setTitle(self.name)

	def KeyConfig(self):
		self.session.open(SystemToolsConfig) 

				
	def go(self):
		returnValue = self["entries"].l.getCurrentSelection()[1]
		print "\n[SystemToolsSc] returnValue: " + returnValue + "\n"
		
		if returnValue is not None:
			if returnValue is "com_one":
				msg = _("Please wait, restarting softcam")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.activityTimer = eTimer()
				self.activityTimer.timeout.get().append(self.SoftcamRestart)
				self.activityTimer.start(300, False)

			elif returnValue is "com_two":
				msg = self.EcmInfo()
				title = "Ecm Info"
				self.session.open(SystemToolsTextBox, msg, title)

			elif returnValue is "com_four":
				self.swap()

			elif returnValue is "com_five":
				self.info() 

			elif returnValue is "com_six":
				self.prombt("init 4; sleep 5; rm -rf /media/hdd/epg.dat; rm -rf /media/usb/epg.dat; rm -rf /media/usb/crossepg; rm -rf /media/hdd/crossepg; sleep 5; init 3" )
			elif returnValue is "com_seven":
				self.prombt("sync; echo 3 > /proc/sys/vm/drop_caches")
			elif returnValue is "com_eight":
				self.prombt("init 4; sleep 5; init 3")
						
			else:
				print "\n[SystemToolsSc] cancel\n"
				self.close(None)

	def prombt(self, com):
		self.session.open(SystemToolsConsole,_("start shell com: %s") % (com), ["%s" % com])

	def prombtbox(self, com):	
		self.session.open(ConsoleBox,_("start shell com: %s") % (com), ["%s" % com])

	def SoftcamRestart(self):
		self.activityTimer.stop()
		del self.activityTimer
		os.system('sleep 2')
		os.system('/etc/init.d/softcam stop')
		self.oldref = self.session.nav.getCurrentlyPlayingServiceReference()
		self.session.nav.stopService()
		os.system('sleep 2')
		os.system('/etc/init.d/softcam start')
		os.system('sleep 3')
		if self.mbox:
			self.mbox.close()
		self.close()
		self.session.nav.playService(self.oldref)
		del self.oldref

	def EcmInfo(self):
		if fileExists("/tmp/ecm.info"):
			ecm = open ("/tmp/ecm.info")			
			msg = ecm.read()
			ecm.close()
			return msg
		else:
			msg = "Your Are watching FTA Channel or\n ecm.info file is missing."
			return msg
							
	def info(self):
		self.session.open(SystemToolsInf)

	def swap(self):
		self.session.open(SystemToolsSwap)

	def cancel(self):
		print "\n[SystemToolsSc] cancel\n"
		self.close(None)

class SystemToolsInf(Screen):
	skin = """
	<screen name="SystemToolsInf" position="center,center" size="670,522" title="System Tools Information Menu">
		<widget name="entries" position="10,10" size="650,466" itemHeight="45" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="buttons/red.png" position="130,482" size="140,40" alphatest="on" />
		<widget name="key_red" position="130,482" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="400,482" size="140,40" pixmap="buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="400,482" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""

	def __init__(self, session):
		self.skin = SystemToolsInf.skin
		Screen.__init__(self, session)
		self.list = []
		
		self.name = "System Tools Information Menu"
		self.onShown.append(self.setWindowTitle)
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("OK"))
				
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"ok": self.go,
			"cancel": self.cancel,
			"red": self.cancel,			
			"green": self.go,
		}, -1)
		
		self.list.append(("  Memory info simple", "com_infone"))
		self.list.append(("  Memory info list", "com_infseven"))
		self.list.append(("  Smartreader Info", "com_inftwo"))
		self.list.append(("  Mounted devices", "com_inftree"))
		self.list.append(("  Storage devices Info", "com_inffour"))
		self.list.append(("  Cpu Information", "com_inffive"))
		self.list.append(("  Linux and gcc version", "com_infsix"))
		self.list.append((_("  Exit"), "exit"))

		self["entries"] = MenuList(self.list)

	def go(self):
		returnValue = self["entries"].l.getCurrentSelection()[1]
		print "\n[SystemToolsInf] returnValue: " + returnValue + "\n"
		
		if returnValue is not None:
			if returnValue is "com_infone":
				memscriptfile = "sh "
				memscriptfile += resolveFilename(SCOPE_PLUGINS)
				memscriptfile += "/Extensions/SystemTools/memorysimple.sh"
				self.prombt(memscriptfile)
								
			elif returnValue is "com_inftwo":
				self.prombtbox("list_smargo")
					
			elif returnValue is "com_inftree":
				title = "Mounted Devices"
				msg = self.mountedDevInf()
				self.session.open(SystemToolsTextBox, msg, title)

			elif returnValue is "com_inffour":
				title = "Sorage Devices Information"
				msg = self.scsiDev()
				self.session.open(SystemToolsTextBox2, msg, title)

			elif returnValue is "com_inffive":
				title = "Cpu Information"
				msg = self.cpuInf()
				self.session.open(SystemToolsTextBox, msg, title)

			elif returnValue is "com_infsix":
				title = "Linux and Gcc Version"
				msg = self.lingccInf()
				self.session.open(SystemToolsTextBox, msg, title)

			elif returnValue is "com_infseven":
				self.prombt("cat /proc/meminfo")

			else:
				print "\n[SystemToolsInf] cancel\n"
				self.close(None)

	def mountedDevInf(self):
		mounteddevinf = open("/proc/mounts")
		msg = mounteddevinf.read().strip()
		mounteddevinf.close()
		return msg

	def lingccInf(self):
		lingccinf = open("/proc/version")
		msg = lingccinf.read().strip()
		lingccinf.close()
		return msg

	def cpuInf(self): 
		cpuinfentrylist = []
		cpuinf = open("/proc/cpuinfo", "r")
		for line in cpuinf:
				entry = line.replace("\t", "").strip().split(':')
				cpuinfentrylist.append(':'.join(entry))
		msg = '\n'.join(cpuinfentrylist)
		cpuinf.close()
		return msg

	def scsiDev(self):
		storage = open("/proc/scsi/scsi")
		msg = storage.read().strip()
		storage.close()
		return msg

	def prombt(self, com):
		self.session.open(SystemToolsConsole,_("start shell com: %s") % (com), ["%s" % com])

	def prombtbox(self, com):	
		self.session.open(ConsoleBox,_("start shell com: %s") % (com), ["%s" % com])

	
	def setWindowTitle(self):
		self.setTitle(self.name)
	
	def cancel(self):
		print "\n[SystemToolsInf] cancel\n"
		self.close(None)

class SystemToolsSwap(Screen):
	skin = """
	<screen name="SystemToolsSwap" position="center,center" size="670,522" title="Swap file Tools Menu">
		<widget name="entries" position="10,10" size="650,466" itemHeight="45" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="buttons/red.png" position="130,482" size="140,40" alphatest="on" />
		<widget name="key_red" position="130,482" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="400,482" size="140,40" pixmap="buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="400,482" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""

	def __init__(self, session):
		self.skin = SystemToolsSwap.skin
		Screen.__init__(self, session)
		self.list = []
		
		self.name = "Swap File Tools Menu"
		self.onShown.append(self.setWindowTitle)
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("OK"))
				
		self["actions"] = ActionMap(["OkCancelActions", "WizardActions", "ColorActions"],
		{
			"ok": self.go,
			"cancel": self.cancel,
			"red": self.cancel,			
			"green": self.go,
		}, -1)
		
		self.list.append(("  Show Aktif Swap", "com_swapone"))
		self.list.append(("  De-activate Swap", "com_swapten"))
		self.list.append(("  Create swap file on hdd", "com_swaptwo"))
		self.list.append(("  Create swap file on cf ", "com_swaptree"))
		self.list.append(("  Create swap file on usb", "com_swapfour"))
		self.list.append(("  Aktivate swap on HDD", "com_swapsix"))
		self.list.append(("  Aktivate swap on CF", "com_swapseven"))
		self.list.append(("  Aktivate swap on USB", "com_swapeight"))
		self.list.append((_("  Exit"), "exit"))

		self["entries"] = MenuList(self.list)

	def go(self):
		returnValue = self["entries"].l.getCurrentSelection()[1]
		print "\n[SystemToolsSwap] returnValue: " + returnValue + "\n"
		
		if returnValue is not None:
			if returnValue is "com_swapone":
				title = "Aktif Swap"
				msg = self.aktswapscreen()
				self.session.open(SystemToolsTextBox, msg, title)
				
			elif returnValue is "com_swaptwo":
				msg = _("Please wait : Creating swap File on hdd")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.activityTimer = eTimer()
				self.activityTimer.timeout.get().append(self.createswaphdd)				
				self.activityTimer.start(100, False)

			elif returnValue is "com_swaptree":
				msg = _("Please wait : Creating swap File on cf")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.activityTimer = eTimer()
				self.activityTimer.timeout.get().append(self.createswapcf)				
				self.activityTimer.start(100, False)
				
			elif returnValue is "com_swapfour":
				msg = _("Please wait : Creating swap File on usb")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.activityTimer = eTimer()
				self.activityTimer.timeout.get().append(self.createswapusb)				
				self.activityTimer.start(100, False)

			elif returnValue is "com_swapsix":
				self.activateswaphdd()
				
			elif returnValue is "com_swapseven":
				self.activateswapcf()
				
			elif returnValue is "com_swapeight":
				self.activateswapusb()
				
			elif returnValue is "com_swapten":
				msg = _("Swap is De-activated")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab")
					
			else:
				print "\n[SystemToolsSwap] cancel\n"
				self.close(None)

	def readFile(self, filename):
		mounts = open(filename)
		msg = mounts.read().strip()
		mounts.close()
		return msg

	def aktswapscreen(self):
		swapentrylist = []
		if fileExists("/proc/swaps"):
			aktifswapfile = open("/proc/swaps", "r")
			counter = 0
			for line in aktifswapfile:
					if line[0] != "\n":
						entry = line.split()
						global lenghtList
						if len(entry[0]) > lengthList[0]:
							lengthList[0] = len(entry[0])
						if len(entry[1]) > lengthList[1]:
							lengthList[1] = len(entry[1])
						if len(entry[2]) > lengthList[2]:
							lengthList[2] = len(entry[2])					
						if len(entry[3]) > lengthList[3]:
							lengthList[3] = len(entry[3])
						counter = counter+1
						if counter >= 2:
							swapentrylist.append(' '.join(["Filename:", entry[0]]))
							swapentrylist.append(' '.join(["Type    :", entry[1]]))
							swapentrylist.append(' '.join(["Size    :", entry[2]]))
							swapentrylist.append(' '.join(["Used    :", entry[3]]))
			if swapentrylist != []:
				return '\n'.join(swapentrylist)
			else:
				return "Swapfile is Not Aktivated !"
		else:
			return "SwapFile is Not Aktif ! or /proc/swaps is missing"		
	
	def createswapcf(self):
		self.activityTimer.stop()
		del self.activityTimer
		if fileExists("/media/cf/swapfile"):
			msg = _("Swap File was already created ! You can activate the SWAP on CF if not done yet")
			self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			self.mbox.close()
		else:
			if pathExists("/media/cf"):
				os.system('sleep 1')
				os.system('dd if=/dev/zero of=/media/cf/swapfile bs=1048576 count=128; mkswap /media/cf/swapfile')
				os.system('sleep 1')
				msg = _("Done! You can now activate the SWAP on CF")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()
			else:
				msg = _("No compact flash mounted on /media/cf")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()

	def createswaphdd(self):
		self.activityTimer.stop()
		del self.activityTimer
		if fileExists("/media/hdd/swapfile"):
			msg = _("Swap File was already created ! You can activate the SWAP on HDD if not done yet")
			self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			self.mbox.close()
		else:
			if pathExists("/media/hdd"):
				os.system('sleep 1')
				os.system('dd if=/dev/zero of=/media/hdd/swapfile bs=1048576 count=128; mkswap /media/hdd/swapfile')
				os.system('sleep 1')
				msg = _("Done! You can now activate the SWAP on HDD")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()
			else:
				msg = _("No hard drive mounted on /media/hdd")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()				

	def createswapusb(self):
		self.activityTimer.stop()
		del self.activityTimer
		if fileExists("/media/usb/swapfile"):
			msg = _("Swap File was already created ! You can activate the SWAP on USB if not done yet")
			self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			self.mbox.close()
		else:
			if pathExists("/media/usb"):
				os.system('sleep 1')
				os.system('dd if=/dev/zero of=/media/usb/swapfile bs=1048576 count=128; mkswap /media/usb/swapfile')
				os.system('sleep 1')
				msg = _("Done! You can now activate the SWAP on USB")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()
			else:
				msg = _("No usb stick mounted on /media/usb")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()

	def activateswaphdd(self):
		if fileExists("/media/hdd/swapfile"):
			os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab; swapon /media/hdd/swapfile")
			os.system("sed -i '/hdd\/swapfile/d' /etc/fstab; echo -e '/media/hdd/swapfile swap swap defaults 0 0' >> /etc/fstab")
			msg = _("Swap is activated on HDD")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else:
			msg = ("There is no swap file found on HDD. Create it first")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)

	def activateswapcf(self):
		if fileExists("/media/cf/swapfile"):
			os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab; swapon /media/cf/swapfile")
			os.system("sed -i '/cf\/swapfile/d' /etc/fstab; echo -e '/media/cf/swapfile swap swap defaults 0 0' >> /etc/fstab")
			msg = _("Swap is activated on CF")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else:
			msg = ("There is no swap file found on CF. Create it first")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			
	def activateswapusb(self):
		if fileExists("/media/usb/swapfile"):
			os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab; swapon /media/usb/swapfile")
			os.system("sed -i '/usb\/swapfile/d' /etc/fstab; echo -e '/media/usb/swapfile swap swap defaults 0 0' >> /etc/fstab")
			msg = _("Swap is activated on USB")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else:
			msg = ("There is no swap file found on USB. Create it first")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			
	def prombt(self, com):
		self.session.open(Console,_("start shell com: %s") % (com), ["%s" % com])

	def prombtbox(self, com):	
		self.session.open(ConsoleBox,_("start shell com: %s") % (com), ["%s" % com])

	
	def setWindowTitle(self):
		self.setTitle(self.name)
	
	def cancel(self):
		print "\n[SystemToolsSwap] cancel\n"
		self.close()

###########################################################################


def main(session, **kwargs):
	print "\n[SystemToolsSc] start\n"	
	session.open(SystemToolsSc)


def menu(menuid, **kwargs):
	if menuid == "mainmenu" and config.SystemTools.mainmenu.value == True :
		return [(_("System Tools"), main, "tools_setup", 45)]
	
	if menuid == "system" and config.SystemTools.systemmenu.value == True :
		return [(_("System Tools"), main, "tools_setup", 45)]

	if menuid == "setup" and config.SystemTools.setupmenu.value == True :
		return [(_("System Tools"), main, "tools_setup", 45)]

	return []
###########################################################################

def Plugins(**kwargs):
	if config.SystemTools.applicationmenu.value == True :
		return [PluginDescriptor(name = "System Tools", description = "basic toolsmenu", where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main),
			PluginDescriptor(name = "System Tools", description = "basic toolsmenu", where = PluginDescriptor.WHERE_MENU, fnc = menu),
			PluginDescriptor(name = "System Tools", description = "basic toolsmenu", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main)]
	
	return [PluginDescriptor(name = "System Tools", description = "basic toolsmenu", where = PluginDescriptor.WHERE_MENU, fnc = menu),
		PluginDescriptor(name = "System Tools", description = "basic toolsmenu", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main)]
	

