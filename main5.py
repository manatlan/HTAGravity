import logging
from htag import Tag, ChromeApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tailwind-demo")

# ====================================================================
# COMPS : Reusable UI Components based on Tailwind CSS
# ====================================================================

class Button(Tag.button):
    """A reusable button component with Tailwind styling."""
    def __init__(self, label, variant="primary", **kwargs):
        super().__init__(label, **kwargs)
        
        # Base styles for all buttons
        base_classes = "px-4 py-2 rounded-lg font-medium transition-colors duration-200 shadow-sm"
        
        # Variant-specific styles
        if variant == "primary":
            self._class = f"{base_classes} bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800"
        elif variant == "secondary":
            self._class = f"{base_classes} bg-slate-200 text-slate-800 hover:bg-slate-300 active:bg-slate-400"
        elif variant == "danger":
            self._class = f"{base_classes} bg-red-600 text-white hover:bg-red-700 active:bg-red-800"
        else:
            self._class = base_classes
            
        # Allow overriding/adding classes via kwargs if needed
        if "_class" in kwargs:
            self._class += f" {kwargs['_class']}"

class Card(Tag.div):
    """A reusable card container component."""
    def __init__(self, title=None, **kwargs):
        super().__init__(**kwargs)
        self._class = "bg-white rounded-xl shadow-md border border-slate-100 overflow-hidden"
        if "_class" in kwargs:
             self._class += f" {kwargs['_class']}"
             
        # Add a header if a title is provided
        if title:
            header = Tag.div(title, _class="px-6 py-4 border-b border-slate-100 font-semibold text-lg text-slate-800 bg-slate-50")
            Tag.div.add(self, header)
            
        # The content area where children will be added
        self.body = Tag.div(_class="p-6")
        Tag.div.add(self, self.body)

    # Override the default append behavior to add to the card body instead of the main wrapper
    def add(self, o):
         self.body += o

class Badge(Tag.span):
    """A small pill badge for status or counts."""
    def __init__(self, text, color="blue", **kwargs):
        super().__init__(text, **kwargs)
        self._class = f"inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-{color}-100 text-{color}-800"

class Alert(Tag.div):
    """An alert banner component."""
    def __init__(self, message, variant="info", **kwargs):
        super().__init__(**kwargs)
        if variant == "info":
            self._class = "p-4 mb-4 text-sm text-blue-800 rounded-lg bg-blue-50 border border-blue-200"
        elif variant == "success":
            self._class = "p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 border border-green-200"
        elif variant == "warning":
            self._class = "p-4 mb-4 text-sm text-yellow-800 rounded-lg bg-yellow-50 border border-yellow-200"
            
        if "_class" in kwargs:
            self._class += f" {kwargs['_class']}"
            
        self += message

class Input(Tag.input):
    """A styled text input component."""
    def __init__(self, placeholder="", **kwargs):
        super().__init__(**kwargs)
        self._type = "text"
        self._placeholder = placeholder
        self._class = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 outline-none transition-colors"
        if "_class" in kwargs:
             self._class += f" {kwargs['_class']}"

