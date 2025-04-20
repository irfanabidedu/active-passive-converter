import streamlit as st
import re

st.set_page_config(page_title="Advanced Active to Passive Voice Converter")

st.title("🧠 Advanced Active to Passive Voice Converter")
st.write("Handles affirmative, negative, interrogative, and interro-negative sentences.")

# Subject to Object Pronoun Map
subject_map = {
    "i": "me", "you": "you", "he": "him", "she": "her",
    "we": "us", "they": "them", "it": "it"
}
object_map = {v: k for k, v in subject_map.items()}

# Basic Tense Rules
tense_map = {
    "present simple": ["am", "is", "are"],
    "past simple": ["was", "were"],
    "future simple": ["will be"]
}

def detect_tense(words):
    if "did" in words:
        return "past simple"
    elif "do" in words or "does" in words:
        return "present simple"
    elif "will" in words:
        return "future simple"
    elif any(w.endswith("ed") for w in words):
        return "past simple"
    else:
        return "present simple"

def to_past_participle(verb):
    irregulars = {"eat": "eaten", "go": "gone", "write": "written", "take": "taken", "see": "seen"}
    if verb in irregulars:
        return irregulars[verb]
    if verb.endswith("e"):
        return verb + "d"
    return verb + "ed"

def convert_affirmative(subject, verb, obj, tense):
    be = tense_map[tense]
    be_verb = be[0] if subject.lower() == "i" else (be[1] if subject.lower() in ["he", "she", "it"] else be[-1])
    past_part = to_past_participle(verb)
    return f"{obj.capitalize()} {be_verb} {past_part} by {subject_map.get(subject.lower(), subject)}."

def convert_negative(subject, verb, obj, tense):
    base_verb = verb
    if tense == "present simple":
        aux = "is not" if subject.lower() in ["he", "she", "it"] else "are not"
    elif tense == "past simple":
        aux = "was not" if subject.lower() in ["he", "she", "it", "i"] else "were not"
    elif tense == "future simple":
        aux = "will not be"
    else:
        aux = "is not"
    past_part = to_past_participle(base_verb)
    return f"{obj.capitalize()} {aux} {past_part} by {subject_map.get(subject.lower(), subject)}."

def convert_interrogative(subject, verb, obj, tense, negative=False):
    if tense == "present simple":
        aux = "Is" if subject.lower() in ["he", "she", "it"] else "Are"
    elif tense == "past simple":
        aux = "Was" if subject.lower() in ["he", "she", "it", "i"] else "Were"
    elif tense == "future simple":
        aux = "Will"
    else:
        aux = "Is"
    
    past_part = to_past_participle(verb)
    not_part = " not" if negative else ""
    return f"{aux}{not_part} {obj.lower()} {past_part} by {subject_map.get(subject.lower(), subject)}?"

def process_sentence(sentence):
    sentence = sentence.strip()
    if not sentence:
        return "Please enter a sentence."
    
    is_question = sentence.endswith("?")
    sentence = sentence[:-1] if is_question else sentence

    words = sentence.lower().split()
    if len(words) < 3:
        return "Enter a complete sentence."

    # Detect tense and sentence type
    tense = detect_tense(words)

    # Identify structure
    if is_question:
        negative = "not" in words
        if "did" in words:
            subject = words[1]
            verb = words[2]
            obj = ' '.join(words[3:]).replace("not", "").strip()
        elif "do" in words or "does" in words:
            subject = words[1]
            verb = words[2]
            obj = ' '.join(words[3:]).replace("not", "").strip()
        elif "will" in words:
            subject = words[1]
            verb = words[2]
            obj = ' '.join(words[3:]).replace("not", "").strip()
        else:
            subject = words[0]
            verb = words[1]
            obj = ' '.join(words[2:])
        return convert_interrogative(subject, verb, obj, tense, negative)

    elif "not" in words:
        # Negative sentence
        try:
            subject = words[0]
            verb_index = words.index("not") + 1
            verb = words[verb_index]
            obj = ' '.join(words[verb_index + 1:])
        except:
            return "Couldn't parse negative sentence."
        return convert_negative(subject, verb, obj, tense)

    else:
        # Affirmative
        subject = words[0]
        verb = words[1]
        obj = ' '.join(words[2:])
        return convert_affirmative(subject, verb, obj, tense)

# Streamlit input/output
sentence = st.text_input("Enter an active voice sentence:")
if st.button("Convert"):
    if sentence:
        passive = process_sentence(sentence)
        st.success(passive)
    else:
        st.warning("Please enter a sentence.")
