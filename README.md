Restricted Python Virtual Machine
====
Restricted Python Virtual Machine (R-PVM) implemented by pure python.

specification
----
* aim for complete safe sandbox
* designed for Python3.6 bytecode
* execute one by one
* good for smart contract of crypto currency
* **No warranty and unstable**

check
----
* cannot use MAKE_FUNCTION op (lambda, comprehension and inner fnc)
* cannot use async/await
* limit to execute function
* YOU must select safe function

Install
----
`pip3 install rpvm`

How to use
----
```python
from rpvm.vm import VirtualMachine
from RestrictedPython import safe_builtins, safe_globals
 
source = """
a = 1
b = 2
c = a + b
"""
code = compile(source, '<example>', 'exec')
 
b = safe_builtins.copy()
l = dict()
g = safe_globals.copy()
vm = VirtualMachine(code, b, l, g)
 
steps = 0
max_steps = 500
while not vm.finish and steps < max_steps:
    vm.exec()
    steps += 1
print("complete?", vm.finish)
print("result", vm.return_value)
print("c is", l['c'])
```

test
----
```bash
python3 -m pytest tests
```

Author
----
[@namuyan_mine](https://twitter.com/namuyan_mine)
