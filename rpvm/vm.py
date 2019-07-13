from rpvm.opcodes import *
from collections import Iterator
from types import CodeType
from opcode import opname
import io


class VirtualMachine(object):
    """
    designed for Python3.6
    playground: https://grassfedcode.com/pbe
    Lib/dis.py: https://docs.python.org/ja/3/library/dis.html
    CPython: https://github.com/python/cpython/blob/3.6/Python/ceval.c

    build&check:
    >>> import RestrictedPython
    >>> import dis
    >>> source = '''
    ... def f(a, b):
    ...     c = len(a)
    ...     d = list(range(3))
    ...     return a + b
    ... '''
    >>> c = RestrictedPython.compile_restricted(source)
    >>> dis.dis(c.co_consts[0])  # disassemble
    >>> c.co_consts[0].co_code   # bytecode
    """

    def __init__(self, code: CodeType, b: dict, l: dict, g: dict) -> None:
        """
        :param code: code object
        :param b: buildins
        :param l: locals
        :param g: globals
        """
        self.code = code
        self.bytecode = io.BytesIO(code.co_code)
        self.bytecode_index = 0
        self.stack = list()
        self.block_stack = [(0, len(code.co_code))]  # [(start, size),..]
        self.buildins = b
        self.locals = l
        self.globals = g
        self.finish = False
        self.return_value = None

    def close(self) -> None:
        self.bytecode.close()
        self.stack.clear()
        self.block_stack.clear()

    def _read(self, size) -> bytes:
        self.bytecode_index += size
        return self.bytecode.read(size)

    def _seek(self, index, flag) -> None:
        if flag == io.SEEK_SET:
            self.bytecode_index = index
            self.bytecode.seek(index, io.SEEK_SET)
        elif flag == io.SEEK_CUR:
            self.bytecode_index += index
            self.bytecode.seek(index, io.SEEK_CUR)
        else:
            raise VirtualMachineError('not found seek flag')

    def exec(self) -> (int, int):
        # fetch
        bytecode = self._read(2)
        if len(bytecode) == 0:
            raise VirtualMachineError('EOF')
        elif len(bytecode) != 2:
            raise VirtualMachineError('unexpected')
        else:
            code, data = bytecode

        # execute
        if code == NOP:
            pass
        if code == POP_TOP:
            # スタックの先頭 (TOS) の要素を取り除きます。
            self.stack.pop(0)
        elif code == ROT_TWO:
            # スタックの先頭の2つの要素を入れ替えます。
            f, s = self.stack[0:2]
            self.stack[0:2] = s, f
        elif code == ROT_THREE:
            # スタックの2番目と3番目の要素の位置を1つ上げ、先頭を3番目へ下げます。
            f, s, t = self.stack[0:3]
            self.stack[0:3] = s, t, f
        elif code == DUP_TOP:
            # スタックの先頭にある参照の複製を作ります。
            tos = self.stack[0]
            self.stack.insert(0, tos)
        elif code == DUP_TOP_TWO:
            # スタックの先頭の2つの参照を、そのままの順番で複製します。
            two_tos = self.stack[0:2]
            self.stack = two_tos + self.stack

        elif code == UNARY_POSITIVE:
            self.stack[0] = + self.stack[0]
        elif code == UNARY_NEGATIVE:
            self.stack[0] = - self.stack[0]
        elif code == UNARY_NOT:
            self.stack[0] = not self.stack[0]
        elif code == UNARY_INVERT:
            self.stack[0] = ~ self.stack[0]
        elif code == GET_ITER:
            self.stack[0] = iter(self.stack[0])
        elif code == GET_YIELD_FROM_ITER:
            if not isinstance(self.stack[0], Iterator):
                self.stack[0] = iter(self.stack[0])

        elif code == BINARY_POWER:
            f, s = self.stack[0:2]
            self.stack[0] = s ** f
            self.stack.pop(1)
        elif code == BINARY_MULTIPLY:
            f, s = self.stack[0:2]
            self.stack[0] = s * f
            self.stack.pop(1)
        elif code == BINARY_MATRIX_MULTIPLY:
            f, s = self.stack[0:2]
            self.stack[0] = s @ f
            self.stack.pop(1)
        elif code == BINARY_FLOOR_DIVIDE:
            f, s = self.stack[0:2]
            self.stack[0] = s // f
            self.stack.pop(1)
        elif code == BINARY_TRUE_DIVIDE:
            f, s = self.stack[0:2]
            self.stack[0] = s / f
            self.stack.pop(1)
        elif code == BINARY_MODULO:
            f, s = self.stack[0:2]
            self.stack[0] = s % f
            self.stack.pop(1)
        elif code == BINARY_ADD:
            f, s = self.stack[0:2]
            self.stack[0] = s + f
            self.stack.pop(1)
        elif code == BINARY_SUBTRACT:
            f, s = self.stack[0:2]
            self.stack[0] = s - f
            self.stack.pop(1)
        elif code == BINARY_SUBSCR:
            f, s = self.stack[0:2]
            self.stack[0] = s[f]
            self.stack.pop(1)
        elif code == BINARY_LSHIFT:
            f, s = self.stack[0:2]
            self.stack[0] = s << f
            self.stack.pop(1)
        elif code == BINARY_RSHIFT:
            f, s = self.stack[0:2]
            self.stack[0] = s >> f
            self.stack.pop(1)
        elif code == BINARY_AND:
            f, s = self.stack[0:2]
            self.stack[0] = s & f
            self.stack.pop(1)
        elif code == BINARY_XOR:
            f, s = self.stack[0:2]
            self.stack[0] = s ^ f
            self.stack.pop(1)
        elif code == BINARY_OR:
            f, s = self.stack[0:2]
            self.stack[0] = s | f
            self.stack.pop(1)

        elif code == INPLACE_POWER:
            self.stack[1] **= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_MULTIPLY:
            self.stack[1] *= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_MATRIX_MULTIPLY:
            self.stack[1] @= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_FLOOR_DIVIDE:
            self.stack[1] //= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_TRUE_DIVIDE:
            self.stack[1] /= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_MODULO:
            self.stack[1] %= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_ADD:
            self.stack[1] += self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_SUBTRACT:
            self.stack[1] -= self.stack[0]
            self.stack.pop(0)
        elif code == STORE_SUBSCR:
            self.stack[1][self.stack[0]] = self.stack[2]
            self.stack.pop(0)
        elif code == DELETE_SUBSCR:
            del self.stack[1][self.stack[0]]
            self.stack.pop(0)
        elif code == INPLACE_LSHIFT:
            self.stack[1] <<= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_RSHIFT:
            self.stack[1] >>= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_AND:
            self.stack[1] &= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_XOR:
            self.stack[1] ^= self.stack[0]
            self.stack.pop(0)
        elif code == INPLACE_OR:
            self.stack[1] |= self.stack[0]
            self.stack.pop(0)

        elif code == GET_AWAITABLE:
            raise NotImplementedError
        elif code == GET_AITER:
            raise NotImplementedError
        elif code == GET_ANEXT:
            raise NotImplementedError
        elif code == BEFORE_ASYNC_WITH:
            raise NotImplementedError
        elif code == SETUP_ASYNC_WITH:
            raise NotImplementedError

        elif code == FOR_ITER:
            # TOS はイテレータです。 その __next__() メソッドを呼び出します。
            # 要素が尽きた場合は、TOS がポップされ、バイトコードカウンタが delta だけ増やされます。
            assert isinstance(self.stack[0], Iterator)
            try:
                new = self.stack[0].__next__()
                self.stack.insert(0, new)
            except StopIteration:
                self.stack.pop(0)
                self._seek(data, io.SEEK_CUR)
        elif code == SETUP_LOOP:
            # ループのためのブロックをブロックスタックにプッシュします。
            # ブロックは現在の命令から delta バイトの大きさを占めます。
            self.block_stack.insert(0, (self.bytecode_index, data))
        elif code == BREAK_LOOP:
            # break 文によってループを終了します。
            start, size = self.block_stack.pop(0)
            self._seek(start + size, io.SEEK_SET)
        elif code == CONTINUE_LOOP:
            # continue 文によってループを継続します。
            # target はジャンプするアドレスです (アドレスは FOR_ITER 命令でなければなりません)。
            self._seek(data, io.SEEK_SET)

        elif code == SET_ADD:
            raise NotImplementedError
        elif code == LIST_APPEND:
            raise NotImplementedError
        elif code == MAP_ADD:
            raise NotImplementedError

        elif code == RETURN_VALUE:
            self.finish = True
            self.return_value = self.stack[0]
        elif code == YIELD_VALUE:
            raise NotImplementedError
        elif code == YIELD_FROM:
            raise NotImplementedError
        elif code == SETUP_ANNOTATIONS:
            pass  # do nothing

        elif code == SETUP_WITH:
            raise NotImplementedError
        elif code == WITH_CLEANUP_START:
            raise NotImplementedError
        elif code == WITH_CLEANUP_FINISH:
            raise NotImplementedError

        elif code == IMPORT_STAR:
            raise NotImplementedError
        elif code == IMPORT_NAME:
            raise NotImplementedError  # use at initialize
        elif code == IMPORT_FROM:
            raise NotImplementedError  # use at initialize

        elif code == POP_BLOCK:
            self.block_stack.pop(0)
        elif code == SETUP_EXCEPT:
            # try-except 節から try ブロックをブロックスタックにプッシュします。
            self.block_stack.insert(0, (self.bytecode_index, data))
        elif code == SETUP_FINALLY:
            raise NotImplementedError
        elif code == POP_EXCEPT:
            self.block_stack.pop(0)
        elif code == END_FINALLY:
            raise NotImplementedError

        elif code == STORE_NAME:
            name = self.code.co_names[data]
            self.locals[name] = self.stack.pop(0)
        elif code == DELETE_NAME:
            name = self.code.co_names[data]
            del self.locals[name]
        elif code == UNPACK_SEQUENCE:
            tos = self.stack.pop(0)
            for d in tos:
                self.stack.insert(0, d)
        elif code == UNPACK_EX:
            raise NotImplementedError
        elif code == STORE_ATTR:
            assert isinstance(self.stack[0], type), self.stack[0]
            setattr(self.stack[0], self.code.co_names[data], self.stack[1])
        elif code == DELETE_ATTR:
            assert isinstance(self.stack[0], type), self.stack[0]
            delattr(self.stack[0], self.code.co_names[data])
        elif code == STORE_GLOBAL:
            name = self.code.co_names[data]
            self.globals[name] = self.stack.pop(0)
        elif code == DELETE_GLOBAL:
            name = self.code.co_names[data]
            del self.globals[name]

        elif code == LOAD_CONST:
            self.stack.insert(0, self.code.co_consts[data])
        elif code == LOAD_NAME:
            name = self.code.co_names[data]
            if name in self.locals:
                self.stack.insert(0, self.locals[name])
            elif name in self.buildins:
                self.stack.insert(0, self.buildins[name])
            else:
                raise VirtualMachineError('not found `{}`'.format(name))
        elif code == LOAD_ATTR:
            self.stack[0] = getattr(self.stack[0], self.code.co_names[data])
        elif code == LOAD_GLOBAL:
            name = self.code.co_names[data]
            self.stack.insert(0, self.globals[name])
        elif code == LOAD_FAST:
            name = self.code.co_varnames[data]
            self.stack.insert(0, self.locals[name])
        elif code == STORE_FAST:
            name = self.code.co_varnames[data]
            self.locals[name] = self.stack.pop(0)
        elif code == DELETE_FAST:
            name = self.code.co_varnames[data]
            del self.locals[name]

        elif code == BUILD_TUPLE:
            n = reversed(self.stack[0:data])
            self.stack = self.stack[data:]
            self.stack.insert(0, tuple(n))
        elif code == BUILD_LIST:
            n = reversed(self.stack[0:data])
            self.stack = self.stack[data:]
            self.stack.insert(0, list(n))
        elif code == BUILD_SET:
            n = reversed(self.stack[0:data])
            self.stack = self.stack[data:]
            self.stack.insert(0, set(n))
        elif code == BUILD_MAP:
            d = dict()
            for i in range(data):
                d[self.stack[i*2+1]] = self.stack[i*2]
            self.stack = self.stack[data*2:]
            self.stack.insert(0, d)
        elif code == BUILD_CONST_KEY_MAP:
            raise NotImplementedError
        elif code == BUILD_STRING:
            raise NotImplementedError
        elif code == BUILD_TUPLE_UNPACK:
            l = list()
            for n in reversed(self.stack[0:data]):
                l.extend(n)
            self.stack = self.stack[data:]
            self.stack.insert(0, tuple(l))
        elif code == BUILD_LIST_UNPACK:
            l = list()
            for n in reversed(self.stack[0:data]):
                l.extend(n)
            self.stack = self.stack[data:]
            self.stack.insert(0, l)
        elif code == BUILD_MAP_UNPACK:
            d = dict()
            for _ in range(data):
                d.update(self.stack.pop(0))
            self.stack.insert(0, d)
        elif code == BUILD_SET_UNPACK:
            s = set()
            for _ in range(data):
                s.update(self.stack.pop(0))
            self.stack.insert(0, s)
        elif code == BUILD_MAP_UNPACK_WITH_CALL:
            raise NotImplementedError
        elif code == BUILD_TUPLE_UNPACK_WITH_CALL:
            raise NotImplementedError

        elif code == COMPARE_OP:
            right = self.stack.pop(0)
            left = self.stack[0]
            if data == 0:
                self.stack[0] = left < right
            elif data == 1:
                self.stack[0] = left <= right
            elif data == 2:
                self.stack[0] = left == right
            elif data == 3:
                self.stack[0] = left != right
            elif data == 4:
                self.stack[0] = left > right
            elif data == 5:
                self.stack[0] = left >= right
            elif data == 6:
                self.stack[0] = left in right
            elif data == 7:
                self.stack[0] = left not in right
            else:
                raise VirtualMachineError('not found cmp code {}'.format(data))

        elif code == JUMP_FORWARD:
            self._seek(data, io.SEEK_CUR)
        elif code == POP_JUMP_IF_TRUE:
            if self.stack.pop(0):
                self._seek(data, io.SEEK_SET)
        elif code == POP_JUMP_IF_FALSE:
            if not self.stack.pop(0):
                self._seek(data, io.SEEK_SET)
        elif code == JUMP_IF_TRUE_OR_POP:
            if self.stack.pop[0]:
                self._seek(data, io.SEEK_SET)
            else:
                self.stack.pop(0)
        elif code == JUMP_IF_FALSE_OR_POP:
            if not self.stack.pop[0]:
                self._seek(data, io.SEEK_SET)
            else:
                self.stack.pop(0)
        elif code == JUMP_ABSOLUTE:
            self._seek(data, io.SEEK_SET)

        elif code == RAISE_VARARGS:
            if data == 0:
                raise NotImplementedError
            elif data == 1:
                raise self.stack.pop(0)
            elif data == 2:
                tos = self.stack.pop(0)
                raise self.stack.pop(0) from tos
            else:
                raise VirtualMachineError('not found argc {}'.format(data))

        elif code == CALL_FUNCTION:
            args = list()
            for _ in range(data):
                args.append(self.stack.pop(0))
            fnc = self.stack.pop(0)
            self.stack.insert(0, fnc(*args))
        elif code == MAKE_FUNCTION:
            raise NotImplementedError
        elif code == BUILD_SLICE:
            if data == 2:
                tos = self.stack.pop(0)
                self.stack[0] = slice(self.stack[0], tos)
            elif data == 3:
                tos = self.stack.pop(0)
                tos1 = self.stack.pop(0)
                self.stack[0] = slice(self.stack[0], tos1, tos)
            else:
                raise VirtualMachineError('slice argc is 2 or 3 not {}'.format(data))
        elif code == LOAD_CLOSURE:
            raise NotImplementedError
        elif code == LOAD_DEREF:
            raise NotImplementedError
        elif code == STORE_DEREF:
            raise NotImplementedError
        elif code == DELETE_DEREF:
            raise NotImplementedError
        elif code == CALL_FUNCTION_KW:
            kwd_list = self.stack.pop(0)
            kwds = dict()
            for k in kwd_list:
                kwds[k] = self.stack.pop(0)
            args = list()
            for _ in range(data - len(kwd_list)):
                args = self.stack.pop(0)
            fnc = self.stack[0]
            self.stack[0] = fnc(*args, **kwds)
        elif code == CALL_FUNCTION_EX:
            if data & 0x01:
                kwds = self.stack.pop(0)
            else:
                kwds = dict()
            args = self.stack.pop(0)
            fnc = self.stack[0]
            self.stack[0] = fnc(*args, **kwds)
        elif code == LOAD_CLASSDEREF:
            raise NotImplementedError

        elif code == PRINT_EXPR:
            raise NotImplementedError
        elif code == LOAD_BUILD_CLASS:
            raise NotImplementedError
        elif code == HAVE_ARGUMENT:
            raise NotImplementedError
        elif code == EXTENDED_ARG:
            raise NotImplementedError
        elif code == FORMAT_VALUE:
            # Used for implementing formatted literal strings (f-strings)
            raise NotImplementedError
        else:
            raise VirtualMachineError('not found op `{}`'.format(code))
        return code, data


