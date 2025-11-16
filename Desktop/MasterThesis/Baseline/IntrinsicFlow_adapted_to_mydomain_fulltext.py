from openai import OpenAI

OPENAI_API_KEY =""
client = OpenAI(api_key=OPENAI_API_KEY)


DOMAIN = """Gesetz zur Neufassung des Landesreisekostengesetzes

§ 1
Geltungsbereich
(1) Dieses Gesetz regelt die Erstattung von Auslagen für Dienstreisen, Dienstgänge und für Reisen zum Zweck der Aus- oder Fortbildung (Reisekostenvergütung) der Beamtinnen und Beamten des Landes, der Gemeinden, der Gemeindeverbände, der Landkreise und der sonstigen der Aufsicht des Landes unterstehenden Körperschaften, Anstalten und Stiftungen des öffentlichen Rechts, der Richterinnen und Richter des Landes, sowie der zu diesen Dienstherren abgeordneten Beamtinnen, Beamten, Richterinnen und Richter. Es regelt auch die Erstattung von Auslagen aus Anlass der Abordnung (Trennungsgeld).

(2) Die Reisekostenvergütung umfasst

1.
Fahrt- und Flugkostenerstattung (§ 4),

2.
Wegstreckenentschädigung (§ 5),

3.
Tagegeld bei Dienstreisen (§ 6),

4.
notwendige Mehraufwendungen bei Dienstgängen (§ 6),

5.
Übernachtungsgeld (§ 7),

6.
Auslagenerstattung bei längerem Aufenthalt am Geschäftsort (§ 8),

7.
Aufwands- und Pauschvergütung (§ 9) und

8.
Erstattung sonstiger Kosten (§ 10).


zur Einzelansicht § 1

§ 2
Dienstreisen und Dienstgänge
(1) Dienstreisen im Sinne dieses Gesetzes sind Reisen zur Erledigung von Dienstgeschäften außerhalb des Dienstortes, die von der oder dem zuständigen Dienstvorgesetzten angeordnet oder genehmigt worden sind, es sei denn, dass eine Anordnung oder Genehmigung nach dem Amt der Dienstreisenden oder dem Wesen des Dienstgeschäfts nicht in Betracht kommt. Die Anordnung oder Genehmigung hat schriftlich oder elektronisch zu erfolgen. Dienstreisen sind auch Reisen von einem dem vorübergehenden Aufenthalt dienenden Ort zum Dienstort, wenn im Übrigen die Voraussetzungen der Sätze 1 und 2 erfüllt sind. Dienstreisen sollen nur durchgeführt werden, wenn eine kostengünstigere Art der Erledigung des Dienstgeschäftes nicht möglich und sinnvoll ist.

(2) Dienstgänge sind Reisen zur Erledigung von Dienstgeschäften außerhalb der Dienststätte am Dienst- oder Wohnort, die von der oder dem zuständigen Vorgesetzten angeordnet oder genehmigt worden sind, es sei denn, dass eine Anordnung oder Genehmigung nach dem Amt der Dienstreisenden oder dem Wesen des Dienstgeschäfts nicht in Betracht kommt. Dem Wohnort steht ein dem vorübergehenden Aufenthalt dienender Ort gleich.

(3) Für Dienstreisen von Richterinnen oder Richtern zur Wahrnehmung von richterlichen Amtsgeschäften oder zur Teilnahme an einer Sitzung des Präsidiums oder eines anderen vergleichbaren Gerichtsverfassungsorgans, dem sie angehören, bedarf es keiner Anordnung oder Genehmigung. Dasselbe gilt für Dienstreisen der oder des Landesbeauftragten für den Datenschutz und die Informationsfreiheit zur Wahrnehmung der Aufgaben nach dem Landesdatenschutzgesetz und für Dienstreisen der oder des Beauftragten der Landesregierung für die Belange von Menschen mit Behinderungen zur Wahrnehmung der Aufgaben nach dem Landesbehindertengleichstellungsgesetz.

zur Einzelansicht § 2

§ 3
Anspruch auf Reisekostenvergütung
(1) Dienstreisende erhalten auf Antrag eine Vergütung der dienstlich veranlassten notwendigen Auslagen. Dies gilt auch bei Reisen zum Zweck der Ausbildung.

(2) Ausgangs- und Endpunkt einer Dienstreise sind von den Dienstreisenden unter Beachtung des Wirtschaftlichkeitsgrundsatzes grundsätzlich selbst zu bestimmen. Abweichend davon kann die oder der zuständige Dienstvorgesetzte die Dienststätte als Ausgangs- oder Endpunkt der Dienstreise anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt. Bei einer Dienstreise, die an der Wohnung angetreten oder beendet wird, bemisst sich die Fahrtkostenerstattung (§ 4) oder die Wegstreckenentschädigung (§ 5) nach der Entfernung von oder bis zur Wohnung, es sei denn, als Ausgangs- und/oder Endpunkt der Dienstreise wurde die Dienststätte angeordnet. Beim Vorliegen mehrerer Wohnungen oder Unterkünfte ist die der Dienststätte am nächsten gelegene Wohnung oder Unterkunft maßgebend.

(3) Die Dienstreisenden sind grundsätzlich in der Wahl der Beförderungsmittel frei. Bei der Wahl des Beförderungsmittels haben die Dienstreisenden neben wirtschaftlichen Gesichtspunkten insbesondere die Erfordernisse des Klimaschutzes zu beachten. Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann.

(4) Der Anspruch auf Reisekostenvergütung erlischt, wenn die Reisekostenvergütung nicht innerhalb einer Ausschlussfrist von sechs Monaten nach Beendigung der Dienstreise schriftlich oder elektronisch beantragt wird. Die Frist beginnt mit dem Tag nach Beendigung der Dienstreise, in den Fällen des § 10 Absatz 2 mit Ablauf des Tages, an dem die Dienstreise geendet hätte. Die zuständigen Stellen können bis zum Ablauf von sechs Monaten nach Antragstellung die Vorlage der maßgeblichen Kostenbelege verlangen. Werden diese Belege auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden. Die Dienstreisenden sind verpflichtet, die Kostenbelege nach Erstattung der Reisekostenvergütung bis zum Ablauf eines Jahres für Zwecke der Rechnungsprüfung aufzubewahren und auf Verlangen vorzulegen.

(5) Leistungen, die Dienstreisende ihres Amtes wegen von dritter Seite aus Anlass einer Dienstreise erhalten, sind auf die Reisekostenvergütung anzurechnen.

(6) Bei Dienstreisen für eine auf Verlangen, Vorschlag oder Veranlassung der zuständigen Behörde wahrgenommene Nebentätigkeit haben die Dienstreisenden nach diesem Gesetz nur insoweit Anspruch auf Reisekostenvergütung, wie nicht eine andere Stelle Auslagenerstattung für dieselbe Dienstreise zu gewähren hat. Das gilt auch dann, wenn die Dienstreisenden auf ihren Anspruch gegen diese Stelle verzichtet haben.

(7) Auf Reisekostenvergütung und Auslagenerstattung kann ganz oder teilweise verzichtet werden. Der Verzicht ist schriftlich oder elektronisch zu erklären.

zur Einzelansicht § 3

§ 4
Fahrt- und Flugkostenerstattung
(1) Entstandene notwendige Kosten für Fahrten mit regelmäßig verkehrenden Beförderungsmitteln werden bis zur Höhe der Kosten der niedrigsten Beförderungsklasse erstattet. Die oberste Dienstbehörde oder die von ihr ermächtigte nachgeordnete Behörde kann für ihren Geschäftsbereich hiervon Ausnahmen zulassen. Ausnahmen sind zulässig, wenn besondere dienstliche Gründe vorliegen. Flugkosten sind erstattungsfähig, wenn die dienstlichen oder wirtschaftlichen Gründe für die Flugzeugbenutzung die Belange des Klimaschutzes überwiegen. Die Kosten für Ausgleichszahlungen für Flugreisen nach Absatz 4 sind bei der Wirtschaftlichkeitsberechnung einzubeziehen. Erstattet werden grundsätzlich die Kosten der niedrigsten Flugklasse. Das Finanzministerium kann hiervon durch Verwaltungsvorschrift Ausnahmen bestimmen.

(2) Dienstreisende, denen nach Absatz 1 die Fahrt- oder Flugkosten der niedrigsten Klasse zu erstatten wären, werden bei einem Grad der Behinderung von mindestens 50 die Auslagen für die nächsthöhere Klasse erstattet. Dieselbe Vergünstigung kann anderen Dienstreisenden gewährt werden, wenn ihr körperlicher oder gesundheitlicher Zustand das Benutzen dieser Klasse rechtfertigt.

(3) Wurde aus triftigem Grund ein Mietwagen, ein Taxi oder ein Fahrzeug im Rahmen eines Carsharing-Modells benutzt, werden die entstandenen notwendigen Kosten erstattet. Liegt kein triftiger Grund vor, so darf keine höhere Reisekostenvergütung gewährt werden als beim Benutzen eines öffentlichen Verkehrsmittels. Bei Nutzung von Fahrzeugen im Rahmen eines Carsharing-Modells erfolgt keine Kürzung der Mitgliedsgebühr wegen eventueller privater Nutzung.

(4) Die obersten Dienstbehörden sind verpflichtet, zum Klimaausgleich für dienstlich veranlasste Flugreisen von Mitgliedern der Landesregierung und Bediensteten der Landesministerien sowie der jeweiligen nachgeordneten Behörden jährliche Ausgleichszahlungen auf der Grundlage der bestehenden Entscheidungen der Landesregierung zu leisten. Gleiches gilt für die staatlichen Hochschulen. Bei Flügen, die bei Projekten staatlicher Hochschulen aus Drittmitteln bezahlt werden, fällt eine Ausgleichszahlung an, sofern Vorgaben der Drittmittelgeber einer entsprechenden Verwendung nicht entgegenstehen.

zur Einzelansicht § 4

§ 5
Wegstreckenentschädigung
(1) Für Fahrten, die von den Dienstreisenden mit einem privaten Kraftfahrzeug zurückgelegt wurden, wird eine Wegstreckenentschädigung gewährt. Sie beträgt 30 Cent je Kilometer zurückgelegter Strecke.

(2) Besteht an der Benutzung eines Kraftfahrzeugs ein erhebliches dienstliches Interesse, beträgt die Wegstreckenentschädigung 35 Cent je Kilometer zurückgelegter Strecke. Zur Wegstreckenentschädigung nach Satz 1 kann mit Zustimmung der obersten Dienstbehörde ein Zuschlag gewährt werden, wenn auf Grund der Art der Dienstgeschäfte regelmäßig in größerem Umfang Fahrten auf unbefestigten Straßen oder schwer befahrbaren Feld- oder Waldwegen durchzuführen sind. Der Zuschlag beträgt 5 Cent je Kilometer.

(3) Für Fahrten, die von den Dienstreisenden mit einem Fahrrad, E-Bike oder Pedelec zurückgelegt wurden, wird eine Wegstreckenentschädigung in Höhe von 25 Cent je Kilometer zurückgelegter Strecke gewährt.

zur Einzelansicht § 5

§ 6
Tagegeld
(1) Zur Abgeltung der Mehraufwendungen für Verpflegung beträgt das Tagegeld für jeden vollen Kalendertag einer Dienstreise 24 Euro. Bei einer Dienstreise, die weniger als einen vollen Kalendertag dauert, für den Tag des Antritts und den Tag der Beendigung einer mehrtägigen Dienstreise, beträgt das Tagegeld bei einer Dienstreisedauer von mehr als 8 Stunden 6 Euro und bei einer Dienstreisedauer von mehr als 14 Stunden 12 Euro.

(2) Die Dauer der Dienstreise bestimmt sich nach der Abreise und Ankunft an der Wohnung, es sei denn, die Dienstreise beginnt oder endet an der Dienststätte oder Beginn oder Ende wurde an der Dienststätte angeordnet. Beim Vorliegen mehrerer Wohnungen oder Unterkünfte ist die der Dienststätte am nächsten gelegene Wohnung oder Unterkunft maßgebend.

(3) Für Dienstgänge besteht kein Anspruch auf Tagegeld nach Absatz 1. Bei Dienstgängen von mehr als acht Stunden Dauer werden die nachgewiesenen notwendigen Auslagen für Verpflegung bis zur Höhe des Tagegeldes bei einer Dienstreise von gleicher Dauer erstattet.

(4) Erhalten Dienstreisende ihres Amtes wegen unentgeltlich Verpflegung, werden von dem ihnen zustehenden Tagegeld nach Absatz 1 für das Frühstück 20 vom Hundert und für das Mittagessen und Abendessen je 40 vom Hundert des Tagegeldes für einen vollen Kalendertag einbehalten. Das Gleiche gilt, wenn von dritter Seite Verpflegung bereitgestellt wird und hierfür das Entgelt in den erstattungsfähigen Fahrt-, Flug-, Übernachtungs- oder Nebenkosten enthalten ist. Die Sätze 1 und 2 sind auch dann anzuwenden, wenn die Dienstreisenden ihres Amtes wegen unentgeltlich bereitgestellte Verpflegung ohne triftigen Grund nicht in Anspruch nehmen.

zur Einzelansicht § 6

§ 7
Übernachtungsgeld
(1) Für eine notwendige Übernachtung erhalten Dienstreisende pauschal 20 Euro im Inland und 30 Euro im Ausland. Höhere Übernachtungskosten werden im notwendigen Umfang erstattet. Durch Verwaltungsvorschrift wird bestimmt, bis zu welcher Höhe Übernachtungskosten notwendig sind.

(2) Übernachtungsgeld wird nicht gewährt

1.
für die Dauer der Benutzung von Beförderungsmitteln,

2.
für die Dauer des Aufenthalts in einer Wohnung der oder des Dienstreisenden,

3.
bei unentgeltlicher Bereitstellung einer Unterkunft von Amts wegen, auch wenn diese Unterkunft ohne triftigen Grund nicht genutzt wird oder

4.
in den Fällen, in denen das Entgelt für die Unterkunft in den erstattungsfähigen Fahrtkosten oder sonstigen Kosten enthalten ist, es sei denn, dass eine Übernachtung aufgrund einer zu frühen Ankunft am Geschäftsort oder einer zu späten Abfahrt von diesem zusätzlich erforderlich wird.


zur Einzelansicht § 7

§ 8
Auslagenerstattung bei längerem Aufenthalt
am Geschäftsort
Dauert der Aufenthalt an demselben auswärtigen Geschäftsort länger als sieben Tage, so wird vom achten Tag an die gleiche Vergütung gewährt, die von diesem Tag an bei einer Abordnung zu gewähren wäre. Zu den Aufenthaltstagen zählen alle Tage zwischen dem Anreisetag und dem Abreisetag.

zur Einzelansicht § 8

§ 9
Aufwands- und Pauschvergütung
(1) Dienstreisende, denen erfahrungsgemäß geringere Aufwendungen für Verpflegung und Unterkunft als allgemein entstehen, können nach näherer Bestimmung der obersten Dienstbehörde oder der von ihr ermächtigten nachgeordneten Behörde anstelle von Tagegeld, Übernachtungsgeld und Auslagenerstattung nach § 8 Satz 1 und 2 entsprechend den notwendigen Aufwendungen mit einer Aufwandsvergütung abgefunden werden.

(2) Die oberste Dienstbehörde oder die von ihr ermächtigte nachgeordnete Behörde kann bei regelmäßigen oder gleichartigen Dienstreisen anstelle der Reisekostenvergütung oder einzelner ihrer Bestandteile eine Pauschvergütung gewähren, die nach dem Durchschnitt der in einem bestimmten Zeitraum sonst anfallenden Einzelvergütungen zu bemessen ist.

zur Einzelansicht § 9

§ 10
Erstattung sonstiger Kosten
(1) Zur Erledigung des Dienstgeschäfts notwendige Auslagen, die nicht nach den §§ 4 bis 9 zu erstatten sind, werden als Nebenkosten erstattet.

(2) Entfallen Dienstreisen aus Gründen, die von den Dienstreisenden nicht zu vertreten sind, werden die durch die Vorbereitung entstandenen notwendigen, nach diesem Gesetz berücksichtigungsfähigen Auslagen erstattet.

zur Einzelansicht § 10

§ 11
Bemessung der Reisekostenvergütung
in besonderen Fällen
(1) Bei Dienstreisen aus Anlass der Versetzung, Abordnung oder Aufhebung einer Abordnung wird das Tagegeld (§ 6) für die Zeit bis zur Ankunft am neuen Dienstort gewährt. Das Tagegeld wird für die Zeit bis zum Ablauf des Ankunftstages gewährt, wenn die Dienstreisenden vom nächsten Tag an Trennungsgeld für auswärtiges Verbleiben erhalten; daneben wird Übernachtungsgeld (§ 7) gewährt.

(2) Für Reisen zum Zwecke der Fortbildung, die zumindest teilweise im dienstlichen Interesse liegen, können entstandene Kosten bis zur Höhe der für Dienstreisen zustehenden Reisekostenvergütung erstattet werden.

(3) Werden Dienstreisen mit einer Urlaubsreise oder einer anderen privaten Reise verbunden, wird die Reisekostenvergütung so bemessen, als ob nur die Dienstreise durchgeführt worden wäre. Die Reisekostenvergütung nach Satz 1 darf die sich nach dem tatsächlichen Reiseverlauf ergebende Reisekostenvergütung nicht übersteigen.

(4) Wird angeordnet oder genehmigt, dass die Dienstreise am Urlaubsort anzutreten oder zu beenden ist, wird die Reisekostenvergütung abweichend von Absatz 3 nach der Abreise von oder der Ankunft an diesem Ort bemessen.

(5) Wird aus dienstlichen Gründen die vorzeitige Beendigung einer Urlaubsreise oder einer anderen privaten Reise angeordnet, gilt die Rückreise vom Urlaubs- oder Aufenthaltsort zur Dienststätte als Dienstreise, für die Reisekostenvergütung gewährt wird.

(6) Aufwendungen der Dienstreisenden und der sie begleitenden Personen, die durch die Unterbrechung oder die vorzeitige Beendigung einer Urlaubsreise oder einer anderen privaten Reise verursacht worden sind, werden in angemessenem Umfang erstattet. Dies gilt auch für Aufwendungen, die aus diesen Gründen nicht ausgenutzt werden konnten.

(7) Erkranken Dienstreisende und werden sie in ein Krankenhaus aufgenommen, werden für jeden vollen Kalendertag des Krankenhausaufenthalts die notwendigen Auslagen für die Unterkunft am Geschäftsort erstattet.

(8) Für Fahrten zwischen Wohnung und regelmäßiger Dienststätte aus besonderem dienstlichen Anlass können die entstandenen notwendigen Fahrtkosten erstattet werden.

zur Einzelansicht § 11

§ 12
Auslandsdienstreisen
(1) Auslandsdienstreisen sind Dienstreisen zwischen dem Inland und dem Ausland sowie im Ausland. Dabei muss mindestens ein Geschäftsort im Ausland liegen.

(2) Für Auslandsdienstreisen gelten die Regelungen der §§ 1 bis 11 entsprechend.

(3) Abweichend von den §§ 6 und 7 werden Auslandstagegelder und Auslandsübernachtungsgelder nach Maßgabe der jeweils gültigen Fassung des § 3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift über die Neufestsetzung der Auslandstage- und Auslandsübernachtungsgelder (ARVVwV) gewährt.

(4) Das Tage- und Übernachtungsgeld wird für das Land gewährt, das die Dienstreisenden vor Mitternacht Ortszeit zuletzt erreichen. Wird bei Auslandsdienstreisen das Inland vor Mitternacht zuletzt erreicht, wird Auslandstagegeld für das Land des letzten Geschäftsortes im Ausland gewährt.

(5) Bei Flugreisen gilt ein Land in dem Zeitpunkt als erreicht, in dem das Flugzeug dort landet. Zwischenlandungen bleiben unberücksichtigt, es sei denn, dass durch sie Übernachtungen notwendig werden. Bei Schiffsreisen gilt Satz 1 entsprechend.

(6) Dauert der Aufenthalt an demselben ausländischen Geschäftsort ohne Hin- und Rückreisetage länger als 14 Tage, ist das Auslandstagegeld nach Absatz 3 vom 15. Tag an um 25 vom Hundert zu ermäßigen. Die oberste Dienstbehörde oder die von ihr ermächtigte nachgeordnete Behörde kann in begründeten Fällen von der Ermäßigung absehen. Anstelle des pauschalen Übernachtungsgeldes werden ab dem 15. Tag die nachgewiesenen notwendigen Übernachtungskosten erstattet.

zur Einzelansicht § 12

§ 13
Trennungsgeld
(1) Beamtinnen, Beamte, Richterinnen und Richter, die ohne Zusage der Umzugskostenvergütung an einen Ort außerhalb des Dienst- oder Wohnortes abgeordnet werden, erhalten für die ihnen dadurch entstehenden notwendigen Auslagen unter Berücksichtigung der häuslichen Ersparnis ein Trennungsgeld. Dasselbe gilt für die vorübergehende Zuteilung aus dienstlichen Gründen zu einem anderen Teil der Beschäftigungsbehörde und der vorübergehenden dienstlichen Tätigkeit bei einer anderen Stelle als der Dienststelle. Der Abordnung steht die Zuweisung nach § 20 des Beamtenstatusgesetzes gleich. Das Finanzministerium wird ermächtigt eine Rechtsverordnung zur Regelung des Trennungsgeldes zu erlassen.

(2) Absatz 1 gilt auch für Beamtinnen und Beamten auf Widerruf im Vorbereitungsdienst bei Abordnungen im Rahmen der Ausbildung. Der für die Ausbildung maßgebliche Dienstort wird von der obersten Dienstbehörde oder der von ihr ermächtigten nachgeordneten Behörde bestimmt. Satz 1 gilt auch bei Abordnungen im Rahmen des Ausbildungs- oder Einführungsdienstes, einer Ausbildungs- oder Einführungszeit, die zum Erwerb einer Laufbahnbefähigung notwendig sind.

zur Einzelansicht § 13

§ 14
Ermächtigung, Verwaltungsvorschriften
(1) Das Finanzministerium wird ermächtigt, durch Rechtsverordnung die in den §§ 5 und 7 Absatz 1 festgesetzten Beträge veränderten wirtschaftlichen Verhältnissen anzupassen.

(2) Die allgemeinen Verwaltungsvorschriften zu diesem Gesetz erlässt das Finanzministerium.

zur Einzelansicht § 14

§ 15
Inkrafttreten
(1) Dieses Gesetz tritt am 1. Januar 2022 in Kraft. Gleichzeitig treten das Landesreisekostengesetz in der Fassung vom 20. Mai 1996 (GBl. S. 466), das zuletzt durch Artikel 2 des Gesetzes zur Weiterentwicklung des Klimaschutzes in Baden-Württemberg vom 15. Oktober 2020 (GBl. S. 937, 943) geändert worden ist, die Auslandsreisekostenverordnung des Landes vom 2. Januar 1984 (GBl. S. 33), die zuletzt durch Verordnung vom 20. November 2015 (GBl. S. 1057) geändert worden ist, und die Verordnung des Finanzministeriums über die Reisekostenvergütung in besonderen Fällen vom 4. März 1975 (GBl. S. 200), die zuletzt durch Artikel 3 der Verordnung vom 12. Dezember 1985 (GBl. S. 409, 411) geändert worden ist, außer Kraft.

(2) Für Dienstreisen, die bis zum 31. Dezember 2021 angetreten werden, gelten die Vorschriften des Landesreisekostengesetzes, der Auslandsreisekostenverordnung des Landes und die Verordnung des Finanzministeriums über die Reisekostenvergütung in besonderen Fällen jeweils in der Fassung vom 31. Dezember 2021. Dies gilt auch, wenn die Dienstreise bis zum 31. Dezember 2021 angetreten wurde und über den Zeitpunkt des Inkrafttretens dieses Gesetzes hinaus andauert.

zur Einzelansicht § 15"""

