from ply.lex import lex
from ply.yacc import yacc

from language.lexer.lambda_expr import *
from language.parser.lambda_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from interpreter import lambda_expr
# from interpreter.enviroment import Enviroment

set_generator_module(lambda_expr)
check_generator_module(used_procedures_and_classes)

lexer = lex()
parser = yacc(start='expression')
env = lambda_expr.env


# TODO: Delete if not used
# def unraw(s: str) -> str:
#     return s \
#         .replace(r'\'', '\'') \
#         .replace(r'\"', '\"') \
#         .replace(r'\\', '\\') \
#         .replace(r'\n', '\n') \
#         .replace(r'\t', '\t')

example = '''
{
    x := True;
    local x := False in
        b := 1;
    lock x in
    {
        a := 3;
        b := 4;
        c := True;
        y := 4
    };

    z :=
    if x > y then
        if x > y then
            y := y + 1
        else
            x*y;
    z := 2;
    a := 0;
    b := 0;
    loop x do
        if z >= 0 then
            loop y do
                {
                    z := z - 1;
                    a := a + 1
                }
        else
            b := b+1;
    while x > z do
        x := x - 1;

    local a := 4 in
        local b := 7 in
        {
            d := a + b;
            a := a * a;
            c := a + 2;
            e := True
        };

    for i := 0; i < 5; i := i+1 do
        lock a in
        {
            a := 4;
            b := a * b;
            c := True
        };

    while a > 0 do
    {
        a := a - 1;
        b := b * 2;
        c := c xor True;
        d := 6
    };

    a := x -> x+1;
    b := a(2);
    c := b + a(7)

    a := 4;
    f := x -> y -> a := a+y;
    b := f(2)(3)
}
'''

example = '''
{
    g := local gauss := x ->
        if x = 0 then 0
        else x + gauss(x - 1) in
            gauss(10);
    f := local fac := x ->
        if x = 0 then 1
        else x * fac(x - 1) in
            fac(8);
    a := 'a';
    s := "ghj";
    n := ""
}
'''

example = '''
{ a1 := []
; a2 := [1]
; a3 := [1,2]
; a4 := [1,2,'c']
; b := 4
; a5 := [1, 2, 3, b]
; a6 := [1, 2+3, 4+b, b+1]
# ; a7 := array()
# ; a8 := array(1,2,3)
}'''

example = '''
{
    a := 2;
    b1 := list(1, a, 2);
    b2 := list(3, a+4);
    b3 := list(3, a+4, 5);
    b4 := list(6, 7+a);
    b5 := list(6, 7+a, 8)
    # b6 := list(9, a+10, a+11, 12);
    # b7 := list(13, 14+a, a+15, 16);
    # b8 := list(17, 18+a, 19+a, 20)
}'''

example = '''
{ arr := [1,2,4,8]
; b := arr[0]
; c := arr[3]
; d := arr[b+1]
; lst := list(1,2,4,8)
; e := head(lst)
; f := tail(lst)
; h := cons('A', f)
; i := [[1,2],3,4]
; j := i[0]
; k := j[0]
; l := [3+b]
}'''

example = '''
{ a := 'a'
; b := "a"
; c := '\n'
; d := "hello\tworld\n!"
}
'''

# example = '''
# { a := 'a'
# # ; b := '\n'
# # ; c := '\t'
# # ; d := '\\'
# # ; e := b = '\t
# '''

# example = '''
# { a := 5
# ; f := x -> x+1
# ; b := f(a)
# }'''

a =6
'''
; f := "test"
; g := "a\nb"
; h := "Hello \"world\"!"
}'''

'''
# ; h := "Hello "world"!"
# ; i := "\t\n\r\'\"\\"'''

# example = '''
# { a := 5
# ; s := struct
#     { x := 1
#     ; y := a
#     ; f:= x -> a := x
#     }
# }'''

result = parser.parse(input=example, lexer=lexer)
# # example = '\n'.join(repr(example).strip('\"').split(';'))
print(example, '\n', result.eval(env))

# for p in precedence:
#     print(*p)

'''
notes:
    1 shift reduce conflict with 'comma' in state 4
order:
    00. datatypes
    01. arithmetic_expr
    02. comparison_expr
    04. assignment_expr
    03. boolean_expr
    05. sequences_expr
    06. loop_expr
    07. for_expr
    08. while_expr
    09. ite_expr (If Then Else)
    10. lock_expr
    11. local_expr (acts like letrec)
    12. lambda_expr
    13. struct_expr

https://en.cppreference.com/w/cpp/language/operator_precedence
'''
