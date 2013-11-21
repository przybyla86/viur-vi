import html5
from network import NetworkService
from priorityqueue import actionDelegateSelector
from widgets.edit import EditWidget
from config import conf
from pane import Pane


class AddAction( html5.ext.Button ):
	"""
		Adds a new node in a hierarchy application.
	"""
	def __init__(self, *args, **kwargs):
		super( AddAction, self ).__init__( "Add", *args, **kwargs )
		self["class"] = "icon add"

	@staticmethod
	def isSuitableFor( modul, actionName ):
		return( (modul == "hierarchy" or modul.startswith("hierarchy.")) and actionName=="add")

	def onClick(self, sender=None):
		print("ADD ACTION HIERARCHY", self.parent().parent().rootNode)
		pane = Pane("Add", closeable=True, iconClasses=["modul_%s" % self.parent().parent().modul, "apptype_hierarchy", "action_add" ])
		conf["mainWindow"].stackPane( pane )
		edwg = EditWidget( self.parent().parent().modul, EditWidget.appHierarchy, node=self.parent().parent().rootNode )
		pane.addWidget( edwg )
		pane.focus()

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert( 1, AddAction.isSuitableFor, AddAction )


class EditAction( html5.ext.Button ):
	"""
		Edits a node in a hierarchy application.
	"""
	def __init__(self, *args, **kwargs):
		super( EditAction, self ).__init__( "Edit", *args, **kwargs )
		self["class"] = "icon edit"

	def onAttach(self):
		super(EditAction,self).onAttach()
		self.parent().parent().selectionChangedEvent.register( self )

	def onDetach(self):
		self.parent().parent().selectionChangedEvent.unregister( self )
		super(EditAction,self).onDetach()

	def onSelectionChanged(self, table, selection ):
		return
		if len(selection)>0:
			self.setEnabled(True)
		else:
			self.setEnabled(False)


	@staticmethod
	def isSuitableFor( modul, actionName ):
		return( (modul == "hierarchy" or modul.startswith("hierarchy.")) and actionName=="edit")

	def onClick(self, sender=None):
		selection = self.parent().parent().getCurrentSelection()
		if not selection:
			return
		for s in selection:
			pane = Pane("Edit", closeable=True)
			conf["mainWindow"].stackPane( pane )
			edwg = EditWidget( self.parent().parent().modul, EditWidget.appHierarchy, key=s["id"])
			pane.addWidget( edwg )
			pane.focus()

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert( 1, EditAction.isSuitableFor, EditAction )


class DeleteAction( html5.ext.Button ):
	"""
		Deletes a node from a hierarchy application.
	"""
	def __init__(self, *args, **kwargs):
		super( DeleteAction, self ).__init__( "Delete", *args, **kwargs )
		self["class"] = "icon delete"


	def onAttach(self):
		super(DeleteAction,self).onAttach()
		self.parent().parent().selectionChangedEvent.register( self )

	def onDetach(self):
		self.parent().parent().selectionChangedEvent.unregister( self )
		super(DeleteAction,self).onDetach()

	def onSelectionChanged(self, table, selection ):
		return #FIXME!
		if len(selection)>0:
			self.setEnabled(True)
		else:
			self.setEnabled(False)


	@staticmethod
	def isSuitableFor( modul, actionName ):
		return( (modul == "hierarchy" or modul.startswith("hierarchy.")) and actionName=="delete")

	def onClick(self, sender=None):
		selection = self.parent().parent().getCurrentSelection()
		if not selection:
			return
		print( "Deleting "+str([x["id"] for x in selection]))
		d = html5.ext.YesNoDialog("Delete %s Entries?" % len(selection), title="Delete them?", yesCallback=self.doDelete)
		d.deleteList = [x["id"] for x in selection]
		return
		for s in selection:
			pane = Pane("Edit", closeable=True)
			conf["mainWindow"].stackPane( pane )
			edwg = EditWidget( self.parent.modul, EditWidget.appList, key=s["id"])
			pane.addWidget( edwg )
			pane.focus()

	def doDelete(self, dialog):
		deleteList = dialog.deleteList
		for x in deleteList:
			NetworkService.request( self.parent().parent().modul, "delete", {"id": x}, secure=True, modifies=True )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert( 1, DeleteAction.isSuitableFor, DeleteAction )
