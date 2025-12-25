from openai import OpenAI
import re
from pathlib import Path
from typing import List
import time


OPENAI_API_KEY =""
client = OpenAI(api_key=OPENAI_API_KEY)


# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_SMART.txt", "r", encoding="utf-8") as f:
    document = f.read()

#with open("/Users/diana/Desktop/BW_Gesetz.txt", "r", encoding="utf-8") as f:
#    document = f.read()


#with open("/Users/diana/Desktop/MasterThesis/Improved_Graph.md", "r", encoding="utf-8") as f:
#    flow = f.read()

with open("/Users/diana/Desktop/MasterThesis/PHA_Improvement_2.md", "r", encoding="utf-8") as f:
    flow = f.read()

OUT_PATH = Path("/Users/diana/Desktop/MasterThesis/PHA_Improved_Graph_After_Merging_FINAL.md")


def merge_flow_multi (flow, multiturndialog, document):
    prompt = f"""
You are given:
the existing Mermaid flow {flow}
one multi-turn dialog {multiturndialog}


Your task is to rearrange the nodes within the correct branch of the flow into a clearer, chatbot-like follow-up structure.
The rearrangement must follow the logical sequence demonstrated by the dialogue and must improve guided user navigation.

---

## STEP 1 — Identify the relevant branch

Identify the branch whose MAIN QUESTION corresponds to the user’s initial question in the multi-turn dialogue.
Identify which existing Q-nodes or A-nodes in that branch correspond to the dialogue’s intermediate questions or its answer content.

---

## STEP 2 — Determine whether reorganisation is meaningful

Reorganisation is meaningful only if the dialogue shows:

• clear logical dependencies between some of the branch’s existing questions
• or a need to guide the user through Yes/No diagnostic checks
• or a need for separate final outcomes for different scenarios (Yes vs. No)

If the dialogue does not reveal such relations, leave the branch unchanged.

---

## STEP 3 — Build a “main question + follow-up checks” structure

If reorganisation is meaningful, restructure the branch according to this pattern:

MAIN QUESTION
 → DIRECT ANSWER (if applicable)
 → FOLLOW-UP CHECK 1 (Yes/No)
  → answer for YES
  → answer for NO
 → FOLLOW-UP CHECK 2 (Yes/No)
  → answer for YES
  → answer for NO
 → OPTIONAL: FINAL SUMMARY for Yes and for No scenarios

### Important distinction:

### ✔ **A. Diagnostic questions (user-dependent):**

Questions about the user’s situation (e.g., “Sind Sie …?”, “Trifft dies zu?”)
→ must use explicit Yes/No branching:

```
Q_NODE -->|"Ja"| A_NODE_YES
Q_NODE -->|"Nein"| A_NODE_NO
```

### ✔ **B. General informational questions (not user-dependent):**

Questions that are **not checks about the user**, and have **only one factual answer**
(e.g., “Wer ist zuständig und in welcher Form soll angeordnet werden?”)
→ must **NOT** use Yes/No branching
→ these remain single-answer follow-up nodes
→ may still appear after the main question as a follow-up

**Do NOT force Yes/No structure on general factual questions.**

### Additional mandatory rules:

• Do NOT introduce new follow-up checks.
• Use only Q-nodes from the original branch.
• No hanging or disconnected nodes are allowed.

---

## STEP 4 — Reuse existing nodes; allow conversational reformulation

• Reuse Q-nodes and A-nodes from the branch if they appear in the dialogue.
• You may conversationally reformulate Q-nodes so they sound like chatbot diagnostic questions.
• Reformulation may change perspective, but the meaning must remain identical.
• Remove old edges and attach nodes correctly in the new hierarchy.
• A node must never appear twice.

---

## STEP 5 — Do NOT create new FAQ nodes

• Do not create new Q-nodes with new legal content.
• Only reuse existing nodes (with optional conversational reformulation).
• You may add Yes/No edges, but no entirely new Q-nodes.

---

## STEP 6 — Preserve unrelated nodes

Any Q/A pair in the branch that:
• does not appear in the dialogue, and
• is not needed in the follow-up logic

→ must remain in its original placement, untouched.

---

## STEP 7 — Final answer nodes

When the logic distinguishes a Yes-scenario from a No-scenario, produce **two** final summary answers:

• one for the Yes-scenario
• one for the No-scenario

These summaries must be concise, legally accurate, and must not copy earlier node texts verbatim.

---

## OUTPUT FORMAT

Return:

1. Only the updated Mermaid code block for the affected branch
2. Aassign a new branch name to this branch if necessary (optional)

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
      "id": 1,
      "title": "Braucht eine Dienstreise eine Anordnung/Genehmigung?",
      "turns": [
        {"role": "USER", "text": "Ich plane vom 10.–12. Dez. eine Inlands-Dienstreise nach München zu einer mehrtägigen Fortbildung (Bahn 2. Kl., Hotel, ca. 400 € Übernachtungskosten). Braucht eine Dienstreise eine Anordnung/Genehmigung?"},
        {"role": "SYSTEM", "text": "Wurde die Dienstreise von Ihrer zuständigen Dienstvorgesetzten schriftlich oder elektronisch angeordnet oder genehmigt?"},
        {"role": "USER", "text": "Nein — bisher wurde die Reise nicht angeordnet oder genehmigt."},
        {"role": "SYSTEM", "text": "Ja. Nach § 2 Abs. 1 müssen Dienstreisen grundsätzlich schriftlich oder elektronisch angeordnet oder genehmigt werden; Ausnahmen bestehen nur, wenn eine Anordnung nach dem Amt oder dem Wesen des Dienstgeschäfts nicht in Betracht kommt. Für Richterinnen und Richter sowie bestimmte Beauftragte gelten nach § 2 Abs. 3 besondere Ausnahmen."},
        {"role": "USER", "text": "Danke — noch eine Frage: Gibt es Fälle, in denen ich ohne schriftliche oder elektronische Anordnung Dienstreisen antreten darf (z. B. kurzfristige Fahrten oder besondere Dienstgänge)?"},
        {"role": "SYSTEM", "text": "Ja. § 2 Abs. 1 sieht eine Ausnahme vor, wenn eine Anordnung oder Genehmigung nach dem Amt der Dienstreisenden oder dem Wesen des Dienstgeschäfts nicht in Betracht kommt. § 2 Abs. 3 nennt zudem ausdrücklich Ausnahmen für Richterinnen und Richter sowie bestimmte Beauftragte (Landesdatenschutz- und Behindertenbeauftragte). Das LRKG nennt keine weiteren konkreten Beispiele (z. B. kurzfristige Fahrten)."}
      ]
    },
    {
      "id": 2,
      "title": "Woran unterscheidet man Dienstreise und Dienstgang?",
      "turns": [
        {"role": "USER", "text": "Ich habe eine eintägige Dienstfahrt am 25.11.2025 innerhalb des Bundeslands ohne Übernachtung (Abfahrt von meiner Wohnung, privates Auto, Fahrt- und Parkkosten) zu einem Behördenmeeting. Woran unterscheidet man in diesem Gesetz Dienstreise und Dienstgang?"},
        {"role": "SYSTEM", "text": "Findet das Meeting außerhalb Ihrer Dienststätte statt?"},
        {"role": "USER", "text": "Ja, das Meeting findet außerhalb meiner Dienststätte in einem anderen Behördengebäude in derselben Stadt statt."},
        {"role": "SYSTEM", "text": "Nach § 2 LRKG sind Dienstreisen Reisen zur Erledigung dienstlicher Aufgaben außerhalb des Dienstortes, Dienstgänge sind Reisen zur Erledigung dienstlicher Aufgaben außerhalb der Dienststätte am Dienst- oder Wohnort. Weil Ihr Meeting außerhalb Ihrer Dienststätte, aber in derselben Stadt und von Ihrer Wohnung aus angetreten wird, fällt dies gemäß § 2 Absatz 2 als Dienstgang. Beide erfordern in der Regel eine Anordnung oder Genehmigung."},
        {"role": "USER", "text": "Besteht bei Dienstgang Anspruch auf Tagegeld?"},
        {"role": "SYSTEM", "text": "Dauert der Dienstgang mehr als acht Stunden?"},
        {"role": "USER", "text": "Nein — voraussichtlich nicht. Gesamtdauer inkl. An-/Abfahrt etwa 6 Stunden (z. B. Anfahrt 09:00, Meeting 10:00–14:00, Rückfahrt bis 15:00)."},
        {"role": "SYSTEM", "text": "Nein. Nach § 6 Abs. 3 LRKG besteht bei Dienstgängen kein Anspruch auf Tagegeld; da Ihr Dienstgang etwa 6 Stunden dauert, wird kein Tagegeld gewährt. Bei Dienstgängen von mehr als acht Stunden können die nachgewiesenen notwendigen Verpflegungsaufwendungen bis zur Höhe des entsprechenden Tagegeldes erstattet werden."}
      ]
    },
    {
      "id": 3,
      "title": "Wer bestimmt Ausgangs-/Endpunkt der Reise?",
      "turns": [
        {"role": "USER", "text": "Ich plane eine eintägige Dienstreise innerhalb des Bundeslandes am 12.12.2025 zu einem Kundentermin in Musterstadt, fahre mit meinem privaten Pkw und möchte Fahrtkosten/Tagegeld abrechnen. Wer bestimmt grundsätzlich, ob Start/Ende der Reise meine Wohnung oder die Dienststätte ist?"},
        {"role": "SYSTEM", "text": "Führt Ihre Fahrtstrecke unmittelbar an Ihrer Dienststätte vorbei?"},
        {"role": "USER", "text": "Nein, sie führt nicht unmittelbar an meiner Dienststelle vorbei."},
        {"role": "SYSTEM", "text": "Grundsätzlich dürfen Sie Ausgangs- und Endpunkt Ihrer Dienstreise selbst bestimmen (z. B. Ihre Wohnung). Eine Anordnung der Dienststätte als Ausgangs- oder Endpunkt durch die oder den zuständigen Dienstvorgesetzten kommt nur in Betracht, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt — was bei Ihnen nicht der Fall ist."},
        {"role": "USER", "text": "Kann meine Dienststelle verbindlich vorschreiben, dass die Dienstreise an der Dienststelle beginnen oder enden muss?"},
        {"role": "SYSTEM", "text": "Grundsätzlich dürfen Sie Ausgangs- und Endpunkt selbst bestimmen. Die oder der zuständige Dienstvorgesetzte kann jedoch die Dienststätte als Ausgangs- oder Endpunkt anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt (§ 3 Abs. 2 LRKG)."}
      ]
    },
    
    {
      "id": 4,
      "title": "Freiheit in der Wahl des Beförderungsmittels",
      "turns": [
        {"role": "USER", "text": "Ich plane eine Inlandsdienstreise am 10.12.2025 von Stuttgart nach Berlin zur ganztägigen Fortbildung, Hin- und Rückfahrt am selben Tag; Bahn ca. 150 €, Flug ca. 200 €, Privat-PKW nach Kilometerpauschale. Bin ich frei in der Wahl des Beförderungsmittels?"},
        {"role": "SYSTEM", "text": "Besteht für diese Dienstreise eine unentgeltliche Beförderungsmöglichkeit (z. B. Dienstwagen)?"},
        {"role": "USER", "text": "Nein — es gibt keine unentgeltliche Beförderungsmöglichkeit; ein Dienstwagen steht nicht zur Verfügung."},
        {"role": "SYSTEM", "text": "Ja: Dienstreisende sind grundsätzlich frei in der Wahl des Beförderungsmittels (§3 Abs.3). Sie müssen dabei wirtschaftliche Gesichtspunkte und den Klimaschutz beachten; Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit besteht (§3 Abs.3), Erstattung erfolgt grundsätzlich nur bis zur niedrigsten Beförderungsklasse bei regelmäßig verkehrenden Verkehrsmitteln (§4 Abs.1) und bei Privat-PKW nach Wegstreckenentschädigung 0,30 €/km (§5 Abs.1)."},
        {"role": "USER", "text": "Danke, das beantwortet meine Frage. Kann die Dienststelle für diese Reise ein bestimmtes Verkehrsmittel vorschreiben?"},
        {"role": "SYSTEM", "text": "Hat die zuständige Dienstvorgesetzte bereits ausdrücklich ein bestimmtes Beförderungsmittel vorgeschrieben?"},
        {"role": "USER", "text": "Nein — die zuständige Vorgesetzte hat kein bestimmtes Beförderungsmittel vorgeschrieben."},
        {"role": "SYSTEM", "text": "Da die zuständige Vorgesetzte kein Beförderungsmittel vorgeschrieben hat, gilt nach § 3 Abs. 3 LRKG die grundsätzliche Wahlfreiheit der Dienstreisenden. Beachten müssen Sie dabei wirtschaftliche Gesichtspunkte und Klimaschutz; erstattet wird grundsätzlich nur die niedrigste Beförderungsklasse (§ 4 Abs. 1)."}
      ]
    },

    {
      "id": 5,
      "title": "Flugkosten und Flugklasse",
      "turns": [
        {"role": "USER", "text": "Ich habe eine Dienstreise nach Brüssel vom 5.–7. Dezember 2025 (Konferenz). Im Landesreisekostengesetz: Sind Flugkosten erstattungsfähig und welche Flugklasse wird grundsätzlich übernommen?"},
        {"role": "SYSTEM", "text": "Überwiegen bei Ihrer Flugreise dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"},
        {"role": "USER", "text": "Dienstliche Gründe überwiegen — die persönliche Teilnahme an der Konferenz ist fachlich erforderlich und nicht durch virtuelle Teilnahme ersetzbar."},
        {"role": "SYSTEM", "text": "Haben Sie einen Grad der Behinderung von mindestens 50 oder besteht aus gesundheitlichen Gründen die Notwendigkeit, eine höhere Flugklasse zu nutzen?"},
        {"role": "USER", "text": "Nein, ich habe keinen Grad der Behinderung ≥50 und aus gesundheitlichen Gründen ist eine höhere Flugklasse nicht erforderlich."},
        {"role": "SYSTEM", "text": "Ja — Flugkosten sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Belange des Klimaschutzes überwiegen. Erstattet werden grundsätzlich die Kosten der niedrigsten Flugklasse; eine Erstattung der nächsthöheren Klasse kommt nur bei einem Grad der Behinderung ≥50 oder bei medizinischer Notwendigkeit in Betracht, und Ausgleichszahlungen sind in die Wirtschaftlichkeitsberechnung einzubeziehen."},
        {"role": "USER", "text": "Wer entscheidet, ob in meinem Fall ausnahmsweise die nächsthöhere Flugklasse übernommen wird?"},
        {"role": "SYSTEM", "text": "Die Entscheidung trifft die oberste Dienstbehörde oder die von ihr ermächtigte nachgeordnete Behörde (§ 4 Abs. 1). Bei einem Grad der Behinderung ≥50 oder bei gesundheitlicher Notwendigkeit ist die Erstattung der nächsthöheren Klasse nach § 4 Abs. 2 möglich."}
      ]
    },

    {
      "id": 6,
      "title": "Kilometerentschädigung Privat-KFZ",
      "turns": [
        {"role": "USER", "text": "Ich plane am 10.12.2025 eine innerlandliche Dienstfahrt mit meinem Privat-Pkw (ca. 120 km einfach) zu einer dienstlichen Besprechung; Parkgebühren und Maut fallen an. In dem Landesreisekostengesetz: Wie hoch ist die Kilometerentschädigung für Privat-KFZ (Ct/km) und unter welchen Bedingungen gilt der erhöhte Satz von 35 Ct/km?"},
        {"role": "SYSTEM", "text": "Besteht an der Benutzung Ihres Privat-Kfz ein erhebliches dienstliches Interesse (ja/nein)?"},
        {"role": "USER", "text": "Ja — wegen engem Zeitplan und fehlender gleichwertiger ÖPNV-Verbindung."},
        {"role": "SYSTEM", "text": "Die Wegstreckenentschädigung beträgt grundsätzlich 30 Cent je Kilometer; bei einem erheblichen dienstlichen Interesse (wie von Ihnen angegeben) 35 Cent je Kilometer (§ 5 Abs. 1–2 LRKG). Zusätzlich kann mit Zustimmung der obersten Dienstbehörde ein Zuschlag von 5 Cent/km gewährt werden, wenn regelmäßig Fahrten auf unbefestigten oder schwer befahrbaren Wegen nötig sind (§ 5 Abs. 2)."},
        {"role": "USER", "text": "Wer entscheidet, ob bei einer Fahrt der erhöhte Satz von 35 Ct/km gilt — die zuständige Dienststelle oder muss das die oberste Dienstbehörde genehmigen?"},
        {"role": "SYSTEM", "text": "Das LRKG enthält keine relevanten Informationen zu Ihrer Frage."}
      ]
    },

    {
      "id": 7,
      "title": "Mietwagen, Taxi, Carsharing und Nachweise",
      "turns": [
        {"role": "USER", "text": "Ich habe nächste Woche (1.–3. Dezember) eine dreitägige Inlandsdienstreise zu Terminen in verschiedenen Städten und plane gelegentlich Fahrten mit Mietwagen, Taxi oder Carsharing. Wann werden Mietwagen, Taxi und Carsharing erstattet und welche Nachweise bzw. Abrechnungsregeln gelten dafür laut Landesreisekostengesetz?"},
        {"role": "SYSTEM", "text": "Lag bei den geplanten Fahrten ein triftiger Grund für die Nutzung von Mietwagen, Taxi oder Carsharing vor?"},
        {"role": "USER", "text": "Ja — es liegen triftige Gründe vor: enge Terminketten in verschiedenen Städten mit zeitkritischen Terminen und teilweise ungünstigen ÖPNV-Verbindungen sowie Transport von Unterlagen/kleinem Equipment zwischen Terminen. Deshalb plane ich kurze Transfers mit Taxi/Carsharing und für ganztägige, flexible Ortswechsel einen Mietwagen."},
        {"role": "SYSTEM", "text": "Bei Vorliegen eines triftigen Grundes werden die erforderlichen Kosten für Mietwagen, Taxi oder Carsharing erstattet (§4 Abs. 3 LRKG). Fehlt ein triftiger Grund, darf die Vergütung nicht höher sein als bei Benutzung eines öffentlichen Verkehrsmittels; bei Carsharing erfolgt keine Kürzung der Mitgliedsgebühr wegen privater Nutzung (§4 Abs. 3). Die Vergütung ist schriftlich oder elektronisch binnen sechs Monaten nach Reiseende zu beantragen; die Dienststelle kann Belege bis sechs Monate nach Antrag verlangen (bei Nichtvorlage binnen 1 Monat kann abgelehnt werden) und die Belege sind nach Erstattung bis zu einem Jahr aufzubewahren (§3 Abs. 4)."},
        {"role": "USER", "text": "Wie genau soll ich beim Carsharing abrechnen und welche Belege muss ich dafür einreichen (z. B. Fahrtnachweis, Rechnung, Mitgliedsbestätigung)?"},
        {"role": "SYSTEM", "text": "Das LRKG legt nicht konkret fest, welche konkreten Belege (z. B. Fahrtnachweis, Rechnung, Mitgliedsbestätigung) vorzulegen sind. Es sieht jedoch vor, dass die zuständigen Stellen bis sechs Monate nach Antrag die Vorlage der maßgeblichen Kostenbelege verlangen können und diese nach Erstattung ein Jahr aufzubewahren sind (§3 Abs.4) und dass bei Carsharing die Mitgliedsgebühr wegen privater Nutzung nicht gekürzt wird (§4 Abs.3)."}
      ]
    },

    {
      "id": 8,
      "title": "Kürzung des Tagegelds bei unentgeltlicher Verpflegung",
      "turns": [
        {"role": "USER", "text": "Ich habe eine dreitägige Dienstreise im Inland vom 12.–14.12. zur Fortbildung; Übernachtung ist gebucht und an zwei Tagen werden mir Mittag- und Abendessen vom Veranstalter unentgeltlich gestellt. Wie wird in so einem Fall das Tagegeld gekürzt?"},
        {"role": "SYSTEM", "text": "Wird an einem der drei Tage auch das Frühstück unentgeltlich bereitgestellt?"},
        {"role": "USER", "text": "Nein, Frühstück wird an keinem der drei Tage unentgeltlich bereitgestellt."},
        {"role": "SYSTEM", "text": "Handelt es sich an den zwei Tagen, an denen Mittag- und Abendessen unentgeltlich gestellt werden, jeweils um volle Kalendertage mit Anspruch auf das volle Tagegeld von 24 €?"},
        {"role": "USER", "text": "Ja — an beiden Tagen handelt es sich jeweils um volle Kalendertage mit Anspruch auf das volle Tagegeld von 24 €."},
        {"role": "SYSTEM", "text": "Nach § 6 Abs. 4 LRKG werden für Frühstück 20 % und für Mittag-/Abendessen je 40 % des Tagegeldes (24 €) einbehalten; bei den beiden vollen Tagen mit Mittag+Abend sind somit 80 % = 19,20 € einzubehalten, verbleiben 4,80 € pro Tag. Am dritten Tag ohne bereitgestellte Mahlzeiten erhalten Sie 24 €, insgesamt also 24 € + 4,80 € + 4,80 € = 33,60 €."},
        {"role": "USER", "text": "Danke, das beantwortet meine Frage. Noch eine kurze Frage: Besteht Tagegeldanspruch bei einem Dienstgang (z. B. kurzer Außentermin), oder gilt das nur für Dienstreisen?"},
        {"role": "SYSTEM", "text": "Für Dienstgänge besteht kein Anspruch auf Tagegeld (§ 6 Abs. 3 LRKG). Bei Dienstgängen von mehr als acht Stunden werden jedoch die nachgewiesenen notwendigen Verpflegungsaufwendungen bis zur Höhe des Tagegeldes bei einer Dienstreise gleicher Dauer erstattet."}
      ]
    },

    {
      "id": 9,
      "title": "Übernachtungsgelder Inland und Ausland",
      "turns": [
        {"role": "USER", "text": "Ich fahre Mitte September (3 Tage) zu einer dienstlichen Fortbildung nach Berlin und brauche dafür Hotelübernachtungen. Wie hoch sind die pauschalen Übernachtungsgelder für Inland und Ausland und wann entfällt der Anspruch (z. B. bei Arbeitgebergestellung)?"},
        {"role": "SYSTEM", "text": "Wird Ihnen die Unterkunft vom Arbeitgeber unentgeltlich bereitgestellt?"},
        {"role": "USER", "text": "Nein — mir wird keine Unterkunft unentgeltlich gestellt; ich buche das Hotel selbst."},
        {"role": "SYSTEM", "text": "Für Inland 20 Euro und für Ausland 30 Euro pauschal je § 7 Abs. 1 LRKG. Der Anspruch entfällt nach § 7 Abs. 2 u. a. bei Benutzung von Beförderungsmitteln, bei Aufenthalt in eigener Wohnung, bei unentgeltlich vom Dienstherrn bereitgestellter Unterkunft (auch wenn diese ohne triftigen Grund nicht genutzt wird) oder wenn die Unterkunftskosten in erstattungsfähigen Fahrt- oder sonstigen Kosten enthalten sind; ein zusätzlicher Anspruch besteht nur bei zusätzlich notwendiger Übernachtung wegen zu früher Ankunft oder zu später Abfahrt."},
        {"role": "USER", "text": "Wer legt die Höchstbeträge für erstattungsfähige höhere Übernachtungskosten fest, falls mein Hotel teurer ist als die Pauschale?"},
        {"role": "SYSTEM", "text": "Das Finanzministerium legt das durch eine Verwaltungsvorschrift fest (§7 Abs.1 und §14 LRKG)."}
      ]
    },

    {
      "id": 10,
      "title": "Pauschalvergütung statt Einzelvergütung",
      "turns": [
        {"role": "USER", "text": "Ich bin Sachbearbeiter und habe monatlich 2–3 eintägige Dienstreisen im Land (meist Fahrt ab Wohnung, 6–10 Std.) und gelegentlich mehrtägige Fortbildungen mit Übernachtung; typische Kosten sind Verpflegung, Übernachtung, Park/ÖPNV. Kann statt einzelner Tage-/Übernachtungs- und Auslagenerstattung eine Pauschalvergütung (Aufwandsvergütung) oder regelmäßige Pauschale gezahlt werden — und wie wird die Höhe dafür bemessen?"},
        {"role": "SYSTEM", "text": "Hat Ihre oberste Dienstbehörde bereits eine Aufwands- oder Pauschvergütungsregelung für Ihren Geschäftsbereich eingeführt?"},
        {"role": "USER", "text": "Nein — meine oberste Dienstbehörde hat bisher keine Aufwands- oder Pauschvergütungsregelung eingeführt und meine Dienststelle zahlt auch keine regelmäßige Pauschale."},
        {"role": "SYSTEM", "text": "Nach §9 LRKG können Aufwandsvergütungen oder Pauschvergütungen nur durch die oberste Dienstbehörde oder eine von ihr ermächtigte nachgeordnete Behörde eingeführt werden. Die Aufwandsvergütung wird nach näherer Bestimmung der Behörde festgelegt; die Pauschvergütung bemisst sich nach dem Durchschnitt der in einem bestimmten Zeitraum sonst anfallenden Einzelvergütungen (§9 Abs.1–2)."},
        {"role": "USER", "text": "Kannst du mir noch kurz erklären, wie genau die Höhe der Pauschalvergütung berechnet wird — welche Auslagen (z. B. Verpflegung, Übernachtung, Park/ÖPNV) werden dabei berücksichtigt und über welchen Zeitraum wird der Durchschnitt gebildet?"},
        {"role": "SYSTEM", "text": "Soll die Pauschvergütung anstelle der gesamten Reisekostenvergütung gewährt werden?"},
        {"role": "USER", "text": "Ja. Die Pauschale soll anstelle der gesamten Reisekostenvergütung gezahlt werden — also Verpflegung, Übernachtung und sonstige Auslagen (z. B. Park/ÖPNV) für meine regelmäßigen eintägigen Dienstreisen und gelegentlichen mehrtägigen Fortbildungen."},
        {"role": "SYSTEM", "text": "Nach § 9 Abs. 2 LRKG kann die oberste Dienstbehörde bei regelmäßigen oder gleichartigen Dienstreisen anstelle der Reisekostenvergütung eine Pauschvergütung gewähren; sie bemisst sich nach dem Durchschnitt der in einem bestimmten Zeitraum sonst anfallenden Einzelvergütungen. Damit werden grundsätzlich die Bestandteile der Reisekostenvergütung zugrunde gelegt (Fahrt-/Flugkosten §4, Wegstreckenentschädigung §5, Tagegeld §6, Übernachtungsgeld §7, Auslagenerstattung §8 und sonstige Nebenkosten §10), die genaue Auswahl der berücksichtigten Auslagen, der Zeitraum für den Durchschnitt und die konkrete Berechnungsweise bestimmt jedoch die oberste Dienstbehörde durch nähere Festlegungen. Da Ihre oberste Dienstbehörde bisher keine Regelung eingeführt hat, kann aktuell keine solche Pauschalvergütung gezahlt werden."}
      ]
    },

    {
      "id": 11,
      "title": "Ausschlussfrist, Belege, Aufbewahrung",
      "turns": [
        {"role": "USER", "text": "Ich habe eine dreitägige Dienstreise innerhalb Deutschlands (Weiterbildung) vom 10.–12. September dieses Jahres, mit Bahn, Hotel, Verpflegung, Taxi und Parkkosten. Bis wann muss ich die Reisekostenvergütung beantragen, welche Belege kann die Stelle verlangen und wie lange muss ich diese Belege aufbewahren?"},
        {"role": "SYSTEM", "text": "Ist die Dienstreise bereits beendet?"},
        {"role": "USER", "text": "Nein, die Dienstreise ist noch nicht beendet; sie steht noch bevor."},
        {"role": "SYSTEM", "text": "Sie müssen die Reisekostenvergütung schriftlich oder elektronisch innerhalb von sechs Monaten nach Beendigung der Dienstreise beantragen; bei Ihrer Reise (Ende 12. September) beginnt die Frist am 13. September und läuft damit bis zum 13. März des Folgejahres. Die zuständige Stelle kann bis zum Ablauf von sechs Monaten nach Antragstellung die Vorlage der maßgeblichen Kostenbelege verlangen; werden diese auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Antrag insoweit abgelehnt werden. Nach Erstattung müssen Sie die Kostenbelege für Zwecke der Rechnungsprüfung bis zum Ablauf eines Jahres aufbewahren und auf Verlangen vorlegen."},
        {"role": "USER", "text": "Danke — noch eine Frage: Wann beginnt die sechsmonatige Ausschlussfrist genau — am Tag nach dem Ende der Dienstreise oder am letzten Reisetag?"},
        {"role": "SYSTEM", "text": "Die sechsmonatige Ausschlussfrist beginnt mit dem Tag nach Beendigung der Dienstreise (§ 3 Abs. 4). In den Fällen des § 10 Abs. 2 beginnt die Frist mit Ablauf des Tages, an dem die Dienstreise geendet hätte."}
      ]
    },

    {
      "id": 12,
      "title": "LRKG für Auslandsdienstreisen",
      "turns": [
        {"role": "USER", "text": "Ich plane eine dreitägige Auslandsdienstreise nach Paris nächste Woche (Geschäftsmeetings, Hotel, Verpflegung, Bahn/Flug), daher geht es mir um Erstattung von Tage- und Übernachtungsgeldern. Gilt das neue Landesreisekostengesetz auch für Auslandsdienstreisen?"},
        {"role": "SYSTEM", "text": "Handelt es sich um eine Dienstreise, bei der mindestens ein Geschäftsort im Ausland liegt (z. B. Paris)?"},
        {"role": "USER", "text": "Ja — es handelt sich um eine Dienstreise, bei der mindestens ein Geschäftsort in Paris liegt."},
        {"role": "SYSTEM", "text": "Ja. Nach § 12 Absatz 2 LRKG gelten die §§ 1–11 entsprechend auch für Auslandsdienstreisen; abweichend werden Auslandstage- und Auslandsübernachtungsgelder nach § 12 Absatz 3 in Verbindung mit der Auslandsreisekostenverordnung des Bundes (ARV) und der ARVVwV gewährt."},
        {"role": "USER", "text": "Danke — noch eine Frage: Nach welchen Regeln werden die Auslandstage- und Übernachtungsgelder konkret berechnet, bzw. welche Sätze gelten für Frankreich/Paris?"},
        {"role": "SYSTEM", "text": "Das LRKG enthält keine relevanten Informationen zu Ihrer Frage."}
      ]
    },

    {
      "id": 13,
      "title": "Verwaltungsvorschriften / Besonderheiten",
      "turns": [
        {"role": "USER", "text": "Ich habe eine eintägige Inlandsdienstreise zu einer Fortbildung am 12.12.2025 (Fahrt mit Dienst-PKW, keine Übernachtung, nur Fahrtkosten und Verpflegungspauschale). Wer schreibt die Verwaltungsvorschriften — gibt es landes- oder dienststellenspezifische Besonderheiten, die ich beachten muss?"},
        {"role": "SYSTEM", "text": "Wollen Sie wissen, ob die oberste Dienstbehörde bzw. Ihre Dienststelle abweichende Regelungen treffen kann (dienststellenspezifische Besonderheiten)?"},
        {"role": "USER", "text": "Ja. Ich arbeite in Baden-Württemberg — bitte prüfen Sie, ob die oberste Dienstbehörde bzw. meine Dienststelle abweichende Verwaltungsvorschriften erlassen darf und welche landes- bzw. dienststellenspezifischen Besonderheiten in BW gelten."},
        {"role": "SYSTEM", "text": "Das LRKG enthält keine relevanten Informationen zu Ihrer Frage."},
        {"role": "USER", "text": "Ich bin Landesbeamtin bei einer Landesbehörde im Ministeriumsbereich. Bitte prüfen Sie konkret, ob das Land bzw. das zuständige Ministerium Verwaltungsvorschriften zum LRKG erlassen kann und ob meine Dienststelle abweichende, dienststellenspezifische Regelungen treffen darf."},
        {"role": "SYSTEM", "text": "Möchten Sie wissen, ob das Finanzministerium des Landes Verwaltungsvorschriften zum LRKG erlassen darf (ja/nein)?"},
        {"role": "USER", "text": "Ja. Bitte prüfen Sie, ob das Finanzministerium Verwaltungsvorschriften zum LRKG erlassen darf und ob meine Dienststelle abweichende, dienststellenspezifische Regelungen treffen darf."},
        {"role": "SYSTEM", "text": "Ja. Nach § 14 Absatz 2 LRKG erlässt das Finanzministerium die allgemeinen Verwaltungsvorschriften zu diesem Gesetz; in § 4 Absatz 1 ist zudem geregelt, dass das Finanzministerium durch Verwaltungsvorschrift Ausnahmen (z. B. zur Flugklassen-Erstattung) bestimmen kann. Abweichende oder bereichsbezogene Regelungen/ Ausnahmen kann die jeweilige oberste Dienstbehörde oder von ihr ermächtigte nachgeordnete Behörde für ihren Geschäftsbereich zulassen (vgl. § 4 Abs.1; § 9; § 5 Abs.2)."}
      ]
    },

    {
      "id": 14,
      "title": "Belege – Fristen und Folgen",
      "turns": [
        {"role": "USER", "text": "Ich plane eine Inlandsdienstreise 10.–16.09.2025 zu einer Fortbildung in Berlin (Bahn, Hotel, Tagegeld/Verpflegung). Bis wann kann die Dienststelle Belege verlangen und was passiert, wenn ich sie nicht vorlege; und wie lange muss ich Belege nach Erstattung aufbewahren?"},
        {"role": "SYSTEM", "text": "Haben Sie den Antrag auf Reisekostenvergütung bereits gestellt?"},
        {"role": "USER", "text": "Ja, ich habe den Antrag am 20.09.2025 elektronisch über das Abrechnungstool eingereicht."},
        {"role": "SYSTEM", "text": "Die zuständige Stelle kann bis zum Ablauf von sechs Monaten nach Antragstellung (bei Ihrem Antrag vom 20.09.2025 also bis zum 20.03.2026) die Vorlage der maßgeblichen Kostenbelege verlangen. Werden diese Belege auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden. Nach Erstattung sind die Belege bis zum Ablauf eines Jahres aufzubewahren und auf Verlangen vorzulegen."},
        {"role": "USER", "text": "Noch eine Frage: Bis wann muss die Reisekostenvergütung beantragt werden (Ausschlussfrist)?"},
        {"role": "SYSTEM", "text": "Endete Ihre Dienstreise am 16.09.2025?"},
        {"role": "USER", "text": "Ja — die Dienstreise endete am 16.09.2025. Kurz gefragt: Bis wann muss die Reisekostenvergütung spätestens beantragt werden (Ausschlussfrist)?"},
        {"role": "SYSTEM", "text": "Die Ausschlussfrist beträgt sechs Monate und beginnt mit dem Tag nach Beendigung der Dienstreise (bei Ende am 16.09.2025 also ab dem 17.09.2025). Sie ist schriftlich oder elektronisch zu beantragen; die Frist läuft demnach bis zum Ablauf des 17.03.2026."}
      ]
    },

    {
      "id": 15,
      "title": "Sonderregeln An-/Abreise, Anschlüsse, Nachtfahrten",
      "turns": [
        {"role": "USER", "text": "Ich plane eine 3-tägige Dienstreise nach Berlin (Inland) nächste Woche für eine Konferenz, Hinflug mit Anschluss und Rückfahrt per Nachtzug; es fallen Flug-, Taxi- und Übernachtungskosten an. Gibt es dafür Sonderregeln zu An-/Abreisezeiten oder Zwischentransfers (z. B. Fluganschlüsse, Nachtfahrten)?"},
        {"role": "SYSTEM", "text": "Beginnt oder endet Ihre Dienstreise an Ihrer Dienststelle (anstatt an Ihrer Wohnung)?"},
        {"role": "USER", "text": "Die Dienstreise beginnt und endet bei meiner Wohnung, nicht an der Dienststelle."},
        {"role": "SYSTEM", "text": "Reisedauer wird bei Ihnen nach Abreise und Ankunft an der Wohnung bemessen (§ 6 Abs. 2); daraus folgen Tagegeldsätze: voller Kalendertag 24 €, bei mehr als 8 Std. 6 € und bei mehr als 14 Std. 12 € (§ 6 Abs. 1). Übernachtungsgeld Inland pauschal 20 €; notwendige höhere Übernachtungskosten werden erstattet (§ 7 Abs. 1), jedoch wird Übernachtungsgeld nicht für die Dauer der Benutzung von Beförderungsmitteln gewährt (§ 7 Abs. 2 Nr. 1) — Schlafen im Nachtzug bringt also kein Übernachtungsgeld, die Fahrtzeit zählt aber für das Tagegeld. Flugkosten werden grundsätzlich nur in der niedrigsten Beförderungsklasse erstattet (§ 4 Abs. 1) und Taxi/Mietwagen werden nur bei triftigem Grund erstattet, sonst höchstens in Höhe der Kosten des öffentlichen Verkehrs (§ 4 Abs. 3)."},
        {"role": "USER", "text": "Danke. Noch eine Frage: Wie werden Zwischenlandungen/Anschlussflüge behandelt — gelten Wartezeiten/Umsteigezeiten als Reisezeit und beeinflussen sie Tagegeld oder Erstattung von zusätzlichen Transferkosten?"},
        {"role": "SYSTEM", "text": "Führt die Zwischenlandung/der Anschlussflug zu einer zusätzlichen notwendigen Übernachtung am dem Zwischenstopp?"},
        {"role": "USER", "text": "Nein — beim Hinflug entsteht dadurch keine zusätzliche notwendige Übernachtung, die Umsteigezeit beträgt etwa 3 Stunden am Zwischenhalt."},
        {"role": "SYSTEM", "text": "Warte- und Umsteigezeiten gelten als Teil der Reisedauer, weil diese nach Abreise und Ankunft an der Wohnung bemessen wird (§ 6 Abs. 2) und damit das Tagegeld nach § 6 Abs. 1 beeinflussen kann. Zusätzliche Transferkosten sind nur erstattungsfähige notwendige Auslagen; Taxi/Mietwagen werden nur bei triftigem Grund erstattet, sonst höchstens in Höhe der Kosten des öffentlichen Verkehrs (§ 4 Abs. 3); sonstige notwendige Nebenkosten nach § 10 Abs. 1. Da keine zusätzliche notwendige Übernachtung entsteht, entsteht kein zusätzliches Übernachtungsgeld (§ 7 Abs. 2 Nr. 4)."}
      ]
    }
  ]



dialogues_pha = [

    {
      "id": 1,
      "title": "Wann besteht Schutz als Haus-/Wohnungsbesitzer:in?",
      "turns": [
        {"role": "USER", "text": "Ich besitze eine selbstgenutzte Eigentumswohnung (kein Vermietungsmodell). Wann habe ich in den Versicherungsbedingungen Schutz als Haus-/Wohnungsbesitzer:in?"},
        {"role": "SYSTEM", "text": "Befindet sich Ihre selbstgenutzte Eigentumswohnung in Deutschland (im Inland)?"},
        {"role": "USER", "text": "Ja, die Wohnung befindet sich in Deutschland (im Inland)."},
        {"role": "SYSTEM", "text": "Nutzen Sie die Wohnung ausschließlich zu eigenen privaten Wohnzwecken (also nicht vermietet oder gewerblich genutzt)?"},
        {"role": "USER", "text": "Ja."},
        {"role": "SYSTEM", "text": "Ja. Da Ihre Eigentumswohnung im Inland liegt und ausschließlich zu eigenen privaten Wohnzwecken genutzt wird, haben Sie Versicherungsschutz als Haus-/Wohnungsbesitzer:in. Die Privat-Haftpflicht deckt Ihre gesetzliche Haftpflicht für solche selbstgenutzten Immobilien (inkl. zugehöriger Außenanlagen) für Schadenereignisse, die während der Wirksamkeit der Versicherung eintreten."},
        {"role": "USER", "text": "Danke, Tschüss."},
        {"role": "SYSTEM", "text": "Gern geschehen, Tschüss."}
      ]
    },
    {
      "id": 2,
      "title": "Gilt Schutz für Pedelecs (E-Tretunterstützung)?",
      "turns": [
        {"role": "USER", "text": "Ich prüfe gerade meine Privathaftpflicht-Bedingungen. Gilt darin der Versicherungsschutz auch für Pedelecs mit elektrischer Tretunterstützung (E-Tretunterstützung)?"},
        {"role": "SYSTEM", "text": "Hat Ihr Pedelec eine bauartbedingte Höchstgeschwindigkeit von maximal 25 km/h und benötigt dafür kein amtliches Kennzeichen/Versicherungskennzeichen und keinen Führerschein?"},
        {"role": "USER", "text": "Ja — mein Pedelec hat elektrische Tretunterstützung bis 25 km/h und braucht dafür kein Kennzeichen und keinen Führerschein."},
        {"role": "SYSTEM", "text": "Ja. Laut Ihren Versicherungsbedingungen sind Pedelecs mit Tretunterstützung bis 25 km/h, die kein amtliches Kennzeichen/Versicherungskennzeichen und keinen Führerschein benötigen, durch die Privat-Haftpflicht gedeckt."},
        {"role": "USER", "text": "Wie sieht es aus, wenn das Pedelec ein amtliches Kennzeichen/Versicherungskennzeichen braucht — wäre das dann ausgeschlossen?"},
        {"role": "SYSTEM", "text": "Ja. Wenn für das Pedelec ein amtliches Kennzeichen oder Versicherungskennzeichen erforderlich ist, fällt es nicht unter die Privat-Haftpflicht; dafür ist eine Kfz-Haftpflichtversicherung abzuschließen."}
      ]
    },
    {
      "id": 3,
      "title": "Deckt die Allianz Haftpflicht durch private Internetnutzung?",
      "turns": [
        {"role": "USER", "text": "In dem vorliegenden Allianz-Dokument möchte ich wissen: Deckt die Privathaftpflicht Schäden, die durch meine private Internetnutzung entstehen (z. B. Verbreitung von Schadsoftware, Verletzung von Persönlichkeitsrechten, Datenverlust bei Dritten)? Bitte nur aus dem Dokument beantworten."},
        {"role": "SYSTEM", "text": "Wurde die Schadsoftware bewusst oder unbefugt eingesetzt (z. B. Hacker-Angriff oder absichtliches Einbringen von Viren)?"},
        {"role": "USER", "text": "Unbeabsichtigt — ich habe keine Schadsoftware bewusst verbreitet; vermutlich wurde mein Gerät gehackt oder ich habe versehentlich einen infizierten Link/Anhang geöffnet."},
        {"role": "SYSTEM", "text": "Ja. Haftpflichtansprüche aus privatem elektronischem Datenaustausch sind grundsätzlich versichert (Ziff. 2.2.10) — unbeabsichtigtes Versenden bzw. durch Hack/versehentlich geöffneten Anhang verursachte Schäden werden im Beispiel genannt. Ausgeschlossen sind dagegen vorsätzliches/unbefugtes Eingreifen oder bewusstes Einbringen von Schadsoftware, Persönlichkeits- und Namensrechtsverletzungen sowie bestimmte Vermögensschäden und das unberechtigte Herunterladen urheberrechtlich geschützter Daten (Ziff. 2.2.10, 2.2.11, 2.3)."},
        {"role": "USER", "text": "Perfekt, damit ist meine Frage beantwortet. Danke, Tschüss."},
        {"role": "SYSTEM", "text": "Gern geschehen, Tschüss."}
      ]
    },
    {
      "id": 4,
      "title": "Deckt die Police Verlust fremder Schlüssel / Codekarten?",
      "turns": [
        {"role": "USER", "text": "Ich habe eine Privat-Haftpflichtversicherung. Deckt die Police den Verlust fremder Schlüssel oder Codekarten (z. B. Wohnungsschlüssel oder Zugangskarten)?"},
        {"role": "SYSTEM", "text": "War der verlorene Schlüssel rechtmäßig in Ihrem Gewahrsam und handelte es sich nicht um einen Autoschlüssel oder um einen Schlüssel aus Ihrer selbstständigen gewerblichen Tätigkeit?"},
        {"role": "USER", "text": "Ja — der fremde Schlüssel war rechtmäßig in meinem Gewahrsam; es handelt sich nicht um einen Autoschlüssel und auch nicht um einen Schlüssel aus meiner selbstständigen gewerblichen Tätigkeit."},
        {"role": "SYSTEM", "text": "Ja. Ihre Police deckt den Verlust fremder Schlüssel/Codekarten, wenn diese rechtmäßig in Ihrem Gewahrsam waren und es sich nicht um Autoschlüssel oder um im Rahmen Ihrer selbstständigen gewerblichen Tätigkeit verwahrte Schlüssel handelt. Ersetzt werden u. a. Kosten für Auswechslung/Änderung von Schlössern und Schließanlagen, Ersatzschlüssel, vorübergehende Sicherungsmaßnahmen (bis 14 Tage) und Folgeschäden; Entschädigung je Versicherungsfall bis 50.000 €."},
        {"role": "USER", "text": "Danke, Tschüss."},
        {"role": "SYSTEM", "text": "Gern geschehen, Tschüss."}
      ]
    },
    {
      "id": 5,
      "title": "Wer sind 'Dritte'?",
      "turns": [
        {"role": "USER", "text": "Gelten mitversicherte Personen (z. B. Ehepartner:innen, Kinder oder mitversicherte Haushaltspersonen) in diesem Dokument als „Dritte“?"},
        {"role": "SYSTEM", "text": "Bezieht sich Ihre Frage darauf, ob Ansprüche von mitversicherten Personen gegen Sie als \"Dritte\" gelten?"},
        {"role": "USER", "text": "Ja, genau — ich möchte wissen, ob im Dokument Ansprüche von mitversicherten Personen gegen mich als Ansprüche von „Dritten“ gelten."},
        {"role": "SYSTEM", "text": "Meinen Sie direkte Schadenersatzansprüche einer mitversicherten Person gegen Sie (nicht Regressansprüche von Sozialversicherungsträgern)?"},
        {"role": "USER", "text": "Ja — genau das meine ich: direkte Schadenersatzansprüche von mitversicherten Personen gegen mich (keine Regressansprüche von Sozialversicherungsträgern)."},
        {"role": "SYSTEM", "text": "Nein. Das Dokument definiert \"Dritte\" als alle Personen außer den Versicherten und der Versicherung; mitversicherte Personen zählen somit nicht zu den Dritten. Direkte Schadenersatzansprüche von mitversicherten Personen gegen Sie sind daher nicht versichert (Ziffer 1.4)."},
        {"role": "USER", "text": "Sind Ansprüche zwischen mitversicherten Personen (z. B. Ehepartner:innen) untereinander in diesem Dokument gedeckt?"},
        {"role": "SYSTEM", "text": "Nein — Ansprüche von mitversicherten Personen untereinander sind nicht versichert (Ziffer 1.4). Ausnahme: Versichert sind Regressansprüche von Sozialversicherungsträgern, Sozialhilfsträgern, privaten Krankenversicherungsträgern sowie öffentlichen und privaten Arbeitgebern wegen Personenschäden, vorausgesetzt Schädiger und Geschädigter leben nicht als Familienangehörige in häuslicher Gemeinschaft."}
      ]
    },
    {
      "id": 6,
      "title": "Sind Kinder während Studium/Ausbildung versichert, auch bei Arbeit?",
      "turns": [
        {"role": "USER", "text": "Ich bin Elternteil; mein Kind macht gerade Studium/Ausbildung und arbeitet nebenbei. Sind Kinder während Studium/Ausbildung versichert, auch bei Arbeit?"},
        {"role": "SYSTEM", "text": "Handelt es sich bei der Tätigkeit Ihres Kindes bereits um eine auf Dauer angelegte berufliche Tätigkeit (also nicht nur ein Nebenjob)?"},
        {"role": "USER", "text": "Es ist kein dauerhaftes Berufsstudium: Mein Kind hat nur einen nebenbei ausgeübten Teilzeit-/Minijob (z. B. Minijob/Studentenjob) während Studium/Ausbildung."},
        {"role": "SYSTEM", "text": "Ja. Kinder bleiben laut Vertrag während Studium/Ausbildung mitversichert — auch wenn sie einen Nebenjob/Minijob ausüben. Die Mitversicherung endet erst, wenn sie erstmals eine auf Dauer angelegte berufliche Tätigkeit aufnehmen und dabei eigenes Einkommen erzielen."},
        {"role": "USER", "text": "Sind Kinder mitversichert, auch wenn sie während Studium/Ausbildung nicht in meinem Haushalt wohnen?"},
        {"role": "SYSTEM", "text": "Ja. Kinder sind in den Varianten „Single mit Kind(ern)“ und „Familie“ mitversichert, „egal wo diese wohnen“. Die Mitversicherung endet erst, wenn sie nach Abschluss von Studium/Ausbildung erstmals eine auf Dauer angelegte berufliche Tätigkeit aufnehmen und dabei eigenes Einkommen erzielen; in Pflegeeinrichtungen untergebrachte Kinder sind immer mitversichert."}
      ]
    },
    {
      "id": 7,
      "title": "Sind Vermietung einzelner Zimmer oder Einliegerwohnungen gedeckt?",
      "turns": [
        {"role": "USER", "text": "Ich vermiete gelegentlich ein einzelnes Zimmer in meiner Wohnung bzw. eine kleine Einliegerwohnung an Untermieter. Sind solche Vermietungen in den Bedingungen gedeckt?"},
        {"role": "SYSTEM", "text": "Vermieten Sie das Zimmer bzw. die Einliegerwohnung in Ihrer selbstbewohnten Wohnung oder in Ihrem selbstbewohnten Einfamilien-/Zweifamilienhaus an Privatpersonen?"},
        {"role": "USER", "text": "Ja — das Zimmer/Die Einliegerwohnung ist Teil meiner selbstgenutzten Wohnung, und ich vermiete gelegentlich an Privatpersonen (Untermieter)."},
        {"role": "SYSTEM", "text": "Ja. Wenn Sie in Ihrer selbstbewohnten Wohnung ein Zimmer oder eine Einliegerwohnung an Privatpersonen vermieten, sind daraus resultierende Haftpflichtansprüche durch die Police gedeckt (z. B. bei Verletzung durch einen unsachgemäß befestigten Deckenleuchter). Mitversichert ist auch die Vermietung zugehöriger Garagen."},
        {"role": "USER", "text": "Gilt der Schutz auch als Haus-/Grundbesitzer:in — also wenn ich Eigentümer:in der Wohnung oder des Grundstücks bin?"},
        {"role": "SYSTEM", "text": "Handelt es sich bei der Wohnung/dem Grundstück um eine ausschließlich zu eigenen privaten Wohnzwecken genutzte Immobilie im Inland? (Ja/Nein)"},
        {"role": "USER", "text": "Ja — die Wohnung wird ausschließlich zu eigenen privaten Wohnzwecken im Inland genutzt. Gilt der Versicherungsschutz auch, wenn ich Eigentümer der Wohnung bzw. des Grundstücks bin?"},
        {"role": "SYSTEM", "text": "Ja. Wenn die Wohnung inländisch ausschließlich zu eigenen privaten Wohnzwecken genutzt wird und Sie Eigentümer:in sind, deckt die Police Haftpflichtansprüche aus der gelegentlichen Vermietung von Zimmern/Einliegerwohnungen an Privatpersonen; mitversichert ist auch die Vermietung dazugehöriger Garagen."}
      ]
    },
    {
      "id": 8,
      "title": "Besteht Schutz als Bauherr:in bei Umbau/Renovierung?",
      "turns": [
        {"role": "USER", "text": "Ich renoviere/umbau gerade mein Zuhause und beauftrage Handwerker; ich möchte wissen, ob in diesem Dokument Schutz als Bauherr:in bei Umbau oder Renovierung besteht. Was steht konkret dazu?"},
        {"role": "SYSTEM", "text": "Handelt es sich bei der Immobilie um eine von Ihnen ausschließlich zu eigenen privaten Wohnzwecken genutzte, versicherte Immobilie, bei der durch die Umbau-/Renovierungsarbeiten der Charakter der Immobilie erhalten bleibt (also keine Nutzungsänderung zu gewerblichen Zwecken)?"},
        {"role": "USER", "text": "Ja — es ist mein ausschließlich privat genutztes Wohnhaus, und durch den Umbau/ die Renovierung bleibt die Nutzung als Wohnraum erhalten (keine gewerbliche Nutzungsänderung)."},
        {"role": "SYSTEM", "text": "Ja. Nach Ziffer 2.2.1 ist Ihre gesetzliche Haftpflicht als Bauherr:in bei Umbauten und Renovierungen (einschließlich Erweiterungs-, An- und Zusatzbauten, Renovierungs-/Sanierungs- und Abbrucharbeiten) versichert, sofern der Charakter der Immobilie erhalten bleibt und sich die Nutzungsart nicht ändert (z. B. kein Umbau zu einer gewerblich genutzten Immobilie; der Bau eines Mehrfamilienhauses ist nicht versichert)."},
        {"role": "USER", "text": "Danke, das beantwortet meine Hauptfrage. Noch eine kurze Frage: Wann genau besteht der Versicherungsschutz bei den Umbau-/Renovierungsarbeiten — z. B. ab Beginn der Arbeiten, nur bei Beauftragung von Handwerkern oder erst nach Meldung an die Versicherung?"},
        {"role": "SYSTEM", "text": "Versicherungsschutz besteht, wenn das Schadenereignis während der Wirksamkeit der Versicherung eingetreten ist (Ziffer 2.1) und Ziffer 2.2.1 nennt ausdrücklich Deckung als Bauherr:in bei Umbauten/Renovierungen, sofern der Charakter der Immobilie erhalten bleibt. Das Dokument enthält jedoch keine ausdrückliche Regelung, ob der Schutz bereits mit Beginn der Arbeiten, erst bei Beauftragung von Handwerkern oder erst nach Meldung an die Versicherung beginnt."}
      ]
    },
    {
      "id": 9,
      "title": "Sind Praktika/Schnupperlehren mitversichert?",
      "turns": [
        {"role": "USER", "text": "Ich schaue in meine Privat-Haftpflichtbedingungen, mein Sohn/meine Tochter macht demnächst eine einwöchige Schnupperlehre bei einer Firma. Sind Praktika/Schnupperlehren in der Police mitversichert?"},
        {"role": "SYSTEM", "text": "Hat das Unternehmen, bei dem die einwöchige Schnupperlehre stattfindet, eine eigene Betriebshaftpflichtversicherung, die für Schäden aus der Tätigkeit eintreten würde (Ja/Nein)?"},
        {"role": "USER", "text": "Nein, die Firma hat keine eigene Betriebshaftpflichtversicherung."},
        {"role": "SYSTEM", "text": "Hat die Firma Ihrem Sohn/Ihrer Tochter vertraglich oder schriftlich einen Rückgriffs-/Anspruchsverzicht oder eine Freistellung erteilt (Ja/Nein)?"},
        {"role": "USER", "text": "Nein."},
        {"role": "SYSTEM", "text": "Ja. Laut Ziffer 2.2.5 sind Haftpflichtansprüche im Zusammenhang mit praktischen Tätigkeiten (Praktikum/Schnupperlehre) mitversichert; auch Ansprüche des Betriebs (z. B. wegen Beschädigung von Lehrgeräten) sind eingeschlossen. Voraussetzung ist, dass kein anderer Versicherungsschutz besteht (Subsidiarität) und es darf kein Rückgriffs-/Anspruchsverzicht oder eine Freistellung zugunsten der versicherten Person vorliegen; Schäden an den von Ihnen bearbeiteten Sachen sind dagegen nicht versichert."},
        {"role": "USER", "text": "Danke für die Info. Gibt es Einschränkungen bei der Mitversicherung von Praktika/Schnupperlehren?"},
        {"role": "SYSTEM", "text": "Ja. Der Versicherungsschutz gilt nur subsidiär (also nur, soweit kein anderer Versicherungsschutz besteht) und entfällt, wenn ein Rückgriffs-/Anspruchsverzicht oder eine Freistellung zugunsten der versicherten Person vorliegt. Außerdem sind Ansprüche wegen Schäden an den von der Praktikantin/dem Praktikanten bearbeiteten Sachen nicht versichert."}
      ]
    },
    {
      "id": 10,
      "title": "Ist ehrenamtliche Tätigkeit versichert und subsidiär?",
      "turns": [
        {"role": "USER", "text": "Ich engagiere mich ehrenamtlich im Sportverein (z. B. beim Training und auf Veranstaltungen). Steht in diesem Versicherungsdokument, dass ehrenamtliche Tätigkeiten gedeckt sind und ob der Versicherungsschutz nur subsidiär gilt?"},
        {"role": "SYSTEM", "text": "Handeln Sie in Ihrem Ehrenamt in einer verantwortlichen Position (z. B. Vorstand) oder üben Sie ein öffentlich-hoheitliches Ehrenamt aus?"},
        {"role": "USER", "text": "Nein, ich bin kein Vorstand und übe kein öffentlich-hoheitliches Ehrenamt aus; ich bin als Trainer/Betreuer aktiv und helfe bei Vereinsveranstaltungen."},
        {"role": "SYSTEM", "text": "Ja. In Ziffer 2.2.7 steht, dass ehrenamtliche Tätigkeiten in nichtverantwortlicher Position (z. B. Trainer) versichert sind. Der Schutz gilt jedoch subsidiär — wir leisten nur, soweit kein anderer Versicherungsschutz eintritt; öffentliche/hoheitliche Ehrenämter sowie Fälle mit Rückgriffs-/Anspruchsverzicht oder Freistellung sind ausgeschlossen."},
        {"role": "USER", "text": "Danke — noch kurz: Welche Einschränkungen gelten für ehrenamtliche Tätigkeiten in den Bedingungen (z. B. zu verantwortlichen Positionen, Rückgriff/Anspruchsverzicht oder bestimmten Einsätzen)?"},
        {"role": "SYSTEM", "text": "Der Schutz gilt für ehrenamtliche Tätigkeiten in nichtverantwortlicher Funktion und ist subsidiär — wir leisten nur, soweit kein anderer Versicherungsschutz eintritt. Ausgeschlossen sind verantwortliche Betätigungen in Vereinigungen (z. B. Vorstand), öffentliche/hoheitliche Ehrenämter sowie Fälle, in denen ein Rückgriffs- oder Anspruchsverzicht bzw. eine Freistellung zugunsten der versicherten Person besteht; außerdem besteht kein Schutz, wenn die Haftpflichtversicherung des Vereins oder Trägers eintrittspflichtig ist."}
      ]
    },
    {
      "id": 11,
      "title": "Welche Einschränkungen gelten für ehrenamtliche Tätigkeiten?",
      "turns": [
        {"role": "USER", "text": "Im vorliegenden Dokument: Welche Einschränkungen gelten für ehrenamtliche Tätigkeiten?"},
        {"role": "SYSTEM", "text": "Handelt es sich bei Ihrer ehrenamtlichen Tätigkeit um ein öffentliches oder hoheitliches Ehrenamt? (Ja/Nein)"},
        {"role": "USER", "text": "Nein — es handelt sich um ein privates Ehrenamt in einem Verein (z. B. Trainer im Sportverein), kein öffentliches/hoheitliches Amt."},
        {"role": "SYSTEM", "text": "Versicherungsschutz besteht für private Ehrenämter in nicht-verantwortlicher Position bzw. für Freiwilligenarbeit aus sozialem, unentgeltlichem Engagement. Ausgeschlossen sind öffentliche/hoheitliche Ehrenämter; der Schutz ist subsidiär (nur, wenn nicht eine andere Haftpflicht eintritt), kein Versicherungsschutz, wenn die Haftpflicht des Vereins/Trägers eintrittspflichtig ist oder ein Rückgriffs-/Anspruchsverzicht bzw. eine Freistellung vorliegt. Ansprüche aus einer verantwortlichen Betätigung in Vereinigungen (z. B. Vorstandsamt) sind ebenfalls ausgeschlossen."},
        {"role": "USER", "text": "Danke, das hilft weiter. Eine letzte Frage: Wer genau ist in dem Dokument mit \"Versicherungsnehmer:in\" gemeint — die versicherte Privatperson selbst, ein Verein oder der Vertragspartner (z. B. die Firma/Institution)?"},
        {"role": "SYSTEM", "text": "„Versicherungsnehmer:in“ ist laut Dokument „Sie“ — also der Vertragspartner bzw. die Vertragspartnerin und Käufer bzw. Käuferin des Versicherungsschutzes (der/die Policeninhaber:in). Das meint damit die versicherte Person als Vertragspartner; ein Verein oder eine Firma wäre nur dann Versicherungsnehmer, wenn dieser ausdrücklich im Versicherungsschein als Vertragspartner genannt ist."}
      ]
    },
    {
      "id": 12,
      "title": "Gilt Schutz für selbstgenutzte Ferienimmobilie im EU-Ausland?",
      "turns": [
        {"role": "USER", "text": "Ich habe eine selbstgenutzte Ferienwohnung in Spanien, die ich gelegentlich selbst nutze. Gilt mein Versicherungsschutz (z. B. Privathaftpflicht/Deckung für Haus-/Wohnungsbesitzer) auch für eine selbstgenutzte Ferienimmobilie im EU-Ausland?"},
        {"role": "SYSTEM", "text": "Ist die Ferienimmobilie ausschließlich zu Ihren eigenen privaten Wohnzwecken genutzt (also nicht vermietet)?"},
        {"role": "USER", "text": "Ja — die Ferienimmobilie wird ausschließlich privat von mir genutzt und niemals vermietet."},
        {"role": "SYSTEM", "text": "Ja — als Eigentümer einer ausschließlich privat genutzten Ferienimmobilie in einem EU-Staat (Spanien) besteht Versicherungsschutz gemäß Ziffer 2.2.1. Mitversichert sind auch die zugehörigen Außenanlagen; maßgeblich bleiben die genauen Regelungen und ggf. Ausschlüsse in Ihren Versicherungsbedingungen und Ihrem Versicherungsschein."},
        {"role": "USER", "text": "Deckt die Police mich auch als Haus- bzw. Grundeigentümer der Ferienimmobilie in Spanien?"},
        {"role": "SYSTEM", "text": "Ja. Gemäß Ziffer 2.2.1 ist Ihre gesetzliche Haftpflicht als Eigentümer:in einer ausschließlich zu eigenen privaten Wohnzwecken genutzten Ferienimmobilie in einem EU-Staat (z. B. Spanien) mitversichert; mitversichert sind auch die zugehörigen Außenanlagen. Maßgeblich bleiben die genauen Regelungen und ggf. Ausschlüsse in Ihren Versicherungsbedingungen und Ihrem Versicherungsschein."}
      ]
    },
    {
      "id": 13,
      "title": "Sind Schäden an den Anlagen selbst versichert?",
      "turns": [
        {"role": "USER", "text": "Ich habe ein Versicherungsdokument und will kurz klären: Sind Schäden an den Anlagen selbst versichert? Ich kann bei Nachfrage konkrete Textstellen oder Tarifnamen aus dem Dokument nennen."},
        {"role": "SYSTEM", "text": "Meinen Sie Anlagen zur Energieversorgung (z. B. Photovoltaik, Geothermie, Wallbox)?"},
        {"role": "USER", "text": "Ja, genau — Photovoltaik, Geothermie und Wallboxen. Sind Schäden an diesen Anlagen selbst versichert?"},
        {"role": "SYSTEM", "text": "Befinden sich die Photovoltaik-/Geothermie-Anlagen bzw. die Wallboxen in Ihrem Eigentum und dienen ausschließlich privaten Wohnzwecken? (Ja/Nein)"},
        {"role": "USER", "text": "Ja."},
        {"role": "SYSTEM", "text": "Nein. Nach Ziffer 2.2.1 sind Ansprüche wegen Schäden an den Anlagen selbst ausdrücklich nicht versichert. Ebenfalls ausgeschlossen sind Schäden, die beim Errichten der Anlagen entstehen, sowie Ansprüche des Netzbetreibers aus Vertragsangelegenheiten."},
        {"role": "USER", "text": "Gibt es eine finanzielle Obergrenze für Schäden an Photovoltaik-, Geothermie-Anlagen oder Wallboxen — und wenn ja, wie hoch ist sie?"},
        {"role": "SYSTEM", "text": "Meinen Sie eine Begrenzung für Entschädigungen wegen Schäden an den Anlagen selbst? (Ja/Nein)"},
        {"role": "USER", "text": "Ja. Gibt es eine finanzielle Obergrenze für Schäden an Photovoltaik-, Geothermie-Anlagen oder Wallboxen — und wenn ja, wie hoch ist sie?"},
        {"role": "SYSTEM", "text": "Nein — Schäden an den Anlagen selbst sind ausdrücklich vom Versicherungsschutz ausgeschlossen (Ziffer 2.2.1), daher nennt das Dokument keine Entschädigungsobergrenze dafür."}
      ]
    },
    {
      "id": 14,
      "title": "Sind Hundehaltung oder Pferdehalterhaftpflicht gedeckt?",
      "turns": [
        {"role": "USER", "text": "Ich habe ein Versicherungsdokument vor mir und möchte kurz Punkt 14 prüfen: Deckt die Police die Haltung von Hunden oder die Pferdehalterhaftpflicht? Ich habe privat einen Hund und reite gelegentlich, bitte im Dokument nachsehen."},
        {"role": "SYSTEM", "text": "Ist Ihr Hund ein ausgebildeter Assistenzhund (z. B. Blindenhund)?"},
        {"role": "USER", "text": "Nein, mein Hund ist kein Assistenzhund, sondern ein privater Familienhund."},
        {"role": "SYSTEM", "text": "Besitzen Sie ein eigenes Pferd?"},
        {"role": "USER", "text": "Nein, ich habe kein eigenes Pferd — ich reite nur gelegentlich fremde Pferde."},
        {"role": "SYSTEM", "text": "Die Police deckt die Haftpflicht als Halter von Hunden nicht ab, außer für ausgebildete Assistenzhunde — Ihr privater Familienhund ist demnach nicht versichert. Gelegentliches Reiten oder Hüten fremder Pferde ist dagegen versichert (nicht gewerbsmäßig; subsidiär, also nur wenn keine andere Versicherung eintritt)."},
        {"role": "USER", "text": "Sind Ansprüche des Tierhalters wegen Verletzung oder Abhandenkommens des Tieres beim Hüten mitversichert?"},
        {"role": "SYSTEM", "text": "Ja. Bei gelegentlichem, nicht gewerbsmäßigem Hüten fremder Hunde oder Pferde sind Ansprüche des Halters wegen Verletzung, Abhandenkommens und Tod des Tieres mitversichert; beim Hütenden selbst besteht hingegen nur für den Personenschaden Deckung, wenn der Halter verletzt wird. Der Schutz gilt subsidiär (nur wenn keine andere Versicherung eintritt)."}
      ]
    },
    {
      "id": 15,
      "title": "Was macht die Allianz nach Meldung eines Versicherungsfalls?",
      "turns": [
        {"role": "USER", "text": "Ich brauche Info zu meiner privaten Haftpflicht: Was macht die Allianz, nachdem ich einen Versicherungsfall gemeldet habe? Zur Klarstellung: es geht nicht um Reisen, sondern um meine Privat-Haftpflichtpolice."},
        {"role": "SYSTEM", "text": "Wurde gegen Sie bereits ein Haftpflichtanspruch gerichtlich geltend gemacht?"},
        {"role": "USER", "text": "Nein, noch nicht; ich habe nur den Schaden gemeldet und es liegt kein gerichtliches Verfahren vor."},
        {"role": "SYSTEM", "text": "Möchten Sie, dass die Allianz den Rechtsstreit für Sie führt, falls Ansprüche gegen Sie erhoben werden?"},
        {"role": "USER", "text": "Ja, bitte — ich möchte, dass die Allianz bei erhobenen Ansprüchen den Rechtsstreit für mich übernimmt."},
        {"role": "SYSTEM", "text": "Nach Ihrer Schadenmeldung prüft die Allianz, ob die gegen Sie geltend gemachten Ansprüche berechtigt sind; berechtigte Ansprüche werden erstattet, unberechtigte abgewehrt. Kommt es zum Rechtsstreit, ist die Allianz zur Prozessführung bevollmächtigt, führt den Rechtsstreit in Ihrem Namen und auf ihre Kosten (diese Kosten werden nicht auf die Versicherungssumme angerechnet). Sie müssen den Schaden unverzüglich melden, Untersuchungen ermöglichen, wahrheitsgemäß Auskunft geben und im Gerichtsfall der Allianz die Verfahrensführung überlassen sowie Vollmacht und erforderliche Unterlagen erteilen."},
        {"role": "USER", "text": "Das beantwortet meine Frage, danke. Was genau muss ich nach einem Schaden der Allianz melden und welche Mitwirkungspflichten habe ich?"},
        {"role": "SYSTEM", "text": "Ja. Melden Sie jeden Versicherungsfall unverzüglich; informieren Sie die Allianz außerdem sofort, wenn ein Haftpflichtanspruch gegen Sie erhoben, ein staatsanwaltschaftliches/behördliches oder gerichtliches Verfahren eingeleitet, ein Mahnbescheid erlassen wird oder Ihnen gerichtlich der Streit verkündet wird. Ermöglichen Sie Untersuchungen zu Ursache und Höhe des Schadens, erteilen Sie jederzeit ausführliche und wahrheitsgemäße Auskünfte, senden Sie alle angeforderten Unterlagen, sorgen Sie nach Möglichkeit für Abwendung und Minderung des Schadens und befolgen zumutbare Weisungen der Allianz; gegen Mahnbescheide oder verwaltungsrechtliche Verfügungen müssen Sie fristgerecht Rechtsbehelfe einlegen. Wird der Haftpflichtanspruch gerichtlich geltend gemacht, überlassen Sie der Allianz die Verfahrensführung, erteilen dem beauftragten Rechtsanwalt Vollmacht und die erforderlichen Auskünfte; Aufwendungen zur Schadenminderung erstattet die Allianz, wenn sie geboten waren oder gemäß ihren Weisungen erfolgten."}
      ]
    }
]




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

extensions = [
"""%%
  BAS_DEF["A.1 Begriff & Genehmigung"]

  %% Main question
  BAS_DEF --> Q_APPROVAL["Frage: Muss eine Dienstreise schriftlich oder elektronisch angeordnet bzw. genehmigt werden?"]
  Q_APPROVAL --> A_APPROVAL["Antwort: Ja. Dienstreisen sind grundsätzlich schriftlich oder elektronisch anzuordnen bzw. zu genehmigen (§2 Abs.1). (vgl. §2 Abs.1)"]

  %% Factual follow-up about form/zuständigkeit
  A_APPROVAL --> Q_FORMAL["Frage: Welche formalen Regeln gelten für die Anordnung (Zuständigkeit, Form)?"]
  Q_FORMAL --> A_FORMAL["Antwort: Zuständig ist der zuständige Dienstvorgesetzte; die Anordnung/Genehmigung muss schriftlich oder elektronisch erfolgen; nur gesetzlich geregelte Ausnahmen sind zulässig (§2 Abs.1). (vgl. §2 Abs.1)"]

  %% Diagnostic follow-up: Ausnahmen für bestimmte Personen (Ja/Nein)
  A_FORMAL --> Q_APPROXCEPT["Trifft für Sie eine der besonderen Ausnahmen zu (Richter/in, Landesbeauftragte für Datenschutz oder für Belange von Menschen mit Behinderungen)?"]
  Q_APPROXCEPT -->|"Ja"| A_APPROXCEPT["Antwort (Ja): Für Richterinnen/Richter sowie den Landesbeauftragten für Datenschutz und die Landesbeauftragte für Belange von Menschen mit Behinderungen besteht keine Anordnungspflicht (§2 Abs.3). (vgl. §2 Abs.3)"]
  Q_APPROXCEPT -->|"Nein"| A_SUMMARY_NO["Kurz-Zusammenfassung (Nein): Dann gilt die Regel: Dienstreisen müssen schriftlich oder elektronisch angeordnet bzw. genehmigt werden (§2 Abs.1). (vgl. §2 Abs.1)"]
