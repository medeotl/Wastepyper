# window.py
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

from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Adw

from .model import WastepyperSentinelListModel
from .newTaskRow import WastepyperNewTaskRow
from .task import WastepyperTask
from .taskRow import WastepyperTaskRow


@Gtk.Template(resource_path='/com/github/medeotl/Wastepyper/window.ui')
class WastepyperWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WastepyperWindow'

    _listbox = Gtk.Template.Child(name="listbox")
    _listNameRow = Gtk.Template.Child(name="listNameRow")
    _listPage = Gtk.Template.Child(name="listPage")
    _navigationView = Gtk.Template.Child(name="navigationView")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # action per creare una nuova lista (attivata dal pulsante apposito)
        self._createListAction = Gio.SimpleAction.new(name="create-list")
        self._createListAction.connect("activate", self._createList)
        self.add_action(self._createListAction)
        self._validateListName()

        self._tasksModel = Gio.ListStore(item_type=WastepyperTask)

        self._model = WastepyperSentinelListModel(model=self._tasksModel)
        self._listbox.bind_model(self._model, lambda item: self._createRow(item))

    @Gtk.Template.Callback()
    def _validateListName(self, *args):
        text = self._listNameRow.props.text.strip()
        self._createListAction.props.enabled = len(text) > 0

    @Gtk.Template.Callback()
    def _activateListNameRow(self, *args):
        self._createListAction.activate()

    def _createList(self, *args):
        text = self._listNameRow.props.text.strip()

        assert text and len(text) > 0, "nome lista vuoto"

        self.props.title = _("Wastepyper - %s").format(text)

        self._listPage.props.title = text
        self._navigationView.push(self._listPage)

    def _createRow(self, item):
        row = None

        if isinstance(item, WastepyperTask):
            row = WastepyperTaskRow(task=item)
        else:
            row = WastepyperNewTaskRow()
            row.connect(
                "task-created", lambda _, task: self._tasksModel.append(task)
            )

        assert row is not None

        return row

    def _on_entry_activate(self, row):
        # python non gestisce le lambda multilinea
        title = row.props.text.strip()
        if len(title) > 0:
            self._addTask(title)
            row.props.text = ""

    def _addTask(self, title):
        assert title is not None and len(title) > 0
        self._tasksModel.append(WastepyperTask(title=title))

