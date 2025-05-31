# Embedded Examples

This uses code fences to embed marimo components as marimo islands.

```python {marimo}
import marimo as mo

name = mo.ui.text(placeholder="Enter your name")
name
```

```python {marimo}
mo.md(f"Hello, **{name.value or '__'}**!")
```

## Embedding the marimo playground

For an easy way to embed marimo notebooks or applications, we recommend embedding the marimo playground. This feature uses pymdownx.blocks to embed marimo notebooks in your MkDocs documentation, creating iframes that render the marimo playground.

/// marimo-embed
    height: 400px
    mode: run

```python
@app.cell
def __():
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure(figsize=(8, 4))
    plt.plot(x, y)
    plt.title('Sine Wave')
    plt.xlabel('x')
    plt.ylabel('sin(x)')
    plt.grid(True)
    plt.gca()
    return
```

///
