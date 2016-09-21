from priorityqueue import HandlerClassSelector, initialHashHandler
from widgets import HierarchyWidget
from config import conf
from pane import Pane
from widgets.edit import EditWidget
from i18n import translate

class HierarchyHandler( Pane ):
	def __init__(self, moduleName, modulInfo, *args, **kwargs):
		icon = "icons/modules/hierarchy.svg"
		if "icon" in modulInfo.keys():
			icon = modulInfo["icon"]

		super(HierarchyHandler, self).__init__(modulInfo["visibleName"], icon )
		if "hideInMainBar" in modulInfo.keys() and modulInfo["hideInMainBar"]:
			self["style"]["display"] = "none"
		self.moduleName = moduleName
		initialHashHandler.insert( 1, self.canHandleInitialHash, self.handleInitialHash)

	def canHandleInitialHash(self, pathList, params ):
		if len(pathList)>1:
			if pathList[0]==self.moduleName:
				if pathList[1] in ["list"] or (pathList[1]=="edit" and len(pathList)>2):
					return( True )
		return( False )

	def handleInitialHash(self, pathList, params):
		assert self.canHandleInitialHash( pathList, params )
		if pathList[1] == "list":
			self.addWidget( HierarchyWidget( self.moduleName ) )
			self.focus()
		elif pathList[1] == "edit" and len(pathList)>2:
			pane = Pane(translate("Edit"), closeable=True, iconClasses=["modul_%s" % self.moduleName, "apptype_hierarchy", "action_edit" ])
			edwg = EditWidget( self.moduleName, EditWidget.appHierarchy, key=pathList[2], hashArgs=(params or None))
			pane.addWidget( edwg )
			conf["mainWindow"].addPane( pane, parentPane=self)
			pane.focus()


	@staticmethod
	def canHandle( moduleName, modulInfo ):
		return( modulInfo["handler"]=="hierarchy" or modulInfo["handler"].startswith("hierarchy."))

	def onClick(self, *args, **kwargs ):
		if not len(self.widgetsDomElm._children):
			self.addWidget( HierarchyWidget(self.moduleName ) )
		super( HierarchyHandler, self ).onClick( *args, **kwargs )


HandlerClassSelector.insert( 3, HierarchyHandler.canHandle, HierarchyHandler )