""",

""" Reworked branch: A.2 Dienstreise vs. Dienstgang (chatbot-like diagnostic flow)

  BAS_DIFF["A.2 Dienstreise vs. Dienstgang"]

  %% Main diagnostic check (reformulated)
  BAS_DIFF --> Q_WHENDG["Frage (Diagnose): Findet der Einsatz außerhalb Ihrer regelmäßigen Dienststätte am Dienst- oder Wohnort statt? (Ja/Nein)"]

  %% YES → it's a Dienstgang (definition)
  Q_WHENDG -->|"Ja"| A_WHENDG["Antwort: Dann liegt ein Dienstgang vor – das sind dienstliche Erledigungen außerhalb der Dienststätte am Dienst‑ oder Wohnort; Abgrenzung nach Ort und Zweck. (§2 Abs.2)"]

  %% After establishing Dienstgang → follow-up: Tagegeld-Relevanz (diagnose)
  A_WHENDG --> Q_TAGE_DG["Folgefrage (Diagnose): Dauert der Dienstgang länger als 8 Stunden? (Ja/Nein)"]

  Q_TAGE_DG -->|"Ja"| A_TAGE_DG_YES["Antwort (Ja): Bei Dienstgängen von mehr als 8 Stunden können nachgewiesene Verpflegungsaufwendungen bis zur Höhe des Tagegeldes ersetzt werden. (§6 Abs.3)"]
  Q_TAGE_DG -->|"Nein"| A_TAGE_DG_NO["Antwort (Nein): Bei Dienstgängen besteht grundsätzlich kein Anspruch auf Tagegeld; bei ≤ 8 Stunden kein Tagegeldanspruch. (§6 Abs.3)"]

  %% NO → in der Regel Dienstreise (pointer to the general rule)
  Q_WHENDG -->|"Nein"| A_WHENDG_NO["Antwort: Trifft das Merkmal 'außerhalb der Dienststätte am Dienst‑ oder Wohnort' nicht zu, handelt es sich in der Regel um eine Dienstreise (Reise zur Erledigung dienstlicher Aufgaben außerhalb des Dienstortes; Anordnung/Genehmigung erforderlich). (§2 Abs.1)"]
