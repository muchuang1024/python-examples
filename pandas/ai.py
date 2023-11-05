import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
llm = OpenAI(api_token="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")

# 随机初始化各国名称，GDP数据，幸福指数数据
df = pd.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "gdp": [19294482071552, 2891615567872, 2411255037952, 3435817336832, 1745433788416, 1181205135360, 1607402389504, 1490967855104, 4380756541440, 14631844184064],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 6.12]
})
df = SmartDataframe(df, config={"llm": llm})
df.chat('Which are the 5 happiest countries?')
