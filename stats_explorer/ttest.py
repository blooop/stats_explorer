import bencher as bch
import random
import numpy as np
from scipy import stats


class Ttest(bch.ParametrizedSweep):
    """Performs statistical t-tests between two sample distributions.

    This class implements a parametrized sweep for t-test analysis between two
    sample distributions generated from normal distributions with opposite means.
    It allows exploring how different parameters (mean difference, sample size,
    standard deviation) affect the p-value of the t-test.

    Attributes:
        mean_delta (bch.FloatSweep): Difference between the means of the two distributions.
            Default is 0, with bounds [0, 0.5], measured in arbitrary units (ul).
        samples (bch.IntSweep): Number of samples to generate for each distribution.
            Default is 30, with bounds [10, 100], measured in samples.
        std (bch.FloatSweep): Standard deviation of both distributions.
            Default is 1, with bounds [0.1, 5], measured in arbitrary units (ul).
        p_value (bch.ResultVar): The resulting p-value from the t-test,
            measured in arbitrary units (ul).
    """

    mean_delta = bch.FloatSweep(default=0, bounds=[0, 0.5], units="ul")
    samples = bch.IntSweep(default=30, bounds=[10, 100], units="samples")
    std = bch.FloatSweep(default=1, bounds=[0.1, 5], units="ul")

    p_value = bch.ResultVar(units="ul")

    def __call__(self, **kwargs) -> dict:
        """Execute the t-test with the given parameters.

        Generates two sample distributions with opposite means and performs
        a t-test to determine if they come from different distributions.

        Args:
            **kwargs: Parameter overrides that can include mean_delta, samples, and std.
                These values will override the default class attributes.

        Returns:
            dict: Results dictionary containing the p-value and input parameters,
                as returned by the parent class's __call__ method.
        """
        self.update_params_from_kwargs(**kwargs)

        # Generate N samples from a Gaussian distribution
        sample1 = np.random.normal(self.mean_delta, self.std, self.samples)

        # Generate another N samples from the same distribution
        sample2 = np.random.normal(-self.mean_delta, self.std, self.samples)

        # Perform a t-test to see if those values are from the same distribution
        _, p_value = stats.ttest_ind(sample1, sample2, equal_var=True)

        # Save the p-value
        self.p_value = p_value

        return super().__call__(**kwargs)


def example_ttest(run_cfg: bch.BenchRunCfg = None, report: bch.BenchReport = None) -> bch.Bench:
    """Creates and visualizes t-test results with various parameter sweeps.

    This example demonstrates how to create a t-test benchmark and visualize
    the results through different parameter sweeps. It shows how to fix certain
    parameters while varying others to explore the t-test's behavior.

    Args:
        run_cfg (bch.BenchRunCfg, optional): Configuration for the benchmark run,
            including parameters like number of repeats. Defaults to None.
        report (bch.BenchReport, optional): Report object for capturing benchmark
            results. Defaults to None.

    Returns:
        bch.Bench: The benchmark object containing all results and plots.
    """

    bench = Ttest().to_bench(run_cfg, report)
    bench.plot_sweep(input_vars=[], const_vars=dict(std=1.0, samples=30, mean_delta=0))
    # bench.plot_sweep(input_vars=[],const_vars=dict(std=1., samples=30, mean_delta=0.01))
    bench.plot_sweep(input_vars=["mean_delta"], const_vars=dict(std=1.0, samples=30))
    return bench


if __name__ == "__main__":
    run_config = bch.BenchRunCfg(repeats=1000, level=5)
    example_ttest(run_config).report.show()
