from rpvm.vm import VirtualMachine
from RestrictedPython import safe_builtins


def source_execute(source, add_buildins=None, max_steps=5000):
    """compile source, execute by VM, eval and compare result"""
    # compile
    code = compile(source=source, filename='<example>', mode='exec')
    # vm
    b = safe_builtins.copy()
    if add_buildins:
        b.update(add_buildins)
    l1 = dict()
    g1 = dict()
    vm = VirtualMachine(code, b, l1, g1)
    steps = 0
    while not vm.finish and steps < max_steps:
        vm.exec()
        steps += 1
    # eval
    l2 = dict()
    g2 = {'__builtins__': b}
    r = eval(code, g2, l2)
    del g2['__builtins__']
    # check
    assert l1 == l2, "{} X {}".format(l1, l2)
    assert g1 == g2, "{} X {}".format(g1, g2)
    assert vm.return_value == r, "{} X {}".format(vm.return_value, r)
    # assert l1 == {}, l1


__all__ = [
    "source_execute",
]
