# -*- coding: utf-8 -*-
# Written by Loïc Fontaine (ljph.fontaine@gmail.com / lfont.blog.jit.su)
# Largely inspired by the work of Eric Martel (emartel@gmail.com / www.ericmartel.com)

# available commands
#   google_translate_selection
#   google_translate_from_input

import sublime
import sublime_plugin

import webbrowser

import urllib


def get_target_language():
    settings = sublime.load_settings(__name__ + '.sublime-settings')
    return settings.get('target_language')


def translate(text, target_language):
    text = text.encode('utf-8')
    text = urllib.quote(text)
    url = 'http://translate.google.com/#auto/{0}/{1}'.format(target_language,
                                                             text)
    webbrowser.open_new_tab(url)


class GoogleTranslateSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        target_language = get_target_language()

        for selection in self.view.sel():
            # if the user didn't select anything, search the currently
            # highlighted word
            if selection.empty():
                text = self.view.word(selection)
            else:
                text = self.view.substr(selection)

            translate(text, target_language)


class GoogleTranslateFromInputCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Get the search item
        self.window.show_input_panel('Google Translate', '',
            self.on_done, self.on_change, self.on_cancel)

    def on_done(self, input):
        target_language = get_target_language()
        translate(input, target_language)

    def on_change(self, input):
        pass

    def on_cancel(self):
        pass
