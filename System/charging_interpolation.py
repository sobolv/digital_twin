from scipy.interpolate import UnivariateSpline


def spline_interpolation(x_array, y_array, current_value):
    x_array_prepared, y_array_prepared = zip(*sorted(zip(x_array, y_array)))
    return UnivariateSpline(x_array_prepared, y_array_prepared, s=0)(current_value)