""",

"""
%%
  BAS_POINT["A.3 Ausgangs- / Endpunkt; Wohnsitze (Neustrukturierung)"]

  %% Main question
  BAS_POINT --> Q_CHOOSE_POINT["Frage: Wer bestimmt grundsätzlich, ob Start/Ende der Reise meine Wohnung oder die Dienststätte ist?"]
  Q_CHOOSE_POINT --> A_CHOOSE_POINT["Direkte Antwort: Grundsätzlich bestimmt die/der Dienstreisende den Ausgangs‑/Endpunkt (z. B. die Wohnung), unter Beachtung des Wirtschaftlichkeitsgrundsatzes (§3 Abs.2)."]

  %% Follow-up diagnostic check (Ja/Nein)
  A_CHOOSE_POINT --> Q_FORCE_STATION["Prüfung: Führt Ihre Fahrtstrecke unmittelbar an Ihrer Dienststätte vorbei?"]
  Q_FORCE_STATION -->|"Ja"| A_FORCE_STATION["Bei JA: Die/der zuständige Dienstvorgesetzte kann die Dienststätte als Ausgangs- oder Endpunkt anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt (§3 Abs.2)."]
  Q_FORCE_STATION -->|"Nein"| A_CHOOSE_POINT 
  %% reuse of the direct answer for the NO-path

  %% Additional general informational follow-ups (nicht diagnostisch)
  A_CHOOSE_POINT --> Q_TRAVEL_FROM_HOME["Frage: Wie wird die Fahrtkostenerstattung berechnet, wenn die Reise an der Wohnung beginnt oder endet?"]
  Q_TRAVEL_FROM_HOME --> A_TRAVEL_FROM_HOME["Antwort: Fahrtkostenerstattung oder Wegstreckenentschädigung bemisst sich nach der Entfernung von/bis Wohnung, sofern nicht die Dienststätte als Ausgangs-/Endpunkt angeordnet wurde (§3 Abs.2)."]

  A_CHOOSE_POINT --> Q_MULTIPLE_HOME["Frage: Welche Wohnung gilt bei mehreren Wohnsitzen?"]
  Q_MULTIPLE_HOME --> A_MULTIPLE_HOME["Antwort: Maßgeblich ist die der Dienststätte am nächsten gelegene Wohnung oder Unterkunft (§3 Abs.2)."]
