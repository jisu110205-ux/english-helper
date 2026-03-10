import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64
import time

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# 화면 어디에서도 보이지 않는 곳에 소리를 재생시키는 함수
def play_sound_hidden(text, key):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    b64 = base64.b64encode(data.getvalue()).decode()
    # 이 HTML 코드가 버튼들 사이에 끼어들지 않도록 독립된 위치에 띄웁니다.
    audio_html = f"""
        <audio autoplay="true" id="aud_{key}_{int(time.time())}" style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    # st.empty()를 활용하거나 하단에 배치하여 틈새 발생 방지
    st.components.v1.html(audio_html, height=0, width=0)

st.title("🇺🇸 English Pronunciation Helper")

# --- 데이터 유지 설정 ---
if "input_txt" not in st.session_state: st.session_state.input_txt = ""
if "ipa_out" not in st.session_state: st.session_state.ipa_out = ""

# --- 사이드바: 틈새 제로 가이드 ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.caption("Click to hear sounds (No shifts!)")
    
    ipa_samples = {
        "Vowels": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Long/Diphthongs": {"i:": "see", "u:": "blue", "eɪ": "say", "aɪ": "eye", "oʊ": "go"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }

    for category, symbols in ipa_samples.items():
        st.markdown(f"#### {category}")
        # 버튼들 사이의 간격을 고정하기 위해 HTML 스타일 사용
        for symbol, example in symbols.items():
            cols = st.columns([1, 3])
            with cols[0]:
                if st.button(symbol, key=f"btn_{symbol}"):
                    play_sound_hidden(example, symbol)
            with cols[1]:
                # 텍스트 높이를 버튼과 맞춰서 틈새가 안 느껴지게 함
                st.markdown(f"<div style='line-height:2.5;'>as in <b>{example}</b></div>", unsafe_allow_html=True)

def highlight_stress(text):
    # eng_to_ipa는 강세가 있는 음절 앞에 ' 기호를 붙입니다.
    # 이를 시각적으로 강조하기 위해 스타일링을 적용합니다.
    ipa_text = ipa.convert(text)
    # 강세 기호(') 뒤의 글자를 강조하는 로직 (단순 구현 예시)
    highlighted = ipa_text.replace("'", "<span style='color:red; font-weight:bold; font-size:1.2em;'>'</span>")
    return highlighted

# --- 메인 화면 ---

user_input = st.text_area("Enter English Text:", value=st.session_state.input_txt, height=150)
st.session_state.input_txt = user_input



if st.button("Convert & Speak 🚀"):
    if user_input:
        st.session_state.ipa_out = ipa.convert(user_input)


if st.session_state.ipa_out:
    st.subheader("Original Text")
    st.write(st.session_state.input_txt)
    st.divider()
    st.subheader("IPA Transcription")
    st.info(st.session_state.ipa_out)

    
    # 메인 음성 플레이어 (이건 위치 고정이라 괜찮습니다)
    snd = BytesIO()
    gTTS(text=st.session_state.input_txt, lang='en').write_to_fp(snd)
    st.audio(snd) 

# ... 기존 임포트 및 함수들 ...
import librosa
import matplotlib.pyplot as plt

def plot_pitch(audio_bytes):
    # librosa는 파일 경로뿐만 아니라 BytesIO 객체도 읽을 수 있습니다.
    y, sr = librosa.load(audio_bytes)
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), 
                                                fmax=librosa.note_to_hz('C7'))
    times = librosa.times_like(f0)
    fig, ax = plt.subplots(figsize=(10, 3)) # 사이드바와 조화를 위해 높이 조절
    ax.plot(times, f0, color='#FF4B4B', linewidth=2) # Streamlit 테마색 추천
    ax.set_ylim(0, 400) 
    ax.axis('off') # 깔끔하게 선만 보여주고 싶을 때 사용
    return fig

# --- 메인 화면 결과 출력 부분 ---
if st.session_state.ipa_out:
    st.subheader("IPA Transcription")
    st.info(st.session_state.ipa_out)
    
    # 1. 음성 생성
    snd = BytesIO()
    gTTS(text=st.session_state.input_txt, lang='en').write_to_fp(snd)
    
    # 2. 오디오 플레이어
    st.audio(snd)
    
    # 3. 피치 그래프 분석 (추가된 부분)
    with st.expander("📈 상세 억양 곡선(Intonation) 보기"):
        snd.seek(0) # 포인터를 처음으로 되돌리는 것이 핵심!
        with st.spinner("Analyzing pitch..."):
            fig = plot_pitch(snd)
            st.pyplot(fig)
        st.caption("위 곡선의 흐름을 따라 발음해 보세요. 높낮이가 변하는 지점이 핵심 강세 구간입니다.")
