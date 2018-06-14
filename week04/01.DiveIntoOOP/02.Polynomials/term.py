import re


class Term:
    def __init__(self, *, coeff, var, power):
        self.coeff = coeff
        self.var = var
        self.power = power

    def derivative(self):
        return Term(coeff=self.coeff * self.power, var=self.var, power=max(0, self.power-1))

    @classmethod
    def constant(cls, const):
        return Term(coeff=const, var=None, power=0)

    @property
    def is_constant(self):
        return self.power == 0

    @classmethod
    def parse(cls, s):
        pattern = r'^(?P<coeff>\d*)\*?(?P<var>[a-z])?\^?(?P<power>\d*)$'
        match = re.match(pattern, s)
        if not match:
            raise ValueError('Invalid term')

        coeff = match.group('coeff')
        power = match.group('power')
        var = match.group('var')

        coeff = int(coeff) if coeff != '' else 1
        power = int(power) if power != '' else 0 if 'x' not in s else 1

        return cls(coeff=coeff, var=var, power=power)

    def __repr__(self):
        return f'(coeff: {self.coeff}, var: {self.var}, power: {self.power})'

    def __str__(self):
        if self.coeff == 0:
            return ''
        elif self.power == 0:
            return f'{self.coeff}'
        elif self.power == 1:
            return f'{self.coeff}*{self.var}'

        return f'{self.coeff}*{self.var}^{self.power}'

    def __add__(self, other):
        if self.var is None:
            self.var = other.var
        if other.var is None:
            other.var = self.var

        if self.power != other.power or self.var != other.var:
            raise ValueError('Terms must be of the same power and variable', self.var, other.var)

        return Term(coeff=self.coeff + other.coeff,
                    var=self.var if self.var != None else other.var,
                    power=self.power)

    def __sub__(self, other):
        if self.power != other.power or self.var != other.var:
            raise ValueError('Terms must be of the same variable and have the same power')
        return Term(coeff=self.coeff - other.coeff, var=self.var, power=self.power)

    def __mul__(self, other):
        return Term(coeff=self.coeff * other.coeff, var=self.var if self.var is not None else other.var, power=self.power + other.power)

    # TODO:
    def eval(self, **kwargs):
        pass

    def __eq__(self, other):
        if self.coeff == 0 and other.coeff == 0:
            return True
        if self.power == 0 and other.power == 0:
            return self.coeff == other.coeff

        return (self.coeff == other.coeff and
                self.power == other.power and
                self.var == other.var) 
