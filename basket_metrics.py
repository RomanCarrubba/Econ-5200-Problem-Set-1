"""YOUR ONE-LINE DESCRIPTION OF THE MODULE."""

import numpy as np
import pandas as pd


def audit_report(df: pd.DataFrame) -> pd.DataFrame:
  """
  Returns a dataframe with the audit report.
  """
  result = []
  for column in df:
    series = df[column]

    missing = series.isna().mean()

    dtype = series.dtype

    if (pd.api.types.is_numeric_dtype(series)):
        skew = series.skew()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_count = (
            (series < lower_bound) |
            (series > upper_bound)
        ).sum()

    else:
        skew = np.nan
        outlier_count = np.nan

    result.append({
        "column": column,
        "missing": missing,
        "dtype": dtype,
        "skew": skew,
        "outlier_count": outlier_count
    })
  return pd.DataFrame(result)

def robust_mean(
    x: pd.Series,
    method: str,
    order_type: pd.Series| None = None
    ) -> float:
  """
  Returns median, trimmed or rule-based exclusion
  """
  match method:
    case "median":
      return x.median()

    case "trimmed":
      lower = x.quantile(0.1)
      upper = x.quantile(0.9)

      return x.loc[
          (x >= lower) & (x <= upper)
      ].mean()

    case "rule-based":
      if order_type is None:
        raise ValueError("order_type must be provided")
      return x.loc[order_type == "B2C"].mean()

    case _:
            raise ValueError(
                "The method is not valid. "
                "Use 'median', 'trimmed', or 'rule-based'."
            )

if __name__ == "__main__":
    df = pd.DataFrame({
        "basket_value": [10, 12, 15, 20, 25, 30, 1000],
        "order_type": ["B2C", "B2C", "B2C", "B2C", "B2C", "B2C", "B2B"]
    })

    print("Audit Report:")
    print(audit_report(df))

    print("\nMedian:")
    print(robust_mean(df["basket_value"], "median"))

    print("\nTrimmed Mean:")
    print(robust_mean(df["basket_value"], "trimmed"))

    print("\nRule-based Exclusion:")
    print(robust_mean(df["basket_value"], "rule-based", df["order_type"]))
