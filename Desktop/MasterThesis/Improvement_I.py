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
#  document = f.read()

#task_description = """You are planning a business trip, and you don't know anything about the procedures nor the requirements or regulations.
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



#if __name__ == "__main__":
#    print("Printing Improved Graph")
#    questions = create_questions(document, task_description)
#    print(questions)
#    structure_result = structure (questions, document)
#    print(structure_result)


hierarchy = """
1) Anordnung, Definitionen und grundsätzliche Regeln
  1.1) Was ist eine Dienstreise / Dienstgang & Genehmigung
    - Buchung: Muss eine Dienstreise vorab von der zuständigen Dienstvorgesetzten bzw. dem zuständigen Dienstvorgesetzten schriftlich oder elektronisch angeordnet oder genehmigt werden?
    - Buchung: Gibt es Ausnahmen, bei denen keine Anordnung oder Genehmigung für eine Dienstreise erforderlich ist (z. B. Richterinnen und Richter oder bestimmte Beauftragte)?
    - Buchung: Dürfen Dienstreisen nur durchgeführt werden, wenn keine kostengünstigere Art der Erledigung des Dienstgeschäfts möglich und sinnvoll ist?
  1.2) Dienstreise vs. Dienstgang (Abgrenzung, Anspruch auf Tagegeld)
    - Buchung: Besteht für Dienstgänge ein Anspruch auf Tagegeld und wie werden längere Dienstgänge (>8 Stunden) vergütet?
  1.3) Ausgangs‑/Endpunkt der Dienstreise; Wohnung(en)
    - Buchung: Darf ich als Dienstreisende oder Dienstreisender das Ausgangs- und Endpunkt der Dienstreise grundsätzlich selbst bestimmen?
    - Buchung: Kann die oder der zuständige Dienstvorgesetzte anordnen, dass die Dienststätte Ausgangs- oder Endpunkt der Dienstreise ist, und wann ist das zulässig?
    - Buchung: Wie verhält es sich, wenn ich die Dienstreise an der Wohnung antrete oder beende – welche Strecke wird für die Fahrtkostenerstattung bzw. Wegstreckenentschädigung zugrunde gelegt?
    - Buchung: Welche Regelung gilt bei mehreren Wohnungen oder Unterkünften – welche ist maßgebend?

2) Vergütung, Fahrtkosten und Beförderungsmittel (Anwendungsregeln und Erstattung)
  2.1) Grundsätze zur Wahl des Beförderungsmittels
    - Buchung: Bin ich grundsätzlich frei in der Wahl des Beförderungsmittels oder gibt es Einschränkungen?
    - Buchung: Muss ich bei der Wahl des Verkehrsmittels die Erfordernisse des Klimaschutzes beachten?
    - Buchung: Werden Fahrtkosten nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann?
  2.2) Fahrt- und Flugkostenerstattung (allgemein und Klassen)
    2.2.1) Erstattung der jeweils niedrigsten Klasse; Ausnahmen
      - Buchung: Bis zu welcher Klasse werden die Kosten für regelmäßig verkehrende Beförderungsmittel erstattet?
      - Buchung: Unter welchen Voraussetzungen können Ausnahmen von der Erstattung nur der niedrigsten Beförderungsklasse zugelassen werden?
    2.2.2) Flüge: Erstattungsfähigkeit und besondere Regeln
      - Buchung: Sind Flugkosten grundsätzlich erstattungsfähig und unter welchen Bedingungen dürfen sie genutzt werden?
      - Buchung: Werden bei Flugreisen grundsätzlich nur die Kosten der niedrigsten Flugklasse erstattet?
    2.2.3) Höhere Klasse bei Behinderung / Gesundheit
      - Buchung: Wann wird bei Dienstreisenden mit einem Grad der Behinderung von mindestens 50 die Auslage für die nächsthöhere Klasse erstattet?
      - Buchung: Können auch andere Dienstreisende aus gesundheitlichen Gründen eine höhere Beförderungsklasse erstattet bekommen?
  2.3) Mietwagen, Taxi, Carsharing
    - Buchung: Werden Kosten für Mietwagen, Taxi oder Carsharing erstattet und unter welchen Bedingungen (triftiger Grund)?
    - Buchung: Dürfen bei fehlendem triftigen Grund für Mietwagen/Taxi/Carsharing höhere Vergütungen als bei Nutzung öffentlicher Verkehrsmittel gewährt werden?
    - Buchung: Erfolgt bei Nutzung von Carsharing eine Kürzung der Mitgliedsgebühr wegen eventueller privater Nutzung?
  2.4) Flüge und Klimaausgleich / besondere Vorgaben
    - Buchung: Muss bei Flugreisen eine Klimaausgleichszahlung berücksichtigt werden und in welcher Weise?
    - Buchung: Gelten besondere Vorgaben für Flüge von Mitgliedern der Landesregierung, Bediensteten der Ministerien und staatlichen Hochschulen hinsichtlich jährlicher Ausgleichszahlungen?
    - Erstattung: Gelten für Flüge, die von staatlichen Hochschulen bei Projekten aus Drittmitteln bezahlt werden, Ausgleichszahlungen und unter welchen Bedingungen?

3) Wegstreckenentschädigung (km‑Sätze, Fahrrad, Zuschläge)
  3.1) Private Kraftfahrzeuge
    - Buchung: Welche Wegstreckenentschädigung gilt für Fahrten mit einem privaten Kraftfahrzeug (Cent pro Kilometer)?
    - Buchung: Wann erhöht sich die Wegstreckenentschädigung auf 35 Cent pro Kilometer?
  3.2) Zuschläge für schwierige Wege
    - Buchung: Kann bei regelmäßigem Fahren auf unbefestigten Straßen oder schwer befahrbaren Wegen ein Zuschlag gewährt werden und wie hoch ist dieser?
  3.3) Fahrrad / E‑Bike / Pedelec
    - Buchung: Welche Wegstreckenentschädigung gilt bei Fahrten mit Fahrrad, E-Bike oder Pedelec?

4) Tagegeld (Sätze, Dauer, Kürzungen)
  4.1) Höhe und Bemessung
    - Buchung: Wie hoch ist das Tagegeld für jeden vollen Kalendertag einer Dienstreise?
    - Buchung: Wie viel Tagegeld steht für den An- oder Abreisetag bei mehrtägigen Dienstreisen zu, wenn die Dienstreise mehr als 8 Stunden bzw. mehr als 14 Stunden dauert?
  4.2) Bestimmung der Reisedauer (Abreise/Ankunft)
    - Buchung: Nach welchen Zeitpunkten bestimmt sich die Dauer der Dienstreise (Abreise und Ankunft bezogen auf die Wohnung oder Dienststätte)?
  4.3) Kürzung bei unentgeltlicher Verpflegung
    - Buchung: Wie wird das Tagegeld gekürzt, wenn Dienstreisende unentgeltlich Verpflegung erhalten (Frühstück, Mittag, Abendessen in Prozenten)?
  4.4) Dienstgänge (keine volle Tagegeldansprüche)
    - (siehe 1.2) Buchung: Besteht für Dienstgänge ein Anspruch auf Tagegeld und wie werden längere Dienstgänge (>8 Stunden) vergütet?

5) Übernachtungsgeld, Langzeitaufenthalte und Auslagenerstattung
  5.1) Pauschbeträge und Erstattung höherer Kosten
    - Buchung: Wie hoch ist das pauschale Übernachtungsgeld im Inland und im Ausland?
    - Buchung: Werden höhere Übernachtungskosten ersetzt und wer legt durch Verwaltungsvorschrift fest, bis zu welcher Höhe Übernachtungskosten notwendig sind?
  5.2) Fälle, in denen Übernachtungsgeld nicht gewährt wird
    - Buchung: In welchen Fällen wird Übernachtungsgeld nicht gewährt (z. B. bei Benutzung von Beförderungsmitteln, Aufenthalt in der eigenen Wohnung, unentgeltliche Unterkunft, wenn Unterkunftskosten in Fahrtkosten enthalten sind)?
  5.3) Auslagenerstattung bei längerem Aufenthalt am Geschäftsort (ab 8. Tag)
    - Buchung: Wann werden Auslagenerstattungen bei längerem Aufenthalt am Geschäftsort (ab dem 8. Tag) gezahlt und wie werden diese bemessen?
    - Buchung: Kann ab dem 15. Tag im Ausland anstelle des pauschalen Übernachtungsgeldes die Erstattung der nachgewiesenen notwendigen Übernachtungskosten erfolgen? (siehe auch Auslandsdienstreisen)
  5.4) Sonderregel: Langzeit im Ausland (15. Tag)
    - (verlinkt auch zu Kapitel 7 Auslands) Buchung: Wann wird bei längeren Aufenthalten im Ausland das Auslandstagegeld ab dem 15. Tag um 25% ermäßigt und wer kann davon absehen?

6) Aufwands‑ und Pauschvergütung / Nebenkosten
  6.1) Aufwandsvergütung statt Einzelvergütungen
    - Buchung: Können Dienstreisende anstelle von Tagegeld, Übernachtungsgeld und Auslagenerstattung eine Aufwandsvergütung erhalten und unter welchen Bedingungen?
  6.2) Pauschvergütung bei regelmäßigen oder gleichartigen Reisen
    - Buchung: Kann die oberste Dienstbehörde Pauschvergütungen für regelmäßige oder gleichartige Dienstreisen festlegen?
  6.3) Erstattung sonstiger notwendiger Auslagen (Nebenkosten)
    - Buchung: Welche sonstigen notwendige Auslagen (Nebenkosten) können erstattet werden, wenn sie nicht unter §§ 4–9 fallen?

7) Besondere Fälle / Bemessung bei Versetzung, Fortbildung, Krankheit, Urlaub
  7.1) Versetzung, Abordnung, Aufhebung einer Abordnung
    - Buchung: Welche Besonderheiten gelten bei Dienstreisen im Zusammenhang mit Versetzung, Abordnung oder Aufhebung einer Abordnung hinsichtlich Tagegeld und Übernachtungsgeld?
  7.2) Fortbildung / Nebentätigkeit
    - Buchung: Können Kosten für Fortbildungen erstattet werden, wenn sie zumindest teilweise im dienstlichen Interesse liegen?
    - Buchung: Haben Dienstreisende Anspruch auf Reisekostenvergütung für Nebentätigkeiten, wenn eine andere Stelle Auslagenerstattung gewährt?
  7.3) Kombination mit Urlaubs- oder Privatreise; vorzeitige Beendigung
    - Buchung: Wie wird die Reisekostenvergütung bemessen, wenn Dienstreisen mit einer Urlaubsreise oder privaten Reise verbunden werden?
    - Buchung: Welche Sonderregelung gilt, wenn die Dienstreise am Urlaubsort anzutreten oder zu beenden ist und dies angeordnet oder genehmigt wurde?
    - Buchung: Wie werden Aufwendungen behandelt, die durch die vorzeitige Beendigung einer Urlaubs- oder privaten Reise auf Anordnung aus dienstlichen Gründen entstehen?
  7.4) Krankheit und Krankenhausaufnahme
    - Buchung: Werden im Fall von Krankheit und Krankenhausaufnahme die notwendigen Auslagen für Unterkunft am Geschäftsort für jeden vollen Kalendertag des Krankenhausaufenthalts erstattet?
  7.5) Fahrten Wohnung ↔ regelmäßige Dienststätte aus besonderem Anlass
    - Buchung: Können Fahrten zwischen Wohnung und regelmäßiger Dienststätte aus besonderem dienstlichen Anlass erstattet werden?

8) Auslandsdienstreisen (Definition, Bemessung, Sonderregelungen)
  8.1) Begriff und Anwendungsbereich
    - Buchung: Gelten besondere Regelungen für Auslandsdienstreisen und was ist ein Auslandsdienstreisebegriff?
    - Buchung: Für welches Land wird Tage- und Übernachtungsgeld bei Auslandsreisen gewährt, wenn vor Mitternacht zuletzt ein bestimmtes Land erreicht wurde?
  8.2) Rechtsgrundlage für Auslandstage- und Übernachtungsgelder
    - Buchung: Nach welchen Regelungen werden Auslandstagegelder und Auslandsübernachtungsgelder bemessen?
    - Erstattung: Wie wird die Bemessung des Tage- und Übernachtungsgeldes bei Auslandsdienstreisen gemäß der ARV/ARVVwV geregelt?
  8.3) Zeitliche Bestimmung bei Flug/Schiff (Zwischenlandungen, Mitternacht-Regel)
    - Buchung: Wie werden Zwischenlandungen bei Flug- oder Schiffsreisen für die Bestimmung des Landes berücksichtigt?
    - Erstattung: Wie ist während einer Auslandsdienstreise zu verfahren, wenn das Inland vor Mitternacht zuletzt erreicht wird (Welches Auslandstagegeld gilt)?
  8.4) Längerer Auslandsaufenthalt (ab 15. Tag)
    - Buchung: Wann wird bei längeren Aufenthalten im Ausland das Auslandstagegeld ab dem 15. Tag um 25% ermäßigt und wer kann davon absehen?
    - Buchung: Wer kann in begründeten Fällen von der Ermäßigung des Auslandstagegeldes ab dem 15. Aufenthaltstag absehen?
    - Buchung: Kann ab dem 15. Tag im Ausland anstelle des pauschalen Übernachtungsgeldes die Erstattung der nachgewiesenen notwendigen Übernachtungskosten erfolgen?

9) Trennungsgeld (Abordnung ohne Umzugskosten)
  9.1) Anspruchsvoraussetzungen
    - Buchung: Wann entsteht Anspruch auf Trennungsgeld bei Abordnung ohne Zusage der Umzugskostenvergütung?
  9.2) Anwendbarkeit auf Auszubildende / Widerrufsdienstverhältnisse
    - Buchung: Gilt das Trennungsgeld auch für Beamtinnen und Beamte auf Widerruf im Vorbereitungsdienst bei bestimmten Abordnungen?

10) Erstattungspraxis, Anträge, Fristen, Belege, Anrechnung, Verzicht
  10.1) Antragstellung und Anspruchsberechtigte
    - Erstattung: Muss die Reisekostenvergütung schriftlich oder elektronisch beantragt werden und wer erhält auf Antrag die Vergütung?
  10.2) Ausschlussfrist (sechs Monate) — Beginn und Folgen
    - Erstattung: Innerhalb welcher Frist (Ausschlussfrist) muss die Reisekostenvergütung nach Beendigung der Dienstreise beantragt werden?
    - Erstattung: Wann beginnt die sechsmonatige Ausschlussfrist genau zu laufen?
  10.3) Vorlage von Belegen und Folgen bei Nichtvorlage
    - Erstattung: Können zuständige Stellen bis zu welchem Zeitpunkt die Vorlage der Kostenbelege verlangen?
    - Erstattung: Was passiert, wenn die angeforderten Belege nicht innerhalb eines Monats vorgelegt werden?
    - Erstattung: Wie lange sind die Kostenbelege nach Erstattung der Reisekostenvergütung aufzubewahren und vorzulegen (Aufbewahrungsfrist)?
  10.4) Anrechnung Dritter / Nebentätigkeiten / Verzicht
    - Erstattung: Werden Leistungen, die Dienstreisende ihres Amtes wegen von dritter Seite aus Anlass einer Dienstreise erhalten, auf die Reisekostenvergütung angerechnet?
    - Erstattung: Haben Dienstreisende Anspruch auf Reisekostenvergütung für Nebentätigkeiten, wenn eine andere Stelle Auslagenerstattung gewährt?
    - Erstattung: Kann ganz oder teilweise auf Reisekostenvergütung verzichtet werden und in welcher Form muss der Verzicht erklärt werden?

11) Vorbereitungskosten, Nebenkosten und sonstige Erstattungen
  11.1) Vorbereitungsaufwand bei entfallener Dienstreise
    - Buchung: Werden entstandene Vorbereitungsaufwendungen erstattet, wenn Dienstreisen aus Gründen entfallen, die von den Dienstreisenden nicht zu vertreten sind?
    - Erstattung: Werden Vorbereitungsaufwendungen bei entfallener Dienstreise erstattet und unter welcher Bedingung (nicht von den Dienstreisenden zu vertreten)?
  11.2) Sonstige notwendige Nebenkosten (§10)
    - Buchung: Welche sonstigen notwendige Auslagen (Nebenkosten) können erstattet werden, wenn sie nicht unter §§ 4–9 fallen?

12) Administration, Verwaltungsvorschriften, Zuständigkeiten
  12.1) Befugnisse des Finanzministeriums; Anpassung von Sätzen
    - Buchung: Welche Befugnisse hat das Finanzministerium zur Anpassung der in §§ 5 und 7 Absatz 1 festgesetzten Beträge und zur Erlassung allgemeiner Verwaltungsvorschriften?
  12.2) Zuständigkeiten zur Zulassung von Ausnahmen / Pauschalen
    - (verknüpft mit 2.2 und 6.2) z. B. wer kann Ausnahmen von niedrigster Klasse zulassen oder Pauschvergütungen festlegen?
  12.3) Besondere Pflichten zu Klimaausgleichszahlungen (Ministerien, Hochschulen)
    - (verweist auf 2.4) Buchung: Die obersten Dienstbehörden sind verpflichtet, zum Klimaausgleich … jährliche Ausgleichszahlungen zu leisten; entsprechende Fragen wurden unter 2.4 aufgenommen.
"""