""",

""",

  TRA_CHOICE["B.1 Wahl des Verkehrsmittels und Klimaschutz"]

  TRA_CHOICE --> Q_FREE_CHOICE["Frage: Bin ich frei in der Wahl des Verkehrsmittels?"]
  Q_FREE_CHOICE --> A_FREE_CHOICE["Antwort: Grundsätzlich ja; Dienstreisende sind in der Wahl frei, müssen aber Wirtschaftlichkeitsgesichtspunkte und Klimaschutzanforderungen beachten (§3 Abs.3)."]

  %% Follow-up (diagnostische) Prüfung: kostenlose Beförderung vorhanden?
  Q_FREE_CHOICE --> Q_FREE_TRANSPORT_NOT_REFUND["Frage (Diagnose): Besteht eine unentgeltliche Beförderungsmöglichkeit (z. B. Dienstwagen)?"]
  Q_FREE_TRANSPORT_NOT_REFUND -->|"Ja"| A_FREE_TRANSPORT_NOT_REFUND["Antwort (Ja): Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann (§3 Abs.3)."]
  Q_FREE_TRANSPORT_NOT_REFUND -->|"Nein"| A_ROLE_ECONOMY["Antwort (Nein): Bei fehlender unentgeltlicher Beförderungsmöglichkeit sind Dienstinteresse und Wirtschaftlichkeit maßgeblich; die Wahl hat wirtschaftlich zu sein (§2 Abs.1; §3 Abs.2–3)."]

  %% Allgemeine Ergänzung (kein Ja/Nein-Check)
  Q_FREE_CHOICE --> Q_CONSIDER_CLIMATE["Frage: Muss ich Klimaschutz bei der Verkehrsmittelwahl beachten (z. B. ÖPNV vor Auto)?"]
  Q_CONSIDER_CLIMATE --> A_CONSIDER_CLIMATE["Antwort: Ja, neben Wirtschaftlichkeit sind die Erfordernisse des Klimaschutzes bei der Wahl zu beachten (§3 Abs.3)."]
""",

"""
%%
  TRA["B. Beförderung, Fahrt- und Flugkosten, Klimaauflagen"]

  %% Hauptfrage (wie im Dialog)
  TRA_COSTS --> Q_FLIGHT_ALLOWED["B.2 Sind Flugkosten erstattungsfähig und welche Flugklasse wird grundsätzlich übernommen?"]

  %% Direkte gesetzliche Aussage (faktische Grundlage)
  Q_FLIGHT_ALLOWED --> A_FLIGHT_ALLOWED["Antwort (Fakt): Flugkosten sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes überwiegen (§4 Abs.1)."]

  %% FOLLOW-UP CHECK 1: klimabezogener Abwägungsschritt (diagnostisch)
  Q_FLIGHT_ALLOWED --> Q_CLIMATE["Überwiegen bei Ihrer Flugreise dienstliche oder wirtschaftliche Gründe gegenüber den Belangen des Klimaschutzes?"]

  Q_CLIMATE -->|"Ja"| Q_HIGHER_CLASS_DISABILITY["Besteht bei Ihnen ein Grad der Behinderung ≥50? (Ja / Nein)"]
  Q_CLIMATE -->|"Nein"| A_NO_REIMB["Kurzfassung (Nein): Wenn Klimaschutzbelange überwiegen, sind Flugkosten nicht erstattungsfähig (§4 Abs.1)."]

  %% FOLLOW-UP CHECK 2a: Behinderung ≥50
  Q_HIGHER_CLASS_DISABILITY -->|"Ja"| A_HIGHER_CLASS_DISABILITY["Ja: Bei einem Grad der Behinderung ≥50 werden die Auslagen für die nächsthöhere Klasse erstattet (§4 Abs.2)."]
  Q_HIGHER_CLASS_DISABILITY -->|"Nein"| Q_HIGHER_CLASS_HEALTH["Besteht aus gesundheitlichen Gründen die Notwendigkeit einer nächsthöheren Flugklasse? (Ja / Nein)"]

  %% FOLLOW-UP CHECK 2b: sonstige gesundheitliche Gründe
  Q_HIGHER_CLASS_HEALTH -->|"Ja"| A_HIGHER_CLASS_HEALTH["Ja: Bei entsprechendem gesundheitlichen Zustand kann die nächsthöhere Klasse erstattet werden (§4 Abs.2)."]
  Q_HIGHER_CLASS_HEALTH -->|"Nein"| A_LOWEST_FLIGHT["Nein: Grundsätzlich werden nur die Kosten der niedrigsten Flugklasse erstattet; Ausnahmen sind durch die oberste Dienstbehörde/Finanzministerium möglich (§4 Abs.1)."]
