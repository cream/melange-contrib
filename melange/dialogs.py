#!/usr/bin/env python

import gtk
from os.path import join, dirname, abspath


class AddWidgetDialog(object):

    def __init__(self):

        interface = gtk.Builder()
        interface.add_from_file(join(dirname(abspath(__file__)), 'add_dialog.glade'))
        
        self.dialog = interface.get_object('dialog')
        self.dialog.connect('delete_event', lambda *args: self.dialog.hide())
        self.liststore = interface.get_object('liststore')
        self.treeview = interface.get_object('treeview')

    def add(self, widget, path):  
        if 'icon' in widget:
            icon_path = widget['icon']
        else:
            icon_path = join(path, 'melange.png')
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon_path, 35, 35)
        label = '<b>{0}</b>'.format(widget['name']) + '\n'
        label += '  <i>{0}</i>'.format(split_string(widget['description']))
        self.liststore.append((icon, label, widget['name']))


def split_string(description):
    lst = []
    chars = 0
    for word in description.split():
        if chars > 30:
            lst.append('\n  ')
            chars = 0
        lst.append(word + ' ')
        chars += len(word)

    return ''.join(lst)
