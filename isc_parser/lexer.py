import re
from datetime import datetime


import ply.lex as lex


reserved = {
    "set": "SET",
    "on": "ON",
}
tokens = ["STR", "QUOTEDSTR", "INT", "IP4ADDR", "MACADDR", "SEMICOLON",
          "BEGIN_CURVE_BRACE", "END_CURVE_BRACE", "BEGIN_BRACE", "END_BRACE",
          "DATE", "TIME", "EQ", "COMMA"]
tokens += list(reserved.values())

t_ignore = " \t"
t_ignore_COMMENT = r"\#.*"

t_SEMICOLON = r";"
t_BEGIN_CURVE_BRACE = r"{"
t_END_CURVE_BRACE = r"}"
t_BEGIN_BRACE = r"\("
t_END_BRACE = r"\)"
t_COMMA = r","
t_EQ = r"="


def t_IP4ADDR(t):
    r"(\d{1,3}\.){3}\d{1,3}"
    return t


def t_MACADDR(t):
    r"([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}"
    t.value = t.value.lower()
    return t


def t_DATE(t):
    r"\d{4}\/\d{2}\/\d{2}"
    # 2018/12/03
    t.value = datetime.strptime(t.value, "%Y/%m/%d")
    return t


def t_TIME(t):
    r"\d{2}:\d{2}:\d{2}"
    # 09:24:59
    t.value = datetime.strptime(t.value, "%H:%M:%S")
    return t


def t_QUOTEDSTR(t):
    r"\"(.*?)\""
    t.value = t.value[1:-1]
    return t


def t_INT(t):
    r"\b[0-9]+\b"
    t.value = int(t.value)
    return t


def t_STR(t):
    r"[a-zA-Z0-9\-\.]+"
    t.type = reserved.get(t.value, "STR")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


lexer = lex.lex(debug=False, reflags=re.UNICODE)
