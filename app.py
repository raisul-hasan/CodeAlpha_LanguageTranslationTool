import os
import requests
import streamlit as st
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

API_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
REGION = os.getenv("AZURE_TRANSLATOR_REGION")
ENDPOINT = os.getenv(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com"
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="LinguaAI Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "detected_language" not in st.session_state:
    st.session_state.detected_language = ""

if "translation_done" not in st.session_state:
    st.session_state.translation_done = False


# =========================================================
# CLEAR FUNCTION
# =========================================================

def clear_all():
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.detected_language = ""
    st.session_state.translation_done = False


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%,
        rgba(120, 70, 255, 0.30),
        transparent 30%),

        radial-gradient(circle at 90% 15%,
        rgba(0, 210, 255, 0.20),
        transparent 30%),

        radial-gradient(circle at 50% 95%,
        rgba(0, 255, 170, 0.10),
        transparent 30%),

        linear-gradient(
            135deg,
            #060914,
            #0c1123,
            #07101c
        );

    color: white;
}


.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* Main title */

h1 {
    text-align: center;

    font-size: 4rem !important;

    font-weight: 900 !important;

    letter-spacing: -2px;

    background:
        linear-gradient(
            90deg,
            #a16cff,
            #6577ff,
            #17d2ff,
            #32ffc0
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* Subtitle */

.subtitle-text {
    text-align: center;

    color: #aab6d6;

    font-size: 18px;

    margin-top: -15px;

    margin-bottom: 30px;
}


/* Border containers */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        rgba(16, 22, 43, 0.76);

    border:
        1px solid
        rgba(255,255,255,0.10) !important;

    border-radius:
        24px !important;

    padding:
        12px;

    box-shadow:
        0 25px 60px
        rgba(0,0,0,0.35);

    backdrop-filter:
        blur(18px);
}


/* Labels */

label {

    color:
        #dce5ff !important;

    font-weight:
        650 !important;
}


/* Select box */

div[data-baseweb="select"] > div {

    background:
        #12182d !important;

    color:
        white !important;

    border:
        1px solid
        #303b5b !important;

    border-radius:
        13px !important;

    min-height:
        48px;
}


div[data-baseweb="select"] > div:hover {

    border-color:
        #736cff !important;
}


/* Text area */

textarea {

    background:
        #11172b !important;

    color:
        white !important;

    border:
        1px solid
        #303a59 !important;

    border-radius:
        15px !important;

    font-size:
        16px !important;

    line-height:
        1.6 !important;
}


textarea:focus {

    border:
        1px solid
        #745cff !important;

    box-shadow:
        0 0 0 1px
        #745cff !important;
}


/* Buttons */

.stButton > button {

    width:
        100%;

    min-height:
        50px;

    border-radius:
        14px;

    border:
        1px solid
        rgba(255,255,255,0.10);

    background:
        linear-gradient(
            90deg,
            #8157ff,
            #526fff,
            #00bee9
        );

    color:
        white !important;

    font-size:
        16px;

    font-weight:
        700;

    box-shadow:
        0 10px 30px
        rgba(80,90,255,0.30);

    transition:
        0.25s ease;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 15px 40px
        rgba(70,110,255,0.45);
}


/* Badge style */

.badge-box {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid
        rgba(255,255,255,0.08);

    border-radius:
        14px;

    padding:
        10px;

    text-align:
        center;

    color:
        #c9d4f2;

    font-size:
        14px;
}


/* Footer */

.footer-text {

    text-align:
        center;

    color:
        #687695;

    font-size:
        13px;

    line-height:
        1.8;

    margin-top:
        35px;
}


#MainMenu {
    visibility: hidden;
}


footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# LANGUAGES
# =========================================================

languages = {
    "Auto Detect": None,
    "English": "en",
    "Bengali": "bn",
    "Hindi": "hi",
    "Urdu": "ur",
    "Arabic": "ar",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-Hans",
    "Turkish": "tr",
    "Dutch": "nl",
    "Swedish": "sv",
    "Polish": "pl",
    "Thai": "th",
    "Vietnamese": "vi"
}


target_languages = {
    name: code
    for name, code in languages.items()
    if code is not None
}


# =========================================================
# TRANSLATION FUNCTION
# =========================================================

def translate_text(
    text,
    source_language,
    target_language
):

    if not API_KEY:
        raise RuntimeError(
            "Azure Translator API key is missing."
        )

    url = (
        ENDPOINT.rstrip("/")
        + "/translate"
    )

    params = {
        "api-version": "3.0",
        "to": target_language
    }

    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key":
            API_KEY,

        "Content-Type":
            "application/json"
    }

    if REGION:
        headers[
            "Ocp-Apim-Subscription-Region"
        ] = REGION

    body = [
        {
            "Text": text
        }
    ]

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=body,
        timeout=20
    )

    if response.status_code == 401:
        raise RuntimeError(
            "Azure rejected your API key."
        )

    elif response.status_code == 403:
        raise RuntimeError(
            "Access to Azure Translator was denied."
        )

    elif response.status_code == 429:
        raise RuntimeError(
            "Translation request limit reached. "
            "Please try again later."
        )

    elif response.status_code >= 500:
        raise RuntimeError(
            "Azure Translator is temporarily unavailable."
        )

    elif response.status_code != 200:
        raise RuntimeError(
            f"Translator returned error "
            f"{response.status_code}."
        )

    data = response.json()

    translated_text = (
        data[0]
        ["translations"]
        [0]
        ["text"]
    )

    detected_language = (
        data[0]
        .get(
            "detectedLanguage",
            {}
        )
        .get(
            "language",
            ""
        )
    )

    return (
        translated_text,
        detected_language
    )