hierarchy_pha = """1) Versicherte Personen
  1.1) Versicherungsnehmer:in
    - Wer ist als Versicherungsnehmer:in versichert?
    - Wer kann die Versicherungsleistung aus dem Vertrag geltend machen?
  1.2) Mitversicherungs‑Varianten (Aufteilung und wer dazugehört)
    - Welche Mitversicherungs‑Varianten (Single, Single mit Kind(ern), Paar, Familie) gibt es und was genau decken sie jeweils ab?
    - Sind Ehepartner / eingetragene Lebenspartner / in häuslicher Gemeinschaft lebende Partner mitversichert?
  1.3) Kinder und Familienangelegenheiten
    - Sind meine Kinder mitversichert, auch wenn sie nicht bei mir wohnen?
    - Endet die Mitversicherung meiner Kinder, wenn sie eine Ausbildung oder ein Studium abschließen und arbeiten?
    - Was passiert bei Aufhebung der häuslichen Gemeinschaft einer mitversicherten Person (z. B. Umzug der Tochter)?
    - Wie ändert sich die Versicherung bei Tod des Versicherungsnehmers bzw. wie lange sind Mitversicherte versichert?
  1.4) Sonstige mitversicherte Personen und Besonderheiten
    - Welche sonstigen Personen sind automatisch mitversichert (z. B. Au-pairs, Haushaltspersonal, Notfallhelfer)?
    - Sind Au-pairs oder Austauschschüler:innen mitversichert und für welchen Zeitraum?
    - Sind in meinem Haushalt beschäftigte Personen (z. B. Haushaltshilfe, Kinderbetreuerin) mitversichert und welche Einschränkungen gelten (z. B. Arbeitsunfälle)?
    - Sind berufliche oder ehrenamtliche Helfer (z. B. Rettungssanitäter:innen, Feuerwehrleute) als Notfallhelfer mitversichert?
  1.5) Rechte, Pflichten und Beziehungen unter Versicherten
    - Gelten die gleichen Rechte und Pflichten auch für mitversicherte Personen?
    - Deckt die Versicherung Haftpflichtansprüche aus den Gefahren des täglichen Lebens auch für mitversicherte Personen?
    - Sind gegenseitige Ansprüche der Versicherten untereinander gedeckt (z. B. wenn ich das Smartphone meiner Ehefrau beschädige)?

2) Versicherungsschutz: Was ist versichert? (Umfang und Voraussetzungen)
  2.1) Allgemeiner Leistungsumfang und Voraussetzungen
    - Wann besteht Versicherungsschutz (Voraussetzungen für einen Versicherungsfall)?
    - Deckt die Versicherung Haftpflichtansprüche aus beruflichen oder gewerblichen Tätigkeiten?
    - Welche Arten von Schäden (Personen-, Sach- und Vermögensschäden) sind versichert?
  2.2) Besondere private Haftpflichtrisiken (Tarif Smart) — Überblick
    - Welche besonderen privaten Haftpflichtrisiken sind im Tarif Smart besonders geregelt (z. B. Hausbesitzer, Vermietung, Photovoltaik)?
  2.3) Immobilien, Eigenheim, Vermietung, Ferienobjekte
    - Besteht Versicherungsschutz als Haus-, Wohnungs- oder Grundbesitzer:in für selbstgenutzte Immobilien?
    - Sind Außenanlagen, Garagen und Gartenhäuser einer selbstgenutzten Immobilie mitversichert?
    - Deckt die Versicherung Schäden durch häusliche Abwässer und Rückstau des Straßenkanals?
    - Gilt Versicherungsschutz für eine selbstgenutzte Ferienimmobilie im EU-Ausland, Norwegen oder Island?
    - Sind vorübergehend gemietete Ferienimmobilien im Ausland mitversichert?
    - Besteht Versicherungsschutz als Bauherr:in bei Umbauten und Renovierungen und welche Voraussetzungen gelten?
    - Sind unbebaute Grundstücke und land- und forstwirtschaftliche Grundstücke bis zu bestimmten Größen versichert?
    - Sind Schäden bei Vermietung von Zimmern, Einliegerwohnungen oder Garagen in meinem selbstbewohnten Haus mitversichert?
  2.4) Energieanlagen (Photovoltaik, Geothermie, Wallbox)
    - Deckt die Versicherung Anlagen zur Energieversorgung (Photovoltaik, Geothermie, Wallbox) und welche Einschränkungen bestehen?
    - Sind Schäden an den Energieanlagen selbst versichert?
  2.5) Gemietete, geliehene oder geleaste Sachen
    - Deckt die Versicherung Schäden an gemieteten, geliehenen oder geleasten beweglichen Sachen?
    - Gibt es eine Begrenzung für die Entschädigung bei Schäden an gemieteten beweglichen Sachen?
    - Welche Schäden an gemieteten Sachen sind ausgeschlossen (z. B. Abnutzung, Heizungsanlagen, Fahrzeuge)?
    - Sind Schäden an mitgemieteten Einbauküchen und an Mietwohnungen/Mietshaus gedeckt?
  2.6) Fahrzeuge, Wasserfahrzeuge, Luftfahrzeuge und Modellfahrzeuge
    - Welche Kraftfahrzeuge sind über die Privat-Haftpflicht gedeckt (z. B. Pedelecs, Elektrokleinstfahrzeuge ohne Kennzeichen)?
    - Gilt Versicherungsschutz für Fahrräder mit Tretunterstützung (Pedelecs) und welche Bedingungen gelten?
    - Sind Fahrzeuge mit amtlichem Kennzeichen oder Versicherungskennzeichen sowie führerscheinpflichtige Fahrzeuge ausgeschlossen?
    - Gilt Deckung beim Gebrauch von Kraftfahrzeugen ohne Kennzeichenpflicht (z. B. Arbeitsmaschinen bis 20 km/h, nicht zugelassener Pkw zur Restaurierung)?
    - Deckt die Versicherung motorgetriebene Modell- und Spielfahrzeuge?
    - Was ist die sogenannte "Mallorca-Deckung" bei Anmietung eines Fahrzeugs im Ausland und unter welchen Bedingungen greift sie?
    - Gilt die Mallorca-Deckung nur subsidiär zur Kfz-Haftpflicht des Mietwagens?
    - Welche Wasserfahrzeuge und welche Bedingungen sind in der Privat-Haftpflicht mitversichert (z. B. Segelboote, gemietete Motorboote)?
    - Gilt Versicherungsschutz bei kurzzeitiger Anmietung von Segel- und Motorbooten und wie lange ist die Nutzung gedeckt?
    - Sind Haftpflichtansprüche aus dem Gebrauch von Luftfahrzeugen gedeckt (z. B. Modellflugzeuge, Lenkdrachen)?
    - Sind Haftpflichtansprüche wegen Beschädigung der Luft- oder Wasserfahrzeuge selbst versichert?
  2.7) Tiere, Tierhaltung und Hüten
    - Welche Tierarten sind in der Haftpflicht mitversichert (z. B. Katzen, Kaninchen, Bienen, Weidetiere)?
    - Gilt Versicherungsschutz für Hunde- oder Pferdehalter:innen?
    - Besteht Deckung für gelegentliches Hüten fremder Hunde oder Reiten fremder Pferde und welche Einschränkungen gelten?
    - Sind Ansprüche des Tierhalters wegen Verletzung, Abhandenkommen oder Tod des Tieres mitversichert, wenn ich das Tier hüte?
  2.8) Praktika, Tagesbetreuung, Ehrenamt
    - Gilt Versicherungsschutz für Praktika, Schnupperlehren und fachpraktischen Unterricht und gibt es Einschränkungen?
    - Sind Haftpflichtansprüche aus Tageseltern- oder Babysittertätigkeiten mitversichert und welche Schäden sind ausgeschlossen?
    - Ist ehrenamtliche Tätigkeit versichert, und welche Voraussetzungen gelten (z. B. subsidiäre Deckung)?
  2.9) Sonstige spezielle Deckungsfälle
    - Übernimmt die Versicherung Kautionsleistungen im Ausland und unter welchen Rückzahlungsbedingungen?
    - Sind Ansprüche wegen Diskriminierung nach dem AGG gedeckt und unter welchen Voraussetzungen?
    - Deckt die Versicherung Haftpflichtansprüche aus privater Internetnutzung und elektronischem Datenaustausch?
    - Welche Internet‑Schäden sind ausgeschlossen (z. B. bewusstes Eindringen in fremde Datennetze, Virenverbreitung, illegales Herunterladen)?
    - Sind Vermögensschäden ohne Personen‑ oder Sachschaden versichert und welche Vermögensschäden sind ausgeschlossen?
    - Deckt die Versicherung Gewässerschäden und Ansprüche nach dem Umweltschadensgesetz (USchadG) und welche Einschränkungen gelten (z. B. Lagergrößen von Stoffbehältern)?
    - Sind Schäden durch elementare Naturkräfte (z. B. Überflutung) von der Gewässerschaden‑Deckung ausgeschlossen?
    - Ist der Gebrauch von erlaubten Waffen, Munition und Geschossen versichert und welche Nutzungsarten sind ausgeschlossen (z. B. Jagd, Straftaten)?
    - Deckt die Versicherung Gefälligkeitshandlungen (z. B. Hilfe beim Umzug)?
    - Deckt die Versicherung Schäden durch nicht deliktsfähige Personen (z. B. Kleinkinder) und gibt es hierfür Begrenzungen?
    - Was ist die Forderungsausfalldeckung und unter welchen Voraussetzungen kann ich sie in Anspruch nehmen?
    - Welche Voraussetzungen müssen für die Forderungsausfalldeckung erfüllt sein (z. B. rechtskräftiges Urteil, erfolglose Vollstreckung, Abtretung)?
    - Gilt Gewaltopferschutz (Erstattung bei vorsätzlichem Handeln des Täters) im Rahmen der Forderungsausfalldeckung?
    - Welche Schäden sind von der Forderungsausfalldeckung ausgeschlossen (z. B. Schäden an Fahrzeugen oder Immobilien)?
    - Deckt die Versicherung den Verlust fremder Schlüssel oder Codekarten und welche Kosten werden erstattet?
    - Gibt es eine Begrenzung der Entschädigung beim Schlüsselverlust und welche Schlüssel sind ausgeschlossen (z. B. Autoschlüssel)?
    - Welche Frist gilt für vorübergehende Sicherungsmaßnahmen nach Schlüsselverlust (z. B. Objektschutz bis 14 Tage)?

3) Leistungsausschlüsse, Einschränkungen und Begrenzungen
  3.1) Allgemeine Leistungsausschlüsse
    - Welche Leistungsausschlüsse und -einschränkungen gelten allgemein (z. B. Vorsatz, Angehörige, Asbest, Persönlichkeitsrechtsverletzungen)?
    - Sind Ansprüche aus der Übertragung von Krankheiten ausgeschlossen und gibt es Ausnahmen?
  3.2) Spezifische Ausschlüsse (Umwelt, Natur, Strahlung, Fahrzeuge)
    - Gibt es Ausschlüsse für Schäden durch Senkungen, Erdrutsch oder Überschwemmungen?
    - Sind Schäden durch energiereiche ionisierende Strahlen (z. B. Radioaktivität, Röntgen) ausgeschlossen?
    - Deckt die Versicherung die Haftpflicht aus der Nutzung von Kraftfahrzeugen grundsätzlich nicht und welche Ausnahmen bestehen?
  3.3) Begrenzungen der Leistung und Selbstbeteiligung
    - Gilt die Versicherungssumme als Grenze der Leistung und wie verhalten sich Prozesskosten hierzu?
    - Kann es eine Selbstbeteiligung geben und wie wirkt sich falsches Verhalten auf Mehrkosten aus?
    - Gibt es besondere Begrenzungen (z. B. Entschädigungsgrenzen für gemietete Sachen, Schäden durch nicht deliktsfähige Personen)?

4) Schadenfall — Ablauf, Leistungen der Allianz und Entschädigung
  4.1) Leistungen der Allianz im Versicherungsfall
    - Welche Leistungen erbringt die Allianz im Versicherungsfall (Prüfung, Erstattung, Abwehr unberechtigter Ansprüche)?
    - Wer führt im Streitfall das Prozessverfahren und wer trägt die Prozesskosten?
  4.2) Berechnung und Grenzen der Entschädigung
    - Wie wird bei Beschädigung eines fremden Gegenstands die Entschädigung berechnet (Reparaturkosten vs. Zeitwert)?
    - Gilt die Versicherungssumme als Grenze der Leistung und wie verhalten sich Prozesskosten hierzu? (Duplikat möglich)
    - Gibt es eine Selbstbeteiligung und wie wirkt sich falsches Verhalten auf Mehrkosten aus? (Duplikat möglich)
  4.3) Sonderfälle im Schadensfall (Forderungsausfall, Kaution, Schlüsselverlust)
    - Was ist die Forderungsausfalldeckung und unter welchen Voraussetzungen kann ich sie in Anspruch nehmen? (Duplikat möglich)
    - Übernimmt die Versicherung Kautionsleistungen im Ausland und unter welchen Rückzahlungsbedingungen? (Duplikat möglich)
    - Deckt die Versicherung den Verlust fremder Schlüssel oder Codekarten und welche Kosten werden erstattet? (Duplikat möglich)

5) Obliegenheiten, Mitwirkungspflichten und Rechtsfolgen bei Pflichtverletzungen
  5.1) Obliegenheiten vor Eintritt des Versicherungsfalls
    - Welche Obliegenheiten muss ich vor Eintritt eines Versicherungsfalls beachten (z. B. Beseitigung gefahrdrohender Umstände)?
  5.2) Obliegenheiten nach Eintritt des Versicherungsfalls
    - Welche Pflichten habe ich nach Eintritt des Versicherungsfalls (Anzeige, Schadenminderung, Befolgung von Weisungen)?
    - Welche Mitteilungs- und Mitwirkungsobliegenheiten bestehen (z. B. bei Mahnbescheid, Einleitung behördlicher Verfahren)?
  5.3) Folgen bei Verletzung von Obliegenheiten und arglistige Täuschung
    - Was passiert, wenn ich die Obliegenheiten verletze (z. B. Kürzung der Leistung, Verlust des Anspruchs, Kündigungsrecht der Allianz)?
    - Welche Rechtsfolgen hat arglistige Täuschung nach Eintritt des Versicherungsfalls?

6) Vertragliche Regelungen, Beitragsanpassung, Laufzeit, Kündigung, Änderungen, Kommunikation
  6.1) Risikoänderungen, Vorsorgeversicherung und Meldepflichten
    - Wie sind Risikoänderungen im Vertrag geregelt (automatische Mitversicherung, Vorsorgeversicherung)?
    - Für welche neu entstehenden Risiken gilt die Vorsorgeversicherung mindestens sechs Monate (z. B. Anschaffung eines Hundes, Erwerb einer Immobilie)?
    - Welche Meldepflichten habe ich bei neu eintretenden Risiken und welche Folgen hat unterlassene Meldung?
  6.2) Beitragsanpassung und Ihre Rechte bei Beitragserhöhung
    - Wie und wann kann die Allianz den Beitrag anpassen und wie werde ich darüber informiert?
    - Welche Rechte habe ich, wenn der Beitrag aufgrund der Neukalkulation erhöht wird?
  6.3) Beginn des Versicherungsschutzes, Beiträge, Laufzeit und Kündigung
    - Wann beginnt der Versicherungsschutz (z. B. nach Zahlung des ersten Beitrags)?
    - Welche Zahlungspflichten und -fristen gelten für Erst- und Folgebeiträge und welche Zahlungsperioden sind möglich?
    - Wie lange läuft der Vertrag und welche Regeln gelten für automatische Verlängerung?
    - Wie und bis wann muss ich kündigen, wenn ich den Vertrag zum Ablauf beenden möchte?
    - Welche Formalitäten gelten bei Kündigung (Textform) und bei Kündigung nach einem Versicherungsfall?
    - Unter welchen Voraussetzungen kann die Allianz die Versicherungsbedingungen im vereinfachten Verfahren umstellen?
  6.4) Beschwerden, Recht, Gerichtsstände und digitale Kommunikation
    - An welche Stellen kann ich mich mit Beschwerden wenden (Allianz, Vermittler, Ombudsmann, BaFin) und welche Grenzen gelten beim Ombudsmann-Verfahren?
    - Welches Recht und welche Gerichtsstände gelten für meinen Vertrag?
    - Wie funktioniert die digitale Vertragskommunikation (Versand per E-Mail, Widerspruchsrecht gegen digitale Kommunikation)?"""


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
Root = "Was möchten Sie zur Privathaftpflicht Smart wissen?"
Nodes = categories, sub-categories, questions.
Each level should expand naturally into more specific nodes.
"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()



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


if __name__ == "__main__":
    print("Printing Improved Graph")
    improved_graph = improve(hierarchy_pha)
    print (improved_graph)
    print("Printing Graph with Answers")
    results = add_answers(improved_graph, document)
    print (results)
