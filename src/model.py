# model.py
#
# Copyright 2024 medeo
#
# self program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# self program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with self program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

# references for self code:
# https://pygobject.gnome.org/tutorials/gobject/interfaces.html#example
# https://pygobject.gnome.org/tutorials/gobject/subclassing.html#properties
# https://pygobject.gnome.org/guide/api/properties.html
# https://python-gtk-3-tutorial.readthedocs.io/en/latest/objects.html#GObject.GObject.__gproperties__

from gi.repository import Gio, GObject


class WastepyperSentinel(GObject.GObject):
    __gtype_name__ = 'WastepyperSentinel'

    def __init__(self):
        super().__init__()


class WastepyperSentinelListModel(GObject.GObject, Gio.ListModel):
    __gtype_name__ = 'WastepyperSentinelListModel'

    __gproperties__ = {
        "has-sentinel": (bool,
                         '',
                         '',
                         True,
                         GObject.ParamFlags.READWRITE),
        "model": (Gio.ListModel,
                  '',
                  '',
                  GObject.ParamFlags.READWRITE),
    }

    def __init__(self, model=None):
        super().__init__()

        self._model = model
        self._has_sentinel = True
        self._sentinel = WastepyperSentinel()

    def do_get_item_type(self):
        return GObject.Object.__gtype__

    def do_get_n_items(self):
        n_items = self._model.props.n_items if hasattr(self, "_model") else 0
        return n_items + 1 if hasattr(self, "_has_sentinel") else n_items

    def do_get_item(self, index):
        n_items = self.do_get_n_items()

        if (index >= n_items):
            return None

        if index == n_items - 1:
            return self._sentinel
        else:
            if hasattr(self, "_model"):
                return self._model.get_item(index)
            else:
                return None

    @property
    def has_sentinel(self):
        return self._has_sentinel

    @has_sentinel.setter
    def has_sentinel(self, v):
        if self._has_sentinel == v:
            return

        self._has_sentinel = v

        if (self._has_sentinel):
            self.items_changed(postition=self.do_get_n_items(), removed=0, added=1)
        else:
            self.items_changed(position=self.do_get_n_items(), removed=1, added=0)

        self.notify('has-sentinel')

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, v):
        if self._model == v:
            return

        nAdded = 0
        nRemoved = 0

        if (self._model):
            nRemoved = self._model.get_n_items()
            self._model.disconnect(self._itemsChangedId)
            del self._itemsChangedId

        self._model = v

        if (self._model):
            nAdded = self._model.get_n_items()
            self._itemsChangeId = self._model.connect('items-changed',
            lambda _, position, removed, added: 
                self.items_changed(position, removed, added))

        self.notify('model')
        self.items_changed(position=0, removed=nRemoved, added=nAdded)

