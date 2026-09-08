"""Master CLI runner for Statistics and Scientific Inference suite."""

from __future__ import annotations

import argparse
import logging

from statistics.descriptive.run_examples import (
    demo_bivariate,
    demo_outliers,
    demo_summary,
)
from statistics.distributions.run_examples import (
    demo_binomial,
    demo_exponential,
    demo_goodness_of_fit,
    demo_normal,
    demo_poisson,
)
from statistics.hypothesis_testing.run_examples import (
    demo_anova,
    demo_chi_square,
    demo_one_sample,
    demo_paired,
    demo_two_sample_ab,
)
from statistics.regression.run_examples import (
    demo_multiple,
    demo_simple,
)

logger = logging.getLogger(__name__)


def run_all_descriptive() -> None:
    print("================================================================================")
    print("           Statistics: Descriptive Metrics, Outliers & Bivariate Trends         ")
    print("================================================================================")
    demo_summary()
    demo_outliers()
    demo_bivariate()
    print()


def run_all_distributions() -> None:
    print("================================================================================")
    print("          Statistics: Probability Distributions & Goodness-of-Fit Tests         ")
    print("================================================================================")
    demo_normal()
    demo_binomial()
    demo_poisson()
    demo_exponential()
    demo_goodness_of_fit()
    print()


def run_all_hypothesis() -> None:
    print("================================================================================")
    print("          Statistics: Hypothesis Testing, A/B Testing & ANOVA Inference         ")
    print("================================================================================")
    demo_one_sample()
    demo_two_sample_ab()
    demo_paired()
    demo_anova()
    demo_chi_square()
    print()


def run_all_regression() -> None:
    print("================================================================================")
    print("         Statistics: Simple & Multiple Linear Regression (OLS Analysis)         ")
    print("================================================================================")
    demo_simple()
    demo_multiple()
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Statistics Master Suite Demonstrations")
    parser.add_argument(
        "--submodule",
        choices=["descriptive", "distributions", "hypothesis_testing", "regression", "all"],
        default="all",
        help="Submodule to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "descriptive": run_all_descriptive,
        "distributions": run_all_distributions,
        "hypothesis_testing": run_all_hypothesis,
        "regression": run_all_regression,
    }

    if args.submodule == "all":
        for fn in dispatch.values():
            fn()
        print("✅ All Statistics demonstrations executed successfully across all submodules!")
    else:
        dispatch[args.submodule]()


if __name__ == "__main__":
    main()
