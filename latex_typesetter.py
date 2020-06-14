BinaryOperators = {'/' : lambda a, b: '\\frac{' + a + '}{' + b + '}'}
UnaryOperators = {'sqrt' : lambda a: '\\sqrt{'+ a + '}'}

def set(equation):
    Output = []
    terms = equation.split(" ")
    i = 0
    while i < len(terms):
        term = terms[i]
        if term == '*':
            Output.append('\\cdot')
            i += 1
            continue
        if term in BinaryOperators:
            Output[-1] = (BinaryOperators[term](terms[i-1],terms[i+1]))
            i += 2
            continue
        if term in UnaryOperators:
            Output.append(UnaryOperators(terms[i+1]))
            enumerate(terms).next()
            i += 2
            continue
        i += 1
        Output.append(term)
    return Output


def read(output):
    s = ''
    for term in output:
        s = s + term + ' '
    print(s[:-1])


read(set('2 / 4 * 3'))
