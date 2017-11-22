import pandas as pd


def get_data():
    #path = "alienvault-alarms-csv.csv"

    path = input("What data should I look at? ")
    df = pd.read_csv("../samples/"+path)
    return df


def check_sytem_compromise(df):
    g = df[df.Sources.str.startswith('10.') | df.Sources.str.startswith('192.168')]
    g = g.drop(['Labels', 'Sensors'], axis=1)
    g = g.groupby(['Sources', 'Intent']).size()
    g = g.unstack().fillna(0)
    g = g.sort_values('System Compromise', ascending=False).head(1)
    return [g.index[0], int(g.unstack()['System Compromise'][0])]


if __name__ == "__main__":

    print("Hi, I'm Dagny and I'm learning cybersecurity.")
    df = get_data()
    result = check_sytem_compromise(df)
    print('Got it! Analyzing...')
    print("After reviewing the data, I recommend investigating host", result[0]+". It had", str(result[1]), "alarms for System Compromise.")
