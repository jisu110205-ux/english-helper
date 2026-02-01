import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64
import re  

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")
# 검색 기록을 저장할 바구니를 만들어요
if 'history' not in st.session_state:
    st.session_state.history = []
# 오디오 자동 재생을 위한 함수 (하얀 박스 방지)
def autoplay_audio(text):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    b64 = base64.b64encode(data.getvalue()).decode()
    footer_html = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
# 발음 기호를 예쁘게 꾸며주는 함수에요
def format_ipa(ipa_text):
    # 1. 점(.)을 중간 점( · )으로 바꿔서 보기 편하게 만들어요
    formatted = ipa_text.replace(".", " · ")
    # 2. 강세(')가 붙은 글자만 빨간색으로 만들어요
    formatted = re.sub(r"'([^ ·\s/]+)", r'<span style="color: #ff4757; font-weight: bold; font-size: 1.2em;">\1</span>', formatted)
    return formatted
st.title("🇺🇸 English Pronunciation Helper")

# --- 사이드바: IPA 가이드 ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    
    ipa_samples = {
        "Vowels": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Long & Diphthongs": {"i:": "see", "u:": "blue", "eɪ": "say", "aɪ": "eye", "oʊ": "go"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }

    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                # 버튼 클릭 시 하얀 박스 없이 소리만 재생
                if st.button(symbol, key=f"guide_{symbol}"):
                    autoplay_audio(example)
            with col2:
                st.caption(f"as in **{example}**")

# --- 메인 화면: 글자 기억 기능 ---
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# 입력창 (session_state와 연결되어 글자가 지워지지 않음)
input_text = st.text_area("Enter English Text:", value=st.session_state.text_input, height=150, key="main_input")
st.session_state.text_input = input_text

if st.button("Convert & Speak 🚀"):
        if input_text:
            # --- 히스토리 저장 ---
            if 'history' not in st.session_state:
                st.session_state.history = []
            if input_text not in st.session_state.history:
                st.session_state.history.insert(0, input_text)

            st.subheader("Original Text")
            st.write(input_text)
            st.divider()

            st.subheader("IPA Transcription")
            ipa_result = ipa.convert(input_text).replace("*", "") # 별표 제거

            # --- 강세 하이라이트 마법 ---
            formatted_ipa = ipa_result.replace(".", " · ") 
            formatted_ipa = re.sub(r"'([^ ·\s/]+)", r'<span style="color: #ff4757; font-weight: bold;">\1</span>', formatted_ipa)
            st.markdown(f"### {formatted_ipa}", unsafe_allow_html=True)

            # --- 오디오 재생 (선택한 속도로!) ---
            # 주의: speed_choice 변수는 버튼들 위에 st.radio로 미리 만들어둬야 해요!
            autoplay_audio(input_text, speed=speed_choice)

# --- 맨 마지막 줄 (사이드바 기록 보여주기) ---
st.sidebar.markdown("---")
st.sidebar.title("🕒 최근 검색 기록")
if 'history' in st.session_state:
    for word in st.session_state.history[:5]:
        st.sidebar.write(f"- {word}")