""",

"""
  %% Updated branch: C. Wegstreckenentschädigung (Chatbot-like follow-up)
  WEG_PKW["C.1 Privates Kraftfahrzeug (Sätze)"]

  %% Main question (reuse existing node id)
  Q_PKW_RATE["Frage: Wie viel Wegstreckenentschädigung gilt für private PKW-Fahrten (Ct/km)?"]
  A_PKW_RATE["Antwort: 30 Cent je Kilometer zurückgelegter Strecke (§5 Abs.1)."]

  %% Follow-up diagnostic: erheblicher dienstlicher Interesse? (reformuliert)
  Q_PKW_35["Trifft ein erhebliches dienstliches Interesse an der Nutzung des Privat-PKW zu (z. B. wegen Zeitdruck oder fehlender gleichwertiger ÖPNV-Verbindung)?"]
  A_PKW_35["Antwort: Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 35 Cent/km (§5 Abs.2)."]

  %% Zuschlag für schlechte Wege (weiterer Check)
  Q_BAD_ROAD["Sind regelmäßig Fahrten auf unbefestigten oder schwer befahrbaren Wegen erforderlich?"]
  A_BAD_ROAD["Antwort: Ja — mit Zustimmung der obersten Dienstbehörde kann ein Zuschlag von 5 Cent/km gewährt werden (§5 Abs.2)."]
  Q_ZUSCHLAG_PROOF["Frage: Welche Nachweise gelten für den Zuschlag?"]
  A_ZUSCHLAG_PROOF["Antwort: Die Zustimmung der obersten Dienstbehörde ist erforderlich; Nachweise und Begründungen richten sich nach dienstlichen Vorgaben (§5 Abs.2)."]

  %% Edges: main flow with Yes/No branching
  WEG_PKW --> Q_PKW_RATE
  Q_PKW_RATE --> A_PKW_RATE

  Q_PKW_RATE --> Q_PKW_35
  Q_PKW_35 -->|"Ja"| A_PKW_35
  Q_PKW_35 -->|"Nein"| A_PKW_RATE

  %% After determining rate, optional check for bad roads (leads to possible extra 5 Ct/km)
  A_PKW_35 --> Q_BAD_ROAD
  A_PKW_RATE --> Q_BAD_ROAD

  Q_BAD_ROAD -->|"Ja"| A_BAD_ROAD
  Q_BAD_ROAD -->|"Nein"| A_PKW_RATE

  A_BAD_ROAD --> Q_ZUSCHLAG_PROOF
  Q_ZUSCHLAG_PROOF --> A_ZUSCHLAG_PROOF
""",

"""
%%
  TRA_TAXI["B.3 Mietwagen, Taxi, Carsharing und Klimaausgleich"]

  %% Hauptfrage + direkte Antwort
  TRA_TAXI --> Q_RENT_TAXI_CARSHARE["Frage: Werden Mietwagen-, Taxi- oder Carsharing‑Kosten ersetzt?"]
  Q_RENT_TAXI_CARSHARE --> A_RENT_TAXI_CARSHARE["Antwort: Ja — sofern aus triftigem Grund benutzt; sonst darf die Vergütung nicht über der Vergütung für öffentliche Verkehrsmittel liegen (§4 Abs.3)."]

  %% Folgecheck (diagnostisch): liegt ein triftiger Grund vor?
  %% (Benutzen vorhandenen Q-Knoten Q_PAY_MORE_THAN_OPNV, hier als diagnostische Frage umformuliert)
  Q_RENT_TAXI_CARSHARE --> Q_PAY_MORE_THAN_OPNV["Diagnose: Liegt ein triftiger Grund für die Nutzung vor?"]
  Q_PAY_MORE_THAN_OPNV -->|"Ja"| A_RENT_TAXI_CARSHARE
  Q_PAY_MORE_THAN_OPNV -->|"Nein"| A_PAY_MORE_THAN_OPNV["Antwort: Ohne triftigen Grund darf keine höhere Vergütung als beim ÖPNV gezahlt werden (§4 Abs.3 Satz2)."]

  %% Ergänzende Information zu Carsharing‑Mitgliedsgebühren (allgemein, kein Ja/Nein-Check)
  Q_RENT_TAXI_CARSHARE --> Q_CARSHARE_MEMBER_FEE["Frage: Wird bei Carsharing die Mitgliedsgebühr wegen privater Nutzung gekürzt?"]
  Q_CARSHARE_MEMBER_FEE --> A_CARSHARE_MEMBER_FEE["Antwort: Nein, die Mitgliedsgebühr wird nicht wegen privater Nutzung gekürzt (§4 Abs.3 Satz3)."]

  %% Erhaltener Branch‑Inhalt zu Klimaausgleich bei Flügen (unverändert)
  TRA_TAXI --> Q_FLIGHT_OFFSET["Frage: Müssen Klimaausgleichszahlungen bei Flügen berücksichtigt werden?"]
  Q_FLIGHT_OFFSET --> A_FLIGHT_OFFSET["Antwort: Ja, Kosten für Ausgleichszahlungen sind in die Wirtschaftlichkeitsberechnung einzubeziehen; Behörden müssen jährliche Ausgleichszahlungen leisten (§4 Abs.1, Abs.4)."]

  TRA_TAXI --> Q_ANNUAL_OFFSET_OBLIGATION["Frage: Wer muss jährliche Ausgleichszahlungen für dienstliche Flüge leisten?"]
  Q_ANNUAL_OFFSET_OBLIGATION --> A_ANNUAL_OFFSET_OBLIGATION["Antwort: Mitglieder der Landesregierung, Ministerien, nachgeordnete Behörden und staatliche Hochschulen sind verpflichtet, jährliche Ausgleichszahlungen zu leisten (§4 Abs.4)."]

  TRA_TAXI --> Q_THIRD_FUNDED_FLIGHTS["Frage: Gelten Ausgleichszahlungen auch für Hochschulflüge aus Drittmitteln?"]
  Q_THIRD_FUNDED_FLIGHTS --> A_THIRD_FUNDED_FLIGHTS["Antwort: Ja, bei Projekten staatlicher Hochschulen sind Ausgleichszahlungen fällig, sofern Vorgaben der Drittmittelgeber dem nicht entgegenstehen (§4 Abs.4 Satz2)."]
""",

"""
%%
  TAGE["D. Tagegeld (Sätze, Dauer, Kürzungen)"]

  %% Main Q + direct answer
  TAGE --> Q_FULL_DAY["Frage: Wie hoch ist das Tagegeld für einen vollen Kalendertag?"]
  Q_FULL_DAY --> A_FULL_DAY["Antwort: Das Tagegeld beträgt 24 Euro für jeden vollen Kalendertag (§6 Abs.1)."]

  %% Non-diagnostic factual follow-up about An-/Abreisetag (general info, no Yes/No branching)
  A_FULL_DAY --> Q_ARR_DEP_DAY["Frage: Wie viel Tagegeld steht für An‑/Abreisetag bei mehrtägigen Reisen zu?"]
  Q_ARR_DEP_DAY --> A_ARR_DEP_DAY["Antwort: Bei Dienstreisedauer >8 Std. 6 Euro, bei >14 Std. 12 Euro für An‑/Abreisetag (§6 Abs.1)."]

  %% Diagnostic follow-up: check whether unentgeltliche Verpflegung gewährt wird
  A_FULL_DAY --> Q_UNPAID_MEALS["Frage (diagnostisch): Erhalten Sie während der Fortbildung unentgeltlich Verpflegung (z. B. Frühstück, Mittag oder Abendessen)?"]

  Q_UNPAID_MEALS -->|"Ja"| A_UNPAID_MEALS["Antwort (Ja): Dann wird das Tagegeld gekürzt: Frühstück 20 %; Mittag und Abendessen je 40 % des vollen Tagegeldes (§6 Abs.4)."]
  Q_UNPAID_MEALS -->|"Nein"| A_NO_REDUCTION["Antwort (Nein): Es erfolgen keine Abzüge; Sie erhalten das volle Tagegeld (24 €) bzw. die oben genannten An‑/Abreisetagsbeträge (§6 Abs.1, Abs.4)."]

  %% Weitere (unveränderte) Unterpunkte der D-Gruppe bleiben erhalten
  TAGE --> TAGE_DURATION["D.2 Bestimmung der Reisedauer und Kürzungen"]

  TAGE_DURATION --> Q_DETERMINE_DURATION["Frage: Nach welchen Zeitpunkten bestimmt sich die Dauer der Dienstreise (Abreise/Ankunft)?"]
  Q_DETERMINE_DURATION --> A_DETERMINE_DURATION["Antwort: Dauer richtet sich nach Abreise und Ankunft an der Wohnung, außer die Reise beginnt/endet an der Dienststätte oder dies wurde so angeordnet; bei mehreren Wohnungen gilt die der Dienststätte nächste (§6 Abs.2)."]

  TAGE_DURATION --> Q_TIMEZONE_NIGHT["Frage: Wie werden Zeitzonen, Nachtfahrten und Zwischenlandungen berücksichtigt?"]
  Q_TIMEZONE_NIGHT --> A_TIMEZONE_NIGHT["Antwort: Gesonderte Regeln fehlen; maßgeblich bleiben Abreise/Ankunftszeitpunkte nach Ortszeit und die besonderen Vorschriften bei Auslandsdienstreisen (§6; §12)."]

  TAGE_DURATION --> Q_TAGE_DG_RESTATE["Frage: Besteht für Dienstgänge Anspruch auf Tagegeld bzw. wie werden längere Dienstgänge vergütet?"]
  Q_TAGE_DG_RESTATE --> A_TAGE_DG_RESTATE["Antwort: Bei Dienstgängen besteht kein Tagegeldanspruch; bei Dienstgängen >8 Std. werden nachgewiesene Verpflegungsauslagen bis zur Höhe des Tagegeldes für die gleich lange Dienstreise erstattet (§6 Abs.3)."]
""",

"""
%%
  UEBN_BASIC["E.1 Pauschalbeträge und Ersatz höherer Übernachtungskosten"]

  UEBN_BASIC --> Q_OVN_DOM_ABR["Frage: Wie hoch ist das pauschale Übernachtungsgeld im Inland und Ausland?"]
  Q_OVN_DOM_ABR --> A_OVN_DOM_ABR["Antwort: Pauschales Übernachtungsgeld: 20 Euro im Inland, 30 Euro im Ausland (§7 Abs.1)."]

  Q_OVN_DOM_ABR --> Q_OVN_EXCLUSIONS["Check: Wird Ihnen die Unterkunft vom Arbeitgeber unentgeltlich bereitgestellt?"]
  Q_OVN_EXCLUSIONS -->|"Ja"| A_OVN_EXCLUSIONS["Antwort: Der Anspruch entfällt u. a. bei unentgeltlich vom Dienstherrn bereitgestellter Unterkunft; ebenso entfällt er bei Benutzung von Beförderungsmitteln, bei Aufenthalt in eigener Wohnung oder wenn Unterkunftskosten im erstattungsfähigen Fahrpreis enthalten sind. Eine zusätzliche Übernachtung wird nur ersetzt, wenn sie wegen früher Ankunft oder später Abfahrt erforderlich ist (§7 Abs.2)."]
  Q_OVN_EXCLUSIONS -->|"Nein"| A_OVN_DOM_ABR

  Q_OVN_DOM_ABR --> Q_OVN_HIGHER["Frage: Wer legt die Höchstbeträge für erstattungsfähige höhere Übernachtungskosten fest, falls mein Hotel teurer ist als die Pauschale?"]
  Q_OVN_HIGHER --> A_OVN_HIGHER["Antwort: Höhere notwendige Übernachtungskosten werden im notwendigen Umfang erstattet; das Finanzministerium bestimmt per Verwaltungsvorschrift bis zu welcher Höhe (§7 Abs.1; §14)."]

  UEBN_BASIC --> Q_OVN_TICKET_INCLUDED["Frage: Was gilt, wenn Unterkunftskosten Teil eines Ticketpreises sind (z. B. Bahnreise mit Hotel)?"]
  Q_OVN_TICKET_INCLUDED --> A_OVN_TICKET_INCLUDED["Antwort: Übernachtungsgeld wird nicht gewährt, wenn Unterkunftskosten im erstattungsfähigen Fahrpreis enthalten sind, außer eine zusätzliche Übernachtung ist wegen früher Ankunft oder später Abfahrt erforderlich (§7 Abs.2 Nr.4)."]
""",

"""
%%
  PAUS["F. Aufwands- und Pauschvergütung / sonstige Nebenkosten (§9–10)"]

  %% Main question
  PAUS --> Q_LUMP_INSTEAD["Frage: Können Dienstreisende statt Tagegeld/Übernachtung eine Aufwandsvergütung erhalten?"]
  Q_LUMP_INSTEAD --> A_LUMP_INSTEAD["Antwort: Ja. Dienstreisende mit erfahrungsgemäß geringeren Aufwendungen können nach näherer Bestimmung der obersten Dienstbehörde eine Aufwandsvergütung erhalten (§9 Abs.1)."]

  %% Diagnostic check (Has the authority already introduced a rule?)
  Q_LUMP_INSTEAD --> Q_PAUCH_REGULAR["Kontrollfrage: Hat Ihre oberste Dienstbehörde bereits eine Aufwands‑ oder Pauschvergütungsregelung eingeführt?"]

  %% YES path: authority has a rule — explain calculation and follow-ups
  Q_PAUCH_REGULAR -->|"Ja"| A_PAUCH_REGULAR["Antwort (Wenn Ja): Die oberste Dienstbehörde kann für regelmäßige oder gleichartige Dienstreisen eine Pauschvergütung anstelle der Einzelvergütungen festlegen; die Pauschale bemisst sich nach dem Durchschnitt der andernfalls anfallenden Einzelvergütungen (§9 Abs.2)."]
  A_PAUCH_REGULAR --> Q_LUMP_FORM["Frage: Welche Form der Regelung/Vereinbarung ist nötig, um Aufwandsvergütung zu erhalten?"]
  Q_LUMP_FORM --> A_LUMP_FORM["Antwort: Die Form regelt die oberste Dienstbehörde; üblicherweise durch dienstliche Festlegung oder Vereinbarung (§9 Abs.1)."]

  A_PAUCH_REGULAR --> Q_PAUCH_PROOF["Frage: Wie sind Nachweise bzw. Prüfpflichten bei Pauschalvergütungen geregelt?"]
  Q_PAUCH_PROOF --> A_PAUCH_PROOF["Antwort: Nachweise und Prüfpflichten regelt die zuständige Dienststelle; das Gesetz verlangt Prüfungen und formale Vorgaben (§3 Abs.4; §10)."]

  A_PAUCH_REGULAR --> Q_PAUCH_LIMITS["Frage: Gibt es Obergrenzen oder Zuständigkeiten zur Festsetzung von Pauschalen?"]
  Q_PAUCH_LIMITS --> A_PAUCH_LIMITS["Antwort: Zuständigkeit liegt bei der obersten Dienstbehörde bzw. ermächtigten Behörden; Obergrenzen können durch Verwaltungsvorschrift geregelt werden (§9 Abs.2; §14)."]

  %% NO path: authority has not introduced rule — outcome
  Q_PAUCH_REGULAR -->|"Nein"| A_NO_RULE["Antwort (Wenn Nein): Kurz: Ohne eine Regelung der obersten Dienstbehörde kann derzeit keine Pauschalvergütung anstelle der Einzelvergütungen gezahlt werden. Die oberste Dienstbehörde müsste eine Regelung erlassen, die auch den Durchschnittszeitraum und welche Auslagen (z. B. Verpflegung, Übernachtung, Park/ÖPNV) in die Pauschale einbezogen werden, festlegt (§9 Abs.1–2)."]
""",

"""
ANTR["J. Anträge, Fristen, Belege, Anrechnung, Verzicht"]

  ANTR --> ANTR_FILE["J.1 Antragstellung & Ausschlussfrist"]
  ANTR --> ANTR_BELEGE["J.2 Belege, Anrechnung, Verzicht"]

  %% Antragstellung & Ausschlussfrist (neu geordnet als Chatbot‑Flow)
  ANTR_FILE --> Q_HOW_TO_APPLY["Frage: Muss Reisekostenvergütung schriftlich oder elektronisch beantragt werden und wer erhält die Vergütung?"]
  Q_HOW_TO_APPLY --> A_HOW_TO_APPLY["Antwort: Reisekostenvergütung ist schriftlich oder elektronisch zu beantragen; die Vergütung wird den Dienstreisenden auf Antrag gezahlt (§3 Abs.1, §3 Abs.4)."]

  ANTR_FILE --> Q_DEADLINE["Frage: Innerhalb welcher Frist muss die Vergütung beantragt werden und wann beginnt die Frist?"]
  Q_DEADLINE --> A_DEADLINE["Antwort: Ausschlussfrist 6 Monate nach Beendigung der Dienstreise; die Frist beginnt mit dem Tag nach Beendigung der Dienstreise (bei §10 Abs.2 mit dem Tag, an dem die Reise geendet hätte) (§3 Abs.4)."]

  %% Geführte Nachfragen zu Belegen und Aufbewahrung (folgegerichtet)
  Q_DEADLINE --> Q_REQUEST_RECEIPTS["Frage: Bis zu welchem Zeitpunkt dürfen zuständige Stellen die Vorlage der Kostenbelege verlangen?"]
  Q_REQUEST_RECEIPTS --> A_REQUEST_RECEIPTS["Antwort: Zuständige Stellen können bis zum Ablauf von sechs Monaten nach Antragstellung die Vorlage der maßgeblichen Kostenbelege verlangen (§3 Abs.4)."]

  Q_REQUEST_RECEIPTS --> Q_NO_RECEIPT_REJECT["Frage: Was passiert, wenn angeforderte Belege nicht innerhalb eines Monats vorgelegt werden?"]
  Q_NO_RECEIPT_REJECT --> A_NO_RECEIPT_REJECT["Antwort: Werden Belege auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden (§3 Abs.4)."]

  Q_NO_RECEIPT_REJECT --> Q_KEEP_RECEIPTS["Frage: Wie lange sind Kostenbelege nach Erstattung aufzubewahren und vorzulegen?"]
  Q_KEEP_RECEIPTS --> A_KEEP_RECEIPTS["Antwort: Dienstreisende müssen Kostenbelege nach Erstattung bis zum Ablauf eines Jahres aufbewahren und auf Verlangen vorlegen (§3 Abs.4)."]

  %% Unveränderte ergänzende Knoten in J.2 (bleiben an ihrem Platz)
  ANTR_BELEGE --> Q_THIRD_PARTY_CREDITS["Frage: Werden Leistungen Dritter auf die Reisekostenvergütung angerechnet?"]
  Q_THIRD_PARTY_CREDITS --> A_THIRD_PARTY_CREDITS["Antwort: Ja, erhaltene Leistungen Dritter sind auf die Reisekostenvergütung anzurechnen (§3 Abs.5)."]

  ANTR_BELEGE --> Q_SECONDARY_CLAIM["Frage: Haben Dienstreisende Anspruch auf Vergütung für Nebentätigkeiten, wenn eine andere Stelle Auslagenerstattung gewährt?"]
  Q_SECONDARY_CLAIM --> A_SECONDARY_CLAIM["Antwort: Dienstreisende haben nur insoweit Anspruch nach diesem Gesetz, wie nicht eine andere Stelle Auslagenerstattung für dieselbe Reise gewährt (§3 Abs.6)."]

  ANTR_BELEGE --> Q_WAIVER["Frage: Kann auf Reisekostenvergütung ganz oder teilweise verzichtet werden und wie muss das erfolgen?"]
  Q_WAIVER --> A_WAIVER["Antwort: Ja, Verzicht ist möglich; er ist schriftlich oder elektronisch zu erklären (§3 Abs.7)."]
