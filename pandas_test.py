import pandas as pd
import numpy as np


def main():
    s = pd.Series([3, 5, 4, 5, 8])

    print(s)
    p = pd.DataFrame(np.random.rand(3, 4), columns=list("ABCD"))
    print(p)
    print(p.shape)
    df = pd.DataFrame(np.random.randint(1, 100, 24).reshape(6, 4), columns=list("ABCD"))
    print(df)
    print("第三行")
    print(df[3:4])
    print("第1 2 col")
    print(df[["A", "B"]])
    print("head(3)")
    print(df.head(3))
    print("tail(3)")
    print(df.tail(3))
    print(df.describe())
    df["TAG"] = ["M", "F", "F", "M", "F", "M"]
    print(df)
    print(df.groupby("TAG").sum())
    df2 = pd.read_csv("https://bit.ly/uforeports")
    print(df2.columns)
    print(df2.head(25))
    print(df2.City.isnull())

    df3 = pd.read_json("https://bit.ly/2Qfzovb")
    print(df3.head(5))
    df3["UVI"] = pd.to_numeric(df3["UVI"])
    print(df3.head(5))




if __name__ == "__main__":
    main()