import streamlit as st
import json
import os
from datetime import datetime

# إعدادات الصفحة عشان تطلع مرتبة بالتلفون
st.set_page_config(page_title="مناسباتي", page_icon="📅", layout="centered")

FILE_NAME = 'my_events_web.json'

def load_events():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_events(events):
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(events, file, ensure_ascii=False, indent=4)

events = load_events()

# --- عنوان الموقع ---
st.title("📅 نظام إدارة المناسبات")
st.write("رتب طلعاتك ومناسباتك بسهولة")

# --- قسم إضافة مناسبة ---
st.header("إضافة مناسبة جديدة")
with st.form("add_event_form", clear_on_submit=True):
    name = st.text_input("شنو المناسبة؟ (مثال: عرس، مزرعة):")
    event_date = st.date_input("متى وقتها؟")
    
    submitted = st.form_submit_button("➕ إضافة للجدول")
    if submitted:
        if name:
            events.append({"name": name, "date": str(event_date)})
            save_events(events)
            st.success("✅ تمت الإضافة بنجاح!")
            st.rerun() # تحديث الصفحة عشان تطلع المناسبة الجديدة
        else:
            st.warning("⚠️ لا تنسى تكتب اسم المناسبة!")

st.divider()

# --- فرز المناسبات (قادمة وسابقة) ---
today = datetime.today().date()
upcoming_events = []
past_events = []

for ev in events:
    try:
        ev_date = datetime.strptime(ev['date'], "%Y-%m-%d").date()
        if ev_date >= today:
            upcoming_events.append(ev)
        else:
            past_events.append(ev)
    except ValueError:
        upcoming_events.append(ev)

# --- عرض المناسبات في عمودين ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔮 القادمة")
    if not upcoming_events:
        st.info("ماكو مناسبات قادمة.")
    for i, ev in enumerate(upcoming_events):
        with st.container(border=True):
            st.write(f"**{ev['name']}**")
            st.write(f"📅 {ev['date']}")
            if st.button("🗑️ حذف", key=f"del_up_{i}"):
                events.remove(ev)
                save_events(events)
                st.rerun()

with col2:
    st.subheader("⏳ السابقة")
    if not past_events:
        st.info("ماكو مناسبات سابقة.")
    for i, ev in enumerate(past_events):
        with st.container(border=True):
            st.write(f"**{ev['name']}**")
            st.write(f"📅 {ev['date']}")
            if st.button("🗑️ حذف", key=f"del_past_{i}"):
                events.remove(ev)
                save_events(events)
                st.rerun()