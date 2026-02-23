---
name: htagravity-development
description: Guidelines and best practices for building modern, state-of-the-art web applications using the htagravity framework.
---

# htagravity Developer Skill

Use this skill to design, implement, and refine web applications using the **htagravity** framework.

## Core Architecture

### 1. Components (`GTag`)
Every UI element in htagravity is a component inheriting from `GTag`.
- Use the `Tag` factory for standard HTML elements (e.g., `Tag.div`, `Tag.button`).
- Create custom components by subclassing `GTag` or any `Tag.*` class.

```python
from htag import Tag

class MyComponent(Tag.div):
    def __init__(self, name):
        super().__init__()
        self += Tag.h1(f"Hello {name}")
```

### 2. Composite Components
When creating complex UI components (like a Card or a Window), you should override the `add(self, o)` method so that when users do `my_card += content`, the content goes into the correct inner container, not the root tag.

```python
class Card(Tag.div):
    def __init__(self, title):
        super().__init__(_class="card")
        self += Tag.h2(title)
        self.body = Tag.div(_class="card-body")
        # Use Tag.div.add to bypass the overridden add method during init
        Tag.div.add(self, self.body)

    def add(self, o):
        # Redirect append operations (+-) to the body container
        self.body += o
```

### 3. State & Reactivity
htagravity uses a "dirty-marking" system for UI updates.
- **HTML Attributes**: MUST start with `_` to be rendered as HTML attributes.
  - Correct: `_class="btn"`, `_src="image.png"`, `_type="checkbox"`
  - Incorrect: `class="btn"`, `src="image.png"`
- **Events**: Properties starting with `_on` are mapped to Python callbacks.

### 4. Forms & Inputs
htagravity automatically binds input events to Python.
- For text/number inputs, the current value is accessed safely via event handlers: `val = event.value`
- For checkboxes/toggles, the framework synchronizes the boolean state. Access it safely using `getattr(self.checkbox, "_value", False)`. Do not use `.value` directly on a checkbox component as it will raise an `AttributeError`.

## Best Practices

### Layout & Styling
- Define CSS/JS dependencies in the `statics` class attribute on your main `App` class.
- Use modern, curated color palettes and typography.
- Prefer `Tag.style` and `Tag.script`. Remember to use `_src` for script/image URLs.

```python
class App(Tag.App):
    statics = [
        Tag.script(_src="https://cdn.tailwindcss.com"),
        Tag.style("body { background-color: #f8fafc; }")
    ]
```

### Event Control
Use decorators to control event behavior:
- `@prevent`: Calls `event.preventDefault()` on the client side.
- `@stop`: Calls `event.stopPropagation()` on the client side.

## Runner Choice
- **`ChromeApp`**: Primary choice. Attempts to launch a clean desktop-like Kiosk window via Chromium/Chrome binaries. If none are found, it falls back to opening the default system browser via `webbrowser.open`.
- **`WebApp`**: For shared web access. Opens in the default browser in a new tab.

## Multi-Session Deployment
To ensure each user has their own isolated session/state:
- **ALWAYS** pass the `Tag.App` class to the runner, NOT an instance.

```python
if __name__ == "__main__":
    from htag import ChromeApp
    ChromeApp(MyApp).run() # Correct: unique instance per user
```
