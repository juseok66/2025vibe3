import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도 만들기")
st.markdown("원하는 장소를 추가하고 지도를 북마크처럼 사용하세요!")

# 세션 상태로 북마크 리스트 저장
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 입력 폼
with st.form("bookmark_form"):
    name = st.text_input("장소 이름", placeholder="예: 한강공원")
    lat = st.number_input("위도 (Latitude)", format="%.6f")
    lon = st.number_input("경도 (Longitude)", format="%.6f")
    submitted = st.form_submit_button("📌 북마크 추가")

    if submitted:
        if name and lat and lon:
            st.session_state.bookmarks.append({"name": name, "lat": lat, "lon": lon})
            st.success(f"✅ '{name}' 이(가) 북마크에 추가되었습니다.")
        else:
            st.warning("모든 입력 항목을 채워주세요.")

# 지도 생성
# 기본 중심좌표: 북마크가 하나도 없으면 서울로
if st.session_state.bookmarks:
    center_lat = st.session_state.bookmarks[-1]["lat"]
    center_lon = st.session_state.bookmarks[-1]["lon"]
else:
    center_lat = 37.5665  # 서울
    center_lon = 126.9780

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# 북마크된 장소 마커로 표시
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=1000, height=600)

# 북마크 리스트 출력
st.markdown("### 📌 현재 북마크 목록")
if st.session_state.bookmarks:
    for i, bm in enumerate(st.session_state.bookmarks, 1):
        st.write(f"{i}. {bm['name']} ({bm['lat']}, {bm['lon']})")
else:
    st.write("아직 북마크가 없습니다.")
