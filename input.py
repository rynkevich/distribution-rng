from generators import UniformParameters, GaussianParameters, ExponentialParameters, GammaParameters, \
    TriangularParameters, SimpsonParameters


def read_uniform_parameters():
    a = read_float('a')
    b = read_float('b', lambda x: x > a, error_message='{} must be a valid float, greater than a')
    return UniformParameters(a, b)


def read_gaussian_parameters():
    return GaussianParameters(read_float('mean'), read_float('scale'))


def read_exponential_parameters():
    return ExponentialParameters(read_positive_float('rate'))


def read_gamma_parameters():
    return GammaParameters(read_positive_int('shape'), read_positive_float('rate'))


def read_triangular_parameters():
    a = read_float('a')
    b = read_float('b', lambda x: x > a, error_message='{} must be a valid float, greater than a')
    return TriangularParameters(a, b)


def read_simpson_parameters():
    a = read_float('a')
    b = read_float('b', lambda x: x > a, error_message='{} must be a valid float, greater than a')
    return SimpsonParameters(a, b)


def read_positive_int(name, validator=lambda x: True, error_message='{} must be a valid positive integer'):
    return read_typed(name, int, lambda x: x > 0 and validator(x), error_message)


def read_positive_float(name, validator=lambda x: True, error_message='{} must be a valid positive float'):
    return read_typed(name, float, lambda x: x > 0 and validator(x), error_message)


def read_float(name, validator=lambda x: True, error_message='{} must be a valid float'):
    return read_typed(name, float, validator, error_message)


def read_typed(name, type_constructor, validator=lambda x: True, error_message=None):
    result = None
    is_valid = False
    while not is_valid:
        raw_input = input(f'{name}: ')
        result = safe_cast(raw_input, type_constructor)
        is_valid = result is not None and validator(result)
        if not is_valid:
            if error_message is not None:
                print(error_message.format(name))
    return result


def safe_cast(value, type_constructor, default=None):
    try:
        return type_constructor(value)
    except (ValueError, TypeError):
        return default
