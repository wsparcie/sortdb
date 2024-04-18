import random
from math import pi, log10, ceil

from preferences import*

class SetGen:
    def __init__(self):
        self.R = React()
        self.array = []

        self.menu = {
            'all': 'choose all',
            'man': 'manual',
            'non': 'none',
            'nrm': 'normal',
            'vms': 'vonmises',
            'wbl': 'weibull',
            'prt': 'pareto',
            'bta': 'beta',
            'gma': 'gamma',
            'tri': 'triangular',
            'exp': 'exponential',
            'lgn': 'lognormal',
            'ex': 'exit',
        }

        self.menuNonUsable = (
            'all',
            'man',
            'ex',
        )

        self.modesMenu = {
            'a': 'auto',
            'm': 'manual',
        }
    
    def giveArray(self):
        return self.array

    def manual(self, start, stop, quantity):
        try:
            section = 'MANUAL MODE'
            print(f'\t\t\t{self.R.splitL} {section} {self.R.splitR}')
            self.array = []
            text = '\t\t\tpass number of elements: '
            quantity = int(input(text))
            i = 0
            for i in range(quantity):
                text = f'\t\t\tpass {i + 1} value: '
                while True:
                    try:
                        value = int(input(text))
                        self.array.append(value)
                        break
                    except:
                        self.R.printIncorrectItem('value')
                i += 1
        except Exception as e:
            self.R.printException('manual distribution', e)

    def none(self, start, stop, quantity):
        try:
            self.array = []
            rang = stop - start
            gap = rang / quantity
            gap = int(ceil(gap))
            while len(self.array) < quantity:
                value = start
                for i in range(quantity):
                    pool = random.randint(0, 2 * gap)
                    value += pool 
                    if value > stop or len(self.array) >= quantity:
                        break
                    ind = random.randint(0, i)
                    self.array.insert(ind, value)
        except Exception as e:
            self.R.printException('none distribution', e)

    def normal(self, start, stop, quantity):
        try:
            self.array = []
            mu = random.randint(start, stop)
            sigma = random.randint(1, 50)
            for _ in range(quantity):
                number = int(random.gauss(mu, sigma))
                number = max(start, min(stop, number))
                self.array.append(number)
        except Exception as e:
            self.R.printException('normal distribution', e)

    def triangular(self, start, stop, quantity):
        try:
            self.array = []
            modeParam = random.randint(start, stop)
            for _ in range(quantity):
                args = (start, stop, modeParam)
                number = random.triangular(*args)
                number = int(number)
                self.array.append(number)
        except Exception as e:
            self.R.printException('triangular distribution', e)

    def beta(self, start, stop, quantity):
        try:
            self.array = []
            values = (0, 10)
            alpha = random.triangular(0, 10, random.choice(values))
            beta = random.triangular(0, 10, random.choice(values))
            args = (alpha, beta)
            rang = log10(stop)*10
            for _ in range(quantity):
                dist = random.betavariate(*args)
                number = int(start + dist * rang)
                self.array.append(number)
        except Exception as e:
            self.R.printException('beta distribution', e)

    def exponential(self, start, stop, quantity):
        try:
            self.array = []
            lambd = random.triangular(5, 10, 10)
            sel = random.choice((-1, 1))
            lambd *= sel
            rang = log10(stop)*10
            for _ in range(quantity):
                dist = random.expovariate(lambd)
                if abs(lambd) != lambd:
                    number = int(stop + dist * rang)
                else:
                    number = int(start + dist * rang)
                self.array.append(number)
        except Exception as e:
            self.R.printException('exponential distribution', e)

    def gamma(self, start, stop, quantity):
        try:
            self.array = []
            values = (0, 10)
            alpha = random.triangular(0, 10, random.choice(values))
            beta = random.triangular(0, 10, random.choice(values))
            args = (alpha, beta)
            rang = log10(stop)*10
            for _ in range(quantity):
                dist = random.betavariate(*args)
                number = int(start + dist * rang)
                self.array.append(number)
        except Exception as e:
            self.R.printException('gamma distribution', e)

    def lognormal(self, start, stop, quantity):
        try:
            self.array = []
            mu = random.randint(1, 10)
            sigma = 1
            args = (mu, sigma)
            for _ in range(quantity):
                dist = random.lognormvariate(*args)
                number = int(start + dist)
                self.array.append(number)
        except Exception as e:
            self.R.printException('log normal distribution', e)

    def vonmises(self, start, stop, quantity):
        try:
            self.array = []
            mu = random.triangular(0, pi, 0)
            kappa = abs(random.uniform(start, stop))
            args = (mu, kappa)
            rang = log10(stop)*10
            for _ in range(quantity):
                dist = random.vonmisesvariate(*args)
                number = int(start + dist * rang)
                self.array.append(number)
        except Exception as e:
            self.R.printException('von mises distribution', e)

    def pareto(self, start, stop, quantity):
        try:
            self.array = []
            upper = 10**int(log10(stop) - 1)
            sel = random.choice((-10, 0, 0, 10))
            alpha = random.triangular(-10, 10, sel)
            for _ in range(quantity):
                dist = random.paretovariate(alpha)
                if sel >= 0:
                    number = int(start + dist * upper)
                else:
                    number = int(start + dist * upper)
                self.array.append(number)
        except Exception as e:
            self.R.printException('pareto distribution', e)

    def weibull(self, start, stop, quantity):
        try:
            self.array = []
            upper = 10**int(log10(stop))
            sel = random.choice((-10, 0, 0, 10))
            alpha = random.uniform(1, upper)
            beta = random.triangular(-10, 10, sel)
            args = (alpha, beta)
            for _ in range(quantity):
                dist = random.weibullvariate(*args)
                number = int(start + dist)
                self.array.append(number)
        except Exception as e:
                self.R.printException('weibull distribution', e)