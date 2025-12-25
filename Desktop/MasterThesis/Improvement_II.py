from openai import OpenAI

OPENAI_API_KEY =""
client = OpenAI(api_key=OPENAI_API_KEY)

models = client.models.list()
for m in models.data:
    print(m.id)

import json

# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_SMART.txt", "r", encoding="utf-8") as f:
    document = f.read()

#with open("/Users/diana/Desktop/BW_Gesetz.txt", "r", encoding="utf-8") as f:
#    document = f.read()



# Access the graph
#with open("/Users/diana/Desktop/MasterThesis/Created_BW.md", "r", encoding="utf-8") as f:
#   graph_withanswers = f.read()


# Access the graph
with open("/Users/diana/Desktop/MasterThesis/PHA_new.md", "r", encoding="utf-8") as f:
 graph_withanswers = f.read()




def improving_more (graph, document):
    prompt = f"""
Task:
Review the provided graph {graph} based on {document}. 
Rebuild the flow so users can navigate from general topics to precise answers in a clear, intuitive way.

Goals:
• Improve clarity  
• Improve structure and depth (target depth at least 4)  
• Improve logic and placement  
• Improve user experience  
• Keep all legal information, but reorganize it  

Core Principles
1. Preserve all underlying information from the graph and from the document.
2. You may merge, split, rephrase, relocate, or rename nodes.
3. You may create new parent nodes and intermediate nodes to improve logic, readability, and depth.
4. You may rewrite questions and answers for clarity as long as meaning and legal accuracy stay the same.
5. You may reassign a question–answer pair to a different parent if the logic improves.
6. If a question–answer pair fits more naturally under another question, place it there.
7. Aim for natural depth (at least four levels) in each major section.
8. No content may be removed. If the graph contains a rule, it must appear somewhere in the final structure.

User-Facing Questions (Q)
1. Rewrite each question so it covers exactly one issue.
2. Split compound questions into separate nodes.
3. Keep questions short, direct, and informal.
4. Replace vague questions (“Gibt es Ausnahmen?”) with explicit questions naming the context.
5. Ensure every question aligns precisely with the meaning of its answer.

Answers (A)
1. Keep answers short and conclusive (1–2 sentences).
2. State the rule and include the legal reference.
3. Every question ends in exactly one final answer node.
4. You may insert intermediate decision or clarification nodes if they improve the flow.

Structure & Navigation
1. Reorganize all content from general → specific.
2. Move definitions and basic rules to the top of each major section.
3. Use plain-language grouping nodes.
4. Remove or rewrite headings that are overly formal or unclear.
5. Place exceptions, special rules, and conditions directly under the rule they modify.
6. Move misplaced nodes (e.g., “Ausnahmen” must sit under the rule they refer to).
7. Eliminate redundant or parallel branches; prefer cross-references over duplication.
8. Build a clear, nested hierarchy so users can drill down through structured levels.

Node Naming
1. Replace technical or bureaucratic labels with descriptive, plain-language names.
2. Use short, simple labels for categories and subcategories.

Completeness & Integrity
1. Preserve all legal content exactly once.
2. You may rewrite, merge, or split content to improve clarity but not reduce information.
3. Introduce new grouping or decision nodes if necessary.
4. No legal rule, exception, condition, or edge case may be omitted or softened.

Output Format
Return:
• A refined Mermaid graph (flowchart TD)
• With a clean, logical hierarchy
• With user-friendly categories
• With improved questions and correct answers
• With exceptions placed under the rules they modify
• With consistent naming and formatting


"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    new_graph = improving_more (graph_withanswers, document)
    print (new_graph)





"""Task: Review the current dialogue flow {graph}  that maps questions (Q) to answers (A) based on {document}. Apply structural and content improvements to make the flow deeper, more logical, and user-friendly.

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
Dont lose any nodes, information etc. Only add and improve"""