""",

"""
%%
  AUSW["H. Auslandsdienstreisen (Definition, Länderregel, Langzeit)"]

  %% Main question -> direkte Antwort
  AUSW --> Q_APPLY_RULES["Frage: Gilt das LRKG auch für Auslandsdienstreisen?"]
  Q_APPLY_RULES --> A_APPLY_RULES["Antwort: Ja, nach §12 Abs.2 gelten die §§1–11 entsprechend auch für Auslandsdienstreisen; abweichend werden Auslandstage‑ und -übernachtungsgelder nach §12 Abs.3 in Verbindung mit der Auslandsreisekostenverordnung (ARV) und der ARVVwV bemessen."]

  %% Folgefrage: Begriff klären (hilft Nutzer festzustellen, ob die Regelung greift)
  Q_APPLY_RULES --> Q_ABROAD_DEF["Folgefrage: Trifft Ihre Reise die Definition einer Auslandsdienstreise (mind. ein Geschäftsort im Ausland)?"]
  Q_ABROAD_DEF --> A_ABROAD_DEF["Antwort: Auslandsdienstreisen sind Dienstreisen zwischen Inland und Ausland sowie im Ausland; mindestens ein Geschäftsort im Ausland muss vorliegen (§12 Abs.1)."]

  %% Konkrete Bemessung der Auslandssätze (häufige Nachfolgefrage)
  Q_APPLY_RULES --> Q_ABROAD_RATES["Frage: Nach welchen Regeln werden Auslandstage- und -übernachtungsgelder bemessen?"]
  Q_ABROAD_RATES --> A_ABROAD_RATES["Antwort: Auslandstage- und -übernachtungsgelder werden nach §3 der Auslandsreisekostenverordnung (ARV) und der ARVVwV bemessen (§12 Abs.3)."]

  %% Weitere einschlägige Klarstellungen (Länderbestimmung, Zwischenlandungen, Langzeitregelungen)
  Q_ABROAD_RATES --> Q_COUNTRY_BY_MIDNIGHT["Frage: Welchem Land ist das Tage‑/Übernachtungsgeld zuzuordnen, wenn vor Mitternacht ein Land erreicht wurde?"]
  Q_COUNTRY_BY_MIDNIGHT --> A_COUNTRY_BY_MIDNIGHT["Antwort: Es gilt das Land, das vor Mitternacht Ortszeit zuletzt erreicht wurde; wird Inland vor Mitternacht zuletzt erreicht, gilt das Land des letzten Geschäftsortes im Ausland (§12 Abs.4)."]

  Q_ABROAD_RATES --> Q_STOP_OVERNIGHT["Frage: Wie werden Zwischenlandungen bei Flug/Schiff berücksichtigt?"]
  Q_STOP_OVERNIGHT --> A_STOP_OVERNIGHT["Antwort: Ein Land gilt beim Flug/Schiff als erreicht, wenn das Flugzeug/Schiff dort landet; Zwischenlandungen bleiben unberücksichtigt, es sei denn, sie erfordern Übernachtungen (§12 Abs.5)."]

  Q_ABROAD_RATES --> Q_ABROAD_15_WHEN_REDUCE["Frage: Was gilt bei Langzeitaufenthalten im Ausland ab dem 15. Tag?"]
  Q_ABROAD_15_WHEN_REDUCE --> A_ABROAD_15_WHEN_REDUCE["Antwort: Dauert ein Auslandsaufenthalt ohne Hin‑/Rückreisetage länger als 14 Tage, ist das Auslandstagegeld ab dem 15. Tag um 25% zu ermäßigen; die oberste Dienstbehörde kann in begründeten Fällen absehen und ab dem 15. Tag auch tatsächliche Übernachtungskosten statt Pauschale erstatten (§12 Abs.6)."]
""",

"""
%%
  ADMIN["L. Verwaltung, Zuständigkeiten, Anpassungen"]

  %% Main question (reformulated from existing node Q_ADMIN_REGS)
  Q_ADMIN_REGS["Frage: Wer erlässt die allgemeinen Verwaltungsvorschriften zum LRKG und wie werden Sätze/Zuständigkeiten geregelt?"]
  A_ADMIN_REGS["Antwort: Das Finanzministerium erlässt die allgemeinen Verwaltungsvorschriften zu diesem Gesetz und regelt Verfahren und Zuständigkeiten für Anpassungen (§14 Abs.2)."]

  %% Follow-ups: Befugnisse des Finanzministeriums
  Q_ADAPT_RATES["Frage: Welche Befugnisse hat das Finanzministerium zur Anpassung der Beträge in §§5 und 7?"]
  A_ADAPT_RATES["Antwort: Das Finanzministerium darf durch Rechtsverordnung die in §§5 und 7 Abs.1 festgesetzten Beträge an veränderte wirtschaftliche Verhältnisse anpassen (§14 Abs.1)."]

  %% Follow-ups: Ausnahmen / dienststellenspezifische Regelungen
  Q_WHO_ALLOW_EXCEPT["Frage: Können oberste Dienstbehörden oder nachgeordnete Dienststellen Ausnahmen bzw. abweichende Regelungen für ihren Geschäftsbereich zulassen?"]
  A_WHO_ALLOW_EXCEPT["Antwort: Ja, die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörden können Ausnahmen zulassen; Zuständigkeiten sind gesetzlich geregelt (§4 Abs.1)."]

  Q_SERVICE_EXCEPTION_PROCESS["Frage: Wie können Dienststellen Ausnahmen begründen und Genehmigungsprozesse gestalten?"]
  A_SERVICE_EXCEPTION_PROCESS["Antwort: Dienststellen können Ausnahmen mit besonderem dienstlichen Grund begründen und müssen dies dokumentieren; die oberste Dienstbehörde kann Ermächtigungen erteilen (§4 Abs.1; §12 Abs.6)."]

  %% Optional/related Pflichten (original nodes preserved)
  Q_MIN_CLIMATE_OBLIG["Frage: Welche Pflichten haben Ministerien und Hochschulen bzgl. Klimaausgleichszahlungen?"]
  A_MIN_CLIMATE_OBLIG["Antwort: Ministerien und staatliche Hochschulen sind verpflichtet, jährliche Ausgleichszahlungen für dienstliche Flüge zu leisten (§4 Abs.4)."]

  Q_REPORT_DRM["Frage: Wie sind Melde- und Nachweispflichten für Drittmittelfinanzierte Flüge geregelt?"]
  A_REPORT_DRM["Antwort: Melde‑ und Nachweispflichten regeln die Verwaltungen; das Gesetz nennt die Pflicht zur Leistung der Ausgleichszahlung, sofern Drittmittelvorgaben dem nicht entgegenstehen (§4 Abs.4)."]

  %% Connections
  ADMIN --> Q_ADMIN_REGS
  Q_ADMIN_REGS --> A_ADMIN_REGS

  Q_ADMIN_REGS --> Q_ADAPT_RATES
  Q_ADAPT_RATES --> A_ADAPT_RATES

  Q_ADMIN_REGS --> Q_WHO_ALLOW_EXCEPT
  Q_WHO_ALLOW_EXCEPT --> A_WHO_ALLOW_EXCEPT

  Q_ADMIN_REGS --> Q_SERVICE_EXCEPTION_PROCESS
  Q_SERVICE_EXCEPTION_PROCESS --> A_SERVICE_EXCEPTION_PROCESS

  Q_ADMIN_REGS --> Q_MIN_CLIMATE_OBLIG
  Q_MIN_CLIMATE_OBLIG --> A_MIN_CLIMATE_OBLIG

  Q_ADMIN_REGS --> Q_REPORT_DRM
  Q_REPORT_DRM --> A_REPORT_DRM
""",

"""
%%
  ANTR["J. Anträge, Fristen, Belege, Anrechnung, Verzicht"]

  %% reorganised into a chatbot-like, guided sequence for questions about receipts, rejection, retention and application deadline
  ANTR --> ANTR_BELEGE["J.2 Belege, Anrechnung, Verzicht (geführte Abfrage)"]
  ANTR --> ANTR_FILE["J.1 Antragstellung & Ausschlussfrist"]

  %% Main question: Bis wann dürfen Belege verlangt werden? (Direkte Antwort)
  ANTR_BELEGE --> Q_REQUEST_RECEIPTS["Frage: Bis zu welchem Zeitpunkt dürfen zuständige Stellen die Vorlage der Kostenbelege verlangen?"]
  Q_REQUEST_RECEIPTS --> A_REQUEST_RECEIPTS["Antwort: Zuständige Stellen können bis zum Ablauf von sechs Monaten nach Antragstellung die Vorlage der maßgeblichen Kostenbelege verlangen (§3 Abs.4)."]

  %% Follow-up: Was passiert, wenn Belege nicht vorgelegt werden?
  Q_REQUEST_RECEIPTS --> Q_NO_RECEIPT_REJECT["Frage: Was passiert, wenn angeforderte Belege nicht innerhalb eines Monats vorgelegt werden?"]
  Q_NO_RECEIPT_REJECT --> A_NO_RECEIPT_REJECT["Antwort: Werden Belege auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden (§3 Abs.4)."]

  %% Follow-up: Wie lange Belege nach Erstattung aufbewahren?
  Q_REQUEST_RECEIPTS --> Q_KEEP_RECEIPTS["Frage: Wie lange sind Kostenbelege nach Erstattung aufzubewahren und vorzulegen?"]
  Q_KEEP_RECEIPTS --> A_KEEP_RECEIPTS["Antwort: Dienstreisende müssen Kostenbelege nach Erstattung bis zum Ablauf eines Jahres aufbewahren und auf Verlangen vorlegen (§3 Abs.4)."]

  %% Weitere, separate (nicht-diagnostische) Informationen zur Antragstellung und Ausschlussfrist
  ANTR_FILE --> Q_HOW_TO_APPLY["Frage: Muss Reisekostenvergütung schriftlich oder elektronisch beantragt werden und wer erhält die Vergütung?"]
  Q_HOW_TO_APPLY --> A_HOW_TO_APPLY["Antwort: Reisekostenvergütung ist schriftlich oder elektronisch zu beantragen; die Vergütung wird den Dienstreisenden auf Antrag gezahlt (§3 Abs.1, §3 Abs.4)."]

  ANTR_FILE --> Q_DEADLINE["Frage: Innerhalb welcher Frist muss die Vergütung beantragt werden und wann beginnt die Frist?"]
  Q_DEADLINE --> A_DEADLINE["Antwort: Ausschlussfrist 6 Monate nach Beendigung der Dienstreise; die Frist beginnt mit dem Tag nach Beendigung der Dienstreise (§3 Abs.4)."]

  %% Unveränderte, sonstige Punkte in J.2 (bleiben an Ort und Stelle)
  ANTR_BELEGE --> Q_THIRD_PARTY_CREDITS["Frage: Werden Leistungen Dritter auf die Reisekostenvergütung angerechnet?"]
  Q_THIRD_PARTY_CREDITS --> A_THIRD_PARTY_CREDITS["Antwort: Ja, erhaltene Leistungen Dritter sind auf die Reisekostenvergütung anzurechnen (§3 Abs.5)."]

  ANTR_BELEGE --> Q_SECONDARY_CLAIM["Frage: Haben Dienstreisende Anspruch auf Vergütung für Nebentätigkeiten, wenn eine andere Stelle Auslagenerstattung gewährt?"]
  Q_SECONDARY_CLAIM --> A_SECONDARY_CLAIM["Antwort: Dienstreisende haben nur insoweit Anspruch nach diesem Gesetz, wie nicht eine andere Stelle Auslagenerstattung für dieselbe Reise gewährt (§3 Abs.6)."]

  ANTR_BELEGE --> Q_WAIVER["Frage: Kann auf Reisekostenvergütung ganz oder teilweise verzichtet werden und wie muss das erfolgen?"]
  Q_WAIVER --> A_WAIVER["Antwort: Ja, Verzicht ist möglich; er ist schriftlich oder elektronisch zu erklären (§3 Abs.7)."]
""",


"""
%%
  TRG["I. Trennungsgeld — Anspruch bei Abordnung ohne Umzugskosten"]

  %% Hauptfrage und direkte Antwort
  TRG --> Q_TRG_WHEN["Frage: Wann entsteht Anspruch auf Trennungsgeld bei Abordnung ohne Zusage von Umzugskostenvergütung?"]
  Q_TRG_WHEN --> A_TRG_WHEN["Antwort: Anspruch entsteht, wenn eine Abordnung außerhalb des Dienst‑ oder Wohnortes erfolgt und keine Zusage zur Erstattung von Umzugskosten gemacht wurde; das Trennungsgeld soll notwendige Auslagen unter Berücksichtigung der häuslichen Ersparnis abdecken (§13 Abs.1)."]

  %% Folgefrage: Bemessung (allgemeine Information, kein Ja/Nein-Check)
  Q_TRG_WHEN --> Q_TRG_AMOUNT["Folgefrage: Wovon hängen Höhe und Dauer des Trennungsgeldes ab?"]
  Q_TRG_AMOUNT --> A_TRG_AMOUNT["Antwort: Höhe und Dauer richten sich nach den notwendigen Auslagen und der zu berücksichtigenden häuslichen Ersparnis; das Finanzministerium kann hierzu eine Rechtsverordnung erlassen (§13 Abs.1 Satz 2)."]

  %% Folgefrage: Gilt das auch für Beamtinnen/Beamte auf Widerruf im Vorbereitungsdienst?
  Q_TRG_WHEN --> Q_TRG_TRAINEES["Folgefrage: Gilt Trennungsgeld auch für Beamtinnen/Beamte auf Widerruf im Vorbereitungsdienst?"]
  Q_TRG_TRAINEES --> A_TRG_TRAINEES["Antwort: Ja. Nach §13 Abs.2 gilt Absatz 1 entsprechend für Beamtinnen/Beamte auf Widerruf im Vorbereitungsdienst; der für die Ausbildung maßgebliche Dienstort wird von der obersten Dienstbehörde bestimmt (§13 Abs.2)."]
"""

]


extensions_pha = ["""

  P2C["2.3 Immobilien, Vermietung & Bauherr — Interaktiver Check"]

  Q2_HausWann["Q: Wann besteht Schutz als Haus-/Wohnungsbesitzer:in?"]
  Q2_FerienAusland["Check 1: Befindet sich die Immobilie im Inland (Deutschland) oder ist es eine selbstgenutzte Ferienimmobilie in EU / Norwegen / Island?"]
  Q2_VermietZimmer["Check 2: Wird die Wohnung ausschließlich zu eigenen privaten Wohnzwecken genutzt (also nicht vermietet)?"]

  A2_HausWann["A (Inland + privat): Für selbstgenutzte Immobilien im Inland (und bestimmte Ferienobjekte in EU/Norwegen/Island) besteht Schutz einschließlich Außenanlagen; Nachhaftung für Besitzwechsel während der Vertragslaufzeit ist möglich (§836 BGB). (VB Smart)"]
  A2_FerienAusland["A (Ferienimmobilie): Selbstgenutzte Ferienhäuser in EU, Norwegen oder Island sind mitversichert, ebenso zugehörige Außenanlagen. (VB Smart)"]
  A2_VermietZimmer["A (vermietet): Die Vermietung einzelner Zimmer oder Einliegerwohnungen an Privatpersonen ist mitversichert, einschließlich zugehöriger Garagen. (VB Smart)"]

  P2C --> Q2_HausWann
  Q2_HausWann --> Q2_FerienAusland

  Q2_FerienAusland -->|"Im Inland (Deutschland)"| Q2_VermietZimmer
  Q2_FerienAusland -->|"Selbstgenutzte Ferienimmobilie in EU/Norwegen/Island" | A2_FerienAusland

  Q2_VermietZimmer -->|"Ja — ausschließlich privat genutzt (nicht vermietet)"| A2_HausWann
  Q2_VermietZimmer -->|"Nein — (teilweise) vermietet" | A2_VermietZimmer
""",

"""

  %% Updated branch: Fahrzeuge, Wasser- & Luftfahrzeuge, Modellfahrzeuge (P2F)

  Q2_Veh_Pedelec["Gilt Schutz für Pedelecs (E‑Tretunterstützung)?"]
  Q2_Veh_KFZex["Braucht Ihr Pedelec ein amtliches Kennzeichen/Versicherungskennzeichen oder einen Führerschein?"]

  A2_Veh_Pedelec["Ja — Pedelecs mit elektrischer Tretunterstützung bis 25 km/h ohne Kennzeichen/Führerschein sind durch die Privat‑Haftpflicht gedeckt. (VB Smart, Ziff. 2.6)"]
  A2_Veh_KFZex["Ja — Fahrzeuge, die zulassungs‑ oder führerscheinpflichtig sind (d.h. Kennzeichen/Versicherungspflicht), sind von der Privat‑Haftpflicht ausgeschlossen; hierfür ist eine Kfz‑Haftpflicht erforderlich. (VB Smart, Ziff. 3.2)"]

  %% Flow: main question → diagnostic check → branching answers
  Q2_Veh_Pedelec --> Q2_Veh_KFZex
  Q2_Veh_KFZex -->|"Nein (kein Kennzeichen / kein Führerschein erforderlich)"| A2_Veh_Pedelec
  Q2_Veh_KFZex -->|"Ja (Kennzeichen / Führerschein erforderlich)"| A2_Veh_KFZex
""",
"""

  P2I["2.9 Sonstige Spezialfälle (Kaution, Internet, Umwelt, Schlüssel)"]

  %% MAIN QUESTION
  P2I --> Q2_Internet["Deckt die Police Haftpflicht durch private Internetnutzung (z. B. Verbreitung von Schadsoftware, Datenverlust bei Dritten)?"]

  %% DIRECT ANSWER
  Q2_Internet --> A2_Internet["Ja — Haftpflichtansprüche aus privatem elektronischen Datenaustausch sind grundsätzlich mitversichert. (Ziff. 2.2.10)"]

  %% FOLLOW-UP CHECK (diagnostic)
  Q2_Internet --> Q2_InternetAus["Wurde das Eindringen/der Einsatz von Schadsoftware bewusst oder unbefugt (z. B. Hacking, absichtliches Einbringen)?"]

  Q2_InternetAus -->|"Ja"| A2_InternetAus["Nein — Ausgeschlossen sind bewusstes Eindringen/Hacking, gezielte Angriffe und der beabsichtigte Einsatz bzw. die bewusste Verbreitung von Schadsoftware sowie unberechtigtes Herunterladen urheberrechtlich geschützter Inhalte. (Ziff. 2.2.11; Ziff. 2.3)"]

  Q2_InternetAus -->|"Nein"| A2_Internet_Unbeabs["Ja — unbeabsichtigte Fälle (z. B. versehentlich geöffnetes Attachment oder kompromittiertes Gerät) können gedeckt sein; konkrete Prüfung nach den Vertragsbedingungen. (Ziff. 2.2.10)"]
