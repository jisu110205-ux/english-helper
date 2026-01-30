import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO

# Page Settings
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸")
st.title("🇺🇸 English Pronunciation Helper")

# --- Sidebar: English-Only IPA Guide ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.write("Click to hear the sounds of these symbols:")

    # Detailed IPA categories without Korean descriptions
    ipa_samples = {
        "Vowels (Short)": {
            "æ": "apple", "ɛ": "bed", "ɪ": "sit",
            "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"
        },
        "Vowels (Long)": {
            "i:": "see", "u:": "blue", "a:": "father", "ɔ:": "door", "ɜ:": "bird"
        },
        "Diphthongs (Double)": {
            "eɪ": "say", "aɪ": "eye", "ɔɪ": "boy", "aʊ": "now", "oʊ": "go"
        },
        "Consonants": {
            "ʃ": "ship", "tʃ": "chair", "dʒ": "jump", "θ": "thin", 
            "ð": "this", "ŋ": "sing", "ʒ": "vision", "j": "yes"
        }
    }

    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                # Unique key for each button
                if st.button(symbol, key=f"btn_{symbol}"):
                    tts_symbol = gTTS(text=example, lang='en')
                    sound_fp = BytesIO()
                    tts_symbol.write_to_fp(sound_fp)
                    st.audio(sound_fp, format='audio/mp3')
            with col2:
                st.write(f"as in **{example}**")

# --- Main Screen: English Match ---
input_text = st.text_area("Enter English Text:", height=150, placeholder="Hello! Type your sentences here.")

if st.button("Convert & Speak 🚀"):
    if input_text:
        lines = input_text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                # Get IPA conversion
                ipa_line = ipa.convert(line)
                
                # Display: Text followed by IPA box immediately
                st.markdown(f"**{line}**")
                st.code(ipa_line, language=None)
                st.write("")

        # Audio player for the entire text
        sound_file = BytesIO()
        tts = gTTS(text=input_text, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)
    else:
        st.warning("Please enter some English text first!")