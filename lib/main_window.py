import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
import cairo

from .annotations import MarkerAnnotation, TextAnnotation

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, application=app, **kwargs)
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.img_surface = None
        self.annotations = []
        self.init_ui()
        self.mode = 1
        self.clipboard_read()

    def init_ui(self):
        self.set_title('Annotate')
        self.set_size_request(400, 250)
        self.set_position(Gtk.WindowPosition.CENTER)

        box = Gtk.Box(spacing=2, orientation=Gtk.Orientation.VERTICAL)
        button_view = self.create_button_view()
        box.pack_start(button_view, False, False, 0)
        self.entry = self.create_entry()
        box.pack_start(self.entry, False, False, 0)
        self.draw_area = self.create_drawarea()
        box.pack_start(self.draw_area, True, True, 0)
        self.add(box)

        self.connect('delete-event', Gtk.main_quit)
        self.show_all()


    def create_entry(self):
        entry = Gtk.Entry()
        entry.connect('changed', self.on_text_change)
        return entry

    def create_drawarea(self):
        draw_area = Gtk.DrawingArea()
        draw_area.set_size_request(200, 300)
        draw_area.connect('draw', self.on_draw)

        draw_area.add_events(Gdk.EventMask.BUTTON_MOTION_MASK
            | Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK)
        draw_area.connect('button-press-event', self.on_area_button_press)
        draw_area.connect('button-release-event', self.on_area_button_release)
        draw_area.connect('motion-notify-event', self.on_area_motion_notify)

        return draw_area

    def on_area_button_press(self, _widget, event):
        point = (event.x, event.y)
        if self.mode == 3:
            if not self.entry.get_text():
                self.entry.set_text('Text')
            annotation = TextAnnotation(self.entry.get_text(), font_size=18, rgba=(255, 0, 0))
        elif self.mode == 2:
            annotation = MarkerAnnotation(line_width=4, rgba=(255, 0, 0, 0.75))
        else:
            annotation = MarkerAnnotation(line_width=24, rgba=(255, 227, 0, 0.4))
        annotation.on_press(point)
        self.annotations.append(annotation)
        self.update()

    def on_area_button_release(self, _widget, event):
        point = (event.x, event.y)
        self.annotations[-1].on_release(point)
        self.update()

    def on_area_motion_notify(self, _widget, event):
        point = (event.x, event.y)
        self.annotations[-1].on_move(point)
        self.update()

    def on_text_change(self, entry):
        if self.annotations:
            ann = self.annotations[-1]
            if isinstance(ann, TextAnnotation):
                ann.text = entry.get_text()
                self.update()

    def create_button_view(self):
        toolbar = Gtk.Toolbar.new()
        toolbar.expand = True

        button_get = create_tool_button('edit-paste', lambda _: self.clipboard_read())
        toolbar.insert(button_get, 0)

        toolbar.insert(create_tool_separator(), -1)

        def on_toggled(button, n):
            if button.get_active():
                self.select_mode(n)

        def on_icon_draw(_widget, cr, tool):
            cr.set_source_rgba(255, 255, 255)
            cr.rectangle(0, 0, 24, 24)
            cr.fill()
            if tool == 1:
                cr.set_line_width(12)
                cr.set_source_rgba(255, 127, 0, 0.4)
                cr.move_to(2, 12)
                cr.line_to(22, 12)
                cr.stroke()
            elif tool == 2:
                cr.set_line_width(4)
                cr.set_source_rgba(255, 0, 0, 0.75)
                cr.move_to(2, 12)
                cr.line_to(22, 12)
                cr.stroke()
            elif tool == 3:
                cr.set_font_size(22)
                cr.set_source_rgba(255, 0, 0, 0.75)
                cr.move_to(2, 20)
                cr.show_text('A')
                cr.stroke()

        tools = [1, 2, 3]
        previous_radio_button = None

        for tool in tools:
            area = Gtk.DrawingArea()
            area.set_size_request(24, 24)
            area.connect('draw', on_icon_draw, tool)

            button = Gtk.RadioToolButton.new_from_widget(previous_radio_button)
            button.set_icon_widget(area)
            button.connect('toggled', on_toggled, tool)
            toolbar.insert(button, -1)
            previous_radio_button = button

        toolbar.insert(create_tool_separator(), -1)

        button_undo = create_tool_button('edit-undo', self.undo)
        toolbar.insert(button_undo, -1)

        toolbar.insert(create_tool_separator(expand=True), -1)

        button_set = create_tool_button('document-save', lambda _: self.clipboard_write())
        toolbar.insert(button_set, -1)

        return toolbar

    def draw_annotations(self, cr):
        for ann in self.annotations:
            ann.render(cr)

    def clipboard_read(self):
        image = self.clipboard.wait_for_image()
        if image is not None:
            self.img_surface = Gdk.cairo_surface_create_from_pixbuf(image, 0, None)
            self.annotations.clear()
            self.update()

    def clipboard_write(self):
        surface = self.img_surface.create_similar_image(self.img_surface.get_format(),
            self.img_surface.get_width(), self.img_surface.get_height())
        cr = cairo.Context(surface)
        self.draw_on_ctx(cr)
        surface.flush()
        pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, surface.get_width(), surface.get_height())
        self.clipboard.set_image(pixbuf)
        surface.finish()

    def on_draw(self, _widget, cr):
        if self.img_surface:
            self.draw_on_ctx(cr)

    def draw_on_ctx(self, cr):
        cr.set_source_surface(self.img_surface, 0, 0)
        cr.paint()
        self.draw_annotations(cr)

    def select_mode(self, mode):
        if mode == 3:
            self.entry.set_editable(True)
        self.mode = mode

    def undo(self, _widget):
        if len(self.annotations):
            self.annotations.pop()
            self.update()

    def update(self):
        self.draw_area.queue_draw()

def create_tool_button(icon_name, callback):
    image = Gtk.Image()
    image.set_from_icon_name(icon_name, Gtk.IconSize.SMALL_TOOLBAR)
    button = Gtk.ToolButton.new(image)
    button.connect('clicked', callback)
    return button

def create_tool_separator(expand=False):
    label = Gtk.SeparatorToolItem.new()
    label.set_draw(False)
    label.set_size_request(12, 0)
    label.set_expand(expand)
    return label
