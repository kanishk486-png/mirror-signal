from datetime import datetime
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Mirror // Signal",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Custom Glassmorphic CSS Styling ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #09090b;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .holo-card {
        background: linear-gradient(135deg, rgba(30, 30, 46, 0.9) 0%, rgba(15, 15, 23, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7), inset 0 0 25px rgba(99, 102, 241, 0.15);
        margin-bottom: 20px;
    }
    
    .badge-mythic { background: linear-gradient(90deg, #f59e0b, #ec4899, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.1rem; }
    .badge-epic { background: linear-gradient(90deg, #a855f7, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.1rem; }
    .badge-rare { color: #38bdf8; font-weight: 800; font-size: 1.1rem; }
    .badge-common { color: #94a3b8; font-weight: 800; font-size: 1.1rem; }

    .stat-bar-bg {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin-top: 4px;
        margin-bottom: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Sidebar Controls ---
st.sidebar.markdown(
    "### 🎮 **Daily Telemetry**\nAdjust your daily habits to see your RPG card evolve in real-time."
)

user_name = st.sidebar.text_input("Player Name", value="Kanishk")
sleep_hours = st.sidebar.slider("Sleep (Hours)", 2.0, 12.0, 7.5, 0.5)
deep_work = st.sidebar.slider("Deep Work / Code (Hours)", 0.0, 12.0, 5.0, 0.5)
workout_mins = st.sidebar.slider("Workout / Gym (Minutes)", 0, 180, 45, 5)
screen_time = st.sidebar.slider("Screen Time / Doomscroll (Hours)", 0.0, 14.0, 3.5, 0.5)
streak_days = st.sidebar.number_input(
    "Active Streak (Days)", min_value=1, max_value=365, value=9
)
foil_theme = st.sidebar.selectbox(
    "Choose Holographic Foil",
    [
        "Prismatic Holo",
        "Astral Gold",
        "Neon Cyber-Grid",
        "Void Ultra Dark",
        "Standard Matte",
    ],
)


# --- Core Engine Logic ---
def calculate_rpg_stats(sleep, work, workout, screen):
  focus = min(100, int((work / 6.0) * 100))
  stamina = min(100, int((workout / 60.0) * 100))
  rest = min(100, int((sleep / 8.0) * 100))
  sanity = max(10, 100 - int((screen / 10.0) * 50))
  return {"FOCUS": focus, "STAMINA": stamina, "REST": rest, "SANITY": sanity}


stats = calculate_rpg_stats(sleep_hours, deep_work, workout_mins, screen_time)

# Determine Class & Vibe
buffs = []
debuffs = []

if stats["FOCUS"] >= 80 and stats["REST"] >= 70:
  avatar_class = "Cyber-Sage"
  vibe = "Transcendent Flow State"
  buffs.append("+15% Execution Speed")
elif stats["STAMINA"] >= 75:
  avatar_class = "Iron Juggernaut"
  vibe = "Unstoppable Momentum"
  buffs.append("+20% Physical Endurance Aura")
elif screen_time > 7.0 and stats["SANITY"] < 40:
  avatar_class = "Void-Walker"
  vibe = "Trapped in the Timeline (Doomscrolling)"
  debuffs.append("-10% Energy Drain on Squad")
else:
  avatar_class = "Balanced Wanderer"
  vibe = "Calibrated & Adaptive"
  buffs.append("+5% Daily XP Gain")

if streak_days >= 7:
  buffs.append(f"🔥 {streak_days}-Day Streak Multiplier Active")

# Rarity Determination
avg_score = sum(stats.values()) / len(stats)
if avg_score >= 80 and streak_days >= 7:
  rarity, badge_class = "MYTHIC", "badge-mythic"
elif avg_score >= 65:
  rarity, badge_class = "EPIC", "badge-epic"
elif avg_score >= 45:
  rarity, badge_class = "RARE", "badge-rare"
else:
  rarity, badge_class = "COMMON", "badge-common"


# --- Main UI ---
st.title("⚡ Mirror // Signal")
st.markdown(
    "*Your daily life, gamified into a collectible, tradeable holographic"
    " card.*"
)
st.markdown("---")

# Render Top Card Header inside custom container
st.markdown(
    f"""
    <div class="holo-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div>
                <span class="{badge_class}">★ {rarity} CARD</span>
                <span style="color: #94a3b8; font-size: 0.85rem; margin-left: 10px;">SHADER: {foil_theme}</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem;">{datetime.now().strftime('%Y-%m-%d')}</div>
        </div>
        
        <h2 style="margin: 0 0 5px 0; color: #f8fafc; font-size: 1.8rem;">{user_name}</h2>
        <div style="color: #818cf8; font-weight: 600; font-size: 1.1rem; margin-bottom: 5px;">⚡ Class: {avatar_class}</div>
        <div style="color: #94a3b8; font-style: italic; font-size: 0.95rem; margin-bottom: 25px;">"{vibe}"</div>
        
        <h4 style="color: #cbd5e1; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px; margin-bottom: 15px;">CORE ATTRIBUTES</h4>
    """,
    unsafe_allow_html=True,
)

# Render Stat Bars
for stat_name, val in stats.items():
  color = (
      "#6366f1"
      if stat_name == "FOCUS"
      else "#10b981"
      if stat_name == "STAMINA"
      else "#38bdf8"
      if stat_name == "REST"
      else "#f43f5e"
  )
  st.markdown(
      f"**{stat_name}**: {val} / 100"
      f' <div class="stat-bar-bg"><div style="width:'
      f" {val}%; background-color: {color}; height: 100%;"
      ' border-radius: 8px;"></div></div>',
      unsafe_allow_html=True,
  )

# Render Buffs & Debuffs
st.markdown("<br><b>ACTIVE MODIFIERS:</b>", unsafe_allow_html=True)
for b in buffs:
  st.markdown(f"<span style='color: #4ade80;'>+ {b}</span>", unsafe_allow_html=True)
for d in debuffs:
  st.markdown(f"<span style='color: #f87171;'>- {d}</span>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Action Buttons ---
col1, col2 = st.columns(2)
with col1:
  if st.button("📤 Export Card to Story", use_container_width=True):
    st.success("✨ Card successfully compiled into 1080x1920 holographic asset!")
with col2:
  if st.button("⚔️ Challenge Squad Guild", use_container_width=True):
    st.balloons()
    st.success("🔥 24-hour sprint challenge broadcasted to your guild!")