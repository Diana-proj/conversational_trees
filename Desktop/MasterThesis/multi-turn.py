from openai import OpenAI

OPENAI_API_KEY =""
client = OpenAI(api_key=OPENAI_API_KEY)


import json
from collections import OrderedDict
import re

# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_SMART.txt", "r", encoding="utf-8") as f:
    document = f.read()

#with open("/Users/diana/Desktop/BW_Gesetz.txt", "r", encoding="utf-8") as f:
#    document = f.read()

#with open("/Users/diana/Desktop/MasterThesis/Improved.md", "r", encoding="utf-8") as f:
#    flow = f.read()

with open("/Users/diana/Desktop/MasterThesis/PHA_Improvement_2.md", "r", encoding="utf-8") as f:
    flow = f.read()

chatbot_agent = f"""You are a chatbot designed to answer questions based ONLY on the provided document:

{document}

Rules:

1. **First (main) question:**
If possible begin by asking a single, concise yes/no clarifying question that is derived from a specific condition, alternative, or choice within the relevant chapter of the law text which affects the final answer.
Do not ask meta-questions about scope or sources — the {document} is always the only source.
After each user answer regarding the main question:
    - either ask another yes/no clarifying question (max 2 question), OR
    - provide the final answer once all necessary conditions from the document are clarified.

3. After the first main question has been fully answered, the next question from the user is always treated as a follow-up question.
For follow-up questions other rules apply:
Ask zero clarifying questions
Do not check preconditions
Answer immediately and directly
Never ask another yes/no
There is no branching logic for follow-up questions — only a direct final answer.

4. **Absolute Constraint:** Never assume anything beyond the document. If a question is not covered in the document, reply only:  
   **"Das Dokument enthält keine relevanten Informationen zu Ihrer Frage."**  
   Do not mention external sources or limitations.

5. Keep all messages short (max. 3 sentences).

6. The conversation ends only when the user explicitly says **"Danke, Tschüss."**

7. Never repeat previous clarifications or questions already asked.

8. The final answer must always be concise and limited to what is necessary to resolve the user’s question.

9. After giving the final answer to the follow-up question, and once the user says **"Danke, Tschüss."**, you close politely with  
   **"Gern geschehen, Tschüss."**
"""


def extract_questions(mermaid_text: str) -> list[str]:
    """
    Finds every question label on Q* nodes like:
      Q3B_1 --> A3B_1["...?..."]
    and returns the quoted text that ends with '?'.
    """
    # Match lines that define a Q-node with a quoted label ending in '?'
    # Examples it matches:
    #   S3A --> Q3A_1["Dürfen Dienstreisen ...?"]
    #   S6A --> Q6A_1["Wie hoch ist ...?"]
    pattern = re.compile(r'^[ \t]*\w+[ \t]*-->[ \t]*Q[^\[]*\["(.+?\?)"\]', re.MULTILINE)
    found = pattern.findall(mermaid_text)

    # Keep order, drop duplicates
    unique = list(OrderedDict.fromkeys([q.strip() for q in found]))
    return unique


dialogues =""
questions = extract_questions(flow)
print (questions)



