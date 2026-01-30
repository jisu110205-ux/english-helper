import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO

# Page settings
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸")
st.title("🇺🇸 English Pronunciation Helper")

# --- Sidebar: IPA Guide (English Only) ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.write("Click buttons to hear sounds:")
    ipa_samples = {
        "Vowels (Short)": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Vowels (Long)": {"i:": "see", "u:": "blue", "a:": "father", "ɔ:": "door", "ɜ:": "bird"},
        "Diphthongs": {"eɪ": "say", "aɪ": "eye", "ɔɪ": "boy", "aʊ": "now", "oʊ": "go"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "dʒ": "jump", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }
    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button(symbol, key=f"btn_{symbol}"):
                    tts_symbol = gTTS(text=example, lang='en')
                    sound_fp = BytesIO()
                    tts_symbol.write_to_fp(sound_fp)
                    st.audio(sound_fp, format='audio/mp3')
            with col2:
                st.write(f"as in **{example}**")

# --- Main Screen: Line-by-Line Matching ---
input_text = st.text_area("Enter English Text:", height=150, placeholder="Type your sentences here.")

if st.button("Convert & Speak 🚀"):
    if input_text:
        # 문장 단위(마침표, 물음표 등)나 줄바꿈 단위로 나눕니다.
        # 여기서는 줄바꿈과 마침표를 기준으로 한 문장씩 처리합니다.
        sentences = input_text.replace('\n', '. ').split('. ')
        
        for sentence in sentences:
            clean_sentence = sentence.strip()
            if clean_sentence:
                # 1. 원문 출력
                st.markdown(f"#### {clean_sentence}")
                
                # 2. 바로 밑에 발음기호 출력 (회색 박스 형태)
                ipa_sentence = ipa.convert(clean_sentence)
                st.code(ipa_sentence, language=None)
                
                # 문장 사이 간격
                st.write("")

        # 전체 음성 듣기
        st.divider()
        st.write("▼ Listen to full text")
        sound_file = BytesIO()
        tts = gTTS(text=input_text, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)
    else:
        st.warning("Please enter some English text first!")