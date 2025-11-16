from openai import OpenAI

OPENAI_API_KEY =""
client = OpenAI(api_key=OPENAI_API_KEY)


DOMAIN = "city_info"

def initial_prompt (DOMAIN):
    prompt = f"""
    Given the context of this {DOMAIN}, design a directed acyclic dialog flow suitable for visualization with mermaid.js. This flow should depict the nuances and potential branches of interactions between a bot and a user.Please adhere to the following guidelines:
    Nodes Definition: Use distinct nodes to represent the bot ("B") and the user ("U").
    High-Level Dialog Action: Each node should encapsulate that segment's core sentiment or function in the conversation, relevant to [DOMAIN]. It should be a label for the node representing a high-level dialogue action and not just the dialogue.
    Flow & Directionallty: Create directed connections between nodes to represent the progression of the conversation. The dialogue should flow from sy node to potentially multiple nodes, allowing for various conversational turns.
    Diverse Conversational Possibilities: Ensure that bot nodes can lead to multiple user nodes and vice versa. This should account for various user responses or bot prompts, showcasing the range of interactions possible within [DOMAIN].
    Acyclic Structure: The dialog flow must not have loops or cyclic pathways. If a similar action or sentiment arises later in the conversation, introduce a new node to represent it, rather than looping back to an earlier node.
    Mermaid.js Compatibility: Ensure that the constructed flow is adherent to mermaid.js graph notation, guaranteeing its seamless rendering.
    Considering the guidelines, craft a dialogue flow focused on {DOMAIN}. The bot always begins by greeting the user and asking for what they want. The graph should be connected. The bot and user nodes should be in different colors. A bot node is only followed by user nodes and user nodes are by bot nodes.
    """
    response = client.chat.completions.create(
       model="gpt-4-turbo",
       temperature=0.35,
       top_p=1.0,
       messages=[{"role": "user", "content": prompt}]    )
    return response.choices[0].message.content.strip()

def feedback_prompt (flow):
    prompt = f"""
Based on the below evaluation criteria, suggest some improvements and provide concise + actionable feedback on the {flow} just generated:
Optimality: Check for redundancy. Ensure that nodes aren't replicating the same or very similar dialog actions, even if they arise at different points in the conversation Clarity of High-Level Dialog Action: For every node, evaluate if the high-level dialog action is clear and meaningful. Avoid nodes that are vague or overty complex.
Can someone unfamiliar with the domain understand the flow and interactions by looking at the flow?
Extensiveness: Does the flow account for diverse conversational possibilities? Are all the nodes interconnected to the graph? Does the flow cover all major high level topics and interactions within the given domain?
Representativeness of the Domain: Bot Nodes (B): Do the bot nodes represent clear and unambiguous actions? Are they too broad or too specific? User Nodes (U):
Do user nodes accurately capture an adequate range of potential user responses and inquiries relevant to the domain?"""
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def update_prompt(flow, feedback):
    prompt = f"""Taking into consideration the {feedback} and the original design guidelines - keep it in directed acyclic graph structure and make sure all new components are labeled and connected to the graph correctly- revise the {flow} . Ensure your revised flow addresses the identified areas of improvement while still adhering to the primary instructions for flow construction. Make sure to account for all new nodes including merged nodes and their labels/colors. Make sure all user nodes connect with bot nodes and bot nodes are the end of the conversations. Give your updates in the below format:
'split_nodes':
# 'Node ToSplit: ['NewNode1', 'NewNode2', ...).
'add _nodes':
# 'NodeToAdd': 'Label',
remove_nodes':
# 'NodeToRemove1, 'Node ToRemove2,...
'relabel_nodes':
# Node ToRelabel: 'NewLabel',
'add_edges':
# ('Start Node', 'End Node'),
'remove_edges':
# ('Start Node', 'End Node'),"""
    response = client.chat.completions.create(
       model="gpt-4-turbo",
       temperature=0.35,
       top_p=1.0,
       messages=[{"role": "user", "content": prompt}]    )
    return response.choices[0].message.content.strip()

def finalization_prompt (flow):
    prompt = f"""Clean up the flow {flow} to create a final flow. Ensure your revised flow addresses the identified areas of improvement while still adhering to the primary instructions (Please adhere to the following guidelines:
    Nodes Definition: Use distinct nodes to represent the bot ("B") and the user ("U").
    High-Level Dialog Action: Each node should encapsulate that segment's core sentiment or function in the conversation, relevant to [DOMAIN]. It should be a label for the node representing a high-level dialogue action and not just the dialogue.
    Flow & Directionallty: Create directed connections between nodes to represent the progression of the conversation. The dialogue should flow from sy node to potentially multiple nodes, allowing for various conversational turns.
    Diverse Conversational Possibilities: Ensure that bot nodes can lead to multiple user nodes and vice versa. This should account for various user responses or bot prompts, showcasing the range of interactions possible within [DOMAIN].
    Acyclic Structure: The dialog flow must not have loops or cyclic pathways. If a similar action or sentiment arises later in the conversation, introduce a new node to represent it, rather than looping back to an earlier node.
    Mermaid.js Compatibility: Ensure that the constructed flow is adherent to mermaid.js graph notation, guaranteeing its seamless rendering.
    Considering the guidelines, craft a dialogue flow focused on {DOMAIN}. The bot always begins by greeting the user and asking for what they want. The graph should be connected. The bot and user nodes should be in different colors. A bot node is only followed by user nodes and user nodes are by bot nodes.) for flow construction. Get rid of hanging/loose user nodes (user nodes with no output), have graph in directed acyclic structure,
    bot nodes shouldn't be connected to other bot nodes, and user nodes shouldn't be connected to other user nodes. All nodes should have input/output except begin and end nodes, one node shouldn't point to the another node more than once, and make sure all bot nodes are correctly colored."""
    response = client.chat.completions.create(
       model="gpt-4-turbo",
       temperature=0.35,
       top_p=1.0,
       messages=[{"role": "user", "content": prompt}]    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("=== Generating Initial Flow ===")
    initial = initial_prompt(DOMAIN)
    print(initial)

    print("\n=== Getting Feedback ===")
    feedback = feedback_prompt(initial)
    print(feedback)

    print("\n=== Updating Flow ===")
    updates = update_prompt(initial, feedback)
    print(updates)

    print("\n=== Finalizing Flow ===")
    final = finalization_prompt(updates)
    print(final)
    
