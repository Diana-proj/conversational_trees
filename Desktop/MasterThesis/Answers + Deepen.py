from openai import OpenAI

OPENAI_API_KEY ="x"
client = OpenAI(api_key=OPENAI_API_KEY)

models = client.models.list()
for m in models.data:
    print(m.id)

import json

# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_SMART.txt", "r", encoding="utf-8") as f:
    document = f.read()

# Access the document
with open("/Users/diana/Desktop/MasterThesis/Hierarchy.md", "r", encoding="utf-8") as f:
    graph = f.read()

# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_With_Answers.md", "r", encoding="utf-8") as f:
    graph_withanswers = f.read()



def add_answers (graph, document):
    prompt = f"""
Given the  {graph} add the answer leaves for questions based on the information from the document and {document}
Output a Mermaid TD graph.

"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()






def improving_more (graph, document):
    prompt = f"""
Task: Review the current dialogue flow {graph}  that maps questions (Q) to answers (A) based on {document}. Apply structural and content improvements to make the flow deeper, more logical, and user-friendly.

Goals:
Depth & Choice – Wherever a question has multiple outcomes (e.g. different cases, conditions, thresholds), expand it into explicit sub-choice nodes with mutually exclusive, condition-based labels and short, precise answers.
Rewrite questions so they ask only one thing at a time (e.g. “Wie hoch ist das Übernachtungsgeld?” → Choices: Inland → “20 €”, Ausland → “30 €”).
Choice labels must be short and condition-based (e.g. “Inland”, “Ausland”, “mit Unterkunft gestellt”).
Logical Navigation – Arrange nodes so users move naturally from broad categories → sub-cases → final concise answers. Remove overlaps or redundant nodes. Group related branches under the same parent node.
Conciseness – Keep all questions concise. Keep answers conclusive and no longer than 1–2 sentences, always citing the exact rule/reference (e.g. “20 € Inland, vgl. §7 Abs.1”).
Consistency – Use a uniform style for questions, choice labels, and answers.
Questions: one issue only, phrased directly.
Choices: short, condition-based.
Answers: definitive statement + section reference.
Cross-References – If a question touches more than one section, give the direct answer but add a link/branch to the other relevant node instead of duplicating content.
Output: A refined mermaid graph TD where all questions are concise, answers are conclusive, multi-outcome cases are structured into explicit choice nodes, navigation is logical, and cross-references are handled with links instead of duplication.
Dont lose any nodes, information etc. Only add and improve
"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    #print("Printing Graph with Answers")
    #results = add_answers(graph, document)
    #print (results)
    new_graph = improving_more (graph_withanswers, document)
    print (new_graph)