import pandas as pd


if __name__ == "__main__":
    report = pd.read_csv("va-nayax-production-initial.csv")
    print(report.shape)

    report = report.fillna(0).groupby(['Synopsis'])['CVE','Risk','Host','Solution', 'Plugin Output'].first().sort_values(by='Risk')
    print(report)
    report.to_csv('out.csv')
