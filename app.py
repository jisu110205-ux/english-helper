import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# 소리 재생 함수 (하얀 박스 방지)
def play_audio(text):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    b64 = base64.b64encode(data.getvalue()).decode()
    st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

st.title("🇺🇸 English Pronunciation Helper")

# --- 기억 장치(Session State) 초기화 ---
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "ipa_result" not in st.session_state:
    st.session_state.ipa_result = ""

# --- 사이드바: 가이드 ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    ipa_samples = {
        "Vowels": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot"},
        "Long/Diphthongs": {"i:": "see", "u:": "blue", "eɪ": "say", "aɪ": "eye"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this"}
    }
    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button(symbol, key=f"s_{symbol}"):
                    play_audio(example)
            with col2:
                st.caption(f"as in **{example}**")

# --- 메인 화면 ---
# 입력창: 입력하는 즉시 기억함
user_input = st.text_area("Enter English Text:", value=st.session_state.input_text, height=150)
st.session_state.input_text = user_input

if st.button("Convert & Speak 🚀"):
    if user_input:
        # 변환 결과를 기억 장치에 저장
        st.session_state.ipa_result = ipa.convert(user_input)

# 기억된 결과가 있다면 화면에 계속 보여줌 (버튼 클릭 시에도 유지됨)
if st.session_state.ipa_result:
    st.subheader("Original Text")
    st.write(st.session_state.input_text)
    
    st.divider()
    
    st.subheader("IPA Transcription")
    st.info(st.session_state.ipa_result) # 이 부분이 이제 안 사라집니다!
    
    # 전체 음성 듣기
    sound_file = BytesIO()
    tts_main = gTTS(text=st.session_state.input_text, lang='en')
    tts_main.write_to_fp(sound_file)
    st.audio(sound_file)
