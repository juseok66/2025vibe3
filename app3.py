import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    xls = pd.ExcelFile("범죄율3.xlsx")
    df = xls.parse("범죄율2")
    df.columns = df.columns.astype(str)
    df = df.rename(columns={df.columns[0]: "범죄대분류", df.columns[1]: "범죄유형"})
    df.fillna(method='ffill', inplace=True)
    df["범죄유형"] = df["범죄유형"].replace({"성폭력(강간\u00a0포함)": "성폭력"})
    return df

df = load_data()

# 지역별 범죄 데이터 불러오기
@st.cache_data
def load_region_data():
    xls_region = pd.ExcelFile("범죄발생_지역_20250725140807.xlsx")
    df_region = xls_region.parse("데이터")

    # 연도별 데이터 추출
    years = list(range(2012, 2024))
    region_names = df_region.iloc[0, 4:4+len(years)].tolist()

    records = []
    for i, year in enumerate(years):
        col_idx = 4 + i
        for row in range(4, df_region.shape[0]):
            crime_type = df_region.iloc[row, 0]
            if crime_type.strip() == "형법범 (건)":
                value = df_region.iloc[row+1, col_idx]  # 인구 10만명당 발생률
                region = region_names[i]
                if region != "계":
                    gender = "남성" if "남" in region else ("여성" if "여" in region else None)
                    records.append({"연도": year, "지역": region, "형법범죄율": value, "성별": gender})
                break

    df_region_chart = pd.DataFrame(records)
    return df_region_chart

df_region_chart = load_region_data()

# 데이터 전처리
value_vars = [col for col in df.columns if col.isdigit()]
df_melted = df.melt(id_vars=["범죄대분류", "범죄유형"], value_vars=value_vars, 
                    var_name="연도", value_name="범죄율")
df_melted["연도"] = df_melted["연도"].astype(int)
df_melted.dropna(subset=["범죄율"], inplace=True)

# 페이지 설정
page = st.sidebar.radio("페이지 선택", ["전체 형법범죄", "주요 형법범죄", "지역별 형법범죄"])

if page == "전체 형법범죄":
    st.header("전체 형법범죄 (막대 그래프)")
    df_total = df_melted[df_melted["범죄대분류"] == "전체\u00a0형법범죄"]
    fig_total = px.bar(df_total, x="연도", y="범죄율", title="전체 형법범죄 추이")
    fig_total.update_layout(xaxis_title="연도", yaxis_title="범죄율 (인구 10만 명당)")
    st.plotly_chart(fig_total)

elif page == "주요 형법범죄":
    st.header("주요 형법범죄 (꺾은선 그래프)")
    범죄유형_list = df_melted[df_melted["범죄대분류"] == "주요\u00a0형법범죄"]["범죄유형"].unique()
    selected_types = st.multiselect("범죄유형을 선택하세요", 범죄유형_list, default=[범죄유형_list[0]])

    df_filtered = df_melted[(df_melted["범죄유형"].isin(selected_types)) & (df_melted["범죄대분류"] == "주요\u00a0형법범죄")]

    fig = px.line(df_filtered, x="연도", y="범죄율", color="범죄유형", title="주요 형법범죄별 연도별 추이", markers=True)
    fig.update_layout(xaxis_title="연도", yaxis_title="범죄율 (인구 10만 명당)")
    st.plotly_chart(fig)

elif page == "지역별 형법범죄":
    st.header("2012~2023년 지역별 형법범죄율 (인구 10만 명당)")
    region_avg = df_region_chart.groupby("지역")["형법범죄율"].mean().reset_index()
    region_avg = region_avg.sort_values("형법범죄율", ascending=False)

    # 성별 색상 설정
    df_region_chart["성별"] = df_region_chart["지역"].apply(lambda x: "남성" if "남" in x else ("여성" if "여" in x else "기타"))
    color_map = {"남성": "blue", "여성": "pink", "기타": "gray"}
    region_avg = region_avg.merge(df_region_chart[["지역", "성별"]].drop_duplicates(), on="지역", how="left")

    fig_region = px.bar(region_avg, x="지역", y="형법범죄율",
                        title="2012~2023년 지역별 형법범죄율 평균",
                        color="성별", color_discrete_map=color_map,
                        labels={"형법범죄율": "범죄율 (인구 10만 명당)"})
    fig_region.update_layout(xaxis_title="지역", yaxis_title="범죄율 (인구 10만 명당)")
    st.plotly_chart(fig_region)
