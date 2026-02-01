import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64
import time

# 1. 페이지 설정 및 레이아웃 고정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# 배경에서 소리를 재생하는 마법의 함수 (연속 클릭 가능)
def play_sound(text, key):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    b64 = base64.b64encode(data.getvalue()).decode()
    # 고유한 ID를 가진 오디오 태그를 생성하여 연속 클릭 시에도 소리가 나게 함
    audio_html = f"""
        <audio autoplay="true" id="audio_{key}_{int(time.time())}">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(audio_html, height=0, width=0)

st.title("🇺🇸 English Pronunciation Helper")

# --- 저장 장치 설정 (글자 사라짐 방지) ---
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "ipa_result" not in st.session_state:
    st.session_state.ipa_result = ""

# --- 사이드바: 버튼 간격 고정 ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.caption("Click symbols to hear sounds immediately.")
    
    ipa_samples = {
        "Vowels": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot"},
        "Long/Diphthongs": {"i:": "see", "u:": "blue", "eɪ": "say", "aɪ": "eye"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this"}
    }

    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            # 버튼과 텍스트를 한 줄에 배치하고 간격 고정
            col1, col2 = st.columns([1, 2])
            with col1:
                # 버튼을 눌러도 아래에 아무것도 생기지 않음 (height=0 처리)
                if st.button(symbol, key=f"btn_{symbol}"):
                    play_sound(example, symbol)
            with col2:
                st.markdown(f"<p style='margin-top:10px;'>as in <b>{example}</b></p>", unsafe_allow_html=True)

# --- 메인 화면: 결과 유지 ---
user_input = st.text_area("Enter English Text:", value=st.session_state.input_text, height=150)
st.session_state.input_text = user_input

if st.button("Convert & Speak 🚀"):
    if user_input:
        st.session_state.ipa_result = ipa.convert(user_input)

# 변환된 결과 출력 (절대 사라지지 않음)
if st.session_state.ipa_result:
    st.subheader("Original Text")
    st.write(st.session_state.input_text)
    
    st.divider()
    
    st.subheader("IPA Transcription")
    st.info(st.session_state.ipa_result)
    
    # 전체 음성 재생 (메인은 플레이어 노출)
    sound_file = BytesIO()
    tts_main = gTTS(text=st.session_state.input_text, lang='en')
    tts_main.write_to_fp(sound_file)
    st.audio(sound_file)
