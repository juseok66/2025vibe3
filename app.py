import streamlit as st
import folium
from streamlit_folium import st_folium
from urllib.parse import parse_qs

st.set_page_config(page_title="📍 나만의 북마크 지도", layout="wide")
st.title("📍 나만의 북마크 지도 만들기")

# 기본 북마크 (광화문, 서울시청, 광주시청)
DEFAULT_BOOKMARKS = [
    {"name": "광화문", "lat": 37.5759, "lon": 126.9769},
    {"name": "서울시청", "lat": 37.5663, "lon": 126.9779},
    {"name": "광주시청", "lat": 35.1595, "lon": 126.8526}
]

# URL 쿼리 파라미터 처리
query_params = st.query_params
load_default = query_params.get("default") == "true"

# 북마크 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
    if load_default:
        st.session_state.bookmarks.extend(DEFAULT_BOOKMARKS)

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
    center_lat = 37.5665  # 서울
    center_lon = 126.9780

# 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=1000, height=600)

# 북마크 목록 출력
st.markdown("### 📌 현재 북마크 목록")
if st.session_state.bookmarks:
    for i, bm in enumerate(st.session_state.bookmarks, 1):
        st.write(f"{i}. {bm['name']} ({bm['lat']}, {bm['lon']})")
else:
    st.info("아직 북마크가 없습니다.")

# 초기화 버튼
if st.button("🔄 북마크 전체 초기화"):
    st.session_state.bookmarks.clear()
    st.success("북마크가 초기화되었습니다!")

# 사용 안내
st.markdown("---")
st.markdown("🔗 북마크 자동 등록 링크 예시:")
st.code("http://localhost:8501/?default=true", language="url")
st.caption("실제 배포 시에는 위 주소에서 'localhost' 부분을 당신의 URL로 바꾸세요.")

