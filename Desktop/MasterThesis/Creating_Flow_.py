from openai import OpenAI

OPENAI_API_KEY ="#"
client = OpenAI(api_key=OPENAI_API_KEY)

models = client.models.list()
for m in models.data:
    print(m.id)

import json

# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_SMART.txt", "r", encoding="utf-8") as f:
    document = f.read()

#task_description = """planning a business trip, and you don't know anything about the procedures nor the requirements or regulations.
#Come up with a list of all possible questions (in German only) you might have to consider for
#a) booking a trip   
#b) reimbursing a trip

#Consider common cases as well as exploring exceptions or fringe cases."""

task_description = """You are an Allianz customer and have a private liability insurance policy in the Smart tariff. You know nothing about the conditions, the covered risks, or the procedures in the event of a claim.
Create a list of all possible questions (in German only) that you might ask yourself regarding:
a) the conditions and benefits of the liability insurance (e.g., who is insured, what is covered, what is excluded, special cases, exceptions)
b) the process and requirements in the event of a claim or reimbursement (e.g., reporting, documentation, obligations, possible rejections)
Take into account common everyday situations as well as special and exceptional cases."""


def create_questions (document, task_description):
    prompt = f"""
You are {task_description}

Consider common cases as well as exploring exceptions or fringe cases.

Only ask questions that can be answered by the following document:
{document}

Return a JSON object with the structure:
{{
    "questions": [
        "Frage 1",
        "Frage 2",
        ...
    ]
}}
"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()



def structure (questions, document):
    prompt = f"""
Given is the list of user questions:
{questions}

about the document:
{document}

Group the questions by topics/categories.
Build a nested hierarchy (tree) of topics that becomes more concrete at each level, until a question is reached.
The hierarchy must:
Always start with a single root topic (what do you have questions about?).
At each level, divide into at least two sub-topics (never a flat list of many siblings at once).
Continue nesting until reaching the level of concrete questions.
If a question fits into multiple categories, you may duplicate it under each.
Do not leave all categories at the same level (no flat structures). Each step should go from general → more specific → questions.

For example, start with a high-level division into "Ernährung" and "Bewegung" topics,
and then into more specific topics such as Lebensmittel or Sportarten (could be sub-topic "Training"),
which then divides into type of food or activity (sub-sub topic "Gemüse", "Fleisch", "Yoga", "Krafttraining", ...), etc.
"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()



if __name__ == "__main__":
    print("Printing Improved Graph")
    questions = create_questions(document, task_description)
    print(questions)
    structure_result = structure (questions, document)
    print(structure_result)

