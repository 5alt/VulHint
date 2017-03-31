# author: md5_salt
import sublime
import sublime_plugin

import re

g_regions = []
g_region_lines = []
g_jump_index = 0

g_line_regions = {}

class VulHint(sublime_plugin.EventListener):
    lang = None
    data = {}

    def on_load_async(self, view):
        if not sublime.load_settings("plugin.sublime-settings").get("enable", 1):
            return
        self.init(view)
        self.mark_vul(view)
        get_lines(view)

    def on_post_save_async(self, view):
        if not sublime.load_settings("plugin.sublime-settings").get("enable", 1):
            return
        global g_regions
        self.init(view)
        self.mark_vul(view)
        get_lines(view)

    def on_hover(self, view, point, hover_zone):
        if not sublime.load_settings("plugin.sublime-settings").get("enable", 1):
            return
        global g_regions
        global g_region_lines
        global g_jump_index

        global g_line_regions

        if not self.lang or not self.data:
            return
        #self.init(view)
        # locate smiles in the string. smiles string should be at the beginning and followed by tab (cxsmiles)
        # hovered_line_text = view.substr(view.word(point)).strip()
        #hovered_line_text = view.substr(view.line(point)).strip()
        if (hover_zone == sublime.HOVER_TEXT):
            word = view.substr(view.word(point)).strip()
            for key in g_regions:
                val =  self.data[key]
                if word in val["keyword"]:
                    hovered_text = '<p>%s</p>'%(val["discription"])
                    view.show_popup(hovered_text, 
                             flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, 
                             location=point)
                    g_jump_index = g_region_lines.index(view.rowcol(point)[0])
                    return
            line = view.rowcol(point)[0]
            if g_line_regions.get(line):
                hovered_text = ''
                for key in g_line_regions.get(line):
                    val =  self.data[key]
                    hovered_text += '<p>%s</p><br>'%(val["discription"])
                view.show_popup(hovered_text, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=point)
                g_jump_index = g_region_lines.index(view.rowcol(point)[0])

        return

    def init(self, view):
        global g_regions
        clear_mark(view)
        g_regions = []
        self.lang = self.guess_lang(view)
        self.data = sublime.load_settings("VulData.sublime-settings").get(self.lang, {})

    def mark_vul(self, view):
        global g_regions
        #print([self.data[i]["discription"] for i in self.data])
        if not self.lang or not self.data:
            return
        for key,val in self.data.items():
            if not val['enable']: continue
            vul = view.find_all(val['pattern'])
            if not vul: continue
            for i in vul:
                i.a += val["abais"]
                i.b += val["bbais"]
            view.add_regions(key, vul, "string", "cross", sublime.DRAW_OUTLINED|sublime.DRAW_STIPPLED_UNDERLINE)
            g_regions.append(key)


    def guess_lang(self, view=None, path=None, sublime_scope=None):
        if not view:
            return None
        filename = view.file_name()
        return filename.split('.')[-1].lower()


def clear_mark(view):
    global g_regions
    if not g_regions: return
    for i in g_regions:
        view.erase_regions(i)

def get_lines(view):
    global g_regions
    global g_region_lines
    global g_line_regions

    g_line_regions = {}
    g_region_lines = set()
    for region in g_regions:
        for i in view.get_regions(region):
            line = view.rowcol(i.a)[0]
            g_region_lines.add(line)
            if g_line_regions.get(line, None):
                g_line_regions[view.rowcol(i.a)[0]].add(region)
            else:
                g_line_regions[view.rowcol(i.a)[0]] = set([region])
    g_region_lines = sorted(g_region_lines)



class GotoNextCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global g_jump_index, g_region_lines
        # Convert from 1 based to a 0 based line number
        line = g_region_lines[g_jump_index]
        g_jump_index = (g_jump_index + 1)%len(g_region_lines)

        # Negative line numbers count from the end of the buffer
        if line < 0:
            lines, _ = self.view.rowcol(self.view.size())
            line = lines + line + 1

        pt = self.view.text_point(line, 0)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))

        self.view.show(pt)

class EnableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
         sublime.load_settings("plugin.sublime-settings").set("enable", 1)
         sublime.save_settings("plugin.sublime-settings")

class DisableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
         sublime.load_settings("plugin.sublime-settings").set("enable", 0)
         sublime.save_settings("plugin.sublime-settings")

class ClearCommand(sublime_plugin.TextCommand):
    def run(self, edit):
         clear_mark(self.view)