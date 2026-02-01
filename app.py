import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# 버튼 디자인과 간격을 위한 CSS (틈새 방지)
st.markdown("""
    <style>
    .ipa-row {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        height: 40px; /* 높이 고정으로 틈새 방지 */
    }
    .ipa-btn {
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 6px 12px;
        cursor: pointer;
        font-weight: bold;
        min-width: 50px;
        text-align: center;
        margin-right: 15px;
        transition: 0.2s;
    }
    .ipa-btn:hover {
        background-color: #e0e2e6;
    }
    .example-text {
        font-size: 14px;
        color: #31333F;
    }
    </style>
""", unsafe_allow_html=True)

def get_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    return base64.b64encode(data.getvalue()).decode()

st.title("🇺🇸 English Pronunciation Helper")

# --- 글자 기억 장치 (새로고침 시 데이터 보존) ---
if "user_text" not in st.session_state: st.session_state.user_text = ""
if "ipa_output" not in st.session_state: st.session_state.ipa_output = ""

# --- 사이드바: 디자인 복구 및 고정 ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.write("Click to hear example sounds:")

    ipa_samples = {
        "Vowels (Short)": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Vowels (Long)": {"i:": "see", "u:": "blue", "a:": "father", "ɔ:": "door"},
        "Diphthongs": {"eɪ": "say", "aɪ": "eye", "ɔɪ": "boy", "aʊ": "now", "oʊ": "go"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }

    for category, symbols in ipa_samples.items():
        st.markdown(f"### {category}")
        for symbol, example in symbols.items():
            audio_b64 = get_audio_base64(example)
            
            # 레이아웃을 HTML로 고정하여 버튼 클릭 시에도 틈이 생기지 않음
            # 마우스 올리는거 아니고 '클릭'할 때만 소리납니다!
            st.components.v1.html(f"""
                <div class="ipa-row">
                    <div class="ipa-btn" onclick="new Audio('data:audio/mp3;base64,{audio_b64}').play()">
                        {symbol}
                    </div>
                    <span class="example-text">as in <b>{example}</b></span>
                </div>
            """, height=45)

# --- 메인 화면 ---
# 입력창에 session_state를 연결하여 글자가 안 지워지게 함
text_input = st.text_area("Enter English Text:", value=st.session_state.user_text, height=150)
st.session_state.user_text = text_input

if st.button("Convert & Speak 🚀"):
    if text_input:
        st.session_state.ipa_output = ipa.convert(text_input)

# 결과 출력 영역 (사이드바 버튼 눌러도 절대 안 사라짐)
if st.session_state.ipa_output:
    st.subheader("Original Text")
    st.write(st.session_state.user_text)
    
    st.divider()
    
    st.subheader("IPA Transcription")
    st.info(st.session_state.ipa_output)
    
    # 전체 음성 듣기
    sound_data = BytesIO()
    gTTS(text=st.session_state.user_text, lang='en').write_to_fp(sound_data)
    st.audio(sound_data)
