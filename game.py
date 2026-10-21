import streamlit as st
import random

# --- Constants ---
RUPEE_SYMBOL = "\u20B9"
CHOICES = {'r': '🪨 Rock', 'p': '📄 Paper', 's': '✂️ Scissors'}
BEATS = {'r': 's', 'p': 'r', 's': 'p'}  # key beats value

# --- Page Setup (must be the first Streamlit command) ---
st.set_page_config(page_title="Rock Paper Scissors Deluxe", page_icon="🎮", layout="centered")

# --- Game State (Session Variables) ---
defaults = {"balance": 0.0, "user_wins": 0, "comp_wins": 0, "bet": 0.0}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("🪨📄✂️ Rock Paper Scissors Deluxe")
st.markdown("#### Play the classic game with a modern twist and some flair!")


def play_sound(sound_type):
    urls = {
        "win": "https://actions.google.com/sounds/v1/crowds/cheer.ogg",
        "lose": "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg",
    }
    sound_url = urls.get(sound_type, "https://actions.google.com/sounds/v1/cartoon/pop.ogg")
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True,
    )


def reset_game():
    for key, value in defaults.items():
        st.session_state[key] = value


# --- Betting Section ---
if st.session_state.bet == 0.0:
    bet_input = st.number_input(f"💰 Enter your bet amount ({RUPEE_SYMBOL}):", min_value=1.0, step=1.0)
    if st.button("Start Game"):
        st.session_state.bet = bet_input
        st.session_state.balance = bet_input
        st.rerun()  # switch to the game screen immediately

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
        elif BEATS[user_choice] == comp_choice:
            result = "🎉 You Won! Your balance doubled!"
            st.session_state.balance *= 2
            st.session_state.user_wins += 1
            animation = "win"
        else:
            result = "💀 You Lost! Half your balance lost!"
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
        else:
            st.markdown(
                "<div style='animation: pulse 1s infinite; color:#cccccc;'>😐</div>"
                "<style>@keyframes pulse {0%,100%{opacity:1;}50%{opacity:0.5;}}</style>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔁 Restart Game"):
            reset_game()
            st.rerun()
    with col2:
        if st.button("🏁 New Round"):
            st.rerun()
    with col3:
        if st.button("❌ Quit"):
            st.balloons()
            st.warning(
                f"**Final Results:**\n\n🧍 You: {st.session_state.user_wins}\n\n"
                f"🤖 Computer: {st.session_state.comp_wins}\n\n"
                f"💰 Final Balance: {RUPEE_SYMBOL}{st.session_state.balance:.2f}"
            )
            reset_game()
            st.stop()