def choose_questions (questions):
    prompt = f""" This are all {questions} from the conversational flow. We would like to choose 15 of them, which users are in practice would be most interested in and 
    we can expand in the next step in more detail usin multi-turn dialogues, adding cross-references etc. Please choose the best most relevant 15 questions, but they should be very different (from different branches) and unrealted to each other, not similar to each other in any way.
Also excluse these concrete questions: Wer ist im Paar‑ bzw. Familien‑Tarif mitversichert?
Wer ist "Versicherungsnehmer:in"? 
Ist die Versicherungssumme die Leistungsobergrenze? 
Welche Anzeige‑ und Mitwirkungspflichten habe ich nach einem Schaden?
Was ist Forderungsausfalldeckung und wann greift sie? 
Sind Elementarschäden (z. B. Überschwemmung) gedeckt?
Deckt die Police Verlust fremder Schlüssel / Codekarten?
Deckt die Allianz Haftpflicht durch private Internetnutzung? 
Gilt Schutz für Pedelecs (E‑Tretunterstützung)?
Was ist die "Mallorca‑Deckung" bei Auslandsanmietung?
Sind Außenanlagen (Garagen, Gartenhäuser) mitversichert? 
Wie sind Photovoltaik / Geothermie / Wallboxen gedeckt?
Wann besteht Schutz als Haus-/Wohnungsbesitzer:in? 
Sind Rettungs‑ oder Feuerwehr‑Profis mitversichert, wenn sie helfen?
Sind angestellte Haushaltspersonen bei Tätigkeiten mitversichert?
Wer sind "Dritte"?
Was bedeutet "Ausschluss" in den Bedingungen?
Was sind "Obliegenheiten"?
Wer ist im Single‑Tarif versichert?
Sind Au‑pairs/Austauschschüler mitversichert?
Sind Kinder während Studium/Ausbildung versichert, auch bei Arbeit?
Wie ändert sich der Schutz nach Tod des Versicherungsnehmers?
Deckt die Privat‑Haftpflicht berufliche/gewerbliche Haftpflicht?
Welche Schadenarten sind versichert? 
Welche Vermögensschäden sind ausgeschlossen?
Sind Vermietung einzelner Zimmer oder Einliegerwohnungen gedeckt? 
Besteht Schutz als Bauherr:in bei Umbau/Renovierung?
Gibt es eine Entschädigungsbegrenzung für gemietete bewegliche Sachen? 
Sind Praktika/Schnupperlehren mitversichert?
 Ist ehrenamtliche Tätigkeit versichert und subsidiär?
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()


chosen_questions = choose_questions (questions)
print (chosen_questions)

chosen_questions = [
    line.split(". ", 1)[-1].strip()
    for line in chosen_questions.splitlines()
    if line.strip() and line[0].isdigit()
]


#start_from = 1                
#start_idx = start_from - 1      

#if start_idx >= len(questions):
 #   raise ValueError(f"start_from {start_from} > number of questions ({len(questions)})")

dialogues = ""
max_turns =10

for i, question in enumerate (chosen_questions):
    print(f"\n===== DIALOGUE {i}/{len(chosen_questions)} :: {question} =====")

    history = [{
        "party": "chatbot",
        "utterance": "Hello! I’m here to help with any questions you have about the document. Could you tell me a bit about your situation or question?"
    }]
    done = False
    main_answer_completed = False

    current_turn = 0

    while (not done) and current_turn < max_turns:
        user_agent = f""" You are simulating a person who wants to find an answer to the question regarding the document (formulate question in non-legal natural way):
\"{question}\".
Rules for your simulation:
- You do NOT know the content of the document but only want to know and ask about this document, not external sources.
- You only describe your **realistic, practical scenario**, but not in too many details and ask the main question in a simple non-legal natural way in the first turn.
- User relies on chatbot guidance: Provide the concrete answer to chatbot clarifying questions to help chatbot provide you the relevant information from the document; do not repeat information you already gave. DO not repeat asked questions.
- ONLY AFTER this main question is fully answered, you may ask only ONE more follow up question from this list {questions}  as side-topic logically related to the main question.  
But reformulate it again in a simple non-legal way.
- Keep each message short (max 2-3 sentences).
- End the conversation with “Danke, Tschüss.” **only when both of your questions have been addressed by the chatbot**. This is the end of convo, no further questions possible.

