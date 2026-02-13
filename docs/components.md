# Components

Components are the building blocks of an `htag` application. Every visual element is a `GTag` or a subclass of it.

## GTag

`GTag` is the core class. It handles HTML rendering, state management, and lifecycle.

### Creating a Component

You can create a custom component by subclassing `GTag`:

```python
from htag import GTag

class MyComponent(GTag):
    def __init__(self, name):
        super().__init__()
        self.tag = "div"  # Optional: default is "div"
        self._class = "my-class"
        self.add(f"Hello {name}!")
```

### Attributes and Style

Attributes are managed using properties starting with an underscore:

```python
btn = Tag.button("Click", _class="primary", _id="main-btn", _style="color: blue")
btn._class = "secondary"  # Updates are reactive
```

### Tree Manipulation

- `self.add(*content)`: Adds children (strings or other GTags).
- `self.remove(child)`: Removes a child.
- `self.clear()`: Removes all children.
- `self.remove_self()`: Removes the component from its parent.

## The Tag Creator

The `Tag` singleton allows you to create standard HTML elements dynamically using a clean syntax:

```python
from htag import Tag

# Equivalent to <div class="foo">content</div>
d = Tag.div("content", _class="foo")

# Equivalent to <br/> (Void Element)
b = Tag.br()

# Equivalent to <input type="text" value="hello"/>
i = Tag.input(_type="text", _value="hello")
```

### Void Elements

`htag` automatically handles HTML void elements (self-closing tags) like `input`, `img`, `br`, `hr`, etc. You don't need to specify a closing tag for these.

---

[← Home](index.md) | [Next: Events →](events.md)
