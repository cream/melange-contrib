#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

# note: this is just a workaround until manifests are extended

from os.path import join, dirname

categories = {
    'org.cream.melange.CategoryInternet': {
        'name': 'Internet',
        'icon': join(dirname(__file__), 'images/internet.png'),
        'description': 'Interact with the web!'
    },
    'org.cream.melange.CategoryMultimedia': {
        'name': 'Multimedia',
        'icon': join(dirname(__file__), 'images/multimedia.png'),
        'description': 'Adds multimedia features to your desktop'
    },
    'org.cream.melange.CategoryTools': {
        'name': 'Tools',
        'icon': join(dirname(__file__), 'images/tools.png'),
        'description': 'Helping you to make your life easier'
    },
    'org.cream.melange.CategoryGames': {
        'name': 'Games',
        'icon': join(dirname(__file__), 'images/melange.png'),
        'description': 'Gaming for in between? Here you go!'
    },
    'org.cream.melange.CategoryMiscellaneous': {
        'name': 'Miscellaneous',
        'icon': join(dirname(__file__), 'images/melange.png'),
        'description': 'Various widgets i can\'t classify '
    }

}
