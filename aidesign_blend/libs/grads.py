"""Gradient functions."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

from aidesign_blend.libs import utils

_clamp = utils.clamp


class _GradFunc:

    @classmethod
    def clamp(cls, inval, bound1, bound2):
        """Clamps the input value to the range bounded by bounds 1 and 2.

        All variables are casted to float type.

        Args:
            inval: the input value
            bound1: bound 1
            bound2: bound 2

        Returns:
            result: the clamped result
        """
        result = _clamp(inval, bound1, bound2)
        return result

    def __init__(self):
        """Inits self with the defaults."""
        self.eps = 1e-5
        """Epsilon. A dummy value of (1 / +inf) to avoid NaNs in computation."""
        self.inval_bound1 = float(self.eps)
        """Input value bound 1."""
        self.inval_bound2 = float(1 - self.eps)
        """Input value bound 2."""
        self.outval_bound1 = float(0)
        """Output value bound 1."""
        self.outval_bound2 = float(1)
        """Output value bound 2."""

    def inval_clamp(self, inval):
        """Clamps the inval with the inval bounds of self.

        Args:
            inval: the input value

        Returns:
            result: the result
        """
        result = _GradFunc.clamp(inval, self.inval_bound1, self.inval_bound2)
        return result

    def outval_clamp(self, outval):
        """Clamps the outval (result) with the outval bounds of self.

        Args:
            outval: the output value

        Returns:
            result: the result
        """
        result = _GradFunc.clamp(outval, self.outval_bound1, self.outval_bound2)
        return result

    def __call__(self, inval):
        """Calls self as a function.

        The default behavior is the linear unity function: f(x) = x.

        Args:
            inval: the input value

        Returns:
            result: the result
        """
        inval = float(inval)
        clamped_inval = self.inval_clamp(inval)

        outval = clamped_inval
        outval = self.outval_clamp(outval)

        result = outval
        return result

    def fnstr(self):
        """Finds the string representation of self as a function.

        Returns:
            result: the result
        """
        result = "f(x) = x"
        return result


class LU(_GradFunc):
    """The linear unity function.

    f(x) = x.
    The default gradient function.
    """

    def __init__(self):
        """Inits self with the defaults."""
        super().__init__()

    def __call__(self, inval):
        return super().__call__(inval)

    def fnstr(self):
        return super().fnstr()


class Poly1V(_GradFunc):
    """Polynomial function with 1 variable.

    Single variable polynomial function.
    """

    def __init__(self, coefs, exps):
        """Inits self with the given args.

        Args:
            coefs: the coefficients
            exps: the exponents

        Raises:

        """
        super().__init__()

        coefs = list(coefs)
        exps = list(exps)

        coefs_len = len(coefs)
        exps_len = len(exps)

        if coefs_len == 0:
            raise ValueError("Argument coefs needs to be non-empty")

        if exps_len == 0:
            raise ValueError("Argument exps needs to be non-empty")

        if coefs_len != exps_len:
            err_info = str(
                "Arguments coefs and exps need to have the same length\n"
                "  coefs' length: {}\n"
                "  exps' length: {}"
            ).format(
                coefs_len,
                exps_len
            )
            raise ValueError(err_info)
        # end if

        term_count = coefs_len
        coefs = [float(elem) for elem in coefs]
        exps = [float(elem) for elem in exps]

        self.coefs = coefs
        """Coefficients of the polynomial terms."""
        self.exps = exps
        """Exponents of the polynomial terms."""
        self.term_count = term_count
        """Count of the polynomial terms."""

    def __call__(self, inval):
        """Calls self as a function.

        Args:
            inval: the input value

        Returns:
            result: the result
        """
        inval = self.inval_clamp(inval)
        outval = float(0)

        for idx in range(self.term_count):
            coef = self.coefs[idx]
            exp = self.exps[idx]

            term_val = coef * (inval ** exp)
            outval += term_val
        # end for

        outval = self.outval_clamp(outval)
        result = outval
        return result

    def fnstr(self):
        """Finds the string representation of self as a function.

        Returns:
            result: the result
        """
        lines = []
        lines.append("f(x) =")

        for idx in range(self.term_count):
            coef = self.coefs[idx]
            exp = self.exps[idx]

            term_str = "  {} * (x ^ {}) +".format(coef, exp)
            lines.append(term_str)
        # end for

        lines = [str(elem) for elem in lines]
        result = "\n".join(lines)
        result = result[:-2]
        return result