"""
hierarchy = 
1) Rechtsrahmen & Grundbegriffe
 - 1.1 Geltungsbereich – wer ist erfasst
   - a) Gelten die Regelungen des Landesreisekostengesetzes für Auslandsdienstreisen entsprechend und gibt es abweichende Bestimmungen für Tage- und Übernachtungsgeld im Ausland? (a)  
   - a) Nach welchen Vorschriften werden Auslandstagegelder und Auslandsübernachtungsgelder gewährt (Hinweis auf ARV und ARVVwV)? (a)
 - 1.2 Unterschied: Dienstreise vs. Dienstgang (Wer braucht Anordnung/Genehmigung?)
   - a) Benötige ich für die Dienstreise eine Anordnung oder Genehmigung der zuständigen Dienstvorgesetzten? (a)  
   - a) Muss die Anordnung oder Genehmigung schriftlich oder elektronisch erfolgen? (a)  
   - a) Gibt es Fälle, in denen für Dienstreisen keine Anordnung oder Genehmigung erforderlich ist (z. B. Richterinnen und Richter)? (a)
   - a) Dienstgänge: Besteht für Dienstgänge Anspruch auf Tagegeld und was gilt bei Dienstgängen von mehr als acht Stunden Dauer? (a)

2) Anordnung, Ausgangs-/Endpunkt, Wohnortregelung
 - 2.1 Festlegung des Ausgangs-/Endpunkts
   - a) Gehört die Festlegung des Ausgangs- oder Endpunkts der Dienstreise zu meinen Aufgaben oder kann die Dienststelle die Dienststätte als Ausgangs- oder Endpunkt anordnen? (a)
   - a) Bei einer Dienstreise, die an der Wohnung angetreten oder beendet wird: Nach welcher Entfernung wird die Fahrtkostenerstattung oder Wegstreckenentschädigung bemessen? (a)
 - 2.2 Mehrere Wohnungen / maßgebliche Wohnung
   - a) Welche meiner ggf. mehreren Wohnungen ist maßgeblich für die Bemessung (welche Wohnung gilt)? (a)

3) Wirtschaftlichkeits- und Klimaschutzgrundsätze bei Verkehrsmittelauswahl
 - 3.1 Wirtschaftlichkeitsprinzip
   - a) Dürfen Dienstreisen nur durchgeführt werden, wenn keine kostengünstigere Art der Erledigung des Dienstgeschäfts möglich und sinnvoll ist? (a)
   - a) Werden Fahrtkosten erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann? (a)
 - 3.2 Wahl des Beförderungsmittels und Klimaschutzaspekte
   - a) Bin ich bei der Wahl des Beförderungsmittels grundsätzlich frei und welche zusätzlichen Gesichtspunkte (z. B. Klimaschutz) muss ich beachten? (a)

4) Fahrt- und Flugkosten (§4) — Erstattung, Klassen, Ausnahmen, Sonderfälle
 - 4.1 Regel, niedrigste Beförderungsklasse
   - a) Welche Beförderungsklasse wird bei regelmäßig verkehrenden Beförderungsmitteln erstattet (niedrigste Klasse)? (a)
 - 4.2 Ausnahmen von der Niedrigstklasse
   - a) Unter welchen Voraussetzungen kann eine Ausnahme von der Erstattung nur der niedrigsten Beförderungsklasse zugelassen werden? (a)
   - a) Sind Flugkosten grundsätzlich erstattungsfähig und unter welchen Bedingungen (dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen)? (a)
   - a) In welcher Flugklasse werden Flugkosten grundsätzlich erstattet? (a)
 - 4.3 Behinderung / gesundheitliche Gründe für höhere Klasse
   - a) Habe ich als Dienstreisende/r mit einem Grad der Behinderung von mindestens 50 Anspruch auf Erstattung der nächsthöheren Beförderungsklasse? (a)
   - a) Können auch andere gesundheitliche oder körperliche Gründe eine Erstattung der nächsthöheren Klasse rechtfertigen? (a)
 - 4.4 Klimaschutz-Ausgleich und Verwaltungspflichten
   - a) Werden die Kosten für Klimaschutz-Ausgleichszahlungen bei der Wirtschaftlichkeitsberechnung für Flugreisen berücksichtigt? (a)
   - a) Gibt es Verpflichtungen der obersten Dienstbehörde zu jährlichen Klimaausgleichszahlungen für bestimmte Personengruppen (z. B. Landesregierung, Landesministerien, staatliche Hochschulen)? (a)
 - 4.5 Mietwagen, Taxi, Carsharing — triftiger Grund und Kürzung
   - a) Wird bei Nutzung eines Mietwagens, Taxis oder Carsharing-Modells meine Fahrt erstattet und unter welchen Voraussetzungen (triftiger Grund)? (a)
   - a) Darf bei fehlendem triftigem Grund für Mietwagen/Taxi/Carsharing eine höhere Vergütung als bei Benutzung eines öffentlichen Verkehrsmittels gewährt werden? (a)
   - a) Wird bei Nutzung von Carsharing die Mitgliedsgebühr wegen eventueller privater Nutzung gekürzt? (a)

5) Wegstreckenentschädigung (private Fahrzeuge, Fahrrad) (§5)
 - 5.1 Private Kraftfahrzeuge — Grundsatz und Sätze
   - a) Wie hoch ist die Wegstreckenentschädigung pro Kilometer bei Nutzung eines privaten Kraftfahrzeugs? (a)
 - 5.2 Erhöhter Satz bei erheblichem dienstlichem Interesse
   - a) Unter welchen Voraussetzungen beträgt die Wegstreckenentschädigung 35 Cent statt 30 Cent pro Kilometer? (a)
 - 5.3 Zuschlag für schlechte Fahrwege
   - a) Kann ein Zuschlag zur Wegstreckenentschädigung gewährt werden, wenn regelmäßig Fahrten auf unbefestigten oder schwer befahrbaren Wegen erforderlich sind, und wie hoch ist dieser Zuschlag? (a)
 - 5.4 Fahrrad, E‑Bike, Pedelec
   - a) Wie hoch ist die Wegstreckenentschädigung pro Kilometer bei Nutzung von Fahrrad, E-Bike oder Pedelec? (a)

6) Tagegeld (Verpflegungspauschale) (§6)
 - 6.1 Höhe und Staffelung
   - a) Wie hoch ist das Tagegeld für jeden vollen Kalendertag einer Dienstreise? (a)
   - a) Wie viel Tagegeld gibt es am Tag des Antritts bzw. der Beendigung einer mehrtägigen Dienstreise bei Reisedauer von mehr als 8 bzw. mehr als 14 Stunden? (a)
 - 6.2 Bestimmung der Reisedauer / Abreise- und Ankunftszeitpunkte
   - a) Nach welchen Zeitpunkten (Abreise/Ankunft an Wohnung oder Dienststätte) wird die Dauer der Dienstreise bestimmt? (a)
 - 6.3 Dienstgänge vs. Dienstreisen
   - a) Besteht für Dienstgänge Anspruch auf Tagegeld und was gilt bei Dienstgängen von mehr als acht Stunden Dauer? (a)
 - 6.4 Kürzungen bei unentgeltlicher Verpflegung
   - a) Werden mir bei unentgeltlicher Verpflegung durch Amt oder Dritte Teile des Tagegeldes abgezogen und in welcher Höhe für Frühstück, Mittag- und Abendessen? (a)

7) Übernachtungsgeld (Unterkunftspauschale) (§7)
 - 7.1 Pauschbeträge und Erstattung höherer Kosten
   - a) Wie hoch ist das pauschale Übernachtungsgeld im Inland und im Ausland? (a)
   - a) Unter welchen Umständen werden höhere Übernachtungskosten im notwendigen Umfang erstattet und wer legt per Verwaltungsvorschrift die Höchstbeträge fest? (a)
 - 7.2 Fälle ohne Anspruch auf Übernachtungsgeld
   - a) In welchen Fällen wird Übernachtungsgeld nicht gewährt (z. B. bei Benutzung von Beförderungsmitteln, Aufenthalt in eigener Wohnung, unentgeltlicher Bereitstellung)? (a)
 - 7.3 Unterkunft bereits in anderen Kosten enthalten / zusätzliche notwendige Übernachtung
   - a) Wird Übernachtungsgeld gewährt, wenn das Entgelt für Unterkunft bereits in erstattungsfähigen Fahrtkosten oder sonstigen Kosten enthalten ist? (a)
   - a) Wann rechtfertigt eine zusätzliche Übernachtung trotz bereits enthaltenem Unterkunftsentgelt eine gesonderte Erstattung (z. B. zu früher Ankunft oder zu später Abfahrt)? (a)

8) Längerer Aufenthalt am Geschäftsort & Abschläge (§8, §12 Abs.6)
 - 8.1 Regelung bei längerem Aufenthalt im Inland (§8)
   - a) Ab welchem Tag gelten bei längerem Aufenthalt am selben auswärtigen Geschäftsort besondere Vergütungen (Regelung nach § 8) und wie wird ab dem achten Tag vergütet? (a)
 - 8.2 Langzeit-Auslandsaufenthalt — Ermäßigung und Erstattung ab Tag 15
   - a) Dauert der Aufenthalt im Ausland länger als 14 Tage: Wann wird das Auslandstagegeld ab dem 15. Tag um 25 Prozent ermäßigt und wer kann in begründeten Fällen davon absehen? (a)
   - a) Ab dem 15. Tag eines längeren Auslandsaufenthalts: Werden anstelle des pauschalen Übernachtungsgeldes die nachgewiesenen notwendigen Übernachtungskosten erstattet? (a)

9) Aufwands- und Pauschvergütung (§9) sowie Nebenkosten (§10)
 - 9.1 Aufwandsvergütung bei erfahrungsgemäß geringeren Kosten
   - a) Können Dienstreisende, die erfahrungsgemäß geringere Aufwendungen haben, anstelle von Tagegeld, Übernachtungsgeld und Auslagenerstattung eine Aufwandsvergütung erhalten? (a)
 - 9.2 Pauschvergütung bei regelmäßigen oder gleichartigen Reisen
   - a) Kann die oberste Dienstbehörde bei regelmäßigen oder gleichartigen Dienstreisen eine Pauschvergütung anstelle der Reisekostenvergütung oder einzelner Bestandteile gewähren? (a)
 - 9.3 Sonstige notwendige Auslagen / Nebenkosten
   - a) Werden sonstige zur Erledigung des Dienstgeschäfts notwendige Auslagen (Nebenkosten) erstattet, wenn sie nicht unter §§ 4–9 fallen? (a)
 - 9.4 Erstattung von Vorbereitungsaufwendungen bei Entfall der Reise
   - a) Werden entstandene Vorbereitungsaufwendungen erstattet, wenn eine Dienstreise aus Gründen entfällt, die die Dienstreisenden nicht zu vertreten haben? (a)

10) Spezielle Fälle: Versetzung, Abordnung, Fortbildung, Krankheit, private Verbindung
 - 10.1 Versetzung / Abordnung & Trennungsgeld (Schnittstelle zu §13)
   - a) Wann entsteht Anspruch auf Trennungsgeld bei Abordnung ohne Zusage der Umzugskostenvergütung und für welche Fälle gilt dies? (a)
   - a) Gelten die Trennungsgeldregelungen auch für Beamtinnen und Beamte auf Widerruf im Vorbereitungsdienst bei Abordnung im Rahmen der Ausbildung? (a)
   - b) Wird bei Dienstreisen im Anlass von Versetzung oder Abordnung das Tagegeld bis zur Ankunft am neuen Dienstort gewährt und wie ist die Abgrenzung zum Trennungsgeld geregelt? (b)
 - 10.2 Fortbildung / Nebentätigkeit
   - b) Können Kosten für Fortbildungen, die zumindest teilweise im dienstlichen Interesse liegen, bis zur Höhe der Reisekostenvergütung erstattet werden? (b)
   - b) Habe ich Anspruch auf Reisekostenvergütung bei Dienstreisen, die ich für eine auf Verlangen, Vorschlag oder Veranlassung der zuständigen Behörde wahrgenommene Nebentätigkeit erledige, wenn eine andere Stelle Auslagenerstattung gewähren müsste? (b)
 - 10.3 Dienstliche Anordnung während Urlaubs- oder privater Reise
   - b) Wie wird die Reisekostenvergütung bemessen, wenn Dienstreise mit einer Urlaubs- oder privaten Reise verbunden wird? (b)
   - b) Was gilt, wenn die Dienstreise am Urlaubsort angeordnet oder genehmigt wird (Abweichung bei Bemessung der Reisekostenvergütung)? (b)
   - b) Wird die Rückreise vom Urlaubs- oder Aufenthaltsort zur Dienststätte als Dienstreise gewertet und vergütet, wenn dienstlich die vorzeitige Beendigung einer Urlaubsreise angeordnet wird? (b)
   - b) Werden Aufwendungen, die durch Unterbrechung oder vorzeitige Beendigung einer Urlaubs- oder privaten Reise entstehen, erstattet und in welchem Umfang? (b)
 - 10.4 Krankenhausaufnahme / Krankheit während Dienstreise
   - b) Werden Aufwendungen erstattet, die wegen Krankheit und Krankenhausaufnahme während einer Dienstreise für jeden vollen Kalendertag des Krankenhausaufenthalts entstanden sind? (b)
 - 10.5 Fahrten zwischen Wohnung und regelmäßiger Dienststätte aus besonderem dienstlichen Anlass
   - b) Können für Fahrten zwischen Wohnung und regelmäßiger Dienststätte aus besonderem dienstlichen Anlass die entstandenen notwendigen Fahrtkosten erstattet werden? (b)

11) Auslandsdienstreisen — Detailfragen zur Bemessung und Zeitpunkte (§12)
 - 11.1 Landeszuordnung / Mitternachtsregel
   - a) Für welches Land wird das Tages- und Übernachtungsgeld bei Auslandsreisen bemessen, wenn vor Mitternacht Ortszeit ein bestimmtes Land zuletzt erreicht wird? (a)
 - 11.2 Landekriterium bei Flug- und Schiffsreisen; Zwischenlandungen
   - a) Wie wird bei Flugreisen der Zeitpunkt der Erreichung eines Landes bestimmt (Landekriterium) und wie werden Zwischenlandungen behandelt? (a)
 - 11.3 Absenkung ab dem 15. Tag; Ausnahmen (siehe 8.2)
   - a) Bei längeren Auslandsaufenthalten: Wann wird das Auslandstagegeld ab dem 15. Tag um 25 Prozent ermäßigt und wer kann in begründeten Fällen von der Ermäßigung absehen? (a)

12) Verwaltung, Antragstellung, Fristen, Belege, Anrechnung, Verzicht (§3 Abs.4–7)
 - 12.1 Antragsfrist / Ausschlussfrist
   - b) Bis wann muss ich die Reisekostenvergütung spätestens schriftlich oder elektronisch beantragen (Ausschlussfrist)? (b)
   - b) Wann beginnt die Ausschlussfrist von sechs Monaten zur Beantragung der Reisekostenvergütung? (b)
 - 12.2 Vorlage- und Aufbewahrungspflichten für Belege
   - b) Können die zuständigen Stellen bis wann die Vorlage der maßgeblichen Kostenbelege verlangen und was passiert, wenn ich diese auf Anforderung nicht innerhalb eines Monats vorlege? (b)
   - b) Wie lange muss ich die Kostenbelege nach Erstattung der Reisekostenvergütung für Zwecke der Rechnungsprüfung aufbewahren und auf Verlangen vorlegen? (b)
 - 12.3 Anrechnung von Leistungen Dritter; Koordination mit anderen Stellen
   - b) Werden Leistungen, die ich ihres Amtes wegen von dritter Seite aus Anlass einer Dienstreise erhalte, auf die Reisekostenvergütung angerechnet? (b)
   - b) Habe ich Anspruch auf Reisekostenvergütung bei Dienstreisen, die ich für eine auf Verlangen, Vorschlag oder Veranlassung der zuständigen Behörde wahrgenommene Nebentätigkeit erledige, wenn eine andere Stelle Auslagenerstattung gewähren müsste? (b)  [auch unter 10.2]
 - 12.4 Verzicht auf Vergütung
   - b) Kann ich ganz oder teilweise auf Reisekostenvergütung und Auslagenerstattung verzichten und wie muss ein solcher Verzicht erklärt werden? (b)

13) Weitere spezielle Auslegungsfragen (Querverbindungen)
 - 13.1 Reisekostenbemessung bei Kombination mit Privat-/Urlaubsreise (Querverweis)
   - b) Wie wird die Reisekostenvergütung bemessen, wenn Dienstreise mit einer Urlaubs- oder privaten Reise verbunden wird? (b)  [auch unter 10.3]
   - b) Wird die Rückreise vom Urlaubs- oder Aufenthaltsort zur Dienststätte als Dienstreise gewertet und vergütet, wenn dienstlich die vorzeitige Beendigung einer Urlaubsreise angeordnet wird? (b)  [auch unter 10.3]
 - 13.2 Erstattungsfähigkeit von Vorbereitungsaufwand bei Entfall der Reise (Querverweis)
   - a) Werden entstandene Vorbereitungsaufwendungen erstattet, wenn eine Dienstreise aus Gründen entfällt, die die Dienstreisenden nicht zu vertreten haben? (a)  [auch unter 9.4]"""


def improve (hierarchy):
    prompt = f"""


Given is a structured hierarchy of questions and topics:
{hierarchy}
Your task:
Transform the hierarchy into a natural dialogue flow:
Imagine it as if a user is asking follow-up questions and the system organizes them step by step.
Each level should feel like a user could ask: “Tell me more about …” and then branch deeper.
Deepen the hierarchy where possible:
Add one extra meaningful sub-level under each category (if not already present).
Ensure that every node branches into at least two sub-nodes before reaching concrete questions.
Avoid flat lists of many siblings.

Improve the structure:
If a question or topic fits into multiple categries, you may duplicate it, including sub-topics etc.
Output the improved hierarchy as a Mermaid TD graph.
Root = "Was möchten Sie zur Planung, Durchführung oder Abrechnung von Dienstreisen wissen?"
Nodes = categories, sub-categories, questions.
Each level should expand naturally into more specific nodes.
"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()



if __name__ == "__main__":
    print("Printing Improved Graph")
    results = improve(structure_result)
    print (results)
