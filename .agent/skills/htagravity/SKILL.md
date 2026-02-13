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

### 2. The Application (`App`)
The root of your interface must be an `App` class (which inherits from `Tag.body`).
- Pass the **class** itself to runners to support multi-session isolation.

### 3. State & Reactivity
htagravity uses a "dirty-marking" system for UI updates.
- **Attributes**: Properties starting with `_` are automatically mapped to HTML attributes and trigger a re-render when changed (e.g., `self._class = "active"`).
- **Events**: Properties starting with `on` are mapped to Python callbacks.

## Best Practices

### Layout & Styling
- Define CSS/JS dependencies in the `statics` class attribute.
- Use modern, curated color palettes and typography.
- Prefer `Tag.style` and `Tag.link` for including assets.

```python
class App(Tag.App):
    statics = [
        Tag.style("""
            body { font-family: 'Inter', sans-serif; background: #f0f2f5; }
            .card { padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        """)
    ]
```

### Event Control
Use decorators to control event behavior:
- `@prevent`: Calls `event.preventDefault()` on the client side.
- `@stop`: Calls `event.stopPropagation()` on the client side.

### Forms & Inputs
- Use the `Input` component for form fields.
- htagravity automatically binds the `value` attribute to the Python object for inputs.

## Multi-Session Deployment
To ensure each user has their own isolated session/state:
- **ALWAYS** pass the `App` class to the runner, NOT an instance.

```python
if __name__ == "__main__":
    from htag import WebApp
    WebApp(App).run() # Correct: unique instance per user
```

## Runner Choice
- **`WebApp`**: For shared web access (browsers). Supports multiple users if passed a Class.
- **`ChromeApp`**: For desktop-like "Kiosk" mode. Auto-manages temporary browser profiles.
