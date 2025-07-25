import streamlit as st

# folium 관련 패키지 불러오기 (없을 경우 안내)
try:
    import folium
    from streamlit_folium import st_folium
except ModuleNotFoundError:
    st.error("❗ 필수 라이브러리 `folium`, `streamlit-folium`이 설치되어 있지 않습니다.")
    st.info("아래 명령어를 터미널에 입력해서 설치해주세요:")
    st.code("pip install folium streamlit-folium")
    st.stop()

# 페이지 기본 설정
st.set_page_config(page_title="나만의 북마크 지도", layout="wide")
st.title("📍 나만의 북마크 지도 만들기")
st.markdown("원하는 장소를 입력하고 지도에 북마크를 추가해보세요!")

# 세션 상태 초기화
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
            st.warning("⚠️ 장소 이름과 좌표를 모두 입력해주세요.")

# 지도 중심좌표 설정
if st.session_state.bookmarks:
    center_lat = st.session_state.bookmarks[-1]["lat"]
    center_lon = st.session_state.bookmarks[-1]["lon"]
else:
    center_lat = 37.5665  # 서울 위도
    center_lon = 126.9780  # 서울 경도

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
st_folium(m, width=1000, height=600)

# 북마크 목록 출력
st.markdown("### 📌 현재 북마크 목록")
if st.session_state.bookmarks:
    for i, bm in enumerate(st.session_state.bookmarks, 1):
        st.write(f"{i}. {bm['name']} ({bm['lat']}, {bm['lon']})")
else:
    st.info("북마크가 아직 없습니다.")

# 초기화 버튼
if st.button("🔄 북마크 전체 초기화"):
    st.session_state.bookmarks.clear()
    st.success("북마크가 초기화되었습니다!")