The conversation so far is:
{json.dumps(history, ensure_ascii=False)}"""

        user_response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": user_agent},
                {"role": "user", "content": f"""You are a person trying find out the answer to this question (this is your goal): {question}. 
                 
                 The conversation so far: {json.dumps(history)}.
                 Respond to the last chatbot turn, or ask for further detail concerning the same topic, or end the dialog saying "Danke, Tschüss" if your goal question was answered.
                 Do not repeat the provided informations again. Dont repeat questions or circle back to the same point. """},
        ])
        user_utterance = user_response.choices[0].message.content
        print("USER", user_utterance)
        history.append({"party": "employee", "utterance": user_utterance})


        sys_response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": chatbot_agent},
                {"role": "user", "content": f"The conversation so far:\n {json.dumps(history)}"}
        ])

        sys_utterance = sys_response.choices[0].message.content
        print("SYSTEM", sys_utterance)
        history.append({"party": "chatbot", "utterance": sys_utterance})
        if not main_answer_completed and "?" not in sys_utterance:
            main_answer_completed = True  # chatbot answered the main question
        
        elif main_answer_completed and "?" not in sys_utterance:
        # chatbot also answered follow-up → employee should say goodbye
            history.append({"party": "employee", "utterance": "Danke, Tschüss."})
            done = True

        current_turn += 1


        # print (history)
        current_turn += 1

    dialogues += f"\n===== DIALOGUE {i}: {question} =====\n"
    for turn in history:
        speaker = "Chatbot" if turn["party"] == "chatbot" else "Employee"
        dialogues += f"{speaker}: {turn['utterance'].strip()}\n"

with open("all_dialogues_pha.txt", "w", encoding="utf-8") as f:
    f.write(dialogues)


 

prompt = """You are a chatbot designed to answer questions based ONLY on the provided document:

{document}

Rules:

1. **First (main) question:**
If possible begin by asking a single, concise yes/no clarifying question that is derived from a specific condition, alternative, or choice within the relevant chapter of the law text which affects the final answer.
Do not ask meta-questions about scope or sources — the LRKG is always the only source.
After each user answer regarding the main question:
    - either ask another yes/no clarifying question (max 2 question), OR
    - provide the final answer once all necessary conditions from the document are clarified.

3. After the first main question has been fully answered, the next question from the user is always treated as a follow-up question.
For follow-up questions other rules apply:
Ask zero clarifying questions
Do not check preconditions
Answer immediately and directly
Never ask another yes/no
There is no branching logic for follow-up questions — only a direct final answer.

4. **Absolute Constraint:** Never assume anything beyond the document. If a question is not covered in the document, reply only:  
   **"Das LRKG enthält keine relevanten Informationen zu Ihrer Frage."**  
   Do not mention external sources or limitations.

5. Keep all messages short (max. 3 sentences).

6. The conversation ends only when the user explicitly says **"Danke, Tschüss."**

7. Never repeat previous clarifications or questions already asked.

8. The final answer must always be concise and limited to what is necessary to resolve the user’s question.

9. Always assume the user is within the scope of the LRKG (Beamte / Beschäftigte etc.); never request confirmation.

10. After giving the final answer to the follow-up question, and once the user says **"Danke, Tschüss."**, you close politely with  
   **"Gern geschehen, Tschüss."**
Example flow:

Example:

USER Ich fahre nächste Woche mit der Bahn zu einer Konferenz nach München. Welche Klasse wird erstattet - 2. oder 1. Klasse, und gilt das auch für ICE/IC-Verbindungen? 
SYSTEM Haben Sie einen Grad der Behinderung von mindestens 50 oder einen gesundheitlichen Grund, der die Benutzung der 1. Klasse rechtfertigt?
USER Nein, ich habe keinen GdB ≥50 und keinen gesundheitlichen Grund.  
SYSTEM Für Ihre Bahnreise werden nach § 4 Absatz 1 nur die Kosten der niedrigsten Beförderungsklasse erstattet — also in der Regel die 2. Klasse; bei Nutzung der 1. Klasse wird höchstens der Betrag für die 2. Klasse ersetzt.
USER Noch eine Frage: Wer legt grundsätzlich fest, was als Ausgangs‑ bzw. Endpunkt gilt — mein Wohnort oder die Dienststelle?
SYSTEM Sie dürfen grundsätzlich selbst Ausgangs- und Endpunkt bestimmen (z. B. Ihre Wohnung)
USER Danke, Tschüss
SYSTEM Gern geschehen, Tschüss
"""