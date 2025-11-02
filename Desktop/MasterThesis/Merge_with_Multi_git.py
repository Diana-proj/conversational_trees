from openai import OpenAI
import re
from pathlib import Path
from typing import List
import time


OPENAI_API_KEY ="--"
client = OpenAI(api_key=OPENAI_API_KEY)


# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_SMART.txt", "r", encoding="utf-8") as f:
    document = f.read()
# Access the document
with open("/Users/diana/Desktop/BW_Gesetz.txt", "r", encoding="utf-8") as f:
    document = f.read()

with open("/Users/diana/Desktop/MasterThesis/Improved.md", "r", encoding="utf-8") as f:
    flow = f.read()

OUT_PATH = Path("/Users/diana/Desktop/MasterThesis/Improved_Flow_26.md")


def merge_flow_multi (flow, multiturndialog, document):
    prompt = f"""
Mermaid Flow Integration Prompt (Final Polished Version)
You are given:
the existing Mermaid flow {flow}
one multi-turn dialog {multiturndialog}

🎯 GOAL
Integrate {multiturndialog} into {flow} if meaningful.

1. Decide if the integration is meaningful. Only if the expansion will benefit gradually guiding the user to the final answer node and seems logical, then:


Expand only the dialog’s main statutory topic into Question and Answer nodes.
Handle any side topic as an Xref only (no new Question/Answer tree).
Always anchor edits under the relevant Question or Answer in the existing flow, not at section roots.
Reuse existing node IDs when they match intent or paragraph; otherwise propose short, consistent new IDs.
🧩 EDIT OPTIONS (choose the smallest fitting type)
REPLACE —
If the dialog reveals a statutory condition:
Convert the existing Answer into a Question with conditional Answer(s).
Only create multiple Answers when the statute defines distinct outcomes (e.g., “über 7 Tage / unter 7 Tage”).
If the law yields one outcome, use a single factual Answer — no split.
BRANCH —
Add a follow-up Question under an Answer when the dialog clarifies the same topic.
XREF —
The second alone standing question in the dialog should be treated as a side topic, insert only a cross-reference to the correct node for it (no new logic).
Do not duplicate existing siblings. Refer to them with Xref.
Do not create new top-level S* sections.
⚖️ STRUCTURAL RULES
Node types
Question — conditional or factual check (binary or A/B).
Label it with the condition, not “Kann …?” or “Darf …?”.
Answer — one sentence, statute-based, includes the citation (e.g., “§2 Abs.1”).
Xref — short pointer to another section (e.g., “→ S12”).
Deterministic vs. Conditional logic
Deterministic rule → Single Answer.
If the statute fixes the answer (“ist / gilt / bedarf”), output only one Answer node.
Do not create “Ja/Nein” branches.
Example:
A2_1["Dienstreisen bedürfen einer schriftlichen oder elektronischen Genehmigung. (§2 Abs.1)"]
Default + Exception pattern → One condition gate.
If the law states a default rule and an exception:
Model the default as an Answer (A) node.
Add one Question (Q) under it for the exception condition.
Create Ja/Nein edges only for the exception outcomes.
Example:
A2_1["Dienstreisen bedürfen grundsätzlich einer Genehmigung. (§2 Abs.1)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen Amt/Wesen nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Genehmigung erforderlich. (§2 Abs.1)"]
Scope / Applicability questions → Conditional allowed.
Use binary (Ja/Nein) only if the statute depends on a factual state (e.g., “liegt Auslandsgeschäftsort vor?”).
Never ask vague permission questions.
Avoid “Kann …? (Ja/Nein)” or “Darf …? (Ja/Nein)”.
Phrase as a statutory condition or a factual check.
Label and style rules
German only.
Present tense.
No “(Ja/Nein)” inside labels — only on edges.
Keep every Answer concise and normative.
Cite section numbers briefly (“§3 Abs.2”).
One sentence per Answer node.
🧱 TEXT INTEGRATION RULES
Attach new content under the closest related Question or Answer of the same statutory paragraph.
Prefer updating an existing Answer → Question (REPLACE) to inserting a sibling.
Only create a new node when no existing anchor fits.
When summarizing multiple items of the same legal kind (e.g., costs), keep them in one Answer sentence, not multiple nodes.
🧾 OUTPUT FORMAT
Return only the relevant Mermaid section in full (e.g., %% 3.2) where the update applies.
Do not repeat the rest of the flow.
Output exactly one fenced code block:
%% section header
...nodes and edges...
No prose, no commentary.
💡 EXAMPLES
1) Deterministic → single Answer
%% 2.1 Genehmigung
A2_1["Dienstreisen bedürfen einer schriftlichen oder elektronischen Genehmigung. (§2 Abs.1)"]
2) Default + exception
%% 2.1 Genehmigung mit Ausnahme
A2_1["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Genehmigung. (§2 Abs.1)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen Amt/Wesen nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Genehmigung erforderlich. (§2 Abs.1)"]
3) Scope condition (legitimate binary)
%% 1.1 Ausland
A1_1["Auslandsdienstreisen: §§1–11 LRKG gelten entsprechend. (§12 Abs.2–3)"]
A1_1 --> Q1_1a["Liegt mindestens ein auswärtiger Geschäftsort im Ausland?"]
Q1_1a -->|"Ja"| A1_1a_yes["Auslandsdienstreise: §§1–11 LRKG gelten entsprechend. (§12 Abs.2–3)"]
Q1_1a -->|"Nein"| A1_1a_no["Keine Auslandsdienstreise → Inlandsvorschriften (§§6,7)."]
4) Example fix for §3 Abs.2 (your earlier case)
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start/Ziel angeordnet?"]
Q3_2a -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Start/Zielpunkt. (§3 Abs.2)"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
🔒 Summary Ruleset (for the model)
Only branch when the statute creates a real conditional outcome.
Never branch “Ja/Nein” for fixed legal statements.
Strip “(Ja/Nein)” from labels.
Keep edges labeled “Ja” and “Nein” only when both outcomes exist.
Prefer factual conditions (“liegt vor?”, “wurde angeordnet?”) to permission questions (“darf?”, “kann?”).
All Answers must cite a paragraph.


"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()

dialogues = [
    {
        "id": 0,
        "title": "Gilt LRKG auch für Auslandsdienstreisen?",
        "turns": [
            {"role": "USER", "text": "Ich reise vom 10.–15.11.2025 zu einer mehrtägigen Fortbildung nach Paris; Unterkunft, Verpflegung und Fahrten fallen an. Gilt das neue Landesreisekostengesetz (LRKG) auch für Auslandsdienstreisen?"},
            {"role": "SYSTEM", "text": "Liegt mindestens ein Geschäftsort Ihrer Reise im Ausland (also Paris)?"},
            {"role": "USER", "text": "Ja — Paris ist der Geschäftsort der mehrtägigen Fortbildung."},
            {"role": "SYSTEM", "text": "Ja. Auslandsdienstreisen sind Dienstreisen mit mindestens einem Geschäftsort im Ausland (§12 Abs.1) und die §§1–11 gelten entsprechend (§12 Abs.2). Abweichend werden Auslandstage- und Auslandsübernachtungsgelder nach §3 ARV und der ARVVwV gewährt (§12 Abs.3); zudem regeln §§12 Abs.4–6 Länderzuteilung und die Kürzung ab dem 15. Aufenthaltstag."},
            {"role": "USER", "text": "Danke. Noch eine Frage: Ab wann und wie wird das Auslandstagegeld ab dem 15. Tag gekürzt?"},
            {"role": "SYSTEM", "text": "Das Auslandstagegeld wird vom 15. Tag an um 25 % ermäßigt, wenn der Aufenthalt am selben ausländischen Geschäftsort ohne Hin‑ und Rückreisetage länger als 14 Tage dauert (§ 12 Abs. 6). Die oberste Dienstbehörde kann in begründeten Fällen von der Ermäßigung absehen; ab dem 15. Tag werden statt des pauschalen Übernachtungsgeldes die nachgewiesenen notwendigen Übernachtungskosten erstattet."}
        ]
    },
    {
        "id": 1,
        "title": "Nach welchen Vorschriften werden Auslandstage-/Übernachtungsgelder geregelt?",
        "turns": [
            {"role": "USER", "text": "Ich fahre vom 12.–14. November zu einer dreitägigen Dienstreise/Teilnahme an einer Konferenz nach Paris; geplant sind Hotel, Verpflegung und lokale Verkehrskosten. Nach welchen Vorschriften werden Auslandstage- und Übernachtungsgelder geregelt?"},
            {"role": "SYSTEM", "text": "Handelt es sich um eine Auslandsdienstreise mit mindestens einem Geschäftsort im Ausland?"},
            {"role": "USER", "text": "Ja — es handelt sich um eine Auslandsdienstreise mit einem Geschäftsort in Paris."},
            {"role": "SYSTEM", "text": "Soll das Auslandstagegeld nach dem Land bestimmt werden, das Sie vor Mitternacht Ortszeit zuletzt erreichen?"},
            {"role": "USER", "text": "Ja, bitte das Auslandstagegeld nach dem Land bestimmen, das ich vor Mitternacht zuletzt erreiche."},
            {"role": "SYSTEM", "text": "Nach § 12 Abs. 3 LRKG werden Auslandstagegelder und Auslandsübernachtungsgelder nach der jeweils gültigen Fassung des § 3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt. Das Tage‑ und Übernachtungsgeld wird nach § 12 Abs. 4 für das Land bemessen, das Sie vor Mitternacht Ortszeit zuletzt erreichen; bei Flugreisen gilt als erreicht der Zeitpunkt der Landung (§ 12 Abs. 5), Zwischenlandungen bleiben unberücksichtigt, es sei denn, sie erfordern eine Übernachtung. Bei Aufenthalten am selben ausländischen Geschäftsort länger als 14 Tage wird das Auslandstagegeld ab dem 15. Tag um 25 % ermäßigt (§ 12 Abs. 6)."},
            {"role": "USER", "text": "Gilt das Landesreisekostengesetz (LRKG) auch für Dienstreisen ins Ausland?"},
            {"role": "SYSTEM", "text": "Ja. Für Auslandsdienstreisen gelten die Regelungen der §§ 1–11 entsprechend (§ 12 Abs. 2 LRKG). Abweichend werden Auslandstage‑ und Auslandsübernachtungsgelder nach § 12 Abs. 3 nach § 3 der Auslandsreisekostenverordnung (ARV) und der ARVVwV gewährt."}
        ]
    },
    {
        "id": 2,
        "title": "Braucht eine Dienstreise Anordnung/Genehmigung?",
        "turns": [
            {"role": "USER", "text": "Ich plane eine Inlands-Dienstreise: 2 Tage Fortbildung in München am 10.–11.11.2025, Anreise mit Zug, eine Hotelübernachtung (ca. 120 €) und Tagegeld/Verpflegungskosten. Braucht so eine Dienstreise eine förmliche Anordnung oder Genehmigung durch die Dienststelle?"},
            {"role": "SYSTEM", "text": "Sind Sie Richter/in oder Landesbeauftragte/r für den Datenschutz oder für die Belange von Menschen mit Behinderungen?"},
            {"role": "USER", "text": "Nein — ich bin keine/r Richter/in und auch keine/r Landesbeauftragte; ich arbeite als Mitarbeiterin in der Landesverwaltung."},
            {"role": "SYSTEM", "text": "Findet die Fortbildung außerhalb Ihres Dienstortes statt (also nicht an Ihrer regulären Dienststätte)?"},
            {"role": "USER", "text": "Ja — die Fortbildung findet außerhalb meiner regulären Dienststätte statt; meine Dienststelle ist in Düsseldorf."},
            {"role": "SYSTEM", "text": "Ja. Dienstreisen müssen grundsätzlich von der zuständigen Dienstvorgesetzten oder dem zuständigen Dienstvorgesetzten schriftlich oder elektronisch angeordnet oder genehmigt werden (§ 2 Abs. 1 LRKG). Ausnahmen gelten nur, wenn eine Anordnung wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht kommt; Dienstreisen sollen zudem nur erfolgen, wenn keine kostengünstigere Erledigung möglich ist."},
            {"role": "USER", "text": "In welcher Form muss die Anordnung erfolgen — reicht eine E‑Mail/elektronische Bestätigung, oder braucht es ein spezielles Formular oder eine Unterschrift?"},
            {"role": "SYSTEM", "text": "Meinen Sie mit „E‑Mail/elektronische Bestätigung“, dass die Anordnung per E‑Mail ergeht?"},
            {"role": "USER", "text": "Ja, genau — ich meine eine dienstliche E‑Mail oder eine Anordnung im internen elektronischen System als elektronische Bestätigung."},
            {"role": "SYSTEM", "text": "Wird die dienstliche E‑Mail von der zuständigen Dienstvorgesetzten bzw. dem zuständigen Dienstvorgesetzten gesendet?"}
        ]
    },
    {
        "id": 3,
        "title": "In welcher Form muss die Anordnung erfolgen?",
        "turns": [
            {"role": "USER", "text": "Ich plane eine dreitägige Inlandsdienstreise (10.–12.11.) nach Hannover für ein Projekttreffen; Fahrt per Bahn, Hotelübernachtung und Tagegeld fallen an. In welcher Form muss die Anordnung erfolgen — reicht mündliche Zustimmung, genügt eine E‑Mail, oder braucht es eine schriftliche/unterzeichnete Dienstanordnung?"},
            {"role": "SYSTEM", "text": "Wurde die Dienstreise von der zuständigen Dienstvorgesetzten bzw. dem zuständigen Dienstvorgesetzten angeordnet oder genehmigt?"},
            {"role": "USER", "text": "Bislang nur mündliche Zustimmung durch meine Vorgesetzte; es gibt keine E‑Mail und keine schriftliche/unterzeichnete Dienstanordnung."},
            {"role": "SYSTEM", "text": "Nach § 2 Abs. 1 muss die Anordnung oder Genehmigung schriftlich oder elektronisch erfolgen; eine E‑Mail gilt als elektronische Form und ist damit ausreichend. Eine rein mündliche Zustimmung genügt nicht; Ausnahmen regelt das Gesetz nur für bestimmte Fälle (z. B. nach § 2 Abs. 3)."},
            {"role": "USER", "text": "Danke — noch kurz: Gibt es Fälle, in denen eine mündliche Zustimmung ausreicht, z. B. bei kurzfristigen oder unaufschiebbaren Dienstreisen?"},
            {"role": "SYSTEM", "text": "Nach § 2 Abs. 1 muss die Anordnung oder Genehmigung schriftlich oder elektronisch erfolgen; eine rein mündliche Zustimmung genügt dem Gesetz nicht. Ausnahmen bestehen nur, wenn eine Anordnung oder Genehmigung nach dem Amt oder dem Wesen des Dienstgeschäfts nicht in Betracht kommt (z. B. § 2 Abs. 3 für Richter und bestimmte Beauftragte). Das LRKG enthält keine Regelung, die mündliche Zustimmungen generell für kurzfristige oder unaufschiebbare Dienstreisen erlaubt."}
        ]
    },
    {
        "id": 4,
        "title": "Gibt es Ausnahmen von der Genehmigungspflicht?",
        "turns": [
            {"role": "USER", "text": "Ich habe eine eintägige Inlandsdienstreise am 10.11.2025 nach München zur Pflichtfortbildung (Bahn, ca. 70 €), ohne Übernachtung. Im Landesreisekostengesetz: Gibt es Ausnahmen von der Genehmigungspflicht für Dienstreisen?"},
            {"role": "SYSTEM", "text": "Sind Sie Richter/in oder Landesbeauftragte/r für den Datenschutz oder Beauftragte/r der Landesregierung für die Belange von Menschen mit Behinderungen?"},
            {"role": "USER", "text": "Nein, ich gehöre keiner dieser Gruppen an. Ich bin Sachbearbeiter/in im Personalreferat."},
            {"role": "SYSTEM", "text": "Ja. Nach § 2 Abs. 1 ist grundsätzlich eine Anordnung oder Genehmigung erforderlich, es sei denn, eine Anordnung oder Genehmigung kommt wegen des Amtes der Dienstreisenden oder des Wesens des Dienstgeschäfts nicht in Betracht. Außerdem sind für Richter/innen und die genannten Landesbeauftragten nach § 2 Abs. 3 keine Genehmigungen erforderlich; die Anordnung/Genehmigung muss schriftlich oder elektronisch erfolgen."},
            {"role": "USER", "text": "Muss jede Dienstreise vorher angeordnet oder genehmigt werden?"},
            {"role": "SYSTEM", "text": "Trifft auf Ihre Dienstreise zu, dass wegen Ihres Amtes oder des Wesens des Dienstgeschäfts eine Anordnung oder Genehmigung nicht in Betracht kommt?"},
            {"role": "USER", "text": "Nein, das trifft nicht zu; ich bin Sachbearbeiter/in im Personalreferat und die Fortbildung ist eine normale eintägige Dienstreise. Muss die Dienstreise dann vorab ausdrücklich angeordnet oder genehmigt werden?"},
            {"role": "SYSTEM", "text": "Ja. Nach § 2 Abs. 1 LRKG muss Ihre beschriebene Dienstreise grundsätzlich schriftlich oder elektronisch von der zuständigen Dienstvorgesetzten angeordnet oder genehmigt werden."}
        ]
    },

    {
    "id": 5,
    "title": "Woran unterscheidet man Dienstreise und Dienstgang?",
    "turns": [
      {"role": "USER", "text": "Ich fahre am 10.11.2025 innerhalb des Bundeslandes zu einer ganztägigen Fortbildung (Abfahrt 08:00, Rückkehr 17:30) und möchte wissen, ob das als Dienstreise oder als Dienstgang gilt — ich rechne mit Fahrtkostenerstattung und Tagegeld. Woran unterscheidet man Dienstreise und Dienstgang?"},
      {"role": "SYSTEM", "text": "Ist der Fortbildungsort außerhalb Ihres Dienstortes?"},
      {"role": "USER", "text": "Ja — der Fortbildungsort liegt außerhalb meines Dienstortes (ca. 25 km entfernt). Ich fahre von meiner Wohnung dorthin."},
      {"role": "SYSTEM", "text": "Wurde die Fortbildung von Ihrer zuständigen Dienstvorgesetzten schriftlich oder elektronisch angeordnet oder genehmigt?"},
      {"role": "USER", "text": "Ja — die Teilnahme wurde von meiner Dienstvorgesetzten schriftlich per E‑Mail angeordnet."},
      {"role": "SYSTEM", "text": "Das ist eine Dienstreise (§2), weil der Fortbildungsort außerhalb Ihres Dienstortes liegt und die Teilnahme schriftlich angeordnet wurde. Sie haben Anspruch auf Fahrt-/Flugkostenerstattung bzw. bei Privat-PKW auf Wegstreckenentschädigung von 0,30 €/km; bei öffentlichen Verkehrsmitteln werden die Kosten der niedrigsten Beförderungsklasse erstattet (§§4,5). Für die mehr als 8‑stündige eintägige Reise steht Ihnen Tagegeld in Höhe von 6 € zu; beachten Sie die sechsmonatige Antragsfrist (§6 Abs.1, §3 Abs.4)."},
      {"role": "USER", "text": "Besteht bei einem Dienstgang Anspruch auf Tagegeld?"},
      {"role": "SYSTEM", "text": "Nein; für Dienstgänge besteht nach § 6 Abs. 3 kein Anspruch auf Tagegeld. Bei Dienstgängen von mehr als acht Stunden werden jedoch die nachgewiesenen notwendigen Auslagen für Verpflegung bis zur Höhe des Tagegeldes bei einer Dienstreise gleicher Dauer erstattet."}
    ]
  },


  {
    "id": 6,
    "title": "Wer bestimmt Ausgangs-/Endpunkt grundsätzlich?",
    "turns": [
      {"role": "USER", "text": "Ich plane eine eintägige Inlandsdienstreise per Zug am 15.11.2025 zur Fortbildung in München; Abreise könnte von meiner Wohnung in Augsburg oder von meiner Dienststelle erfolgen und ich will Reisekosten/Tagegeld abrechnen. Im Landesreisekostengesetz: Wer bestimmt grundsätzlich den Ausgangs- und Endpunkt der Dienstreise?"},
      {"role": "SYSTEM", "text": "Hat Ihr zuständiger Dienstvorgesetzter die Dienststätte als Ausgangs‑ oder Endpunkt der Dienstreise angeordnet?"},
      {"role": "USER", "text": "Nein — mein Vorgesetzter hat die Dienststelle nicht als Start- oder Endpunkt angeordnet."},
      {"role": "SYSTEM", "text": "Wenn die Dienststelle nicht als Ausgangs‑ oder Endpunkt angeordnet wurde, dürfen Dienstreisende Ausgangs- und Endpunkt grundsätzlich selbst bestimmen (z. B. Ihre Wohnung). Abweichend davon kann die zuständige Dienstvorgesetzte oder der zuständige Dienstvorgesetzte die Dienststätte als Ausgangs‑ oder Endpunkt anordnen."},
      {"role": "USER", "text": "Kann meine Dienststelle verbindlich anordnen, dass die Dienststätte Start- oder Zielpunkt der Reise sein muss?"},
      {"role": "SYSTEM", "text": "Ja. Die zuständige oder der zuständige Dienstvorgesetzte kann die Dienststätte als Ausgangs‑ oder Endpunkt anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt; die Anordnung muss schriftlich oder elektronisch erfolgen (§ 3 Abs. 2, § 2 Abs. 1)."}
    ]
  },
  {
    "id": 7,
    "title": "Kann die Dienststelle verbindlich die Dienststätte als Start/Ziel anordnen?",
    "turns": [
      {"role": "USER", "text": "Ich plane eine eintägige Dienstreise innerhalb des Bundeslandes am 12.11.2025 zu einem Meeting in der Außenstelle; Abfahrt wäre sonst normalerweise von meiner Wohnung, kein Hotel nötig, nur Fahrtkosten. Kann die Dienststelle verbindlich vorschreiben, dass die Reise stattdessen an der Dienststätte beginnen oder enden muss (also Start/Ziel Dienststelle statt Wohnung)?"},
      {"role": "SYSTEM", "text": "Führt die Fahrtstrecke unmittelbar an Ihrer Dienststätte vorbei?"},
      {"role": "USER", "text": "Nein — die direkte Route von meiner Wohnung zur Außenstelle führt nicht an meiner Dienststelle vorbei."},
      {"role": "SYSTEM", "text": "Nein. Nach § 3 Abs. 2 LRKG darf die Dienststelle die Dienststätte nur dann als Ausgangs- oder Endpunkt anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt; da das bei Ihrer Fahrt nicht zutrifft, kann sie das nicht verbindlich vorschreiben."},
      {"role": "USER", "text": "Danke — eine kurze Anschlussfrage: Wer legt normalerweise fest, ob eine Dienstreise an der Wohnung oder an der Dienststelle beginnen bzw. enden muss?"},
      {"role": "SYSTEM", "text": "Grundsätzlich bestimmen die Dienstreisenden selbst den Ausgangs‑ und Endpunkt unter Beachtung des Wirtschaftlichkeitsgrundsatzes. Abweichend kann der zuständige Dienstvorgesetzte die Dienststätte als Ausgangs‑ oder Endpunkt anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt (§ 3 Abs. 2 LRKG)."}
    ]
  },
  {
    "id": 8,
    "title": "Wie wird Fahrkostenerstattung bemessen, wenn die Reise an der Wohnung beginnt/endet?",
    "turns": [
      {"role": "USER", "text": "Ich plane eine Inlands-Dienstreise am 12.11.2025 zu einem ganztägigen Termin in Stadt B; Abfahrt/Ankunft ist jeweils meine Wohnung in Stadt A, einfache Strecke ca. 50 km, ich nutze mein privates Auto. Wie genau wird in diesem Gesetz die Fahrkostenerstattung bemessen, wenn die Reise an der Wohnung beginnt und endet?"},
      {"role": "SYSTEM", "text": "Hat Ihre oder Ihr zuständige Dienstvorgesetzte die Dienststätte als Ausgangs- oder Endpunkt der Dienstreise angeordnet?"},
      {"role": "USER", "text": "Nein, das wurde nicht angeordnet."},
      {"role": "SYSTEM", "text": "Da die Dienstreise an Ihrer Wohnung beginnt und endet und die Dienststätte nicht als Ausgangs‑/Endpunkt angeordnet wurde, bemisst sich die Fahrkostenerstattung nach der Entfernung von bzw. bis zur Wohnung (§ 3 Abs. 2). Bei Nutzung eines privaten Kraftfahrzeugs beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer (bei erheblichem dienstlichen Interesse 0,35 €) (§ 5 Abs. 1–2). Bei 50 km einfacher Strecke = 100 km insgesamt × 0,30 € = 30,00 €."},
      {"role": "USER", "text": "Kann die Dienststelle verbindlich anordnen, dass die Dienstreise an der Dienststätte statt an meiner Wohnung beginnt bzw. endet?"},
      {"role": "SYSTEM", "text": "Ja — die zuständige Dienstvorgesetzte kann die Dienststätte als Ausgangs‑ oder Endpunkt anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt (§ 3 Abs. 2 LRKG)."}
    ]
  },
  {
    "id": 9,
    "title": "Bin ich frei in der Wahl des Beförderungsmittels?",
    "turns": [
      {"role": "USER", "text": "Ich habe am 10.11.2025 eine ganztägige Dienstreise von meiner Wohnung in Stadt A nach Musterstadt (Inland) zur Fortbildung; mögliche Optionen sind DB-Fernzug, eigenes Auto oder Mietwagen. Bin ich dabei grundsätzlich frei in der Wahl des Beförderungsmittels?"},
      {"role": "SYSTEM", "text": "Gibt es für Ihre Reise eine unentgeltliche Beförderungsmöglichkeit (z. B. Dienstfahrkarte)?"},
      {"role": "USER", "text": "Nein — die Dienststelle stellt keine unentgeltliche Beförderung (keine Dienstfahrkarte oder Dienstwagen). Ich müsste also Bahn-Ticket selbst kaufen oder mit meinem Privat‑PKW bzw. einem Mietwagen fahren."},
      {"role": "SYSTEM", "text": "Ja — grundsätzlich sind Sie in der Wahl des Beförderungsmittels frei (§ 3 Abs. 3 LRKG). Dabei haben Sie wirtschaftliche Gesichtspunkte und den Klimaschutz zu beachten; Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit besteht (§ 3 Abs. 3). Zur Erstattung: Bahn/Flug nur in der niedrigsten Klasse (§ 4 Abs. 1), Privat-PKW nach § 5 (30 ct/km bzw. 35 ct bei erheblichem dienstlichem Interesse) und Mietwagen/Taxi nur bei triftigem Grund (§ 4 Abs. 3)."},
      {"role": "USER", "text": "Vielen Dank. Noch eine Frage: Kann die Dienststelle vorschreiben, welches Verkehrsmittel ich benutzen muss (z. B. Bahn statt Privat‑PKW)?"},
      {"role": "SYSTEM", "text": "Grundsätzlich sind Sie in der Wahl des Beförderungsmittels frei (§ 3 Abs. 3 LRKG). Dabei müssen Sie wirtschaftliche Gesichtspunkte und die Erfordernisse des Klimaschutzes beachten; Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit besteht, und Erstattungsbeschränkungen nach § 4 und § 5 können praktische Vorgaben setzen."}
    ]
  },
  {
    "id": 10,
    "title": "Kann die Dienststelle ein Verkehrsmittel vorschreiben?",
    "turns": [
      {"role": "USER", "text": "Ich habe eine Inlandsdienstreise zu einer Fortbildung vom 12.–14.11.2025 (An- und Abreise möglich mit Auto, Zug oder Flug; geschätzte Kosten: Zug ~120 €, Flug ~200 €, Hotel 2 Nächte). Kann die Dienststelle mir vorschreiben, welches Verkehrsmittel ich benutzen muss?"},
      {"role": "SYSTEM", "text": "Hat Ihre Dienststelle aus dienstlichen Gründen bereits die Benutzung eines bestimmten Verkehrsmittels angeordnet?"},
      {"role": "USER", "text": "Nein — die Dienststelle hat noch kein bestimmtes Verkehrsmittel vorgeschrieben; ich wurde nur gebeten, wirtschaftlich zu reisen und die Kosten zur Abrechnung vorzulegen."},
      {"role": "SYSTEM", "text": "Nach § 3 Abs. 3 LRKG sind Dienstreisende grundsätzlich in der Wahl des Beförderungsmittels frei; die Dienststelle kann also nicht pauschal eine bestimmte Verkehrsart vorschreiben. Sie kann aber z. B. den Ausgangs‑/Endpunkt anordnen (§ 3 Abs. 2), und Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit besteht; außerdem sind Klimaschutzaspekte zu beachten (§ 3 Abs. 3)."},
      {"role": "USER", "text": "Kurz noch: Bin ich grundsätzlich frei in der Wahl des Beförderungsmittels?"},
      {"role": "SYSTEM", "text": "Gibt es für Ihre Dienstreise eine unentgeltliche Beförderungsmöglichkeit (z. B. vom Dienstherrn oder dritter Seite)?"},
      {"role": "USER", "text": "Nein — es gibt keine unentgeltliche Beförderungsmöglichkeit für diese Dienstreise. Bin ich grundsätzlich frei in der Wahl des Verkehrsmittels?"},
      {"role": "SYSTEM", "text": "Ja. Nach § 3 Abs. 3 LRKG sind Sie grundsätzlich frei in der Wahl des Beförderungsmittels; dabei sind Wirtschaftlichkeitsgesichtspunkte und Klimaschutz zu beachten und Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit besteht."}
    ]
  },
  {
    "id": 11,
    "title": "Sind Flugkosten erstattungsfähig?",
    "turns": [
      {"role": "USER", "text": "Ich plane eine Dienstreise nach New York (Hinflug 10.11.2025, Rückflug 17.11.2025) für eine Konferenz; voraussichtliche Flugkosten ca. 900–1.400 €. Sind Flugkosten in diesem Fall erstattungsfähig?"},
      {"role": "SYSTEM", "text": "Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Klimaschutzbelangen, die die Flugnutzung rechtfertigen?"},
      {"role": "USER", "text": "Ja. Dienstliche Gründe überwiegen: Ich trete als Referent auf und habe mehrere persönliche Meetings/Netzwerktermine, die nicht virtuell möglich sind; alternative, kostengünstige Reisemöglichkeiten kommen praktisch nicht in Frage."},
      {"role": "SYSTEM", "text": "Ja. Nach § 4 Abs. 1 LRKG sind Flugkosten erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Belange des Klimaschutzes überwiegen. Erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; bei der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen."},
      {"role": "USER", "text": "Noch eine Frage: Welche Flugklasse wird grundsätzlich erstattet?"},
      {"role": "SYSTEM", "text": "Grundsätzlich werden die Kosten der niedrigsten Flugklasse erstattet (also Economy) (§ 4 Abs. 1 LRKG). Ausnahmen sind möglich bei einem Grad der Behinderung ≥ 50 oder gesundheitlichen Gründen (§ 4 Abs. 2) sowie bei besonderen dienstlichen Gründen oder durch Anordnung der obersten Dienstbehörde (§ 4 Abs. 1)."}
    ]
  },
  {
    "id": 12,
    "title": "Welche Flugklasse gilt grundsätzlich?",
    "turns": [
      {"role": "USER", "text": "Ich plane eine dreitägige Auslandsdienstreise nach Paris (10.–12.11.) für Dienstbesprechungen; voraussichtliche Flugkosten ca. 300 € (Hin- und Rückflug). Welche Flugklasse gilt grundsätzlich nach dem Landesreisekostengesetz?"},
      {"role": "SYSTEM", "text": "Haben Sie einen Grad der Behinderung von mindestens 50 oder einen gesundheitlichen Grund, der die Benutzung einer höheren Flugklasse rechtfertigt?"},
      {"role": "USER", "text": "Nein, ich habe keinen Grad der Behinderung ≥50 und es liegen keine gesundheitlichen Gründe für eine höhere Flugklasse vor."},
      {"role": "SYSTEM", "text": "Nach § 4 Absatz 1 werden grundsätzlich nur die Kosten der niedrigsten Flugklasse erstattet. Flugkosten sind nur erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Belange des Klimaschutzes überwiegen; das Finanzministerium kann Ausnahmen bestimmen."},
      {"role": "USER", "text": "Gibt es Ausnahmen, in denen ausnahmsweise eine höhere Flugklasse erstattet wird, und wer entscheidet darüber?"},
      {"role": "SYSTEM", "text": "Ja. Nach § 4 Abs. 2 werden bei einem Grad der Behinderung von mindestens 50 oder bei gesundheitlicher Notwendigkeit die Auslagen für die nächsthöhere Klasse erstattet. Außerdem kann die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde bei besonderen dienstlichen Gründen Ausnahmen zulassen, und das Finanzministerium kann durch Verwaltungsvorschrift weitere Ausnahmen bestimmen."}
    ]
  },
  {
    "id": 13,
    "title": "Wie sind Reservierungen/Tarifunterschiede zu behandeln?",
    "turns": [
      {"role": "USER", "text": "Ich habe nächste Woche eine zweitägige Inlandsdienstreise zu einer Fortbildung und überlege, ob ich ein teureres flexibles Ticket mit Sitzplatzreservierung oder einen günstigeren Spartarif ohne Umbuchung kaufe — die Bahn/Fluggesellschaft bieten beides an. Wie sind Reservierungen und Tarifunterschiede dabei zu behandeln?"},
      {"role": "SYSTEM", "text": "Haben Sie einen Grad der Behinderung von mindestens 50 oder einen gesundheitlichen Grund, der die Benutzung einer höheren Beförderungsklasse rechtfertigt?"},
      {"role": "USER", "text": "Nein — ich habe keinen GdB ≥50 und keine gesundheitlichen Gründe."},
      {"role": "SYSTEM", "text": "Da Sie keinen GdB ≥50 genannt haben: Nach § 4 Absatz 1 werden nur die Kosten der niedrigsten Beförderungsklasse erstattet (bei Flügen grundsätzlich die niedrigste Flugklasse). Zu Sitzplatzreservierungen oder zu Erstattungsregelungen für flexible gegenüber Spartarifen enthält das LRKG keine relevanten Informationen."},
      {"role": "USER", "text": "Da das LRKG dazu nichts regelt: Wer entscheidet konkret, ob Sitzplatzreservierungen oder teurere flexible Tarife erstattet werden — das zuständige Landesministerium, die einzelne Dienststelle oder eine Verwaltungsvorschrift?"},
      {"role": "SYSTEM", "text": "Das LRKG regelt Sitzplatzreservierungen nicht ausdrücklich. § 4 Abs. 1 legt jedoch fest, dass Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde für ihren Geschäftsbereich zulassen kann und das Finanzministerium durch Verwaltungsvorschrift Ausnahmen bestimmen kann."}
    ]
  },
  {
    "id": 14,
    "title": "Wie hoch ist die Entschädigung für Privat-KFZ (Ct/km)?",
    "turns": [
      {"role": "USER", "text": "Ich plane am 05.11.2025 eine dienstliche Inlandsfahrt mit meinem privaten Pkw zu Außendienstterminen (einfach 120 km). Wie hoch ist die Entschädigung pro Kilometer (Ct/km) für Privat-KFZ nach dem Landesreisekostengesetz?"},
      {"role": "SYSTEM", "text": "Besteht an der Benutzung Ihres privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"},
      {"role": "USER", "text": "Ja — es besteht erhebliches dienstliches Interesse, weil keine zumutbare öffentliche Direktverbindung besteht und die Termine zeitlich eng getaktet sind."},
      {"role": "SYSTEM", "text": "Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 35 Cent je Kilometer (§ 5 Abs. 2 LRKG)."},
      {"role": "USER", "text": "Danke — kurze Zusatzfrage: Wann genau gilt der erhöhte Satz von 35 Ct/km; welche Voraussetzungen müssen dafür konkret vorliegen?"},
      {"role": "SYSTEM", "text": "Nach § 5 Abs. 2 LRKG gilt der erhöhte Satz von 35 Cent/km, wenn an der Benutzung eines Kraftfahrzeugs ein erhebliches dienstliches Interesse besteht. Das LRKG benennt keine näheren, konkreten Kriterien zur Definition dieses „erheblichen dienstlichen Interesses“. Mit Zustimmung der obersten Dienstbehörde kann zudem ein Zuschlag von 5 Cent/km gewährt werden, wenn regelmäßig Fahrten auf unbefestigten oder schwer befahrbaren Wegen erforderlich sind."}
    ]
  },
  {
    "id": 15,
    "title": "Wie hoch ist Tagegeld für einen vollen Kalendertag?",
    "turns": [
      {"role": "USER", "text": "Ich habe eine zweitägige Inlandsfortbildung nächsten Monat (Abfahrt morgens, Übernachtung, Rückkehr am nächsten Abend) und trage die Verpflegungskosten selbst. Wie hoch ist das Tagegeld für einen vollen Kalendertag?"},
      {"role": "SYSTEM", "text": "Ist der betreffende Tag ein voller Kalendertag der Dienstreise (also nicht An- oder Abreisetag)?"},
      {"role": "USER", "text": "Ja — es handelt sich um einen vollen Kalendertag der Dienstreise (kein An- oder Abreisetag)."},
      {"role": "SYSTEM", "text": "Das Tagegeld beträgt 24 Euro für jeden vollen Kalendertag einer Dienstreise (§ 6 Absatz 1 LRKG)."},
      {"role": "USER", "text": "Gibt es unterschiedliche Sätze für Inlands- und Auslandsdienstreisen?"},
      {"role": "SYSTEM", "text": "Ja. Das Inlandstagegeld beträgt 24 € (§ 6 Abs. 1); für Auslandsdienstreisen gelten abweichende Auslandstagegelder nach § 12 Abs. 3 (gemäß der Auslandsreisekostenverordnung des Bundes). Das Übernachtungsgeld ist im Inland 20 € und im Ausland 30 € (§ 7 Abs. 1)."}
    ]
  },
  {
    "id": 16,
    "title": "Wie viel Tagegeld steht am An-/Abreisetag bei >8 Std / >14 Std zu?",
    "turns": [
      {"role": "USER", "text": "Ich plane eine zweitägige Inlandsdienstreise (z. B. 5.–6.11.) zur Fortbildung; am An- bzw. Abreisetag bin ich jeweils mehr als 8 Stunden unterwegs, teils auch über 14 Stunden. Wie viel Tagegeld steht mir am An- bzw. Abreisetag bei >8 Std. bzw. >14 Std. Abwesenheit zu?"},
      {"role": "SYSTEM", "text": "Beginnt und endet die Dienstreise an Ihrer Wohnung (nicht an der Dienststätte)?"},
      {"role": "USER", "text": "Ja — die Dienstreise beginnt an meiner Wohnung und endet dort wieder."},
      {"role": "SYSTEM", "text": "Bei An- und Abreisetag: bei mehr als 8 Stunden 6 Euro, bei mehr als 14 Stunden 12 Euro (§ 6 Abs. 1). Für jeden vollen Kalendertag zwischen An- und Abreisetag beträgt das Tagegeld 24 Euro. Die Dienstreisedauer bemisst sich nach Abreise und Ankunft an der Wohnung (§ 6 Abs. 2)."},
      {"role": "USER", "text": "Gibt es unterschiedliche Sätze für Tagegeld zwischen Inlands- und Auslandsdienstreisen?"},
      {"role": "SYSTEM", "text": "Ja. Für Inlandsdienstreisen gilt §6 (24 € pro voller Kalendertag; 6 € bei >8 Std., 12 € bei >14 Std.), für Auslandsdienstreisen werden Auslandstage- und Auslandsübernachtungsgelder abweichend nach §12 Abs. 3 nach der jeweils gültigen Fassung der ARV und ARVVwV gewährt."}
    ]
  },
  {
    "id": 17,
    "title": "Wie wird Tagegeld bei unentgeltlicher Verpflegung gekürzt?",
    "turns": [
      {"role": "USER", "text": "Ich fahre vom 2.–4. Juni zu einer dreitägigen Fortbildung im Land; Frühstück im Hotel und Mittagessen werden vom Veranstalter unentgeltlich gestellt. Wie wird in diesem Fall das Tagegeld gekürzt, wenn Mahlzeiten unentgeltlich sind?"},
      {"role": "SYSTEM", "text": "Handelt es sich an allen drei Tagen um volle Kalendertage mit Anspruch auf das volle Tagegeld von 24 Euro?"},
      {"role": "USER", "text": "Ja — an allen drei Tagen habe ich Anspruch auf das volle Tagegeld (jeweils 24 €)."},
      {"role": "SYSTEM", "text": "Ja — nach § 6 Abs. 4 wird für Frühstück 20 % und für das Mittagessen 40 % des vollen Tagegeldes einbehalten, also bei Frühstück + Mittag insgesamt 60 %. Das sind 14,40 € Kürzung (60 % von 24 €), verbleiben 9,60 € pro Tag; bei drei vollen Tagen also insgesamt 28,80 €."},
      {"role": "USER", "text": "Danke, Tschüss."},
      {"role": "SYSTEM", "text": "Gern geschehen, Tschüss."}
    ]
  },
  {
    "id": 18,
    "title": "Wie hoch ist das pauschale Übernachtungsgeld im Inland?",
    "turns": [
      {"role": "USER", "text": "Ich habe nächste Woche eine fünftägige Dienstreise innerhalb Deutschlands (Mo–Fr) nach München für Besprechungen; ich buche das Hotel selbst und lege Rechnungen vor. Wie hoch ist das pauschale Übernachtungsgeld im Inland?"},
      {"role": "SYSTEM", "text": "Wird Ihnen die Unterkunft unentgeltlich bereitgestellt oder ist das Entgelt für die Unterkunft bereits in erstattungsfähigen Kosten enthalten (ja/nein)?"},
      {"role": "USER", "text": "Nein."},
      {"role": "SYSTEM", "text": "Das pauschale Übernachtungsgeld im Inland beträgt 20 Euro pro notwendiger Übernachtung (§ 7 Abs. 1 LRKG). Höhere Übernachtkosten werden im notwendigen Umfang erstattet; die Höhe des Notwendigen wird durch Verwaltungsvorschrift bestimmt."},
      {"role": "USER", "text": "Noch eine Frage: Wie hoch ist das Tagegeld für einen vollen Kalendertag bei einer Dienstreise im Inland?"},
      {"role": "SYSTEM", "text": "Das Tagegeld beträgt für jeden vollen Kalendertag 24 Euro (§ 6 Abs. 1 LRKG)."}
    ]
  },
  {
    "id": 19,
    "title": "Bis wann muss Reisekostenvergütung beantragt werden (Ausschlussfrist)?",
    "turns": [
      {"role": "USER", "text": "Ich war vom 1.–3. Oktober dienstlich in Hamburg zu einer Fortbildung und habe Bahn, Hotel und Verpflegung selbst bezahlt. Bis wann muss ich die Reisekostenvergütung beantragen — gibt es dafür eine Ausschlussfrist?"},
      {"role": "SYSTEM", "text": "Haben Sie die Reisekostenvergütung bereits schriftlich oder elektronisch beantragt?"},
      {"role": "USER", "text": "Nein — ich habe die Reisekostenvergütung noch nicht beantragt."},
      {"role": "SYSTEM", "text": "Sie müssen die Reisekostenvergütung schriftlich oder elektronisch innerhalb einer Ausschlussfrist von sechs Monaten nach Beendigung der Dienstreise beantragen; die Frist beginnt am Tag nach Beendigung (bei Ihnen also 4. Oktober) und läuft sechs Monate. Damit ist der Antrag spätestens bis zum 4. April zu stellen; die zuständigen Stellen können Belege verlangen, die auf Anforderung binnen eines Monats vorzulegen sind, andernfalls kann der Antrag insoweit abgelehnt werden."},
      {"role": "USER", "text": "Noch eine Frage: Bis wann können die Stellen Belege verlangen, und welche Folgen hat es, wenn ich die angeforderten Belege nicht rechtzeitig vorlege?"},
      {"role": "SYSTEM", "text": "Die zuständigen Stellen können die Vorlage der maßgeblichen Kostenbelege bis zum Ablauf von sechs Monaten nach Antragstellung verlangen. Werden die Belege auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden."}
    ]
  }

]



extension = """
```mermaid
%% 1.1 Geltungsbereich (Auslandsanwendung)
Q1_1["Gilt LRKG auch für Auslandsdienstreisen?"]
A1_1["Grundsatz: Die Vorschriften §§1–11 gelten für Auslandsdienstreisen entsprechend. (§12 Abs.2–3)"]
Q1_1 --> A1_1
A1_1 --> Q1_1a["Liegt mindestens ein auswärtiger Geschäftsort im Ausland (Definition §12 Abs.1)?"]
Q1_1a -->|"Ja"| A1_1a_yes["Auslandsdienstreise: §§1–11 LRKG gelten entsprechend; Auslandstage‑ und Auslandsübernachtungsgelder richten sich nach ARV/ARVVwV. (§12 Abs.1–3)"]
Q1_1a -->|"Nein"| A1_1a_no["Keine Auslandsdienstreise; für Inland gelten die regulären Sätze und Vorschriften. (§12 Abs.2–3)"]
A1_1a_yes --> X1_1_day15["→ S11C"]
```
Processed dialog 1/20
```mermaid
%% 1.1 Geltungsbereich (Auslandsanwendung)
Q1_1["Gilt LRKG auch für Auslandsdienstreisen?"]
A1_1["Grundsatz: Die Vorschriften §§1–11 gelten für Auslandsdienstreisen entsprechend. (§12 Abs.2–3)"]
Q1_1 --> A1_1
A1_1 --> Q1_1a["Liegt mindestens ein auswärtiger Geschäftsort im Ausland (Definition §12 Abs.1)?"]
Q1_1a -->|"Ja"| A1_1a_yes["Auslandsdienstreise: §§1–11 LRKG gelten entsprechend; Auslandstage‑ und Auslandsübernachtungsgelder richten sich nach ARV/ARVVwV. (§12 Abs.1–3)"]
Q1_1a -->|"Nein"| A1_1a_no["Keine Auslandsdienstreise; für Inland gelten die regulären Sätze und Vorschriften. (§12 Abs.2–3)"]
A1_1a_yes --> Q1_1a_dayrules["Welche Vorschriften gelten für Auslandstage‑/Auslandsübernachtungsgelder und welches Land bestimmt die Bemessung?"]
Q1_1a_dayrules --> A1_1a_day["Auslandstagegelder und Auslandsübernachtungsgelder werden nach der jeweils geltenden Fassung des § 3 der Auslandsreisekostenverordnung (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt; das Tage‑ und Übernachtungsgeld bemisst sich nach dem Land, das Sie vor Mitternacht Ortszeit zuletzt erreichen (bei Flugreisen gilt als erreicht der Zeitpunkt der Landung; Zwischenlandungen bleiben unberücksichtigt, es sei denn, sie erfordern eine Übernachtung) und bei Aufenthalten am selben ausländischen Geschäftsort länger als 14 Tage wird das Auslandstagegeld ab dem 15. Tag um 25 % ermäßigt. (§12 Abs.3–6)"]
A1_1a_yes --> X1_1_day15["→ S11C"]
```
Processed dialog 2/20
```mermaid
%% 2.1 Genehmigung / Anordnung von Dienstreisen
A2_1["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung oder Genehmigung. (§2 Abs.1 LRKG)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Anordnung/Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1)"]
A2_1 --> Q2_1_form["In welcher Form muss die Anordnung erfolgen?"]
Q2_1_form --> A2_1_form["Schriftlich oder elektronisch (z. B. dienstliche E‑Mail oder internes elektronisches System). (§2 Abs.1)"]
A2_1_form --> X2_1_mail["→ Zuständigkeit/Vertretung bei der Anordnung prüfen (wer sendet/zeichnet) → S2.3"]
```
Processed dialog 3/20
```mermaid
%% 2.1 Genehmigung / Anordnung von Dienstreisen
A2_1["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung oder Genehmigung. (§2 Abs.1 LRKG)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Anordnung/Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1)"]
A2_1 --> Q2_1_form["In welcher Form muss die Anordnung erfolgen?"]
Q2_1_form --> A2_1_form["Schriftlich oder elektronisch (z. B. dienstliche E‑Mail oder internes elektronisches System); eine rein mündliche Zustimmung genügt nicht. (§2 Abs.1)"]
A2_1_form --> X2_1_mail["→ Zuständigkeit/Vertretung bei der Anordnung prüfen (wer sendet/zeichnet) → S2.3"]
A2_1_form --> X2_1_oral["→ Mündliche Zustimmung genügt nicht; Ausnahmen prüfen → Q2_1_exc"]
```
Processed dialog 4/20
```mermaid
%% 2.1 Genehmigung / Anordnung von Dienstreisen
A2_1["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung oder Genehmigung. (§2 Abs.1 LRKG)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Anordnung/Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1)"]
A2_1 --> Q2_1_form["In welcher Form muss die Anordnung erfolgen?"]
Q2_1_form --> A2_1_form["Schriftlich oder elektronisch (z. B. dienstliche E‑Mail oder internes elektronisches System); eine rein mündliche Zustimmung genügt nicht. (§2 Abs.1)"]
A2_1_form --> X2_1_mail["→ Zuständigkeit/Vertretung bei der Anordnung prüfen (wer sendet/zeichnet) → S2.3"]
A2_1_form --> X2_1_oral["→ Mündliche Zustimmung genügt nicht; Ausnahmen prüfen → Q2_1_exc"]
A2_1 --> X2_1_spec["→ Sonderregel prüfen: Richter/innen und bestimmte Landesbeauftragte benötigen keine Genehmigung (§2 Abs.3) → S2.3"]
```
Processed dialog 5/20
```mermaid
%% 2.1 Genehmigung / Anordnung von Dienstreisen
A2_1["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung oder Genehmigung. (§2 Abs.1 LRKG)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Anordnung/Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1)"]
A2_1 --> Q2_1_loc["Liegt der Fortbildungs-/Geschäftsort außerhalb Ihres Dienstortes?"]
Q2_1_loc -->|"Ja"| A2_1_loc_yes["Liegt der Fortbildungs-/Geschäftsort außerhalb des Dienstortes, handelt es sich um eine Dienstreise; prüfen, ob die Teilnahme angeordnet/genehmigt wurde. (§2 Abs.1)"]
Q2_1_loc -->|"Nein"| A2_1_loc_no["Liegt der Geschäfts- oder Fortbildungsort nicht außerhalb des Dienstortes, liegt keine Dienstreise vor (Dienstgang). (§2 Abs.1)"]
A2_1_loc_yes --> X2_1_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A2_1_loc_no --> X2_1_tg["→ Tagegeldanspruch bei Dienstgang prüfen → S6"]
A2_1 --> Q2_1_form["In welcher Form muss die Anordnung erfolgen?"]
Q2_1_form --> A2_1_form["Schriftlich oder elektronisch (z. B. dienstliche E‑Mail oder internes elektronisches System); eine rein mündliche Zustimmung genügt nicht. (§2 Abs.1)"]
A2_1_form --> X2_1_mail["→ Zuständigkeit/Vertretung bei der Anordnung prüfen (wer sendet/zeichnet) → S2.3"]
A2_1_form --> X2_1_oral["→ Mündliche Zustimmung genügt nicht; Ausnahmen prüfen → Q2_1_exc"]
A2_1 --> X2_1_spec["→ Sonderregel prüfen: Richter/innen und bestimmte Landesbeauftragte benötigen keine Genehmigung (§2 Abs.3) → S2.3"]
```
Processed dialog 6/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
```
Processed dialog 7/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
```
Processed dialog 8/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> A3_2a_no_calc["Fahrkostenerstattung bemisst sich nach der Entfernung von bzw. bis zur Wohnung; bei Nutzung eines privaten Kraftfahrzeugs beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer (bei erheblichem dienstlichen Interesse 0,35 €); z.B. 50 km einfache Strecke = 100 km × 0,30 € = 30,00 €. (§3 Abs.2; §5 Abs.1–2)"]
```
Processed dialog 9/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> A3_2a_no_calc["Fahrkostenerstattung bemisst sich nach der Entfernung von bzw. bis zur Wohnung; bei Nutzung eines privaten Kraftfahrzeugs beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer (bei erheblichem dienstlichen Interesse 0,35 €); z.B. 50 km einfache Strecke = 100 km × 0,30 € = 30,00 €. (§3 Abs.2; §5 Abs.1–2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]
```
Processed dialog 10/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> A3_2a_no_calc["Fahrkostenerstattung bemisst sich nach der Entfernung von bzw. bis zur Wohnung; bei Nutzung eines privaten Kraftfahrzeugs beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer (bei erheblichem dienstlichen Interesse 0,35 €); z.B. 50 km einfache Strecke = 100 km × 0,30 € = 30,00 €. (§3 Abs.2; §5 Abs.1–2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]
```
Processed dialog 11/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> A3_2a_no_calc["Fahrkostenerstattung bemisst sich nach der Entfernung von bzw. bis zur Wohnung; bei Nutzung eines privaten Kraftfahrzeugs beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer (bei erheblichem dienstlichen Interesse 0,35 €); z.B. 50 km einfache Strecke = 100 km × 0,30 € = 30,00 €. (§3 Abs.2; §5 Abs.1–2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]
```
Processed dialog 12/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> A3_2a_no_calc["Fahrkostenerstattung bemisst sich nach der Entfernung von bzw. bis zur Wohnung; bei Nutzung eines privaten Kraftfahrzeugs beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer (bei erheblichem dienstlichen Interesse 0,35 €); z.B. 50 km einfache Strecke = 100 km × 0,30 € = 30,00 €. (§3 Abs.2; §5 Abs.1–2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]
```
Processed dialog 13/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> A3_2a_no_calc["Fahrkostenerstattung bemisst sich nach der Entfernung von bzw. bis zur Wohnung; bei Nutzung eines privaten Kraftfahrzeugs beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer (bei erheblichem dienstlichen Interesse 0,35 €); z.B. 50 km einfache Strecke = 100 km × 0,30 € = 30,00 €. (§3 Abs.2; §5 Abs.1–2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]

A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse (z. B. Sitzplatzreservierungen, Tarifdifferenzen)?"]
Q3_3d --> A3_3d["Die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]
```
Processed dialog 14/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> Q3_2a_no_calc_rate["Besteht an der Benutzung des privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"]
Q3_2a_no_calc_rate -->|"Ja"| A3_2a_no_calc_yes["Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 0,35 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.2)"]
Q3_2a_no_calc_rate -->|"Nein"| A3_2a_no_calc_no["Ohne erhebliches dienstliches Interesse beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.1)"]
A3_2a_no_calc_yes --> X3_2a_no_calc_xref["→ Keine nähere Definition des „erheblichen dienstlichen Interesses“ im LRKG; nähere Regelungen oder Zuschläge können durch die oberste Dienstbehörde bestimmt werden. (§5 Abs.2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]

A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse (z. B. Sitzplatzreservierungen, Tarifdifferenzen)?"]
Q3_3d --> A3_3d["Die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]
```
Processed dialog 15/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> Q3_2a_no_calc_rate["Besteht an der Benutzung des privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"]
Q3_2a_no_calc_rate -->|"Ja"| A3_2a_no_calc_yes["Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 0,35 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.2)"]
Q3_2a_no_calc_rate -->|"Nein"| A3_2a_no_calc_no["Ohne erhebliches dienstliches Interesse beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.1)"]
A3_2a_no_calc_yes --> X3_2a_no_calc_xref["→ Keine nähere Definition des „erheblichen dienstlichen Interesses“ im LRKG; nähere Regelungen oder Zuschläge können durch die oberste Dienstbehörde bestimmt werden. (§5 Abs.2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]
A3_3 --> X3_3_tg["→ Tagegeld: Inland 24 € je voller Kalendertag; Übernachtungsgeld Inland 20 €, Ausland 30 €. (§6 Abs.1; §7 Abs.1; §12 Abs.3)"]

A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse (z. B. Sitzplatzreservierungen, Tarifdifferenzen)?"]
Q3_3d --> A3_3d["Die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]
```
Processed dialog 16/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> Q3_2a_no_calc_rate["Besteht an der Benutzung des privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"]
Q3_2a_no_calc_rate -->|"Ja"| A3_2a_no_calc_yes["Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 0,35 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.2)"]
Q3_2a_no_calc_rate -->|"Nein"| A3_2a_no_calc_no["Ohne erhebliches dienstliches Interesse beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.1)"]
A3_2a_no_calc_yes --> X3_2a_no_calc_xref["→ Keine nähere Definition des „erheblichen dienstlichen Interesses“ im LRKG; nähere Regelungen oder Zuschläge können durch die oberste Dienstbehörde bestimmt werden. (§5 Abs.2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]

A3_3 --> A3_3_tg_full["Tagegeld (Inland): 24 € je voller Kalendertag. (§6 Abs.1)"]
A3_3_tg_full --> Q3_3_tg_14["Übersteigt die Abwesenheit am An- oder Abreisetag 14 Stunden?"]
Q3_3_tg_14 -->|"Ja"| A3_3_tg_14["Am An- bzw. Abreisetag bei >14 Std. Abwesenheit beträgt das Tagegeld 12 €. (§6 Abs.1)"]
Q3_3_tg_14 -->|"Nein"| Q3_3_tg_8["Übersteigt die Abwesenheit am An- oder Abreisetag 8 Stunden?"]
Q3_3_tg_8 -->|"Ja"| A3_3_tg_8["Am An- bzw. Abreisetag bei >8 Std. Abwesenheit beträgt das Tagegeld 6 €. (§6 Abs.1)"]
Q3_3_tg_8 -->|"Nein"| A3_3_tg_none["Bei ≤8 Std. Abwesenheit am An‑ bzw. Abreisetag besteht kein Tagegeldanspruch. (§6 Abs.1)"]
A3_3_tg_full --> X3_3_tg_dur["→ Dienstreisedauer bemisst sich nach Abreise und Ankunft an der Wohnung. (§6 Abs.2)"]
A3_3_tg_full --> X3_3_tg_scope["→ Für Auslandsdienstreisen gelten abweichende Auslandstage‑/Übernachtungsgelder nach §12 Abs.3 i.V.m. ARV/ARVVwV. (§12 Abs.3)"]

A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse (z. B. Sitzplatzreservierungen, Tarifdifferenzen)?"]
Q3_3d --> A3_3d["Die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]
```
Processed dialog 17/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> Q3_2a_no_calc_rate["Besteht an der Benutzung des privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"]
Q3_2a_no_calc_rate -->|"Ja"| A3_2a_no_calc_yes["Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 0,35 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.2)"]
Q3_2a_no_calc_rate -->|"Nein"| A3_2a_no_calc_no["Ohne erhebliches dienstliches Interesse beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.1)"]
A3_2a_no_calc_yes --> X3_2a_no_calc_xref["→ Keine nähere Definition des „erheblichen dienstlichen Interesses“ im LRKG; nähere Regelungen oder Zuschläge können durch die oberste Dienstbehörde bestimmt werden. (§5 Abs.2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]

A3_3 --> A3_3_tg_full["Tagegeld (Inland): 24 € je voller Kalendertag. (§6 Abs.1)"]
A3_3_tg_full --> Q3_3_tg_14["Übersteigt die Abwesenheit am An- oder Abreisetag 14 Stunden?"]
Q3_3_tg_14 -->|"Ja"| A3_3_tg_14["Am An- bzw. Abreisetag bei >14 Std. Abwesenheit beträgt das Tagegeld 12 €. (§6 Abs.1)"]
Q3_3_tg_14 -->|"Nein"| Q3_3_tg_8["Übersteigt die Abwesenheit am An- oder Abreisetag 8 Stunden?"]
Q3_3_tg_8 -->|"Ja"| A3_3_tg_8["Am An- bzw. Abreisetag bei >8 Std. Abwesenheit beträgt das Tagegeld 6 €. (§6 Abs.1)"]
Q3_3_tg_8 -->|"Nein"| A3_3_tg_none["Bei ≤8 Std. Abwesenheit am An‑ bzw. Abreisetag besteht kein Tagegeldanspruch. (§6 Abs.1)"]
A3_3_tg_full --> X3_3_tg_dur["→ Dienstreisedauer bemisst sich nach Abreise und Ankunft an der Wohnung. (§6 Abs.2)"]
A3_3_tg_full --> X3_3_tg_scope["→ Für Auslandsdienstreisen gelten abweichende Auslandstage‑/Übernachtungsgelder nach §12 Abs.3 i.V.m. ARV/ARVVwV. (§12 Abs.3)"]
A3_3_tg_full --> Q3_3_tg_meal["Werden Mahlzeiten unentgeltlich gestellt?"]
Q3_3_tg_meal -->|"Ja"| A3_3_tg_meal_yes["Für Frühstück sind 20 % und für das Mittagessen 40 % des vollen Tagegeldes einzubehalten; bei Frühstück und Mittag zusammen insgesamt 60 %. (§6 Abs.4)"]
Q3_3_tg_meal -->|"Nein"| A3_3_tg_meal_no["Keine Kürzung des Tagegeldes wegen Mahlzeiten. (§6 Abs.4)"]

A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse (z. B. Sitzplatzreservierungen, Tarifdifferenzen)?"]
Q3_3d --> A3_3d["Die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]
```
Processed dialog 18/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> Q3_2a_no_calc_rate["Besteht an der Benutzung des privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"]
Q3_2a_no_calc_rate -->|"Ja"| A3_2a_no_calc_yes["Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 0,35 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.2)"]
Q3_2a_no_calc_rate -->|"Nein"| A3_2a_no_calc_no["Ohne erhebliches dienstliches Interesse beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.1)"]
A3_2a_no_calc_yes --> X3_2a_no_calc_xref["→ Keine nähere Definition des „erheblichen dienstlichen Interesses“ im LRKG; nähere Regelungen oder Zuschläge können durch die oberste Dienstbehörde bestimmt werden. (§5 Abs.2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]

A3_3 --> A3_3_tg_full["Tagegeld (Inland): 24 € je voller Kalendertag. (§6 Abs.1)"]
A3_3_tg_full --> Q3_3_tg_14["Übersteigt die Abwesenheit am An- oder Abreisetag 14 Stunden?"]
Q3_3_tg_14 -->|"Ja"| A3_3_tg_14["Am An- bzw. Abreisetag bei >14 Std. Abwesenheit beträgt das Tagegeld 12 €. (§6 Abs.1)"]
Q3_3_tg_14 -->|"Nein"| Q3_3_tg_8["Übersteigt die Abwesenheit am An- oder Abreisetag 8 Stunden?"]
Q3_3_tg_8 -->|"Ja"| A3_3_tg_8["Am An- bzw. Abreisetag bei >8 Std. Abwesenheit beträgt das Tagegeld 6 €. (§6 Abs.1)"]
Q3_3_tg_8 -->|"Nein"| A3_3_tg_none["Bei ≤8 Std. Abwesenheit am An‑ bzw. Abreisetag besteht kein Tagegeldanspruch. (§6 Abs.1)"]
A3_3_tg_full --> X3_3_tg_dur["→ Dienstreisedauer bemisst sich nach Abreise und Ankunft an der Wohnung. (§6 Abs.2)"]
A3_3_tg_full --> X3_3_tg_scope["→ Für Auslandsdienstreisen gelten abweichende Auslandstage‑/Übernachtungsgelder nach §12 Abs.3 i.V.m. ARV/ARVVwV. (§12 Abs.3)"]
A3_3_tg_full --> Q3_3_tg_meal["Werden Mahlzeiten unentgeltlich gestellt?"]
Q3_3_tg_meal -->|"Ja"| A3_3_tg_meal_yes["Für Frühstück sind 20 % und für das Mittagessen 40 % des vollen Tagegeldes einzubehalten; bei Frühstück und Mittag zusammen insgesamt 60 %. (§6 Abs.4)"]
Q3_3_tg_meal -->|"Nein"| A3_3_tg_meal_no["Keine Kürzung des Tagegeldes wegen Mahlzeiten. (§6 Abs.4)"]

A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse (z. B. Sitzplatzreservierungen, Tarifdifferenzen)?"]
Q3_3d --> A3_3d["Die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]

A3_3 --> A3_3_uebern["Übernachtungsgeld (Inland): Das pauschale Übernachtungsgeld beträgt 20 € je notwendiger Übernachtung; höhere Übernachtungskosten werden im notwendigen Umfang erstattet, die Höhe des Notwendigen bestimmt eine Verwaltungsvorschrift. (§7 Abs.1)"]
A3_3_uebern --> X3_3_tg_ref["→ Siehe Tagegeld (Inland) → A3_3_tg_full"]
```
Processed dialog 19/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte als Start- oder Endpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
A3_2_route_yes --> X3_2_formref["→ Form der Anordnung prüfen → Q2_1_form"]
A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
Q3_2a_no_calc --> Q3_2a_no_calc_rate["Besteht an der Benutzung des privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"]
Q3_2a_no_calc_rate -->|"Ja"| A3_2a_no_calc_yes["Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 0,35 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.2)"]
Q3_2a_no_calc_rate -->|"Nein"| A3_2a_no_calc_no["Ohne erhebliches dienstliches Interesse beträgt die Wegstreckenentschädigung 0,30 € je gefahrenem Kilometer. (§3 Abs.2; §5 Abs.1)"]
A3_2a_no_calc_yes --> X3_2a_no_calc_xref["→ Keine nähere Definition des „erheblichen dienstlichen Interesses“ im LRKG; nähere Regelungen oder Zuschläge können durch die oberste Dienstbehörde bestimmt werden. (§5 Abs.2)"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende ist in der Wahl des Beförderungsmittels frei; wirtschaftliche Gesichtspunkte und der Klimaschutz sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
Q3_3a -->|"Nein"| A3_3a_no["Wahl des Beförderungsmittels bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
Q3_3b -->|"Ja"| A3_3b_yes["Eine dienstliche Anordnung der Benutzung eines bestimmten Beförderungsmittels gilt und schränkt die Wahl ein. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
A3_3 --> Q3_3c["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]
Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten sind erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; in der Wirtschaftlichkeitsprüfung sind auch Kosten für Ausgleichszahlungen zu berücksichtigen. (§4 Abs.1)"]
Q3_3c -->|"Nein"| A3_3c_no["Flugkosten sind nicht erstattungsfähig, da die Belange des Klimaschutzes überwiegen. (§4 Abs.1)"]
A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥ 50 oder eine gesundheitliche Notwendigkeit vor?"]
Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei Grad der Behinderung ≥ 50 oder gesundheitlicher Notwendigkeit werden die Auslagen für die nächsthöhere Flugklasse erstattet. (§4 Abs.2)"]
Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf die niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
A3_3c_yes --> X3_3_flightexc["→ Siehe Ausnahmen und besondere Regelungen (z. B. Grad der Behinderung ≥ 50, gesundheitliche Gründe, besondere dienstliche Anordnung) → §4 Abs.2 ff."]
A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]

A3_3 --> Q3_3e["Welche Ausschlussfrist gilt für die Beantragung der Reisekostenvergütung?"]
Q3_3e --> A3_3e["Reisekostenvergütung ist schriftlich oder elektronisch innerhalb von sechs Monaten nach Beendigung der Dienstreise zu beantragen; die Frist beginnt am Tag nach Beendigung. (§10 Abs.1)"]
A3_3e --> X3_3_belege["→ Vorlage der Kostenbelege prüfen (Vorlagefrist: auf Anforderung binnen 1 Monat; bei Nichtvorlage kann der Antrag insoweit abgelehnt werden). (§10 Abs.2)"]

A3_3 --> A3_3_tg_full["Tagegeld (Inland): 24 € je voller Kalendertag. (§6 Abs.1)"]
A3_3_tg_full --> Q3_3_tg_14["Übersteigt die Abwesenheit am An- oder Abreisetag 14 Stunden?"]
Q3_3_tg_14 -->|"Ja"| A3_3_tg_14["Am An- bzw. Abreisetag bei >14 Std. Abwesenheit beträgt das Tagegeld 12 €. (§6 Abs.1)"]
Q3_3_tg_14 -->|"Nein"| Q3_3_tg_8["Übersteigt die Abwesenheit am An- oder Abreisetag 8 Stunden?"]
Q3_3_tg_8 -->|"Ja"| A3_3_tg_8["Am An- bzw. Abreisetag bei >8 Std. Abwesenheit beträgt das Tagegeld 6 €. (§6 Abs.1)"]
Q3_3_tg_8 -->|"Nein"| A3_3_tg_none["Bei ≤8 Std. Abwesenheit am An‑ bzw. Abreisetag besteht kein Tagegeldanspruch. (§6 Abs.1)"]
A3_3_tg_full --> X3_3_tg_dur["→ Dienstreisedauer bemisst sich nach Abreise und Ankunft an der Wohnung. (§6 Abs.2)"]
A3_3_tg_full --> X3_3_tg_scope["→ Für Auslandsdienstreisen gelten abweichende Auslandstage‑/Übernachtungsgelder nach §12 Abs.3 i.V.m. ARV/ARVVwV. (§12 Abs.3)"]
A3_3_tg_full --> Q3_3_tg_meal["Werden Mahlzeiten unentgeltlich gestellt?"]
Q3_3_tg_meal -->|"Ja"| A3_3_tg_meal_yes["Für Frühstück sind 20 % und für das Mittagessen 40 % des vollen Tagegeldes einzubehalten; bei Frühstück und Mittag zusammen insgesamt 60 %. (§6 Abs.4)"]
Q3_3_tg_meal -->|"Nein"| A3_3_tg_meal_no["Keine Kürzung des Tagegeldes wegen Mahlzeiten. (§6 Abs.4)"]

A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von der Erstattung der niedrigsten Beförderungsklasse (z. B. Sitzplatzreservierungen, Tarifdifferenzen)?"]
Q3_3d --> A3_3d["Die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]

A3_3 --> A3_3_uebern["Übernachtungsgeld (Inland): Das pauschale Übernachtungsgeld beträgt 20 € je notwendiger Übernachtung; höhere Übernachtungskosten werden im notwendigen Umfang erstattet, die Höhe des Notwendigen bestimmt eine Verwaltungsvorschrift. (§7 Abs.1)"]
A3_3_uebern --> X3_3_tg_ref["→ Siehe Tagegeld (Inland) → A3_3_tg_full"]
```"""
def _strip_code_fences(s: str) -> str:
    if s is None:
        return ""
    s = s.strip()
    s = re.sub(r"^```(?:mermaid)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```$", "", s, flags=re.IGNORECASE)
    return s.strip()

def _extract_mermaid_block(s: str) -> str:
    if not s:
        return ""
    m = re.search(r"```mermaid\s*(.+?)\s*```", s, flags=re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else s.strip()

def split_mermaid_blocks(s: str) -> List[str]:
    if not s:
        return []
    return re.findall(r"```mermaid\s*(.+?)\s*```", s, flags=re.DOTALL | re.IGNORECASE)


# ---------- CORE MERGE ----------
def _merge_once(flow_content: str, extension_block: str) -> str:
    flow_clean = _strip_code_fences(flow_content)
    ext_clean = _strip_code_fences(extension_block)
    if not ext_clean:
        return flow_clean

    prompt = f"""
    You are integrating a Mermaid dialog extension into an existing Mermaid flow.

    EXISTING FLOW (FULL):
    ```mermaid
    {flow_clean}
    EXTENSION:
    {ext_clean}
    RULES
    Integrate at the correct node(s), respecting logic, hierarchy, and S1…S13 boundaries.
    Rephrase questions for clarity if needed.
    Convert declaratives to factual checks when appropriate.
    Side topics → XREFs only.
    Keep S1…S13 intact.
    Answers must be concise and cite the paragraph.
    Label conditionals clearly; use Ja/Nein edges only when outcomes differ.
    OUTPUT
    Return ONLY one block:
    <ENTIRE UPDATED FLOW>
    """
    print("\n------------------------------------------")
    print(f"→ Merging one extension ({len(ext_clean)} chars)")
    print("------------------------------------------")
    t0 = time.perf_counter()
    resp = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
      
    )
    print(f"✓ API call done in {time.perf_counter() - t0:.2f}s")
    merged = resp.choices[0].message.content.strip()
    updated = _extract_mermaid_block(merged)
    print(f"→ Extension merged; length now {len(updated)} chars")
    # Save each intermediate result for inspection
    Path("merge_steps").mkdir(exist_ok=True)
    Path(f"merge_steps/step_{int(time.time())}.mmd").write_text(
        f"```mermaid\n{updated}\n```", encoding="utf-8"
    )
    return updated if updated else flow_clean

def merge_flow_multi_all(flow_content: str, extensions: List[str]) -> str:
    current = _strip_code_fences(flow_content)
    total = len(extensions)
    print(f"Total extensions to merge: {total}")
    i=0
    for ext in extensions:
        print(f"\n=== Processing extension {i+1}/{total} ===")
        current = _merge_once(current, ext)
    return f"```mermaid\n{current}\n```"


if __name__ == "__main__":
    print("Merging extensions...")
    extensions = split_mermaid_blocks(extension)

    if not extensions:
        final_graph = f"```mermaid\n{_strip_code_fences(flow)}\n```"
    else:
        final_graph = merge_flow_multi_all(flow, extensions)

    print(final_graph)
    OUT_PATH.write_text(final_graph, encoding="utf-8")
    print(f"Saved: {OUT_PATH.resolve()}")
