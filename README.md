# python-invariant
A simple library for ensuring arguments to functions are constant. For example,
to ensure that the argument to a function named printf is Invariant, you would
include the following lines in the function:

```
def printf(pattern, *args, **kwargs):
    Invariant.ensure(pattern)
```