""",
"""
graph TD

  %% Affected branch: P2I (reorganized for chatbot-style follow-up)
  P2I["2.9 Sonstige Spezialfälle (Kaution, Internet, Umwelt, Schlüssel)"]

  %% Unchanged Q/A nodes in this branch (preserved)
  P2I --> Q2_Kaution["Übernimmt die Police Kautionsleistungen im Ausland?"]
  Q2_Kaution --> A2_Kaution["Ja — Kautionsleistungen werden übernommen, müssen aber in bestimmten Fällen (Strafe, verfallene Kaution, Überzahlung) an die Allianz zurückgezahlt werden (VB Smart)."]

  P2I --> Q2_Forderungsausfall["Was ist Forderungsausfalldeckung und wann greift sie?"]
  Q2_Forderungsausfall --> A2_Forderungsausfall["Sie ersetzt Schäden, wenn der Verursacher unversichert/zahlungsunfähig ist; Voraussetzung ist eine titulierte Forderung, erfolglose Zwangsvollstreckung bzw. Nachweis Zahlungsunfähigkeit und Abtretung an die Allianz (VB Smart)."]

  P2I --> Q2_Internet["Deckt die Police Haftpflicht durch private Internetnutzung?"]
  Q2_Internet --> A2_Internet["Ja — Haftpflichtansprüche aus privater Internetnutzung/Datenaustausch sind mitversichert (VB Smart)."]

  P2I --> Q2_InternetAus["Welche Internet‑Schäden sind ausgeschlossen?"]
  Q2_InternetAus --> A2_InternetAus["Ausgeschlossen sind bewusstes Eindringen/Hacking, gezielte Angriffe, Einsatz von Schadsoftware und Ansprüche wegen unberechtigtem Herunterladen urheberrechtlich geschützter Inhalte (VB Smart)."]

  P2I --> Q2_Gewaesser["Deckt die Police Gewässerschäden und USchadG-Ansprüche?"]
  Q2_Gewaesser --> A2_Gewaesser["Ja — Gewässerschäden und öffentlich‑rechtliche Ansprüche nach dem Umweltschadensgesetz sind gedeckt, sofern keine andere Versicherung eintritt und keine bewusste Missachtung von Vorschriften vorliegt (VB Smart, USchadG)."]

  P2I --> Q2_Elementar["Sind Elementarschäden (z. B. Überschwemmung) gedeckt?"]
  Q2_Elementar --> A2_Elementar["Schäden durch elementare Naturkräfte sind ausgeschlossen; bei Gewässerschäden sind Elementarschäden generell ausgenommen/ausgeschlossen (VB Smart)."]

  P2I --> Q2_AGG["Sind Ansprüche wegen Diskriminierung nach AGG gedeckt?"]
  Q2_AGG --> A2_AGG["Ja — Ansprüche nach dem AGG im privaten Beschäftigungsbereich sind gedeckt, sofern sie vor einem deutschen Gericht geltend gemacht werden (VB Smart, AGG)."]

  %% === Reorganized key topic: Verlust fremder Schlüssel / Codekarten ===
  P2I --> Q2_SchluesselLoss["Deckt die Police Verlust fremder Schlüssel/Codekarten?"]

  %% Follow-up diagnostic check (reused/reformulated node)
  Q2_SchluesselLoss --> Q2_SchluesselLimit["Trifft eine Einschränkung zu (z. B. Autoschlüssel oder beruflich überlassene Schlüssel), oder war der Schlüssel nicht rechtmäßig in Ihrem Gewahrsam?"]

  %% Yes/No branching for the diagnostic question
  Q2_SchluesselLimit -->|"Ja"| A2_SchluesselLimit
  Q2_SchluesselLimit -->|"Nein"| A2_SchluesselLoss

  %% Additional factual follow-up available after a positive YES outcome
  Q2_SchluesselLimit -->|"Nein"| Q2_SchluesselFrist
  Q2_SchluesselFrist --> A2_SchluesselFrist

  %% Existing answer nodes (preserved texts / citations)
  A2_SchluesselLoss["Ja — erstattet werden Auswechslung/Änderung von Schlössern und Schließanlagen, Ersatzschlüssel, vorübergehende Sicherungsmaßnahmen (bis 14 Tage) und Folgeschäden, sofern die Schlüssel rechtmäßig in Ihrem Gewahrsam waren (VB Smart). Entschädigungsobergrenze je Versicherungsfall: z. B. 50.000 €."] 

  A2_SchluesselLimit["Hinweis zu Begrenzungen: Es gibt Entschädigungsobergrenzen (z. B. 50.000 € je Fall) und bestimmte Schlüsselarten sind ausgeschlossen — insbesondere Autoschlüssel und beruflich überlassene bzw. gewerblich verwaltete Schlüssel (VB Smart)."]

  A2_SchluesselFrist["Vorübergehende Sicherungsmaßnahmen (z. B. Notschloss, Objektschutz) werden für bis zu 14 Tage ab Feststellung des Verlusts übernommen (VB Smart)."]
""",

"""
%% Updated branch: 1.4 Rechte, Pflichten & gegenseitige Ansprüche (neu strukturiert für Chatbot‑Flow)
P1D["1.4 Rechte, Pflichten und gegenseitige Ansprüche"]

  %% Kept informational nodes about Rechte & Pflichten (unverändert inhaltlich; Antworten mit Paragraphenangabe)
  P1D --> R_RechtePflichten["Rechte & Pflichten von Mitversicherten"]
  R_RechtePflichten --> Q1_PflichtenMit["Gelten dieselben Rechte und Pflichten für mitversicherte Personen?"]
  Q1_PflichtenMit --> A1_PflichtenMit["Ja — dieselben Bestimmungen und Obliegenheiten gelten; die Vertragsrechte kann nur der Versicherungsnehmer ausüben (VB Smart, Ziff. 1.4)."]

  R_RechtePflichten --> Q1_TaeglichesLeben["Deckt die Police Gefahren des täglichen Lebens für Mitversicherte?"]
  Q1_TaeglichesLeben --> A1_TaeglichesLeben["Ja — Haftpflichtansprüche Dritter aus dem privaten Alltag sind gedeckt; berufliche/gewerbliche Risiken sind ausgeschlossen (VB Smart, Ziff. 1.4)."]

  %% Neu gestalteter Chatbot‑Hauptpfad: Ansprüche unter Mitversicherten (Hauptfrage → direkte Antwort → Folgeinfo)
  P1D --> R_GegenseitAnspr["Ansprüche zwischen Mitversicherten (Chatbot‑Hauptpfad)"]

  %% MAIN QUESTION (reformuliert aus vorhandenem Knoten)
  R_GegenseitAnspr --> Q1_GeraetUntereinander["Gelten direkte Schadenersatzansprüche von mitversicherten Personen (z. B. Ehepartner:innen, Kinder, Haushaltspersonen) gegen Sie als Ansprüche Dritter — sind sie gedeckt?"]
  Q1_GeraetUntereinander --> A1_GeraetUntereinander["Nein — gegenseitige Schadenersatzansprüche unter Mitversicherten sind in der Regel ausgeschlossen (VB Smart, Ziff. 1.4)."]

  %% FOLLOW‑UP INFORMATION (Ausnahmen, nicht als Yes/No‑Check weil allgemeine Faktfrage)
  A1_GeraetUntereinander --> Q1_AusnahmenUnter["Gibt es Ausnahmen (z. B. Regressansprüche Dritter)?"]
  Q1_AusnahmenUnter --> A1_AusnahmenUnter["Ja — regressartige Ansprüche von Sozialversicherungsträgern, Sozialhilfeträgern, privaten Krankenversicherern sowie öffentlichen/privaten Arbeitgebern wegen Personenschäden können gedeckt sein, sofern kein häusliches Gemeinschaftsverhältnis zwischen Schädiger und Geschädigtem besteht (VB Smart, Ziff. 1.4)."]
