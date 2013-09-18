import sublime
import sublime_plugin
import codecs


#
# when api ready called by st3, called manually when using st2
#
def plugin_loaded():
    global ts_settings_filename, ts_settings
    ts_settings = sublime.load_settings(ts_settings_filename)


#
# find any trailing space regions
#
def find_trailing_spaces(view):
    sel = view.sel()[0]
    line = view.line(sel.b)
    regexp = "[ \t]+" + "$"
    offending_lines = view.find_all(regexp)

    return offending_lines


#
# delete the trailing spaces
#
def delete_trailing_regions(view, edit):

    regions = find_trailing_spaces(view)

    if regions:

        regions.reverse()

        for r in regions:
            view.erase(edit, r)

        return len(regions)

    else:

        return 0


#
# DeleteTrailingSpacesCommand command definition
#
class DeleteTrailingSpacesCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        deleted = delete_trailing_regions(self.view, edit)

        if deleted:

            msg_parts = {"nbRegions": deleted,
                         "plural":    's' if deleted > 1 else ''}
            message = "Deleted %(nbRegions)s trailing spaces region%(plural)s" % msg_parts

        else:

            message = "No trailing spaces to delete!"

        sublime.status_message(message)


#
# st3 utalizes a plugin_loaded hook which must be called manually in ST2
#
if not int(sublime.version()) > 3000:

    plugin_loaded()
