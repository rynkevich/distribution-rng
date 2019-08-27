import matplotlib.pyplot as plt
import sys
import statistics as stat

from collections import namedtuple

from generators import UniformDistributionGenerator, GaussianDistributionGenerator, ExponentialDistributionGenerator, \
    GammaDistributionGenerator, TriangularDistributionGenerator, SimpsonDistributionGenerator
from input import read_uniform_parameters, read_gaussian_parameters, read_exponential_parameters, \
    read_gamma_parameters, read_triangular_parameters, read_simpson_parameters
from rng import random_sequence

DistributionInfo = namedtuple('DistributionInfo', ['name', 'generator', 'reader'])

RANDOM_SEQUENCE_SIZE = 50000
HISTOGRAM_BINS_COUNT = 20
RNG_A = 32771
RNG_M = 1046527
RNG_R0 = 65537

DISTRIBUTIONS = {
    'uniform': DistributionInfo(
        name='Uniform',
        generator=UniformDistributionGenerator,
        reader=read_uniform_parameters),
    'gauss': DistributionInfo(
        name='Gaussian',
        generator=GaussianDistributionGenerator,
        reader=read_gaussian_parameters),
    'exp': DistributionInfo(
        name='Exponential',
        generator=ExponentialDistributionGenerator,
        reader=read_exponential_parameters),
    'gamma': DistributionInfo(
        name='Gamma',
        generator=GammaDistributionGenerator,
        reader=read_gamma_parameters),
    'triangular': DistributionInfo(
        name='Triangular',
        generator=TriangularDistributionGenerator,
        reader=read_triangular_parameters),
    'simpson': DistributionInfo(
        name='Simpson',
        generator=SimpsonDistributionGenerator,
        reader=read_simpson_parameters)
}


def main():
    distribution_info = DISTRIBUTIONS.get(sys.argv[1]) if len(sys.argv) > 1 else None
    if distribution_info is None:
        print('Usage: main.py (uniform | gauss | exp | gamma | triangular | simpson)')
        return

    rng = lambda size: random_sequence(RNG_A, RNG_M, RNG_R0, size)
    distribution_generator = distribution_info.generator(rng)
    distribution_params = distribution_info.reader()
    generated_sequence = tuple(distribution_generator.generate_sequence(distribution_params, RANDOM_SEQUENCE_SIZE))

    expected = stat.mean(generated_sequence)
    variance = stat.variance(generated_sequence)
    standard_deviation = stat.stdev(generated_sequence)

    print(f'Expected: {expected}')
    print(f'Variance: {variance}')
    print(f'Standard Deviation: {standard_deviation}')

    plot_freqency_histogram(generated_sequence, distribution_info.name)
    plt.show()


def plot_freqency_histogram(sequence, distribution_name):
    fig, ax = plt.subplots()
    fig.canvas.set_window_title('Distribution Random Number Generator')
    fig.suptitle(f'RNG Frequency Histogram - {distribution_name} Distribution')
    ax.set_xlabel('Generated value')
    ax.set_ylabel('Frequency')
    ax.hist(sequence,
            bins=HISTOGRAM_BINS_COUNT,
            weights=([1 / len(sequence)] * len(sequence)),
            edgecolor='black',
            linewidth=0.5)


if __name__ == '__main__':
    main()
