"""
all opcodes Python3.6.0
"""

# general
NOP = 9
POP_TOP = 1
ROT_TWO = 2
ROT_THREE = 3
DUP_TOP = 4
DUP_TOP_TWO = 5

# one operand
UNARY_POSITIVE = 10
UNARY_NEGATIVE = 11
UNARY_NOT = 12
UNARY_INVERT = 15
GET_ITER = 68
GET_YIELD_FROM_ITER = 69

# two operand
BINARY_POWER = 19
BINARY_MULTIPLY = 20
BINARY_MATRIX_MULTIPLY = 16
BINARY_FLOOR_DIVIDE = 26
BINARY_TRUE_DIVIDE = 27
BINARY_MODULO = 22
BINARY_ADD = 23
BINARY_SUBTRACT = 24
BINARY_SUBSCR = 25
BINARY_LSHIFT = 62
BINARY_RSHIFT = 63
BINARY_AND = 64
BINARY_XOR = 65
BINARY_OR = 66

# inplace
INPLACE_POWER = 67
INPLACE_MULTIPLY = 57
INPLACE_MATRIX_MULTIPLY = 17
INPLACE_FLOOR_DIVIDE = 28
INPLACE_TRUE_DIVIDE = 29
INPLACE_MODULO = 59
INPLACE_ADD = 55
INPLACE_SUBTRACT = 56
STORE_SUBSCR = 60
DELETE_SUBSCR = 61
INPLACE_LSHIFT = 75
INPLACE_RSHIFT = 76
INPLACE_AND = 77
INPLACE_XOR = 78
INPLACE_OR = 79

# coroutine (not implemented)
GET_AWAITABLE = 73
GET_AITER = 50
GET_ANEXT = 51
BEFORE_ASYNC_WITH = 52
SETUP_ASYNC_WITH = 154

# loop
FOR_ITER = 93
SETUP_LOOP = 120      # Distance to target address
BREAK_LOOP = 80
CONTINUE_LOOP = 119   # Target address

# comprehension
SET_ADD = 146
LIST_APPEND = 145
MAP_ADD = 147

# return
RETURN_VALUE = 83
YIELD_VALUE = 86
YIELD_FROM = 72
SETUP_ANNOTATIONS = 85

# context
SETUP_WITH = 143
WITH_CLEANUP_START = 81
WITH_CLEANUP_FINISH = 82

# import
IMPORT_STAR = 84
IMPORT_NAME = 108     # Index in name list
IMPORT_FROM = 109     # Index in name list

# block stack
POP_BLOCK = 87
SETUP_EXCEPT = 121    # ""
SETUP_FINALLY = 122   # ""
POP_EXCEPT = 89
END_FINALLY = 88

# variable
STORE_NAME = 90       # Index in name list
DELETE_NAME = 91      # ""
UNPACK_SEQUENCE = 92   # Number of tuple items
UNPACK_EX = 94
STORE_ATTR = 95       # Index in name list
DELETE_ATTR = 96      # ""
STORE_GLOBAL = 97     # ""
DELETE_GLOBAL = 98    # ""

# load
LOAD_CONST = 100       # Index in const list
LOAD_NAME = 101       # Index in name list
LOAD_ATTR = 106       # Index in name list
LOAD_GLOBAL = 116     # Index in name list
LOAD_FAST = 124        # Local variable number
STORE_FAST = 125       # Local variable number
DELETE_FAST = 126      # Local variable number

# build object
BUILD_TUPLE = 102      # Number of tuple items
BUILD_LIST = 103       # Number of list items
BUILD_SET = 104        # Number of set items
BUILD_MAP = 105        # Number of dict entries
BUILD_CONST_KEY_MAP = 156
BUILD_STRING = 157
BUILD_TUPLE_UNPACK = 152
BUILD_LIST_UNPACK = 149
BUILD_MAP_UNPACK = 150
BUILD_SET_UNPACK = 153
BUILD_MAP_UNPACK_WITH_CALL = 151
BUILD_TUPLE_UNPACK_WITH_CALL = 158

# bool
COMPARE_OP = 107       # Comparison operator

# counter
JUMP_FORWARD = 110    # Number of bytes to skip
POP_JUMP_IF_TRUE = 115     # ""
POP_JUMP_IF_FALSE = 114    # ""
JUMP_IF_TRUE_OR_POP = 112  # ""
JUMP_IF_FALSE_OR_POP = 111 # Target byte offset from beginning of code
JUMP_ABSOLUTE = 113        # ""

# exception
RAISE_VARARGS = 130    # Number of raise arguments (1, 2, or 3)

# function
CALL_FUNCTION = 131    # #args
MAKE_FUNCTION = 132    # Flags
BUILD_SLICE = 133      # Number of items
LOAD_CLOSURE = 135
LOAD_DEREF = 136
STORE_DEREF = 137
DELETE_DEREF = 138
CALL_FUNCTION_KW = 141  # #args + #kwargs
CALL_FUNCTION_EX = 142  # Flags
LOAD_CLASSDEREF = 148

# others
PRINT_EXPR = 70
LOAD_BUILD_CLASS = 71
HAVE_ARGUMENT = 90              # Opcodes from here have an argument:
EXTENDED_ARG = 144
FORMAT_VALUE = 155
