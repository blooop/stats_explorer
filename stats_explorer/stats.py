import bencher as bch
import random


class FalsePositives(bch.ParametrizedSweep):
    """This class has 0 input dimensions and 1 output dimensions.  It samples from a gaussian distribution"""

    # This defines a variable that we want to plot
    diseased = bch.ResultVar(units="ul" )
    healthy = bch.ResultVar(units="ul")
    test_result = bch.ResultVar(units="ul")
    rv = bch.ResultVar()

    def __call__(self, **kwargs) -> dict:
        prevalence = 0.01
        false_positive_rate = 0.02

        self.rv = random.random()
        is_diseased = self.rv < prevalence
        self.diseased = 1 if is_diseased else 0
        self.healthy = 1 if not is_diseased else 0

        if not is_diseased:
            self.test_result = 1 * (random.random() < false_positive_rate)
        else:
            self.test_result = 0.

        return super().__call__(**kwargs)


def example_0_in_1_out(
    run_cfg: bch.BenchRunCfg = None, report: bch.BenchReport = None
) -> bch.Bench:
    """This example shows how to sample a 1 dimensional float variable and plot the result of passing that parameter sweep to the benchmarking function"""

    bench = FalsePositives().to_bench(run_cfg, report)
    bench.plot_sweep()
    return bench


if __name__ == "__main__":
    run_config = bch.BenchRunCfg(repeats=100)
    example_0_in_1_out(run_config).report.show()
