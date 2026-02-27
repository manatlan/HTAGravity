# -*- coding: utf-8 -*-
from htag import Tag
"""
this code could be a good start for the future "htag.ui" module

it should be KISS and respect shoelace/htag2 components on all best practices.

The current toast is still broken ;-(
"""
class ui_App(Tag.App):
    """
    Base class for UI applications.
    Handles dependencies, the design system, and FOUC prevention.
    """
    statics = [
        # Design System (Shoelace)
        Tag.link(_rel="stylesheet", _href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.19.1/cdn/themes/light.css"),
        Tag.script(_type="module", _src="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.19.1/cdn/shoelace-autoloader.js"),
        # FOUC prevention
        Tag.style(":not(:defined) { visibility: hidden; }"),
        # Global Styles using Design Tokens
        Tag.style("""
            body { 
                background: var(--sl-color-neutral-50); 
                display: flex; justify-content: center; align-items: center; 
                height: 100vh; margin: 0; 
                font-family: var(--sl-font-sans);
            }
        """)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class("sl-theme-light")

class ui_Title(Tag.h1):
    def init(self, text, **kwargs):
        super().init(text, **kwargs)
        self._style = "margin:0; font-size: var(--sl-font-size-large); font-weight: var(--sl-font-weight-bold); color: var(--sl-color-neutral-900);"

class ui_Text(Tag.div):
    def init(self, text, **kwargs):
        super().init(text, **kwargs)
        self._style = "color: var(--sl-color-neutral-600); line-height: var(--sl-line-height-normal);"

class ui_Icon(Tag.sl_icon):
    def init(self, name, **kwargs):
        self._name = name
        super().init(**kwargs)
        self._style = "color: inherit; font-size: inherit;"

class ui_IconButton(Tag.sl_icon_button):
    def init(self, name, **kwargs):
        self._name = name
        super().init(**kwargs)
        self._style = "color: var(--sl-color-neutral-600); font-size: 1.25rem;"

class ui_Badge(Tag.sl_badge):
    def init(self, text, variant="primary", **kwargs):
        self._variant = variant
        super().init(text, **kwargs)

class ui_Button(Tag.sl_button):
    def init(self, text, **kwargs):
        self._variant = kwargs.pop("_variant", "default")
        onclick = kwargs.pop("_onclick", None)
        super().init(text, **kwargs)
        if onclick:
            self._onclick = onclick

class ui_Dialog(Tag.sl_dialog):
    def init(self, title, **kwargs):
        self._label = title
        super().init(**kwargs)
    def show(self):
        self._open = True
    def hide(self):
        self._open = False

class ui_Drawer(Tag.sl_drawer):
    def init(self, title, **kwargs):
        self._label = title
        super().init(**kwargs)
    def show(self):
        self._open = True
    def hide(self):
        self._open = False

class ui_Spinner(Tag.sl_spinner):
    def init(self, **kwargs):
        super().init(**kwargs)

def ui_Toast(caller: Tag, text: str, variant: str = "primary", duration: int = 3000):
    """
    KISS implementation of a Shoelace Toast.
    Toasts are ephemeral and do not belong in the htag state tree.
    """
    import json
    import html
    icon_name = {
        "primary": "info-circle", "success": "check2-circle", "neutral": "gear", 
        "warning": "exclamation-triangle", "danger": "exclamation-octagon"
    }.get(variant, "info-circle")
    
    # Safely pass the text to JS as a JSON string
    safe_text = json.dumps(html.escape(text))
    
    js = f"""
    customElements.whenDefined('sl-alert').then(() => {{
        const alert = Object.assign(document.createElement('sl-alert'), {{
            variant: '{variant}',
            closable: true,
            duration: {duration},
            innerHTML: `<sl-icon name="{icon_name}" slot="icon"></sl-icon> ` + {safe_text}
        }});
        document.body.append(alert);
        setTimeout(() => alert.toast(), 10);
    }});
    """
    caller.call_js(js)

class ui_SplitPanel(Tag.sl_split_panel):
    def init(self, **kwargs):
        super().init(**kwargs)
        # Create persistent slots as children
        self.start = Tag.div(_slot="start", _style="display: flex; align-items: center; justify-content: center; height: 100%; width: 100%;")
        self.end = Tag.div(_slot="end", _style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; gap: 1rem;")
        with self:
            self.start
            self.end

class ui_Card(Tag.sl_card):
    def init(self, title=None, footer=None, **kwargs):
        super().init(**kwargs)
        self._style = "width: 100%; max-width: 400px;"
        if title:
            with self:
                with Tag.div(_slot="header", _style="display: flex; align-items: center; justify-content: space-between;"):
                    ui_Title(title)
                    self.header_actions = Tag.div(_style="display: flex; gap: var(--sl-spacing-x-small);")
                    
        if footer:
            with self:
                Tag.div(footer, _slot="footer")

class MyApp(ui_App):
    def init(self):
        self.count = 0
        
        # Overlays
        self.dialog = ui_Dialog("Settings")
        with self.dialog:
            ui_Text("Settings panel content.")
            ui_Button("Close", _onclick=lambda e: self.dialog.hide())

        self.drawer = ui_Drawer("System Info")
        with self.drawer:
            ui_Text("Drawer content.")

        # Root Layout: Split Panel
        with ui_SplitPanel(_style="width: 800px; height: 500px; border: solid 1px var(--sl-color-neutral-200);") as sp:
            # Left Side (Start Slot)
            with sp.start:
                with ui_Card(title="Core Controls") as self.card:
                    with self.card.header_actions:
                        ui_IconButton("gear", _onclick=lambda e: self.dialog.show())
                    
                    ui_Text("Status Dashboard")
                    with Tag.div(_style="margin-top: 1rem; display: flex; align-items: center; gap: 0.5rem;"):
                        self.badge = ui_Badge("Standby", variant="neutral")
                    
                    with Tag.div(_slot="footer", _style="display: flex; gap: 0.5rem;"):
                        ui_Button("Increment", _variant="primary", _onclick=self.inc)
                        ui_Button("Info", _onclick=lambda e: self.drawer.show())

            # Right Side (End Slot)
            with sp.end:
                ui_Spinner(_style="font-size: 3rem;")
                ui_Text("System Processing...")
                ui_Button("Notify User", _variant="success", _onclick=self.notify)

    def inc(self, event):
        self.count += 1
        self.badge.text = f"Activity: {self.count}"
        self.badge._variant = "primary" if self.count < 5 else "success"

    def notify(self, event):
        ui_Toast(self, f"Broadcast: New event recorded ({self.count})", variant="success")

if __name__ == "__main__":
    from htag import ChromeApp
    ChromeApp(MyApp).run(reload=True)
