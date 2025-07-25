import streamlit as st
import folium
from streamlit_folium import st_folium

# 설정
st.set_page_config(page_title="📍 나만의 북마크 지도", layout="wide")
st.title("📍 나만의 북마크 지도 만들기")

# 기본 북마크 목록
DEFAULT_BOOKMARKS = [
    {"name": "광화문", "lat": 37.5759, "lon": 126.9769},
    {"name": "서울시청", "lat": 37.5663, "lon": 126.9779},
    {"name": "광주시청", "lat": 35.1595, "lon": 126.8526}
]

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 🚨 핵심: 첫 로딩 시 query param 검사 -> 다음 렌더링에서 북마크 적용
if "default_loaded" not in st.session_state:
    st.session_state.default_loaded = False
    st.session_state.needs_reload = False  # 렌더링 1번 더 하기 위함

# URL 파라미터 확인
if not st.session_state.default_loaded:
    if st.query_params.get("default") == "true":
        st.session_state.bookmarks.extend(DEFAULT_BOOKMARKS)
        st.session_state.default_loaded = True
        st.session_state.needs_reload = True  # 강제 리렌더

# 강제 리렌더링
if st.session_state.needs_reload:
    st.session_state.needs_reload = False
    st.experimental_rerun()

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
            st.warning("⚠️ 장소 이름과 좌표를 모두 입력해주세요.")

# 지도 중심
if st.session_state.bookmarks:
    center_lat = st.session_state.bookmarks[-1]["lat"]
    center_lon = st.session_state.bookmarks[-1]["lon"]
else:
    center_lat = 37.5665
    center_lon = 126.9780

# Folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_folium(_
