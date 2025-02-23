import bencher as bch
import random


class FalsePositives(bch.ParametrizedSweep):
    """This class has 0 input dimensions and 1 output dimensions.  It samples from a gaussian distribution"""

    prevalence = bch.FloatSweep(default=1, bounds=[1, 10], units="%")
    false_positive_rate = bch.FloatSweep(default=0.02, bounds=[0.01, 0.1], units="%")
    # This defines a variable that we want to plot
    diseased = bch.ResultVar(units="ul")
    healthy = bch.ResultVar(units="ul")
    test_result = bch.ResultVar(units="ul")
    random_var = bch.ResultVar()

    def __call__(self, **kwargs) -> dict:

        # self.prevalence = 1

        self.random_var = random.random()
        is_diseased = self.random_var < self.prevalence / 100.0
        self.diseased = 1. if is_diseased else 0.
        self.healthy = 1. if not is_diseased else 0.

        if not is_diseased:
            self.test_result = 1 * (random.random() < self.false_positive_rate / 100.0)
        else:
            self.test_result = 0.0

        return super().__call__(**kwargs)


def example_0_in_1_out(
    run_cfg: bch.BenchRunCfg = None, report: bch.BenchReport = None
) -> bch.Bench:
    """This example shows how to sample a 1 dimensional float variable and plot the result of passing that parameter sweep to the benchmarking function"""

    bench = FalsePositives().to_bench(run_cfg, report)
    res=bench.plot_sweep(input_vars=["prevalence"])
    bench.report.append(res.to_scatter())
    return bench


if __name__ == "__main__":
    run_config = bch.BenchRunCfg(repeats=100)
    example_0_in_1_out(run_config).report.show()