# =========================================================
# HEADER
# NO HTML USED HERE
# =========================================================

st.title("🌍 LinguaAI")

st.markdown(
    """
<p class="subtitle-text">
Smart, fast and secure AI-powered language translation
</p>
""",
    unsafe_allow_html=True
)


# =========================================================
# FEATURE BADGES
# =========================================================

badge1, badge2, badge3, badge4, badge5 = (
    st.columns(5)
)

with badge1:
    st.markdown(
        """
<div class="badge-box">
⚡ Fast Translation
</div>
""",
        unsafe_allow_html=True
    )

with badge2:
    st.markdown(
        """
<div class="badge-box">
🌎 20+ Languages
</div>
""",
        unsafe_allow_html=True
    )

with badge3:
    st.markdown(
        """
<div class="badge-box">
🤖 AI Powered
</div>
""",
        unsafe_allow_html=True
    )

with badge4:
    st.markdown(
        """
<div class="badge-box">
🔐 Secure Azure
</div>
""",
        unsafe_allow_html=True
    )

with badge5:
    st.markdown(
        """
<div class="badge-box">
✨ Auto Detect
</div>
""",
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# MAIN TRANSLATOR
# =========================================================

with st.container(border=True):

    st.subheader(
        "🌐 Translate your text"
    )

    source_col, target_col = (
        st.columns(2)
    )

    with source_col:

        source_language = (
            st.selectbox(
                "Translate From",
                options=list(
                    languages.keys()
                ),
                index=0
            )
        )

    with target_col:

        target_language = (
            st.selectbox(
                "Translate To",
                options=list(
                    target_languages.keys()
                ),
                index=1
            )
        )


    text = st.text_area(
        "Enter Text",
        height=190,
        max_chars=5000,
        placeholder=(
            "Type or paste your text here...\n\n"
            "Example: Artificial Intelligence "
            "is changing the world."
        ),
        key="input_text"
    )


    st.caption(
        f"{len(text)} / 5000 characters"
    )


    translate_col, clear_col = (
        st.columns([3, 1])
    )


    with translate_col:

        translate_button = (
            st.button(
                "✨ Translate Now",
                use_container_width=True,
                type="primary"
            )
        )


    with clear_col:

        st.button(
            "🗑️ Clear",
            use_container_width=True,
            on_click=clear_all
        )


# =========================================================
# TRANSLATE
# =========================================================

if translate_button:

    if not text.strip():

        st.warning(
            "Please enter some text first."
        )


    elif (
        source_language
        !=
        "Auto Detect"
        and
        languages[source_language]
        ==
        target_languages[
            target_language
        ]
    ):

        st.warning(
            "Source and target languages "
            "must be different."
        )


    elif not API_KEY:

        st.error(
            "Azure Translator API key "
            "was not found."
        )

        st.info(
            "Check the .env file "
            "and restart the app."
        )


    else:

        with st.spinner(
            "Translating..."
        ):

            try:

                translated_text, detected = (
                    translate_text(
                        text.strip(),
                        languages[
                            source_language
                        ],
                        target_languages[
                            target_language
                        ]
                    )
                )

                st.session_state[
                    "translated_text"
                ] = translated_text

                st.session_state[
                    "detected_language"
                ] = detected

                st.session_state[
                    "translation_done"
                ] = True


            except (
                requests.exceptions.Timeout
            ):

                st.error(
                    "The translation service "
                    "took too long to respond."
                )


            except (
                requests.exceptions.ConnectionError
            ):

                st.error(
                    "Unable to connect "
                    "to Azure Translator."
                )


            except RuntimeError as error:

                st.error(
                    str(error)
                )


            except Exception:

                st.error(
                    "Something unexpected "
                    "happened during translation."
                )


# =========================================================
# RESULT
# NO CUSTOM HTML USED
# =========================================================

if (
    st.session_state.translation_done
    and
    st.session_state.translated_text
):

    st.write("")

    with st.container(border=True):

        st.subheader(
            "✨ Translation Result"
        )

        st.write(
            st.session_state.translated_text
        )

        if (
            source_language
            ==
            "Auto Detect"
            and
            st.session_state.detected_language
        ):

            st.info(
                "Detected Language: "
                +
                st.session_state
                .detected_language
                .upper()
            )

        st.success(
            "Translation completed successfully."
        )


# =========================================================
# INFORMATION SECTION
# =========================================================

st.write("")

with st.container(border=True):

    st.subheader(
        "💡 How LinguaAI Works"
    )

    st.write(
        """
Enter or paste your text, select the source
and target languages, and click **Translate Now**.

LinguaAI sends the text securely to
**Microsoft Azure Translator** and displays
the translated result.

If you do not know the original language,
choose **Auto Detect**.
"""
    )


# =========================================================
# FOOTER
# NO RAW HTML STRUCTURE
# =========================================================

st.divider()

st.markdown(
    """
<p class="footer-text">

🌍 <b>Language Translation Tool</b>

<br>



<br>

Powered by Microsoft Azure Translator

</p>
""",
    unsafe_allow_html=True
)