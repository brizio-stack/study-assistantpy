import streamlit as st
from datetime import date
import json, os

ARCHIVO = "tareas.json"

def cargar_tareas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            tareas = json.load(f)
        # en el JSON la fecha queda como texto, la volvemos a convertir a date
        for t in tareas:
            t["deadline"] = date.fromisoformat(t["deadline"])
        return tareas
    return []

def guardar_tareas(tareas):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2, default=str)

if "task" not in st.session_state:
    st.session_state.task = cargar_tareas()

st.title("📕My Study assistant")
st.write("Add your tasks to have a better  organization.")

name  = st.text_input("What task do you have?")

subject = st.selectbox("Subject", ["Maths", "History", "Science", "Spanish", "English", "Other"])
deadline = st.date_input("Deadline", min_value=date.today())

if st.button("Save Task"):
    if name == "":
        st.warning("Please, write the name of the task.")
    else:

        days  = (deadline - date.today()).days
        if days <= 2:
            priority = "High"
        elif days <= 5:
            priority = "Medium"
        else:
             priority = "Low"
        st.session_state.task.append({
            "name": name,
            "subject": subject,
            "deadline": deadline,
            "priority": priority
        })
        guardar_tareas(st.session_state.task)
        st.success("Homework saved!")

st.subheader("📋My homeworks")

colors = {"High": "#B50000", "Medium": "#E66500", "Low": "#FFF31C"}
text_colors = {"High": "white", "Medium": "white", "Low": "black"}

breakdowns = {
    "Maths": "1. Review notes  2. Do practice problems  3. Check answers",
    "Science": "1. Read the topic  2. Make a diagram  3. Review concepts",
    "History": "1. Read the chapter  2. Make a summary  3. Study key dates",
    "English": "1. Read the text  2. Underline key ideas  3. Write your answer",
    "Spanish": "1. Lee el texto  2. Saca las ideas principales  3. Repasa",
}

tips = {
    "Maths": "Practice a little every day, don't leave it all for the end.",
    "Science": "Explain the topic out loud like you're teaching it.",
    "History": "Use timelines to remember dates.",
    "English": "Read out loud, it helps you catch mistakes.",
    "Spanish": "Resume con tus propias palabras, no lo copies igual.",
}

if len(st.session_state.task) == 0:
    st.write("You don't have homework yet. Add one above!")
else:
    sort_by = st.radio("Sort by:", ["Priority", "Deadline"])

    def get_deadline(t):
        return t["deadline"]

    if sort_by == "Deadline":
        task_list = sorted(st.session_state.task, key=get_deadline)
    else:
        task_list = []
        for level in ["High", "Medium", "Low"]:
            for t in st.session_state.task:
                if t["priority"] == level:
                    task_list.append(t)

    for i in range(len(task_list)):
        t = task_list[i]
        color = colors[t["priority"]]
        text = text_colors[t["priority"]]
        st.markdown(
            f"""
            <div style="background-color: {color}; color: {text}; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                <b>{t['name']}</b> — {t['subject']}<br>
                Deadline: {t['deadline']} · Priority: {t['priority']}<br>
                Steps: {breakdowns.get(t['subject'], "No steps yet for this subject.")}<br>
                Tip: {tips.get(t['subject'], "")}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("✅ Done", key="done_" + str(i)):
            st.session_state.task.remove(t)
            guardar_tareas(st.session_state.task)
            st.rerun()

st.write(f"You have {len(st.session_state.task)} tasks.")