class Toggle(Tag.label):
    """A modern toggle switch component."""
    def __init__(self, label_text, **kwargs):
        # Extract the onchange event from kwargs for the inner checkbox if it exists
        onchange = kwargs.pop("_onchange", kwargs.pop("onchange", None))
        
        super().__init__(**kwargs)
        self._class = "relative inline-flex items-center cursor-pointer"
        
        # The hidden checkbox is what stores the state
        # In htagravity, an input automatically updates its `value` attribute on client changes
        self.checkbox = Tag.input(_type="checkbox", _class="sr-only peer")
        if onchange:
             self.checkbox._onchange = onchange
        self += self.checkbox
        
        # The visual toggle
        slider = Tag.div(_class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600")
        self += slider
        
        if label_text:
            self += Tag.span(label_text, _class="ml-3 text-sm font-medium text-gray-900")

    @property
    def value(self):
        # We read the 'checked' state from the underlying input checkbox
        # htag stores synced values in _attrs (accessed via _value)
        return getattr(self.checkbox, "_value", False) == True

class Table(Tag.div):
    """A responsive table component."""
    def __init__(self, headers, rows, **kwargs):
        super().__init__(**kwargs)
        self._class = "relative overflow-x-auto shadow-md sm:rounded-lg"
        if "_class" in kwargs:
             self._class += f" {kwargs['_class']}"
             
        table = Tag.table(_class="w-full text-sm text-left text-gray-500")
        self += table
        
        # Header
        thead = Tag.thead(_class="text-xs text-gray-700 uppercase bg-gray-50")
        tr_head = Tag.tr()
        for h in headers:
            tr_head += Tag.th(h, _class="px-6 py-3", scope="col")
        thead += tr_head
        table += thead
        
        # Body
        tbody = Tag.tbody()
        for i, row in enumerate(rows):
            # Alternating row colors
            bg_class = "bg-white border-b" if i % 2 == 0 else "bg-gray-50 border-b"
            tr = Tag.tr(_class=f"{bg_class} hover:bg-gray-100")
            
            for j, cell in enumerate(row):
                if j == 0:
                     # First column usually highlighted
                     tr += Tag.th(str(cell), _class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap", scope="row")
                else:
                     tr += Tag.td(str(cell), _class="px-6 py-4")
            tbody += tr
        table += tbody

class MessageBox(Tag.div):
    """A modal dialog component."""
    def __init__(self, title, message, on_close=None, type="info", **kwargs):
        super().__init__(**kwargs)
        self.on_close = on_close
        
        # Type styling
        icon_bg = "bg-blue-100 text-blue-600"
        btn_class = "bg-blue-600 hover:bg-blue-700 focus:ring-blue-300"
        icon_svg = '<svg aria-hidden="true" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>'
        
        if type == "danger" or type == "error":
            icon_bg = "bg-red-100 text-red-600"
            btn_class = "bg-red-600 hover:bg-red-800 focus:ring-red-300"
            icon_svg = '<svg aria-hidden="true" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>'
        elif type == "success":
            icon_bg = "bg-green-100 text-green-600"
            btn_class = "bg-green-600 hover:bg-green-800 focus:ring-green-300"
            icon_svg = '<svg aria-hidden="true" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>'
            
        # Modal backdrop (fixed full screen, gray overlay with opacity, flex centering)
        # We start hidden: display: none
        self._class = "fixed inset-0 z-50 flex items-center justify-center overflow-x-hidden overflow-y-auto outline-none focus:outline-none bg-gray-900 bg-opacity-50 transition-opacity"
        self._style = "display: none;"
        
        # Modal Dialog Core
        dialog = Tag.div(_class="relative w-full max-w-md p-4 md:h-auto")
        self += dialog
        
        # Modal Content
        content = Tag.div(_class="relative bg-white rounded-lg shadow-xl")
        dialog += content
        
        # Close 'X' button in top right
        close_btn = Tag.button(_type="button", _onclick=self.close_modal, _class="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center")
        close_btn += Tag.span("✖", _class="w-5 h-5 text-xl leading-none")
        content += close_btn
        
        # Body (Icon + Text)
        body = Tag.div(_class="p-6 text-center")
        icon_container = Tag.div(Tag.HTML(icon_svg), _class=f"mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full {icon_bg}")
        body += icon_container
        body += Tag.h3(title, _class="mb-2 text-lg font-normal text-gray-500")
        body += Tag.p(message, _class="text-sm text-gray-500 mb-6")
        
        # Action Buttons
        ok_btn = Tag.button("OK", _type="button", _onclick=self.close_modal, _class=f"text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center mr-2 {btn_class}")
        body += ok_btn
        
        content += body

    def render_tag(self, tag):
        # We must support Tag.HTML for raw SVG strings
        class HTMLTag(Tag.span):
            def __init__(self, raw_html):
                super().__init__()
                self.raw_html = raw_html
            def __str__(self):
                return self.raw_html
        if not hasattr(Tag, "HTML"):
             Tag.HTML = HTMLTag
        return super().render_tag(tag)
        
    def open_modal(self, event=None):
        self._style = "display: flex;"
        
    def close_modal(self, event=None):
        self._style = "display: none;"
        if self.on_close:
            self.on_close()

# ====================================================================
# APP : Main Application Flow
# ====================================================================

class DemoApp(Tag.App):
    # Using Tailwind Play CDN for prototyping (In production, you'd use a compiled CSS file)
    statics = [
        Tag.script(_src="https://cdn.tailwindcss.com"),
        Tag.style("body { background-color: #f8fafc; }") # Light slate background for the whole page
    ]

    def __init__(self):
        super().__init__()
        self.counter = 0

        # Main Layout Container
        container = Tag.div(_class="min-h-screen p-8 flex flex-col items-center justify-center")
        self += container

        # ... (Title is inside container)
        title_wrapper = Tag.div(_class="text-center mb-10")
        title_wrapper += Tag.h1("Tailwind Components Demo", _class="text-4xl font-extrabold text-slate-900 tracking-tight")
        title_wrapper += Tag.p("htagravity + Tailwind CSS in action", _class="mt-2 text-lg text-slate-600")
        container += title_wrapper

        # Create a Grid for our Cards
        grid = Tag.div(_class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl")
        container += grid

        # --- Card 1: Counter Example ---
        counter_card = Card(title="Counter Example")
        
        self.counter_display = Tag.div(str(self.counter), _class="text-5xl font-bold text-center text-blue-600 mb-6")
        counter_card.add(self.counter_display)
        
        btn_group = Tag.div(_class="flex justify-center gap-4")
        btn_group += Button("-1", variant="secondary", _onclick=self.decrement)
        btn_group += Button("+1", variant="primary", _onclick=self.increment)
        btn_group += Button("Reset", variant="danger", _onclick=self.reset)
        
        counter_card.add(btn_group)
        grid += counter_card

        # --- Card 2: Badges & Static Components ---
        info_card = Card(title="Status Indicators")
        info_card.add(Tag.p("This card demonstrates reusable non-interactive elements.", _class="text-slate-600 mb-4"))
        
        badge_group = Tag.div(_class="flex flex-wrap gap-2 mb-6")
        badge_group += Badge("New", "green")
        badge_group += Badge("Processing", "yellow")
        badge_group += Badge("Error", "red")
        badge_group += Badge("v1.2.0", "blue")
        info_card.add(badge_group)
        
        info_card.add(Button("Acknowledge", variant="primary", _class="w-full", _onclick=lambda e: e.target.call_js("alert('Acknowledged!')")))
        grid += info_card
        
        # --- Card 3: Interactive Forms ---
        form_card = Card(title="Interactive Elements", _class="md:col-span-1 border-t-4 border-t-purple-500") # Span across both columns
        
        form_layout = Tag.div(_class="flex flex-col gap-6")
        
        # Text input example
        input_group = Tag.div(_class="flex flex-col gap-2")
        input_group += Tag.label("Your Name", _class="text-sm font-medium text-gray-700")
        self.name_input = Input(placeholder="Type your name...", _oninput=self.on_type)
        input_group += self.name_input
        self.hello_msg = Tag.div("Hello, stranger!", _class="text-sm text-gray-500 mt-1")
        input_group += self.hello_msg
        form_layout += input_group
        
        # Toggle example
        toggle_group = Tag.div(_class="flex items-center justify-between mt-2 pt-4 border-t border-gray-100")
        self.theme_toggle = Toggle("Enable Dark Text", _onchange=self.on_toggle)
        toggle_group += self.theme_toggle
        form_layout += toggle_group
        
        # Alert area
        self.alert_area = Tag.div(_class="mt-4")
        form_layout += self.alert_area
        
        form_card.add(form_layout)
        grid += form_card

        # --- Card 4: Table Data ---
        table_card = Card(title="Data Table", _class="md:col-span-2")
        headers = ["Nom", "Rôle", "Statut", "Action"]
        rows = [
            ["Alice Dupont", "Admin", Badge("Actif", "green"), Button("Editer", "secondary", _class="text-xs py-1 px-2")],
            ["Bob Martin", "User", Badge("Inactif", "gray"), Button("Editer", "secondary", _class="text-xs py-1 px-2")],
            ["Charlie", "Editor", Badge("Review", "yellow"), Button("Editer", "secondary", _class="text-xs py-1 px-2")]
        ]
        table_card.add(Table(headers, rows))
        grid += table_card
        
        # --- Card 5: Modals / Dialogs ---
        dialog_card = Card(title="Modals & Dialogs", _class="md:col-span-2")
        dialog_group = Tag.div(_class="flex gap-4 p-4 items-center justify-center")
        dialog_group += Button("Show Info Modal", "primary", _onclick=lambda e: self.info_modal.open_modal())
        dialog_group += Button("Show Danger Modal", "danger", _onclick=lambda e: self.danger_modal.open_modal())
        dialog_card.add(dialog_group)
        grid += dialog_card
        
        # Initialize Modals (attached to main container, but hidden)
        self.info_modal = MessageBox("Nouvelle Fonctionnalité", "Les boîtes de dialogue modales sont maintenant disponibles en htag avec Tailwind CSS !", type="info")
        self.danger_modal = MessageBox("Action Irréversible", "Êtes-vous sûr de vouloir supprimer cet élément ? Cette action ne peut pas être annulée.", type="danger")
        container += self.info_modal
        container += self.danger_modal

    # --- Actions (Event Handlers) ---
    def on_type(self, event):
        # We read the value either from event context or directly from the synced input component
        val = event.value
        self.hello_msg.clear()
        if val:
            self.hello_msg += f"Hello, {val}!"
            self.hello_msg._class = "text-sm text-blue-600 font-medium mt-1"
        else:
            self.hello_msg += "Hello, stranger!"
            self.hello_msg._class = "text-sm text-gray-500 mt-1"
            
    def on_toggle(self, event):
        # The htagravity framework doesn't send "checked", it sends "value", so for a checkbox
        # we check the internal value (which we added a property for)
        is_on = self.theme_toggle.value
        self.alert_area.clear() # Clear any existing alert
        
        if is_on:
            self.alert_area += Alert("Feature activated! This would normally switch themes.", variant="success")
        else:
             self.alert_area += Alert("Feature disabled. Back to normal.", variant="warning")

    def increment(self, event):
        self.counter += 1
        self.update_display()

    def decrement(self, event):
        self.counter -= 1
        self.update_display()

    def reset(self, event):
        self.counter = 0
        self.update_display()

    def update_display(self):
        self.counter_display.clear()
        self.counter_display += str(self.counter)
        if self.counter < 0:
            self.counter_display._class = "text-5xl font-bold text-center text-red-600 mb-6"
        elif self.counter > 0:
            self.counter_display._class = "text-5xl font-bold text-center text-green-600 mb-6"
        else:
             self.counter_display._class = "text-5xl font-bold text-center text-blue-600 mb-6"

if __name__ == "__main__":
    ChromeApp(DemoApp, width=1024, height=768).run()
