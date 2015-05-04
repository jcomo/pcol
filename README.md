# pcol
A straightforward color rendering library for python.

## Usage

```python
from pcol import pcol

print pcol.green('Hello', pcol.bold('stdout'), '!')
```

I built this library to have an easy API for coloring output in the
terminal. Therefore, this is the out-of-the-box behavior of the library.

Under the hood, it uses trees to render the output so it can be extended
to render arbitrary values.
