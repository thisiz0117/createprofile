import streamlit as st
import requests # API 요청을 보내기 위한 라이브러리
import json     # JSON 데이터를 다루기 위한 라이브러리

# Streamlit 페이지 설정
st.set_page_config(
    page_title="랜덤 사용자 프로필 생성기",
    page_icon="🧑‍💻",
    layout="centered"
)

# --- API 호출 함수 ---
# API에서 데이터를 가져와 파이썬 딕셔너리로 변환하는 함수
# st.cache_data: 동일한 입력에 대해 결과를 캐싱하여 불필요한 API 호출을 줄여줍니다.
@st.cache_data
def get_random_user():
    """Random User Generator API를 호출하여 사용자 데이터를 가져옵니다."""
    url = "https://randomuser.me/api/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API 호출 중 오류가 발생했습니다: {e}")
        return None

# --- 메인 앱 구성 ---

st.title("🧑‍💻 랜덤 사용자 프로필 생성기")
st.write("디자인 목업이나 테스트 데이터가 필요할 때 유용한 가상 사용자 프로필을 생성합니다.")

# 세션 상태(Session State)를 사용하여 사용자 데이터를 저장합니다.
# 이렇게 하면 버튼을 누르지 않아도 페이지가 새로고침 될 때 데이터가 유지됩니다.
if 'user_data' not in st.session_state:
    st.session_state.user_data = get_random_user()

# '새 프로필 생성' 버튼
if st.button("새 프로필 생성하기 🚀"):
    # 캐시를 지우고 새로운 데이터를 가져옵니다.
    get_random_user.clear()
    st.session_state.user_data = get_random_user()
    st.rerun() # 페이지를 새로고침하여 즉시 변경사항을 반영합니다.

# 사용자 데이터가 정상적으로 로드되었는지 확인 후 화면에 표시합니다.
if st.session_state.user_data and 'results' in st.session_state.user_data:
    user = st.session_state.user_data['results'][0]
    
    # 두 개의 컬럼으로 레이아웃을 나눕니다.
    col1, col2 = st.columns([1, 2]) # 비율을 1:2로 설정

    with col1:
        # 프로필 이미지
        profile_picture = user['picture']['large']
        st.image(profile_picture, width=150, caption="프로필 사진")

    with col2:
        # 사용자 기본 정보
        name = f"{user['name']['title']}. {user['name']['first']} {user['name']['last']}"
        st.header(name)
        
        email = user['email']
        st.write(f"**✉️ 이메일:** {email}")
        
        phone = user['phone']
        st.write(f"**📞 전화번호:** {phone}")

        location = f"{user['location']['city']}, {user['location']['country']}"
        st.write(f"**📍 위치:** {location}")

    st.divider() # 시각적인 구분을 위한 라인

    # 추가 정보 (접을 수 있는 형태로 제공)
    with st.expander("전체 데이터 보기 (JSON)"):
        st.json(st.session_state.user_data)
    
    # 다운로드 버튼
    # 생성된 데이터를 JSON 문자열로 변환합니다.
    json_string = json.dumps(st.session_state.user_data, indent=2)
    st.download_button(
        label="📥 JSON 데이터 다운로드",
        data=json_string,
        file_name=f"random_user_{user['login']['username']}.json",
        mime="application/json"
    )
else:
    st.warning("사용자 데이터를 불러오는 데 실패했습니다. 다시 시도해 주세요.")