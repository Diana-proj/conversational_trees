from openai import OpenAI

OPENAI_API_KEY ="x"
client = OpenAI(api_key=OPENAI_API_KEY)


import json
from collections import OrderedDict
import re 

# Access the document
with open("/Users/diana/Desktop/BW_Gesetz.txt", "r", encoding="utf-8") as f:
    document = f.read()

with open("/Users/diana/Desktop/MasterThesis/Improved.md", "r", encoding="utf-8") as f:
    flow = f.read()


chatbot_agent = f"""You are a chatbot for answering business travel questions.
You should only consider facts from this document:
{document}

Try to ask follow-up question / narrow down the information need in order to guide the user to a single correct answer for their scenario.
Proposed procedure:
1) At your first turn and whenever key info is missing, ASK EXACTLY ONE CLARIFYING QUESTION. Do not answer completely yet.
2) After each user reply, EITHER:
   - ask one new clarifying question, OR
   - state one short fact tailored to the user’s case (not generic law),
   but never both in the same turn. Do not provide more information that was asked, give the user a chance to ask further questions if needed.
3) When the user’s question is fully answered, say only: "Goodbye."
Only output either a single question to the user, or a single fact at each dialog turn. 


- Stay strictly within the Landesreisekostengesetz Baden-Württemberg (LRKG) and the provided document. 
Ask only clarifying questions that are explicitly relevant to provisions in the law, and guide the user step by step toward the specific answer defined in the law. 
Do not discuss local practices, policies, or interpretations not contained in the LRKG.

Clarify the user intent or answer the user's questions, and keep your utterances short and simple.
If the user is satisfied with their answer, end the conversation with this word: "Goodbye."
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



def choose_questions (questions):
    prompt = f""" This are all {questions} from the conversational flow. We would like to choose 20 of them, which users are in practice would be most interested in and 
    we can expand in the next step in more detail usin multi-turn dialogues, adding cross-references etc. Please choose the best most relevant 20 questions.
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
max_turns =8

for i, question in enumerate (chosen_questions):
    print(f"\n===== DIALOGUE {i}/{len(chosen_questions)} :: {question} =====")

    history = [{
        "party": "chatbot",
        "utterance": "Hello! I’m here to help with any questions you have about business travel and the new Landesreisekostengesetz. Could you tell me a bit about the kind of travel you’re planning—e.g., domestic or international trips, the purpose, or any specific concerns?"
    }]
    done = False

    current_turn = 0

    while (not done) and current_turn < max_turns:
        user_agent = f"""You are simulating an employee who is planning a business trip.
Your goal is to find the answer to this question by talking to a chatbot:
"{question}".
 f"The conversation so far: {json.dumps(history, ensure_ascii=False)}.\n"
Although in principle inquiring about this, you are not aware of the regulations of the law and you need to state your problems as human-like as possible, not as legally defined in the question.
Speak in a natural, everyday way, as if you were asking HR or the travel office for help.
Mention your specific travel situation (e.g., conference, customer visit, train tickets).
Ask one or two simple, practical questions at a time. 
Keep each message under three short sentences.

If your question was answer end the conversation with Danke, Tschüss"""

        user_response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": user_agent},
                {"role": "user", "content": f"""You are an employee trying find out the answer to this question (this is your goal): {question}. 
                 
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

        if "goodbye" in sys_utterance.lower():
            done = True
            break

        # print (history)
        current_turn += 1

    dialogues += f"\n===== DIALOGUE {i}: {question} =====\n"
    for turn in history:
        speaker = "Chatbot" if turn["party"] == "chatbot" else "Employee"
        dialogues += f"{speaker}: {turn['utterance'].strip()}\n"

with open("all_dialogues.txt", "w", encoding="utf-8") as f:
    f.write(dialogues)


        