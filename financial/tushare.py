import tushare as ts
import datetime
import pandas as pd
import numpy as np

token="1667c3755882d3c017a033afea020bbf00e8b6e63ecf99617ff40b89"
pro = ts.pro_api(token)

start = "20180101"
end = datetime.datetime.today().strftime("%Y%m%d")
trade_date = pro.trade_cal(start_date=start, end_date=end)
print(trade_date.head())
date_list = list(trade_date[trade_date.is_open==1]["cal_date"].values)
print(date_list[0:300][0], date_list[0:300][-1])

# 北向资金和南向基金流向
def fetch_moneyflow_hsgt(date_list):
    df = []
    step = 300
    length = len(date_list)
    if step > length:
        step = length
    for i in range (0, length, step):
        start = date_list[i]
        if i + step >= length:
            end = date_list[length-1]
        else:
            end = date_list[i+step]
        print(i, step, start, end)
        dd = pro.moneyflow_hsgt(**{
            "trade_date": "",
            "start_date": start,
            "end_date": end,
            "limit": "",
            "offset": ""
        }, fields=[
            "trade_date",
            "ggt_ss",
            "ggt_sz",
            "hgt",
            "sgt",
            "north_money",
            "south_money"
        ])
        return dd

    return df


# 单次请求限制为300条

df = fetch_moneyflow_hsgt(date_list)
# @todo 根据日期排序
# 单位换算：百万->亿
df["ggt_ss"] = df["ggt_ss"] * 0.01
df["ggt_sz"] = df["ggt_sz"] * 0.01
df["hgt"] = df["hgt"] * 0.01
df["sgt"] = df["sgt"] * 0.01
df["north_money"] = df["north_money"] * 0.01
df["south_money"] = df["south_money"] * 0.01
df = df.rename(columns={'ggt_ss': '港股通-上海', 'ggt_sz': '港股通-深圳', 'hgt': '沪股通', 'sgt': '深股通', 'north_money': '北向基金', 'south_money': '南向基金'})

# 剔除休市的日期
df = df.loc[~df['沪股通'].isna(), :].reset_index(drop=True)

for index, row in df.iterrows():
    if index < 252:
        continue
    # 计算均值和标准差
    tmp = df.iloc[index-252:index]
    avg = tmp['北向基金'].sum()/252
    std = tmp['北向基金'].std()
    # 计算上下限
    up_line = float(format(avg + 1.5 * std, ".4f"))
    down_line = float(format(avg - 1.5 * std, ".4f"))
    if row["北向基金"] >= up_line:
        print('{} 信号：买入, 北上净买入: {}, 上限: {}, 下限: {}'.format(row["trade_date"], row["北向基金"], up_line, down_line))
    elif row["北向基金"] <= down_line:
        print('{} 信号：卖出, 北上净买入: {}, 上限: {}, 下限: {}'.format(row["trade_date"], row["北向基金"], up_line, down_line))
print(df)

