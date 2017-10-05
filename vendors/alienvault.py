import pandas as pd


if __name__ == "__main__":

    df = pd.read_csv("alienvault-alarms-csv.csv")

    g = df[df.Sources.str.startswith('10.') | df.Sources.str.startswith('192.168')]
    g = g.drop(['Labels', 'Sensors'], axis=1)
    g = g.groupby(['Sources', 'Intent']).size()
    g = g.unstack().fillna(0)
    g.sort_values('System Compromise', ascending=False)