def initial_prompt (DOMAIN):
    prompt = f"""
Given the context of the document {DOMAIN}, design a structured, logically coherent, directed acyclic dialog flow suitable for visualization with mermaid.js.
The flow must model a realistic conversation between a user and a bot.

Core Behavior

The user always starts with a vague, practical question in natural language (e.g., about reimbursement, travel costs, accommodation, etc.).
Never assume the user knows technical terms or the content of the document.
The bot guides the user through progressive narrowing:
Broad intent
More specific question
Final informative answer

Final Information Nodes

Every dialog path must terminate in a FINAL INFORMATION NODE.

A FINAL INFORMATION NODE contains actual, concrete information from {DOMAIN}, such as:

specific amounts, reimbursement rates, thresholds, requirements etc

Example final answers:

“Bei Nutzung des privaten PKW werden 0,30 €/km erstattet.”

“Übernachtungskosten werden gegen Beleg bis zu … erstattet.”

The flow must be simple:
broad question → specific question → final information node.


    Adhere to the following guidelines:

    Document-Grounded: All answers must be derived strictly from the document’s content. The bot has no external knowledge.
    Nodes Definition: Use distinct nodes to represent the bot ("B") and the user ("U").
    High-Level Dialog Action: Each node should encapsulate that segment's core sentiment or function in the conversation, relevant this document {DOMAIN}. It should be a label for the node representing a high-level dialogue action and not just the dialogue.
    Flow & Directionallty: Create directed connections between nodes to represent the progression of the conversation. The dialogue should flow from one node to potentially multiple nodes, allowing for various conversational turns.
    Diverse Conversational Possibilities: Ensure that bot nodes can lead to multiple user nodes and vice versa. This should account for various user responses or bot prompts, showcasing the range of interactions possible within this document {DOMAIN}.
    Acyclic Structure: The dialog flow must not have loops or cyclic pathways. If a similar action or sentiment arises later in the conversation, introduce a new node to represent it, rather than looping back to an earlier node.
    Mermaid.js Compatibility: Ensure that the constructed flow is adherent to mermaid.js graph notation, guaranteeing its seamless rendering.
    Considering the guidelines, craft a dialogue flow focused on {DOMAIN}. The bot always begins by greeting the user and asking for what they want. The graph should be connected. The bot and user nodes should be in different colors. A bot node is only followed by user nodes and user nodes are by bot nodes.
    """
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
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
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()

def update_prompt(flow, feedback):
    prompt = f"""Taking into consideration the {feedback} and the original design guidelines - keep it in directed acyclic graph structure and make sure all new components are labeled and connected to the graph correctly- revise the {flow} . Ensure your revised flow addresses the identified areas of improvement while still adhering to the primary instructions for flow construction. Make sure to account for all new nodes including merged nodes and their labels/colors.
    Make sure all user nodes connect with bot nodes and bot nodes are the end of the conversations. Give your updates in the below format:
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
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
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
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
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
    
