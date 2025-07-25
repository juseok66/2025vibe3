import pandas as pd
import plotly.express as px

# 엑셀 파일 로드
df = pd.read_excel("범죄율3.xlsx", sheet_name=0)

# 범죄 유형 병합
df["범죄유형"] = df["Unnamed: 0"].fillna("") + df["Unnamed: 1"].fillna("")
df = df.drop(columns=["Unnamed: 0", "Unnamed: 1"])
df = df.set_index("범죄유형").T
df.index.name = "연도"

# 특수기호 제거 및 숫자화
df = df.applymap(lambda x: str(x).replace(",", "").replace(".", "").replace("-", "").replace("없음", "").strip())
df = df.apply(pd.to_numeric, errors="coerce")

# 긴 형식으로 변환
df_long = df.reset_index().melt(id_vars="연도", var_name="범죄유형", value_name="범죄율")

# 시각화
fig = px.line(df_long, x="연도", y="범죄율", color="범죄유형",
              title="연도별 범죄율 변화 (1980–2023)",
              labels={"연도": "Year", "범죄율": "Crime Rate"})
fig.update_layout(legend_title_text="범죄 유형")
fig.show()
