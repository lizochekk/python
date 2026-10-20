import re
import math


TOKEN_RE = re.compile(r"\s*(sin|!=|\d+\.\d*|\.\d+|\d+|\+|-|\*|/|\(|\))")


def tokenize(text):
    tokens = []
    pos = 0
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        if not m:
            raise SyntaxError(f"Плохой символ: {text[pos]!r}")
        tokens.append(m.group(1))
        pos = m.end()
    tokens.append("END")
    return tokens


def evaluate(text):
    tokens = tokenize(text)
    pos = [0]

    def peek():
        return tokens[pos[0]]

    def take():
        t = tokens[pos[0]]
        pos[0] += 1
        return t

    def expression():
        value = comparison()
        while peek() in ("+", "-"):
            op = take()
            rhs = comparison()
            value = value + rhs if op == "+" else value - rhs
        return value

    def comparison():
        value = term()
        while peek() == "!=":
            take()
            rhs = term()
            value = 1 if value != rhs else 0
        return value

    def term():
        value = factor()
        while peek() in ("*", "/"):
            op = take()
            rhs = factor()
            if op == "*":
                value *= rhs
            else:
                if rhs == 0:
                    raise ZeroDivisionError("Деление на ноль")
                value /= rhs
        return value

    def factor():
        if peek() == "+":
            take()
            return factor()
        if peek() == "-":
            take()
            return -factor()
        return primary()

    def primary():
        tok = take()
        if re.fullmatch(r"\d+\.\d*|\.\d+|\d+", tok):
            return float(tok) if "." in tok else int(tok)
        if tok == "sin":
            if take() != "(":
                raise SyntaxError("После sin нужна (")
            value = expression()
            if take() != ")":
                raise SyntaxError("Не закрыта скобка после sin")
            return math.sin(value)
        if tok == "(":
            value = expression()
            if take() != ")":
                raise SyntaxError("Не закрыта скобка")
            return value
        raise SyntaxError(f"Неожиданный токен: {tok!r}")

    result = expression()
    if peek() != "END":
        raise SyntaxError(f"Лишнее: {peek()!r}")
    return result


if __name__ == "__main__":
    print(evaluate(input()))