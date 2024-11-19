# taskRow.py
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

from gi.repository import Adw, Gtk
from gi.repository import GObject

from .task import WastepyperTask


@Gtk.Template(resource_path="/com/github/medeotl/Wastepyper/taskRow.ui")
class WastepyperTaskRow(Adw.PreferencesRow):
    __gtype_name__ = "WastepyperTaskRow"

    _titleText = Gtk.Template.Child(name="titleText")

    task = GObject.Property(
        type=WastepyperTask,
        flags=GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT_ONLY,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.task.bind_property(
            "title",
            self._titleText,
            "text",
            GObject.BindingFlags.BIDIRECTIONAL |
            GObject.BindingFlags.SYNC_CREATE,
        )

