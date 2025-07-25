import streamlit as st
import folium
from streamlit_folium import st_folium
import urllib.parse
import json

st.set_page_config(page_title="📍 나만의 북마크 지도", layout="wide")
st.title("📍 나만의 북마크 지도 만들기")

# 기본 북마크
DEFAULT_BOOKMARKS = [
    {"name": "광화문", "lat": 37.5759, "lon": 126.9769},
    {"name": "서울시청", "lat": 37.5663, "lon": 126.9779},
    {"name": "광주시청", "lat": 35.1595, "lon": 126.8526},
]

# URL에서 bookmarks 파라미터 확인
query_bookmarks_raw = st.query_params.get("bookmarks", "")
loaded_from_url = False
if query_bookmarks_raw:
    try:
        decoded = urllib.parse.unquote(query_bookmarks_raw)
        url_bookmarks = json.loads(decoded)
        if isinstance(url_bookmarks, list):
            st.session_state.bookmarks = url_bookmarks
            loaded_from_url = True
    except Exception as e:
        st.warning("❌ 북마크 링크를 불러오는 데 실패했습니다.")

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = DEFAULT_BOOKMARKS.copy()

# 북마크 추가 폼
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
            st.warning("⚠️ 장소 이름과 좌표를 모두 입력해주세요.")

# 지도 중심
if st.session_state.bookmarks:
    center_lat = st.session_state.bookmarks[-1]["lat"]
    center_lon = st.session_state.bookmarks[-1]["lon"]
else:
    center_lat, center_lon = 37.5665, 126.9780

# 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["name"],
        icon=folium.Icon(color="blue",

