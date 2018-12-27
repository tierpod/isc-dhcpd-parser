from isc_parser.types import Function, Item, ItemSet

from isc_parser.lexer import tokens

import ply.yacc as yacc


def p_error(p):
    print("Syntax error in input!", p.lineno, p)


def p_config(p):
    """
    config : section
           | sections
    """
    p[0] = p[1]


def p_sections(p):
    """
    sections : sections section
             | section
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_section(p):
    """
    section : STR IP4ADDR BEGIN_CURVE_BRACE items END_CURVE_BRACE
            | ON STR BEGIN_CURVE_BRACE items END_CURVE_BRACE
    """
    p[0] = ((p[1], p[2]), p[4])


def p_items(p):
    """
    items : items item
          | item
    """
    if not p[1]:
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_item(p):
    """
    item : STR STR STR SEMICOLON
         | STR STR STR STR SEMICOLON
         | STR QUOTEDSTR SEMICOLON
    """
    if len(p) == 6:
        p[0] = Item(values=(p[1], p[2], p[3], p[4]))
    elif len(p) == 5:
        p[0] = Item(values=(p[1], p[2], p[3]))
    elif len(p) == 4:
        p[0] = Item(values=(p[1], p[2]))


def p_item_datetime(p):
    """
    item : STR INT DATE TIME SEMICOLON
    """
    p[0] = Item(values=(p[1], p[2], p[3], p[4]))


def p_item_macaddr(p):
    """
    item : STR STR MACADDR SEMICOLON
    """
    p[0] = Item(values=(p[1], p[2], p[3]))


def p_item_set(p):
    """
    item : SET STR EQ QUOTEDSTR SEMICOLON
         | SET STR EQ function SEMICOLON
    """
    p[0] = ItemSet(key=p[2], value=p[4])


def p_item_function(p):
    """
    item : function SEMICOLON
    """
    p[0] = p[1]


def p_item_section(p):
    """
    item : section
    """
    p[0] = p[1]


def p_item_none(p):
    """
    item :
    """
    p[0] = []


def p_function(p):
    """
    function : STR BEGIN_BRACE args END_BRACE
    """
    p[0] = Function(name=p[1], args=p[3])


def p_args(p):
    """
    args : args COMMA arg
         | arg
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_arg(p):
    """
    arg : INT
        | STR
        | QUOTEDSTR
        | function
    """
    p[0] = p[1]


# def p_subnet(p):
#     """
#     subnet : SUBNET IP4ADDR NETMASK IP4ADDR BEGIN_CURVE_BRACE options END_CURVE_BRACE
#     """
#     p[0] = Subnet(ip4addr=p[2], netmask=p[4], options=p[6])


# def p_options(p):
#     """
#     options : options option
#             | option
#     """
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = p[1]
#         p[0].append(p[2])


# def p_option(p):
#     """
#     option : OPTION STR STR SEMICOLON
#            | OPTION STR QUOTEDSTR SEMICOLON
#            | OPTION STR IP4ADDR SEMICOLON
#            | OPTION STR MACADDR SEMICOLON
#     """
#     p[0] = (p[2], p[3])


# def p_option_list(p):
#     """
#     option : OPTION STR IP4ADDR STR IP4ADDR SEMICOLON
#     """
#     p[0] = (p[2], (p[3], p[5]))


# def p_option_range(p):
#     """
#     option : RANGE IP4ADDR IP4ADDR SEMICOLON
#     """
#     p[0] = (p[1], (p[2], p[3]))


start = "config"

parser = yacc.yacc(debug=False)


def parse_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return parser.parse(data)
