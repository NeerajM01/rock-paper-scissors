import streamlit as st
import random
import base64

# --- Constants ---
RUPEE_SYMBOL = u"\u20B9"
CHOICES = {'r': '🪨 Rock', 'p': '📄 Paper', 's': '✂️ Scissors'}

# --- Game State (Session Variables) ---
if "balance" not in st.session_state:
    st.session_state.balance = 0.0
if "user_wins" not in st.session_state:
    st.session_state.user_wins = 0
if "comp_wins" not in st.session_state:
    st.session_state.comp_wins = 0
if "bet" not in st.session_state:
    st.session_state.bet = 0.0

# --- Page Setup ---
st.set_page_config(page_title="Rock Paper Scissors Deluxe", page_icon="🎮", layout="centered")
st.title("🪨📄✂️ Rock Paper Scissors Deluxe")
st.markdown("#### Play the classic game with a modern twist and some flair!")

# --- Function to Play Sound ---
def play_sound(sound_type):
    if sound_type == "win":
        sound_url = "https://actions.google.com/sounds/v1/crowds/cheer.ogg"
    elif sound_type == "lose":
        sound_url = "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg"
    else:
        sound_url = "https://actions.google.com/sounds/v1/cartoon/pop.ogg"

    st.markdown(
        f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# --- Betting Section ---
if st.session_state.bet == 0.0:
    bet_input = st.number_input(f"💰 Enter your bet amount ({RUPEE_SYMBOL}):", min_value=1.0, step=1.0)
    if st.button("Start Game"):
        st.session_state.bet = bet_input
        st.session_state.balance = bet_input
        st.success(f"Starting Balance: {RUPEE_SYMBOL}{st.session_state.balance:.2f}")

# --- Game Play Section ---
else:
    st.markdown(f"**Current Balance:** {RUPEE_SYMBOL}{st.session_state.balance:.2f}")
    st.progress(min(st.session_state.balance / 1000, 1.0))
    st.markdown(f"**Score:** 🧍 You - {st.session_state.user_wins} | 🤖 Computer - {st.session_state.comp_wins}")

    st.markdown("---")
    st.markdown("### Choose your move:")

    cols = st.columns(3)
    user_choice = None
    with cols[0]:
        if st.button("🪨 Rock", use_container_width=True):
            user_choice = 'r'
    with cols[1]:
        if st.button("📄 Paper", use_container_width=True):
            user_choice = 'p'
    with cols[2]:
        if st.button("✂️ Scissors", use_container_width=True):
            user_choice = 's'

    if user_choice:
        comp_choice = random.choice(list(CHOICES.keys()))
        result_text = f"You chose {CHOICES[user_choice]} | Computer chose {CHOICES[comp_choice]}"

        if user_choice == comp_choice:
            result = "🤝 It's a Tie!"
            animation = "neutral"
        elif (user_choice == 'r' and comp_choice == 's') or \
             (user_choice == 'p' and comp_choice == 'r') or \
             (user_choice == 's' and comp_choice == 'p'):
            result = "🎉 You Won! Your bet doubled!"
            st.session_state.balance *= 2
            st.session_state.user_wins += 1
            animation = "win"
        else:
            result = "💀 You Lost! Half your bet lost!"
            st.session_state.balance /= 2
            st.session_state.comp_wins += 1
            animation = "lose"

        st.markdown(f"### {result_text}")
        st.markdown(f"#### {result}")
        st.markdown(f"**New Balance:** {RUPEE_SYMBOL}{st.session_state.balance:.2f}")
        st.progress(min(st.session_state.balance / 1000, 1.0))

        # 🎵 Play sound + animation
        play_sound(animation)
        if animation == "win":
            st.balloons()
        elif animation == "lose":
            st.markdown(
                "<div style='animation: shake 0.3s; color:#ff4b4b; font-size:20px;'>😵</div>"
                "<style>@keyframes shake {0%,100%{transform:translateX(0);}25%{transform:translateX(-10px);}75%{transform:translateX(10px);}}</style>",
                unsafe_allow_html=True,
            )
        elif animation == "neutral":
            st.markdown("<div style='animation: pulse 1s infinite; color:#cccccc;'>😐</div>"
                        "<style>@keyframes pulse {0%,100%{opacity:1;}50%{opacity:0.5;}}</style>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔁 Restart Game"):
            st.session_state.bet = 0.0
            st.session_state.balance = 0.0
            st.session_state.user_wins = 0
            st.session_state.comp_wins = 0
            st.experimental_rerun()
    with col2:
        if st.button("🏁 New Round"):
            st.experimental_rerun()
    with col3:
        if st.button("❌ Quit"):
            st.balloons()
            st.warning(f"**Final Results:**\n\n🧍 You: {st.session_state.user_wins}\n🤖 Computer: {st.session_state.comp_wins}\n💰 Final Balance: {RUPEE_SYMBOL}{st.session_state.balance:.2f}")
            st.session_state.bet = 0.0
            st.stop()
