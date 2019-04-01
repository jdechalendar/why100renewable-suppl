import pandas as pd

def readDay(date="2018-01-01"):
    df = pd.read_csv("B1620_%s.csv" % date, skiprows=5,
                     usecols=[4, 7, 8, 9],
                     names=["quantity", "date", "period", "resource"])
    if date in ["2018-09-08", "2018-09-09", "2018-09-11",
                "2018-10-31", "2018-11-25", "2018-12-14",
                "2018-12-15"]:  # Special cases
        # 2018-09-08: duplicate data for period 3
        # 2018-09-09: duplicate data for period 17
        # 2018-09-11: duplicate data for periods 24,25,26
        # 2018-10-31: duplicate data for period 32
        # 2018-11-25: duplicate data for period 3
        # 2018-12-14: duplicate data for period 1
        # 2018-12-15: duplicate data for period 6,7,8
        df = df.drop_duplicates(["date", "period", "resource"]).reset_index()
    
    # bruter force check of duplicates
    dupl = df.duplicated(subset=["date", "period", "resource"])
    if dupl.sum() > 0:
        print("Duplicates for %s:" % date)
        print(df[dupl].period.unique())
        df = df.drop_duplicates(["date", "period", "resource"]).reset_index()
    if len(df) != 529:
        print("%s does not have 529 rows but %d" % (date, len(df)))
        #raise(ValueError("Unexpected number of rows"))
    df = df.drop(len(df)-1)  # row with <EOF>
    df["time"] = pd.to_datetime(df["date"]) + pd.to_timedelta(
        (df.period-1)*30, unit='m')
    try:
        dfp = df.pivot(index="time", columns="resource", values="quantity")
    except ValueError:
        print(date)
        raise 
    return dfp

if __name__ == '__main__':
    df = pd.concat([readDay(date=d.strftime("%Y-%m-%d"))
                    for d in pd.date_range(
                start="2015-01-01", end="2018-12-31")], sort=True)
    df.to_csv("UK_data.csv")