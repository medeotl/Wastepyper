# newTaskRow.py
#
# Copyright 2024 medeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import GObject
from gi.repository import Gtk

from .task import WastepyperTask


@Gtk.Template(resource_path="/com/github/medeotl/Wastepyper/newTaskRow.ui")
class WastepyperNewTaskRow(Adw.PreferencesRow):
    __gtype_name__ = "WastepyperNewTaskRow"

    __gsignals__ = {
        "task-created": (
            GObject.SignalFlags.RUN_FIRST,  # flag
            None,  # return type
            (WastepyperTask,)  # arguments
        )
    }

    _titleEntry = Gtk.Template.Child(name="titleEntry")

    @Gtk.Template.Callback()
    def _onEntryActivatedCb(self, *args):
        title = self._titleEntry.props.text.strip()
        if len(title) > 0:
            self.emit('task-created', WastepyperTask(title=title))
            self._titleEntry.props.text = ''

