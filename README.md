# HTAGravity

<p align="center">
  <img src="docs/assets/logo.png" width="300" alt="htagravity logo">
</p>

Here is a full rewrite of htag, using only antigravity and prompts.

It feels very good. It's not a replacement, it's just a POC.

It's completly crazy, but it works (for the basics, on linux only, and with "chrome app mode" only).

[DOC](https://manatlan.github.io/HTAGravity/)

## Get Started

Check the [Official Documentation](https://manatlan.github.io/HTAGravity/) for more information.

## Antigravity resumes :

HTAGravity is a Python library for building web applications using HTML, CSS, and JavaScript. It is a fork of the HTAG library, designed to be a more complete and feature-rich alternative.

### Key Resiliency Features Added
*   **F5/Reload Robustness**: Refreshing the browser no longer kills the Python backend; the session reconstructs cleanly.
*   **HTTP Fallback (SSE + POST)**: If WebSockets are blocked (e.g. strict proxies) or fail to connect, the client seamlessly falls back to HTTP POST for events and Server-Sent Events (SSE) for receiving UI updates.

### New API Features
*   **`.root`, `.parent`, and `.childs` properties**: Every `GTag` exposes its position in the component tree. `.root` references the main `Tag.App` instance, `.parent` references the direct parent component, and `.childs` is a list of its children. This allows components to easily navigate the DOM tree and trigger app-level actions.