""",

"""
%% Reorganized branch: P1C — Kinder, Haushalt, Aufhebung & Tod (chatbot-like follow-up)
%%{ init: { "theme": "default", "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "linear" } } }%%
graph TD
  P1C["1.3 Kinder, Haushalt, Aufhebung & Tod"]

  %% Main FAQ (user's initial question)
  Q1_Kinder_Ausbildung["Sind Kinder während Studium/Ausbildung versichert, auch bei Arbeit?"]
  A1_Kinder_Ausbildung["Ja. Kinder bleiben während Studium/Ausbildung mitversichert — auch bei nebenberuflicher/teilzeitlicher Tätigkeit. Die Mitversicherung endet erst, wenn das Kind erstmals eine auf Dauer angelegte berufliche Tätigkeit aufnimmt und eigenes Einkommen erzielt (VB Smart)."]

  %% Follow‑up diagnostic: Prüfung, ob die Tätigkeit dauerhaft ist (Ja/Nein)
  Q1_BerufDauer["Handelt es sich bei der Tätigkeit Ihres Kindes bereits um eine auf Dauer angelegte berufliche Tätigkeit (also kein Nebenjob)?"]
  F_NoDauer["Kurzfassung — Nebenjob/Studentenjob: Ihr Kind bleibt mitversichert; Mitversicherung endet erst bei erstmaliger dauerhafter Berufstätigkeit mit eigenem Einkommen (VB Smart)."]
  F_YesDauer["Kurzfassung — Dauerhafte Berufstätigkeit: Sobald Ihr Kind erstmals eine auf Dauer angelegte berufliche Tätigkeit beginnt und eigenes Einkommen erzielt, endet die Mitversicherung nach den Bedingungen (VB Smart)."]

  %% Follow‑up factual question from dialogue (Wohnsitz)
  Q1_Kinder_Wohnen["Sind Kinder mitversichert, wenn sie während Studium/Ausbildung nicht in meinem Haushalt wohnen?"]
  A1_Kinder_Wohnen["Ja. Kinder sind auch außerhalb des Haushalts mitversichert bis zum Eintritt dauerhafter Berufstätigkeit; in Pflegeeinrichtungen untergebrachte Kinder sind ebenfalls mitversichert (VB Smart)."]

  %% Connections
  P1C --> Q1_Kinder_Ausbildung
  Q1_Kinder_Ausbildung --> A1_Kinder_Ausbildung

  %% After the factual answer, guide user to the diagnostic check about permanence
  A1_Kinder_Ausbildung --> Q1_BerufDauer
  Q1_BerufDauer -->|"Nein (nur Nebenjob)"| F_NoDauer
  Q1_BerufDauer -->|"Ja (dauerhafte Tätigkeit)"| F_YesDauer

  %% Also offer the separate living-situation follow-up (non-diagnostic factual Q)
  A1_Kinder_Ausbildung --> Q1_Kinder_Wohnen
  Q1_Kinder_Wohnen --> A1_Kinder_Wohnen

  style P1C fill:#fff4e6
  style Q1_Kinder_Ausbildung fill:#ffffff,stroke:#333,stroke-width:1px
  style A1_Kinder_Ausbildung fill:#e8fff0
  style Q1_BerufDauer fill:#fffaf0
  style F_NoDauer fill:#e6f7ff
  style F_YesDauer fill:#ffecec
  style Q1_Kinder_Wohnen fill:#fffaf0
  style A1_Kinder_Wohnen fill:#e8fff0
""",

"""


  %% Updated branch: 2.3 Immobilien, Vermietung & Bauherr
  P2C["2.3 Immobilien, Vermietung & Bauherr"]

  %% Main diagnostic flow for gelegentliche Vermietung einzelner Zimmer / Einliegerwohnung
  P2C --> Q2_VermietZimmer["Sind Vermietung einzelner Zimmer oder Einliegerwohnungen an Privatpersonen gedeckt?"]
  Q2_VermietZimmer --> A2_VermietZimmer["Ja — die Vermietung an Privatpersonen ist mitversichert, einschließlich zugehöriger Garagen (VB Smart)."]

  %% Follow‑up check (diagnostisch): liegt eine selbstgenutzte, inländische Immobilie vor?
  Q2_VermietZimmer -->|"Ist das vermietete Zimmer/Einliegerwohnung Teil Ihrer selbstgenutzten Wohnung bzw. handelt es sich um eine ausschließlich privat genutzte Immobilie im Inland?"| Q2_Hausbesitzer["Gilt Schutz als Haus-/Grundbesitzer:in? (diagnostische Umformulierung)"]

  Q2_Hausbesitzer -->|"Ja"| A2_Hausbesitzer["Ja — für selbstgenutzte Häuser/Wohnungen/ Wochenendhäuser besteht Schutz als Haus-/Grundbesitzer:in; gelegentliche Vermietung an Privatpersonen ist damit gedeckt, auch zugehörige Außenanlagen (VB Smart)."]
  Q2_Hausbesitzer -->|"Nein"| A2_VermietZimmer

  %% Preserve other existing Q/A nodes in this branch (unchanged placement)
  P2C --> Q2_Aussenanlagen["Sind Außenanlagen (Garagen, Gartenhäuser) mitversichert?"]
  Q2_Aussenanlagen --> A2_Aussenanlagen["Ja — Außenanlagen zu den versicherten Immobilien sind mitversichert (VB Smart)."]

  P2C --> Q2_FerienAusland["Gilt Schutz für selbstgenutzte Ferienimmobilie im EU-Ausland?"]
  Q2_FerienAusland --> A2_FerienAusland["Ja — selbstgenutzte Ferienhäuser in EU, Norwegen oder Island sind mitversichert, ebenso zugehörige Außenanlagen (VB Smart)."]

  P2C --> Q2_Mietobjekte["Sind gemietete Ferienobjekte vorübergehend mitversichert?"]
  Q2_Mietobjekte --> A2_Mietobjekte["Vorübergehend gemietete Ferienimmobilien sind mitversichert, sofern die Bedingungen dies vorsehen (VB Smart)."]

  P2C --> Q2_Bauherr["Besteht Schutz als Bauherr:in bei Umbau/Renovierung?"]
  Q2_Bauherr --> A2_Bauherr["Ja, wenn der private Nutzungscharakter erhalten bleibt und kein gewerblicher Ausbau erfolgt (VB Smart)."]
""",

"""
%% Updated branch: 2.3 Immobilien, Vermietung & Bauherr (restructured for chatbot-style follow-up)

  P2C["2.3 Immobilien, Vermietung & Bauherr"]

  %% Main question (user's initial question)
  P2C --> Q2_Bauherr["Gilt Schutz als Bauherr:in bei Umbau/Renovierung? (Q2_Bauherr)"]
  Q2_Bauherr --> A2_Bauherr["Ja — als Bauherr:in sind Sie bei Umbauten und Renovierungen versichert, sofern der private Nutzungscharakter erhalten bleibt und keine Nutzungsänderung zu gewerblichen Zwecken eintritt (Ziffer 2.2.1, VB Smart)."]

  %% Follow-up diagnostic check (yes/no) — reformulated existing Q-node
  Q2_Bauherr --> Q2_Hausbesitzer["Ist die Immobilie ausschließlich privat genutzt und bleibt der Nutzungscharakter erhalten? (Check: Q2_Hausbesitzer)"]
  Q2_Hausbesitzer -->|"Ja"| A2_Hausbesitzer["Kurzfassung (Ja): Deckung greift für selbstgenutzte Wohnimmobilien (inkl. Wochenendhäuser), solange die Nutzung privat bleibt (Ziffer 2.2.1, VB Smart)."]
  Q2_Hausbesitzer -->|"Nein"| A2_Bauherr

  %% Preserve other original Q/A pairs in this branch (unchanged placement)
  P2C --> Q2_Aussenanlagen["Sind Außenanlagen (Garagen, Gartenhäuser) mitversichert?"]
  Q2_Aussenanlagen --> A2_Aussenanlagen["Ja — Außenanlagen zu den versicherten Immobilien sind mitversichert (VB Smart)."]

  P2C --> Q2_VermietZimmer["Sind Vermietung einzelner Zimmer oder Einliegerwohnungen gedeckt?"]
  Q2_VermietZimmer --> A2_VermietZimmer["Ja — die Vermietung an Privatpersonen ist mitversichert, einschließlich zugehöriger Garagen (VB Smart)."]

  P2C --> Q2_FerienAusland["Gilt Schutz für selbstgenutzte Ferienimmobilie im EU-Ausland?"]
  Q2_FerienAusland --> A2_FerienAusland["Ja — selbstgenutzte Ferienhäuser in EU, Norwegen oder Island sind mitversichert, ebenso zugehörige Außenanlagen (VB Smart)."]

  P2C --> Q2_Mietobjekte["Sind gemietete Ferienobjekte vorübergehend mitversichert?"]
  Q2_Mietobjekte --> A2_Mietobjekte["Vorübergehend gemietete Ferienimmobilien sind mitversichert, sofern die Bedingungen dies vorsehen (VB Smart)."]

  %% Note: A2_Bauherr and A2_Hausbesitzer both cite Ziffer 2.2.1 VB Smart (as required)
""",

"""
  P2H["2.8 Praktika, Tagesbetreuung & Ehrenamt"]

  %% Reorganized chatbot-like flow for Praktika/Schnupperlehren
  P2H --> Q2_Praktika["Sind Praktika/Schnupperlehren mitversichert?"]
  Q2_Praktika --> A2_Praktika["Ja — Haftpflichtansprüche aus Praktika/fachpraktischem Unterricht und Schnupperlehren sind subsidiär mitversichert; auch betriebliche Ansprüche (z. B. wegen Beschädigung von Lehrgeräten) können gedeckt sein. Voraussetzung: es besteht kein anderer Versicherungsschutz und es liegt kein Rückgriffs-/Anspruchsverzicht oder Freistellung zugunsten der versicherten Person vor. Schäden an den von der Praktikantin/dem Praktikanten bearbeiteten Sachen sind ausgeschlossen. (Ziffer 2.2.5, VB Smart)"]

  Q2_Praktika --> Q2_Praktika_Einschr["Welche Einschränkungen gelten für die Praktika‑Deckung?"]
  Q2_Praktika_Einschr --> A2_Praktika_Einschr["Einschränkungen: Der Schutz ist subsidiär (tritt nur ein, wenn kein anderer Schutz besteht); entfällt bei vertraglichem Rückgriffs‑/Anspruchsverzicht oder Freistellung zugunsten der versicherten Person; Schäden an bearbeiteten/überlassenen Sachen sind nicht versichert. (Ziffer 2.2.5, VB Smart)"]

  %% Unrelated P2H-Elemente left in place
  P2H --> Q2_Tageseltern["Sind Tageseltern/Babysitter gedeckt?"]
  Q2_Tageseltern --> A2_Tageseltern["Ja — Beaufsichtigung minderjähriger Kinder ist gedeckt; Schäden durch Abhandenkommen von Sachen/Geld der Kinder und Tätigkeiten in Institutionen sind ausgeschlossen (VB Smart)."]

  P2H --> Q2_EhrenamtSubs["Ist ehrenamtliche Tätigkeit versichert und subsidiär?"]
  Q2_EhrenamtSubs --> A2_EhrenamtSubs["Ja — ehrenamtliche Tätigkeiten sind gedeckt, sofern sie nicht hoheitlich/verantwortlich sind; subsidiär zu Vereins-/Träger‑Versicherungen (VB Smart)."]
""",

"""

  %% Updated branch: 1.2 Sonstige mitversicherte Personen (Ehrenamt — Chatbot‑Struktur)

  P1B["1.2 Sonstige mitversicherte Personen — Ehrenamt (neu strukturiert)"]

  %% Unveränderte (erhaltene) Unterknoten in der Sektion
  P1B --> S_AuPair["Au-pairs, Austauschschüler, Haushaltspersonal"]
  S_AuPair --> Q1_AuPair["Sind Au‑pairs/Austauschschüler mitversichert?"]
  Q1_AuPair --> A1_AuPair["Ja, bis zu einem Jahr im Haushalt eingegliederte Personen sind subsidiär mitversichert (VB Smart)."]

  P1B --> S_Haushaltsp["Angestellte Haushaltspersonen"]
  S_Haushaltsp --> Q1_Haushaltsp["Sind angestellte Haushaltspersonen bei Tätigkeiten mitversichert?"]
  Q1_Haushaltsp --> A1_Haushaltsp["Ja während der Ausübung ihrer Tätigkeit; Arbeitsunfälle/Berufskrankheiten nach SGB VII sind ausgeschlossen (VB Smart, SGB VII)."]

  %% Reorganisierte Ehrenamts‑Dialog (chatbot‑like)
  P1B --> S_NotfallEhrenamt["Ehrenamtliche Tätigkeiten (z. B. Trainer/Betreuer, Vereinsveranstaltungen)"]

  %% MAIN DIAGNOSTIC QUESTION (reused node Q1_EhrenamtEinschr, im Sinne eines Chat‑Checks)
  S_NotfallEhrenamt --> Q1_EhrenamtEinschr["Handeln Sie in Ihrem Ehrenamt in einer verantwortlichen Stellung (z. B. Vorstand) oder üben Sie ein öffentlich‑hoheitliches Ehrenamt aus?"]

  %% Branch: Nutzer nicht in verantwortlicher/hoheitlicher Position → Deckung & Subsidiarität
  Q1_EhrenamtEinschr -->|"Nein"| A1_EhrenamtEinschr["Ja — ehrenamtliche Tätigkeiten in nicht‑verantwortlicher Funktion (z. B. Trainer, Betreuer) sind gedeckt; der Schutz gilt subsidiär gegenüber Vereins-/Träger‑Versicherungen. Ausgeschlossen sind hoheitliche oder leitende/ verantwortliche Ehrenämter (VB Smart, Ziff. 2.2.7)."]

  %% Branch: Nutzer in verantwortlicher/hoheitlicher Position → eingeschränkter/kein Schutz
  Q1_EhrenamtEinschr -->|"Ja"| A1_Notfall["Berufliche bzw. hoheitliche Einsätze (z. B. hauptamtliche Feuerwehr/ASB) sind ausgeschlossen; für spontane private Notfallhilfe kann gesondert geregelt Schutz bestehen (VB Smart)."]

  %% Spezifische FAQ (erhalten)
  S_NotfallEhrenamt --> Q1_Notfall["Sind Rettungs- oder Feuerwehr‑Profis mitversichert, wenn sie helfen?"]
  Q1_Notfall --> A1_Notfall

  %% Hinweis: Keine anderen Knoten entfernt/dupliziert — vorhandene Q/A‑Knoten aus dieser Sektion bleiben erhalten.
""",

"""
  %% Updated branch: P1B (1.2 Sonstige mitversicherte Personen)
  P1B["1.2 Sonstige mitversicherte Personen"]

  %% Unchanged subtree: Au-pairs & Haushaltspersonal (kept as in original)
  P1B --> S_AuPair["Au-pairs, Austauschschüler, Haushaltspersonal"]
  S_AuPair --> Q1_AuPair["Sind Au‑pairs/Austauschschüler mitversichert?"]
  Q1_AuPair --> A1_AuPair["Ja, bis zu einem Jahr im Haushalt eingegliederte Personen sind subsidiär mitversichert (VB Smart)."]
  S_AuPair --> Q1_Haushaltsp["Sind angestellte Haushaltspersonen bei Tätigkeiten mitversichert?"]
  Q1_Haushaltsp --> A1_Haushaltsp["Ja während der Ausübung ihrer Tätigkeit; Arbeitsunfälle/Berufskrankheiten nach SGB VII sind ausgeschlossen (VB Smart, SGB VII)."]

  %% Reorganized subtree: Notfallhelfer & Ehrenamtliche — chatbot-like flow
  P1B --> S_NotfallEhrenamt["Notfallhelfer & Ehrenamtliche (Abgrenzung)"]

  %% MAIN QUESTION
  S_NotfallEhrenamt --> Q1_EhrenamtEinschr["Welche Einschränkungen gelten für ehrenamtliche Tätigkeiten?"]
  Q1_EhrenamtEinschr --> A1_EhrenamtEinschr["Ehrenamt ist gedeckt, wenn es privates, nicht-hoheitliches, nicht-verantwortliches Engagement ist; subsidiär gegenüber Vereins-/Träger‑Versicherungen. Kein Schutz, wenn die Vereins-/Träger‑Haftpflicht eintrittspflichtig ist, bei Rückgriffs-/Anspruchsverzicht oder bei verantwortlicher Tätigkeit (z. B. Vorstandsamt) (VB Smart)."]

  %% FOLLOW-UP CHECK (diagnostic; use existing question node)
  Q1_EhrenamtEinschr --> Q1_Notfall["Sind Rettungs- oder Feuerwehr‑Profis mitversichert, wenn sie helfen?"]
  %% YES path: professional/hoheitliche helpers
  Q1_Notfall -->|"Ja"| A1_Notfall["Notfallhelfer:innen, die spontan helfen, sind mitversichert; berufliche/hoheitliche Helfer wie Feuerwehr/ASB sind hingegen ausgeschlossen (VB Smart)."]
  Q1_Notfall -->|"Ja"| A_SUM_YES["Zusammenfassung (Ja): Bei beruflich/hoheitlich tätigen Helfern (z. B. Feuerwehr/ASB) besteht in der Regel kein Schutz in der Privat‑Haftpflicht; spontane private Hilfeleistende sind dagegen gedeckt (VB Smart)."]

  %% NO path: private volunteer (falls unter die Hauptantwort fällt)
  Q1_Notfall -->|"Nein"| A1_EhrenamtEinschr
  Q1_Notfall -->|"Nein"| A_SUM_NO["Zusammenfassung (Nein): Bei privaten Ehrenämtern in Vereinen (z. B. Trainer) gilt Versicherungsschutz, sofern keine verantwortliche/hoheitliche Stellung vorliegt und keine andere Haftpflicht eintritt. Schutz ist subsidiär gegenüber Vereins-/Träger‑Versicherungen (VB Smart)."]
""",

"""
%% Reorganized branch: Ferienimmobilie (EU) — chatbot-style follow-up

  %% Main diagnostic question (reused/reformulated node)
  Q2_FerienAusland["Gilt mein Versicherungsschutz auch für eine selbstgenutzte Ferienimmobilie im EU‑Ausland?"]

  %% Follow-up YES/NO answers (reused answer nodes, text conversationally reformulated + citation)
  A2_FerienAusland["Ja — als Eigentümer:in einer ausschließlich privat genutzten Ferienimmobilie in einem EU‑Staat (z. B. Spanien) sind Sie mitversichert; mitversichert sind auch zugehörige Außenanlagen. (Ziffer 2.2.1, VB Smart)"]
  A2_Mietobjekte["Nicht automatisch — wird die Immobilie nicht ausschließlich privat genutzt, gelten abweichende Regeln; vorübergehend gemietete Ferienobjekte können unter Voraussetzungen mitversichert sein. Prüfen Sie die Bedingungen in den VB Smart. (Ziffer 2.2.1, VB Smart)"]

  %% Follow-up general informational question about Eigentümer‑Schutz (reused)
  Q2_Hausbesitzer["Deckt die Police mich auch als Haus‑ bzw. Grundeigentümer der Ferienimmobilie?"]
  A2_Hausbesitzer["Ja — der Haftpflichtschutz erstreckt sich auf Sie als Eigentümer:in der selbstgenutzten Ferienimmobilie; beachten Sie mögliche Größen‑/Nutzungsgrenzen und Ausnahmen in den Bedingungen. (Ziffer 2.2.1, VB Smart)"]

  %% Edges with explicit diagnostic branching
  Q2_FerienAusland -->|"Ja — ausschließlich privat genutzt"| A2_FerienAusland
  Q2_FerienAusland -->|"Nein — nicht ausschließlich privat / vermietet"| A2_Mietobjekte

  %% After a Yes, offer the additional factual clarification about Eigentümer‑Schutz
  A2_FerienAusland --> Q2_Hausbesitzer
  Q2_Hausbesitzer --> A2_Hausbesitzer
""",

"""
%%{ init: { "theme": "default", "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "linear" } } }%%


%% Reorganized branch: 2.4 Energieanlagen (chat-like follow-up)
  P2D["2.4 Energieanlagen (Photovoltaik, Geothermie, Wallbox) — Reorganisiert"]

  %% Main question -> direct answer
  P2D --> Q2_Energie_Selbstschaden["Sind Schäden an den Anlagen selbst versichert?"]
  Q2_Energie_Selbstschaden --> A2_Energie_Selbstschaden["Nein — Schäden an den Anlagen selbst sind ausdrücklich ausgeschlossen. (Ziffer 2.2.1, VB Smart)"]

  %% Follow-up informational points (not user-dependent checks)
  A2_Energie_Selbstschaden --> Q2_Energie_Was["Welche Energieanlagen sind grundsätzlich im Tarif berücksichtigt?"]
  Q2_Energie_Was --> A2_Energie_Was["Privat betriebene Photovoltaik (auch Balkonkraftwerke), Geothermie und Wallboxen sind hinsichtlich betrieblicher Haftpflicht (Haftpflicht gegenüber Dritten) geregelt. (Ziffer 2.2, VB Smart)"]

  A2_Energie_Selbstschaden --> Q2_Energie_Einschr["Welche Einschränkungen gelten speziell für diese Anlagen?"]
  Q2_Energie_Einschr --> A2_Energie_Einschr["Kein Schutz für Schäden, die beim Errichten/Installieren der Anlagen entstehen; ferner sind vertragliche Ansprüche von Netzbetreibern ausgeschlossen. (Ziffer 2.2, VB Smart)"]

  A2_Energie_Selbstschaden --> Q2_Energie_Limit["Gibt es eine finanzielle Obergrenze für Schäden an diesen Anlagen?"]
  Q2_Energie_Limit --> A2_Energie_Limit["Da Schäden an den Anlagen selbst ausgeschlossen sind, nennt der Vertrag keine Entschädigungsobergrenze für solche Schäden. (Ziffer 2.2.1, VB Smart)"]
""",

"""

  %% Updated branch: 2.7 Tiere & Hüten (konversational, diagnostic Reihenfolge)

  P2G["2.7 Tiere & Hüten"]

  %% Main question (user-initiated)
  P2G --> Q2_Tier_HundePferd["Q: Deckt die Police die Haftpflicht für Hunde oder die Pferdehalterhaftpflicht?"]

  %% DIRECT ANSWER (allgemein)
  Q2_Tier_HundePferd --> A2_Tier_HundePferd["A: Nein — Haftpflicht für Hunde (außer ausgebildete Assistenzhunde) und Pferde als Halter ist ausgeschlossen; hierfür ist eine separate Tierhalter‑Haftpflicht erforderlich. (VB Smart)"]

  %% FOLLOW-UP CHECK (diagnostisch): Reiten/Hüten fremder Tiere gelegentlich?
  Q2_Tier_HundePferd --> Q2_Tier_Gelegenheits["Q: Reiten oder Hüten fremder Tiere nur gelegentlich und nicht gewerblich?"]

  %% If YES: occasional non‑commercial hueten/reiten — show coverage and follow-up about Halteransprüche
  Q2_Tier_Gelegenheits -->|"Ja"| A2_Tier_Gelegenheits["A: Ja — gelegentliches, nicht gewerbliches Hüten fremder Hunde bzw. Reiten/hüten fremder Pferde ist gedeckt; der Schutz ist subsidiär gegenüber etwaigen anderen Versicherungen. (VB Smart)"]
  A2_Tier_Gelegenheits --> Q2_Tier_HalterAnspr

  %% Follow-up informational question (not a diagnostic) about Halter‑Ansprüche beim Hüten
  Q2_Tier_HalterAnspr["Q: Sind Ansprüche des Tierhalters wegen Verletzung/Abhandenkommens/Tod des Tieres beim Hüten mitversichert?"] --> A2_Tier_HalterAnspr["A: Ja — Ansprüche des Halters wegen Verletzung, Abhandenkommens oder Tod des gehüteten Tieres sind mitversichert; es können Entschädigungsbegrenzungen gelten (z. B. je Fall). (VB Smart)"]

  %% If NO: no occasional hueten/reiten — fall back to the direct (No) outcome
  Q2_Tier_Gelegenheits -->|"Nein"| A2_Tier_HundePferd

  %% Unrelated/other Qs in this branch remain (Platzhalter, unverändert)
  P2G --> Q2_Tier_Kleine["Q: Welche Kleintiere sind gedeckt (z. B. Katzen, Kaninchen)?"]
  Q2_Tier_Kleine --> A2_Tier_Kleine["A: Kleine Haustiere, erlaubte exotische Kleintiere, Bienen und privat gehaltene Weidetiere sind mitversichert. (VB Smart)"]
""",

"""
%% Updated branch: 4 • Schadenfall: Ablauf, Leistungen & Entschädigung

  %% Root of affected branch
  P4["4 • Schadenfall: Ablauf, Leistungen & Entschädigung"]

  %% Main question + direct answer
  P4 --> Q4_WasTun["Was macht die Allianz, nachdem ich einen Versicherungsfall gemeldet habe?"]
  Q4_WasTun --> A4_WasTun["Die Allianz prüft, ob Ansprüche gegen Sie berechtigt sind; berechtigte Ansprüche ersetzt sie (Reparatur oder Zeitwert), unberechtigte Ansprüche wehrt sie ab. (VB Smart, Schadenteil)"]

  %% Follow-up CHECK: Ist bereits ein Mahn-/Gerichtsverfahren anhängig?
  A4_WasTun --> Q5_Mahnbescheid["Ist gegen Sie bereits ein Mahn‑/Gerichtsverfahren oder ein Mahnbescheid anhängig?"]
  Q5_Mahnbescheid -->|"Ja"| A5_Mahnbescheid["Bei Mahnbescheid/gerichtlichem Verfahren: legen Sie fristgerecht Rechtsbehelfe ein, informieren Sie unverzüglich die Allianz und überlassen Sie der Allianz (bzw. dem beauftragten Anwalt) die Prozessführung; erteilen Sie Vollmachten und die erforderlichen Unterlagen. (VB Smart, Ziff.5)"]
  Q5_Mahnbescheid -->|"Nein"| Q5_AnzeigePflicht["OK — haben Sie den Schaden bereits unverzüglich gemeldet und alle relevanten Umstände/Unterlagen übermittelt?"]

  %% If NO → show Mitwirkungspflichten (was zu tun ist)
  Q5_AnzeigePflicht --> A5_AnzeigePflicht["Melden Sie jeden Versicherungsfall unverzüglich; erteilen Sie wahrheitsgemäße Auskünfte, ermöglichen Untersuchungen, senden Sie angeforderte Unterlagen, mindern und vermeiden Sie weiteren Schaden und befolgen Sie zumutbare Weisungen der Allianz. (VB Smart, Ziff.5)"]

  %% Zusatzinfo: Prozessführung & Abwehr (allgemeine Informationen, nicht als Ja/Nein-Check)
  A4_WasTun --> Q4_Abwehr["Wie wehrt die Allianz unberechtigte Ansprüche ab?"]
  Q4_Abwehr --> A4_Abwehr["Die Allianz führt auf ihre Kosten die Abwehr und Prozessführung in Ihrem Namen und wehrt unberechtigte Ansprüche ab. Prozesskosten werden nicht auf die Versicherungssumme angerechnet. (VB Smart, Schadenteil)"]

  A5_Mahnbescheid --> Q4_ProzessWer["Wer führt das Prozessverfahren und wer trägt die Kosten?"]
  Q4_ProzessWer --> A4_ProzessWer["Die Allianz ist zur Prozessführung bevollmächtigt, führt das Verfahren in Ihrem Namen und trägt die Kosten; diese Kosten werden nicht auf die Versicherungssumme angerechnet. (VB Smart, Schadenteil)"]

  %% Weitere Pflichten / Details zur Schadenminderung und Weisungen (nach Meldung)
  A5_AnzeigePflicht --> Q5_Schadenmin["Welche Schadenminderungs‑Pflichten habe ich konkret?"]
  Q5_Schadenmin --> A5_Schadenmin["Sie müssen nach Möglichkeit den Schaden abwenden oder mindern (z. B. Wasser abdrehen). Angemessene Aufwendungen zur Schadenminderung werden unter Umständen ersetzt, insbesondere wenn sie nachweislich geboten oder auf Weisung der Allianz erfolgten. (VB Smart, Ziff.5)"]

  A5_AnzeigePflicht --> Q5_Weisungen["Muss ich Weisungen der Allianz befolgen?"]
  Q5_Weisungen --> A5_Weisungen["Ja — zumutbare Weisungen sind zu befolgen; bei mehreren Versicherern ist pflichtgemäßes Ermessen zu üben. Nichtbefolgung kann zu Leistungskürzungen führen. (VB Smart, Ziff.5)"]

  %% Navigation hint within this branch
  P4 --> NOTE_P4["Hinweis: Bei laufendem Verfahren → lesen Sie insbesondere die Regelungen zur Prozessführung und Ihre Mitwirkungspflichten (VB Smart, Schadenteil / Ziff.5)."]
"""
]

#for d in dialogues_pha:
#    multi = "\n".join([f"{t['role']}: {t['text']}" for t in d["turns"]])
#    ext = merge_flow_multi(flow, multi, document)

    # Extract only the inner Mermaid content
    #inner = _extract_mermaid_block(ext)

    # Build a clean fenced block
    #block = f'"""\n{inner}\n"""'

    # Store for later merging
    #extensions_pha.append(block)

    # Print immediately
    #print(block)
    #print() # blank line for readability
# ---------- PREPARE EXTENSIONS ----------



def strip_fences(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"^```(?:mermaid)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text, flags=re.I)
    return text.strip()


def extract_mermaid(text: str) -> str:
    if not text:
        return ""
    m = re.search(r"```mermaid\s*(.+?)\s*```", text, flags=re.S | re.I)
    return m.group(1).strip() if m else strip_fences(text)


# ------------------------------------------------------------
# Core: ein einzelner Merge-Vorgang
# ------------------------------------------------------------

def merge_once(flow: str, ext: str, client, model="gpt-5-mini") -> str:
    base = strip_fences(flow)
    add = strip_fences(ext)

    if not add:
        return base

    prompt = f"""

You receive two MERMAID graph fragments:

BASE FLOW:
{base}

EXTENSION:
{add}

YOUR JOB:
You do NOT edit, rewrite, reorganize, or clean up ANYTHING in either fragment.

You perform exactly ONE mechanical action:

1. Read the EXTENSION.
2. Detect the FIRST node identifier in the EXTENSION. 
   It is always the first text before the first "[".
   Example: BAS_DEF["..."] → the node identifier is BAS_DEF.
3. Find the FIRST occurrence of a line in the BASE FLOW that starts with exactly that node identifier.
4. Immediately AFTER that line, paste the EXTENSION AS-IS.
   - Keep all indentation as-is.
   - Keep all punctuation as-is.
   - Do NOT expand, compress, rewrite, deduplicate, or “merge”.
   - Do NOT repair or “improve” syntax.
   - Do NOT move other nodes.
   - Do NOT remove anything.
   - This is a literal string insertion task.

The BASE FLOW must remain byte-for-byte unchanged except for inserting the EXTENSION at the correct point.

OUTPUT FORMAT:
Return exactly one fenced code block:
```mermaid
<the updated graph>

    """

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"[merge_once] API call {len(add)} chars → {time.perf_counter() - start:.2f}s")

    result = extract_mermaid(response.choices[0].message.content)
    return result


# ------------------------------------------------------------
# Merge aller Extensions
# ------------------------------------------------------------

def merge_all(flow: str, extensions: List[str], client, out_path: Path) -> str:
    merged = strip_fences(flow)

    print(f"→ Total extensions: {len(extensions_pha)}\n")

    # Ensure the merge_steps folder exists
    steps_folder = Path("merge_steps")
    steps_folder.mkdir(parents=True, exist_ok=True)

    for idx, ext in enumerate(extensions, 1):
        print(f"=== Merging {idx}/{len(extensions_pha)} ===")
        merged = merge_once(merged, ext, client)

        # Save current step as Markdown
        step_path = steps_folder / f"step_{idx}.md"
        step_path.write_text(f"```mermaid\n{merged}\n```", encoding="utf-8")

        # Update the main Markdown file incrementally
        out_path.write_text(f"```mermaid\n{merged}\n```", encoding="utf-8")

    print(f"\n→ Saved final graph to {out_path}")
    return f"```mermaid\n{merged}\n```"


# ------------------------------------------------------------
# Beispiel-Hauptprogramm
# ------------------------------------------------------------

if __name__ == "__main__":

    extensions = [extract_mermaid(e) for e in extensions_pha if e.strip()]

    final = merge_all(flow, extensions, client, OUT_PATH)
    print(final)