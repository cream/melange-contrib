import os.path
import gtk

from cream.util import get_source_file

class AddWidgetDialog(gtk.Dialog):

    def __new__(cls):

        interface = gtk.Builder()
        interface.add_from_file(os.path.join(os.path.dirname(get_source_file(cls)), 'interface.glade'))

        treeview = interface.get_object('treeview')
        liststore = interface.get_object('liststore')
        scrolled = interface.get_object('scrolled')

        d = interface.get_object('dialog')

        d.treeview = treeview
        d.liststore = liststore

        return d
