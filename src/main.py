# main.py
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

import sys
import gi

gi.require_version('Adw', '1')

from gi.repository import Gio, Adw
from .window import WastepyperWindow


class WastepyperApplication(Adw.Application):
    __gtype_name__ = 'WastepyperApplication'

    def __init__(self):
        super().__init__(application_id='com.github.medeotl.Wastepyper',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('about', self.on_about_action)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        # self.create_action('preferences', self.on_preferences_action)

    def on_about_action(self, *args):
        aboutWindow = Adw.AboutWindow(transient_for=self.props.active_window,
                                      application_name='Wastepyper',
                                      application_icon='com.github.medeotl.Wastepyper',
                                      developer_name='medeo',
                                      version='0.1.0',
                                      developers=['medeo'],
                                      copyright='© 2024 medeo')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        aboutWindow.set_translator_credits(_('translator-credits'))
        aboutWindow.present()
        
    def do_activate(self):
        window = WastepyperWindow(application=self)
        window.present()

    # disabilitato per ora
    # def on_preferences_action(self, widget, _):
    #     print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    application = WastepyperApplication()
    return application.run(sys.argv)