class VirtualMachineError(Exception):
    pass


def compile_and_print(source, max_steps=500):
    from RestrictedPython import safe_builtins, safe_globals
    import dis
    code = compile(source=source, filename='<example>', mode='exec')
    print("==== dis ====")
    dis.dis(code)

    print("\n==== vm ====")
    l1 = dict()
    g1 = dict()
    vm = VirtualMachine(code, safe_builtins.copy(), l1, g1)
    steps = 0
    while not vm.finish and steps < max_steps:
        op, data = vm.exec()
        steps += 1
        print("{:5} {:20} {:3} stack={} block_stack={}".format(steps, opname[op], data, vm.stack, vm.block_stack))

    print("\n==== vm result ====")
    print("finish", vm.finish)
    print("local", l1)
    print("global", g1)
    print("return", vm.return_value)

    l2 = dict()
    g2 = safe_globals.copy()
    r = eval(code, g2, l2)
    del g2['__builtins__']
    print("\n==== eval result ====")
    print("local", l2)
    print("global", g2)
    print("return", r)


if __name__ == '__main__':
    compile_and_print("""
a = 1
b = 2
c = 3
d = 0

e = a * b * c * d
f = a + b + c + d
for i in range(10):
    if i == 5:
        break
    if i == 3:
        d -= 1
        continue
    d += 1

k = [d]
g = e // f + d
k.append(g)
""")


__all__ = [
    "VirtualMachine",
    "VirtualMachineError",
    "compile_and_print",
]
