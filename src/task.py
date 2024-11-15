# task.py
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

from gi.repository import GObject

class WastepyperTask(GObject.GObject):
    __gtype_name__ = 'WastepyperTask'
    
    __gproperties__ = {
        "title": (str,
                  '',
                  '',
                  '',
                  GObject.ParamFlags.READWRITE),
    }
    
    def __init__(self, title=""):
        super().__init__()
        self.title = title

