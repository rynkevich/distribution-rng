import math
from collections import namedtuple

UniformParameters = namedtuple('UniformParameters', ['a', 'b'])
GaussianParameters = namedtuple('GaussianParameters', ['mean', 'scale'])
ExponentialParameters = namedtuple('ExponentialParameters', ['rate'])
GammaParameters = namedtuple('GammaParameters', ['shape', 'rate'])
TriangularParameters = namedtuple('TriangularParameters', ['a', 'b'])
SimpsonParameters = namedtuple('SimpsonParameters', ['a', 'b'])


class UniformDistributionGenerator:
    def __init__(self, rng):
        self.__rng = rng

    def generate_sequence(self, params, size):
        for x in self.__rng(size):
            yield params.a + (params.b - params.a) * x


class GaussianDistributionGenerator:
    def __init__(self, rng):
        self.__rng = rng
        self.__n = 6

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value):
        self.__n = value

    def generate_sequence(self, params, size):
        random_sequence = self.__rng(self.n * size)
        for i in range(size):
            random_sum = sum(next(random_sequence) for _ in range(self.n))
            yield params.mean + params.scale * math.sqrt(12 / self.n) * (random_sum - self.n / 2)


class ExponentialDistributionGenerator:
    def __init__(self, rng):
        self.__rng = rng

    def generate_sequence(self, params, size):
        for x in self.__rng(size):
            yield -1 / params.rate * math.log(x)


class GammaDistributionGenerator:
    def __init__(self, rng):
        self.__rng = rng

    def generate_sequence(self, params, size):
        random_sequence = self.__rng(params.shape * size)
        for i in range(size):
            random_log_sum = sum(math.log(next(random_sequence)) for _ in range(params.shape))
            yield -1 / params.rate * random_log_sum


class TriangularDistributionGenerator:
    def __init__(self, rng):
        self.__rng = rng

    def generate_sequence(self, params, size):
        random_numbers = tuple(self.__rng(size * 2))
        for x1, x2 in zip(random_numbers[::2], random_numbers[1::2]):
            yield params.a + (params.b - params.a) * min(x1, x2)


class SimpsonDistributionGenerator:

    #   |\/\/\/\/\/|
    #   |          |
    #   |          |
    #   |          |
    #   |    __  __|
    #   |   /  \/  \
    #   |  (o   )o  )
    #  /C   \__/ --.
    #  \_   ,     -'
    #   |  '\_______)
    #   |      _)
    #   |     |
    #  /`-----'\
    # /         \

    def __init__(self, rng):
        self.__rng = rng

    def generate_sequence(self, params, size):
        random_numbers = tuple(self.__rng(size * 2))
        for x1, x2 in zip(random_numbers[::2], random_numbers[1::2]):
            yield params.a + (params.b / 2 - params.a / 2) * (x1 + x2)
