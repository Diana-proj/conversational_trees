```mermaid
%%{ init: { "theme": "default", "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "linear" } } }%%
%%{init: { "flowchart": { "htmlLabels": true }, "themeVariables": { "fontSize": "12px" } }}%%

graph TD
 Root["Was möchten Sie zur Planung, Durchführung oder Abrechnung von Dienstreisen wissen?"]

  %% Category 1
  C1["1) Anordnung, Definitionen und grundsätzliche Regeln"]
  Root --> C1

  C1A["1.1) Begriff und Genehmigung"]
  C1B["1.2) Abgrenzung Dienstreise / Dienstgang und Ausgangspunkte"]
  C1 --> C1A
  C1 --> C1B

  C1A1["Was ist eine Dienstreise / Dienstgang?"]
  C1A2["Genehmigungspflichten und Ausnahmen"]
  C1A --> C1A1
  C1A --> C1A2

  Q1A1["Buchung: Muss eine Dienstreise vorab schriftlich/e-\\nordnung/genehmigt werden?"]
  Q1A2["Buchung: Gibt es Ausnahmen (z. B. Richterinnen, Beauftragte)?"]
  C1A1 --> Q1A1
  C1A1 --> Q1A2

  Q1A3["Buchung: Dürfen Dienstreisen nur durchgeführt werden,\\nwenn keine kostengünstigere Erledigung möglich ist?"]
  Q1A4["Buchung: Welche formalen Regeln gelten für die Anordnung\\n(z. B. Zuständigkeit, Form)?"]
  C1A2 --> Q1A3
  C1A2 --> Q1A4

  C1B1["Abgrenzung Dienstreise vs. Dienstgang"]
  C1B2["Ausgangs-/Endpunkt der Dienstreise; Wohnung(en)"]
  C1B --> C1B1
  C1B --> C1B2

  Q1B1["Buchung: Besteht für Dienstgänge Anspruch auf Tagegeld?\\nWie werden längere Dienstgänge (>8h) vergütet?"]
  Q1B2["Buchung: Wann gilt ein Einsatz als Dienstgang statt\\nals Dienstreise (rechtliche Kriterien)?"]
  C1B1 --> Q1B1
  C1B1 --> Q1B2

  Q1B3["Buchung: Darf ich Ausgangs- und Endpunkt selbst bestimmen?"]
  Q1B4["Buchung: Kann Dienstvorgesetzte die Dienststätte als\\nAusgang/Endpunkt anordnen und wann ist das zulässig?"]
  C1B2 --> Q1B3
  C1B2 --> Q1B4

  Q1B5["Buchung: Wie wird Fahrtkostenerstattung berechnet, wenn\\nReise an der Wohnung an- oder beendet wird?"]
  Q1B6["Buchung: Welche Wohnung/Unterkunft ist maßgebend bei\\nmehreren Wohnsitzen?"]
  C1B2 --> Q1B5
  C1B2 --> Q1B6

  %% Category 2
  C2["2) Vergütung, Fahrtkosten und Beförderungsmittel"]
  Root --> C2

  C2A["2.1) Grundsätze zur Wahl des Beförderungsmittels"]
  C2B["2.2–2.4) Fahrt-, Flugkosten, Sonderregeln, Mietwagen/Taxi"]
  C2 --> C2A
  C2 --> C2B

  C2A1["Freiheit & Einschränkungen bei Wahl des Beförderungsmittels"]
  C2A2["Klimaschutz, unentgeltliche Beförderung und Erstattungs-\\ngrundsätze"]
  C2A --> C2A1
  C2A --> C2A2

  Q2A1["Buchung: Bin ich frei in der Wahl des Verkehrsmittels\\noder gibt es Einschränkungen?"]
  Q2A2["Buchung: Muss ich die Erfordernisse des Klimaschutzes\\nbei Wahl beachten (z. B. ÖPNV vor Auto)?"]
  C2A1 --> Q2A1
  C2A1 --> Q2A2

  Q2A3["Buchung: Werden Fahrtkosten nicht erstattet, wenn eine\\nunentgeltliche Beförderungsmöglichkeit besteht?"]
  Q2A4["Buchung: Welche Rolle haben Dienstinteresse und\\nWirtschaftlichkeit bei der Entscheidung?"]
  C2A2 --> Q2A3
  C2A2 --> Q2A4

  C2B1["2.2) Fahrt- und Flugkostenerstattung (Klassen, Ausnahmen)"]
  C2B2["2.3/2.4) Mietwagen/Taxi/Carsharing & Klimaausgleich bei Flügen"]
  C2 --> C2B1
  C2 --> C2B2

  C2B1a["Erstattung der jeweils niedrigsten Klasse; Ausnahmen"]
  C2B1b["Flüge: Erstattungsfähigkeit und besondere Regeln"]
  C2B1 --> C2B1a
  C2B1 --> C2B1b

  Q2B1["Buchung: Bis zu welcher Klasse werden Kosten für\\nregelmäßig verkehrende Beförderungsmittel erstattet?"]
  Q2B2["Buchung: Unter welchen Voraussetzungen sind Ausnahmen\\nvon der niedrigsten Klasse zulässig?"]
  C2B1a --> Q2B1
  C2B1a --> Q2B2

  Q2B3["Buchung: Sind Flugkosten grundsätzlich erstattungsfähig\\nund unter welchen Bedingungen dürfen sie genutzt werden?"]
  Q2B4["Buchung: Werden bei Flugreisen nur Kosten der niedrigsten\\nFlugklasse erstattet?"]
  C2B1b --> Q2B3
  C2B1b --> Q2B4

  C2B1c["Höhere Klasse bei Behinderung/Gesundheit"]
  C2B1 --> C2B1c
  Q2B5["Buchung: Wann wird bei GdB ≥ 50 die nächsthöhere Klasse\\nübernommen?"]
  Q2B6["Buchung: Können auch andere Reisende aus Gesundheits-\\ngründen höhere Klasse erstattet bekommen?"]
  C2B1c --> Q2B5
  C2B1c --> Q2B6

  C2B2a["Mietwagen, Taxi, Carsharing: Grundsätze"]
  C2B2b["Klimaausgleich und Vorgaben bei Flugreisen"]
  C2B2 --> C2B2a
  C2B2 --> C2B2b

  Q2B7["Buchung: Werden Mietwagen-/Taxi-/Carsharing-Kosten\\nerstattet und bei welchem triftigen Grund?"]
  Q2B8["Buchung: Dürfen ohne triftigen Grund höhere Vergütungen\\nals ÖPNV gewährt werden?"]
  C2B2a --> Q2B7
  C2B2a --> Q2B8

  Q2B9["Buchung: Erfolgt bei Carsharing eine Kürzung der\\nMitgliedsgebühr wegen privater Nutzung?"]
  Q2B10["Buchung: Muss bei Flügen eine Klimaausgleichszahlung\\nberücksichtigt werden und wie?"]
  C2B2a --> Q2B9
  C2B2b --> Q2B10

  Q2B11["Buchung: Gibt es besondere Vorgaben für Mitglieder der\\nLandesregierung, Ministerien und Hochschulen bzgl.\\njährlicher Ausgleichszahlungen?"]
  Q2B12["Erstattung: Gelten Ausgleichszahlungen für Flüge, die von\\nHochschulen aus Drittmitteln bezahlt werden?"]
  C2B2b --> Q2B11
  C2B2b --> Q2B12

  %% Category 3
  C3["3) Wegstreckenentschädigung (km‑Sätze, Fahrrad, Zuschläge)"]
  Root --> C3

  C3A["3.1) Private Kraftfahrzeuge & km-Sätze"]
  C3B["3.2/3.3) Zuschläge & Radfahren (E-Bike/Pedelec)"]
  C3 --> C3A
  C3 --> C3B

  Q3A1["Buchung: Welche Wegstreckenentschädigung gilt für\nFahrten mit privatem Kraftfahrzeug (Cent/km)?"]
  Q3A2["Buchung: Wann erhöht sich die Wegstreckenentschädigung\nauf 35 Cent/km?"]
  C3A --> Q3A1
  C3A --> Q3A2

  C3B1["Zuschläge für schwierige Wege"]
  C3B2["Fahrrad / E‑Bike / Pedelec"]
  C3B --> C3B1
  C3B --> C3B2

  Q3B1["Buchung: Kann bei Fahren auf unbefestigten oder schwer\nbefahrbaren Wegen ein Zuschlag gewährt werden und wie hoch?"]
  Q3B2["Buchung: Welche Nachweise/Anforderungen gelten für Zuschläge?"]
  C3B1 --> Q3B1
  C3B1 --> Q3B2

  Q3B3["Buchung: Welche Wegstreckenentschädigung gilt bei Fahrten\nmit Fahrrad, E‑Bike oder Pedelec?"]
  Q3B4["Buchung: Gilt Besonderes bei häufiger Nutzung von\nDienstfahrrädern oder Dienstradleasing?"]
  C3B2 --> Q3B3
  C3B2 --> Q3B4

  %% Category 4
  C4["4) Tagegeld (Sätze, Dauer, Kürzungen)"]
  Root --> C4

  C4A["4.1) Höhe und Bemessung der Tagegelder"]
  C4B["4.2/4.3) Reisedauerbestimmung und Kürzungen bei Verpflegung"]
  C4 --> C4A
  C4 --> C4B

  Q4A1["Buchung: Wie hoch ist das Tagegeld für jeden vollen\nKalendertag einer Dienstreise?"]
  Q4A2["Buchung: Wie viel Tagegeld steht für An-/Abreisetag bei\nmehrtägigen Dienstreisen zu (bei >8h und >14h)?"]
  C4A --> Q4A1
  C4A --> Q4A2

  C4B1["Bestimmung der Reisedauer (Abreise/Ankunft)"]
  C4B2["Kürzung bei unentgeltlicher Verpflegung"]
  C4B --> C4B1
  C4B --> C4B2

  Q4B1["Buchung: Nach welchen Zeitpunkten bestimmt sich die\nDauer der Dienstreise (Abreise/Ankunft bezogen auf Wohnung/Dienststätte)?"]
  Q4B2["Buchung: Wie werden Zeitzonen, Nachtfahrten und Zwischen-\\nlandungen berücksichtigt?"]
  C4B1 --> Q4B1
  C4B1 --> Q4B2

  Q4B3["Buchung: Wie wird das Tagegeld gekürzt, wenn Verpflegung\nunentgeltlich gewährt wird (Frühstück/Mittag/Abend in %)?"]
  Q4B4["(siehe 1.2) Buchung: Besteht für Dienstgänge ein Anspruch\nauf Tagegeld und wie werden längere Dienstgänge vergütet?"]
  C4B2 --> Q4B3
  C4B2 --> Q4B4

  %% Category 5
  C5["5) Übernachtungsgeld, Langzeitaufenthalte und Auslagenerstattung"]
  Root --> C5

  C5A["5.1/5.2) Pauschbeträge, Erstattung höherer Kosten & Ausschlüsse"]
  C5B["5.3/5.4) Langzeitregelungen (ab 8./15. Tag) und Auslandsbesonderheiten"]
  C5 --> C5A
  C5 --> C5B

  Q5A1["Buchung: Wie hoch ist das pauschale Übernachtungsgeld\nim Inland und im Ausland?"]
  Q5A2["Buchung: Werden höhere Übernachtungskosten ersetzt und\nwer legt Höchstgrenzen durch Verwaltungsvorschrift fest?"]
  C5A --> Q5A1
  C5A --> Q5A2

  Q5A3["Buchung: In welchen Fällen wird Übernachtungsgeld nicht\ngewährt (z. B. eigene Wohnung, unentgeltliche Unterkunft,\\nwenn Unterkunftskosten in Fahrtkosten enthalten sind)?"]
  Q5A4["Buchung: Wie ist zu verfahren, wenn Übernachtungskosten\nTeil eines Ticketpreises sind (z. B. Bahnreise mit Hotel)?"]
  C5A --> Q5A3
  C5A --> Q5A4

  C5B1["Auslagenerstattung bei längerem Aufenthalt ab 8. Tag"]
  C5B2["Sonderregel Langzeit im Ausland ab 15. Tag"]
  C5B --> C5B1
  C5B --> C5B2

  Q5B1["Buchung: Wann werden Auslagenerstattungen ab dem 8. Tag\ngezahlt und wie werden sie bemessen (Pauschalen)?"]
  Q5B2["Buchung: Können ab dem 15. Tag im Ausland anstelle des\npauschalen Übernachtungsgeldes die nachgewiesenen\nnotwendigen Übernachtungskosten erstattet werden?"]
  C5B1 --> Q5B1
  C5B1 --> Q5B2

  Q5B3["Buchung: Wann wird Auslandstagegeld ab dem 15. Tag um\n25% ermäßigt und wer kann davon absehen?"]
  Q5B4["Buchung: Wer kann in begründeten Fällen von der Ermäßigung\nabsehen (z. B. Dienststelle, oberste Behörde)?"]
  C5B2 --> Q5B3
  C5B2 --> Q5B4

  %% Category 6
  C6["6) Aufwands‑und Pauschvergütung / Nebenkosten"]
  Root --> C6

  C6A["6.1) Aufwandsvergütung statt Einzelvergütungen"]
  C6B["6.2/6.3) Pauschvergütungen und sonstige Nebenkosten (§10)"]
  C6 --> C6A
  C6 --> C6B

  Q6A1["Buchung: Können Dienstreisende anstelle von Tagegeld,\nÜbernachtungsgeld und Auslagenerstattung eine Aufwands-\\nvergütung erhalten und unter welchen Bedingungen?"]
  Q6A2["Buchung: Welche Form der Erklärung oder Vereinbarung ist\nnotwendig, um Aufwandsvergütung zu erhalten?"]
  C6A --> Q6A1
  C6A --> Q6A2

  Q6B1["Buchung: Kann die oberste Dienstbehörde Pauschvergütungen\nfür regelmäßige oder gleichartige Dienstreisen festlegen?"]
  Q6B2["Buchung: Welche sonstigen notwendigen Nebenkosten können\nerstattet werden, wenn sie nicht unter §§ 4–9 fallen?"]
  C6B --> Q6B1
  C6B --> Q6B2

  Q6B3["Buchung: Gibt es Obergrenzen oder besondere Befugnisse zur\nFestsetzung von Pauschalen (Zuständigkeiten)?"]
  Q6B4["Erstattung: Wie sind Nachweise bei Pauschalvergütungen zu\nhandhaben (Belege, Prüfpflichten)?"]
  C6B --> Q6B3
  C6B --> Q6B4

  %% Category 7
  C7["7) Besondere Fälle / Bemessung bei Versetzung, Fortbildung, Krankheit, Urlaub"]
  Root --> C7

  C7A["7.1/7.2) Versetzung, Abordnung & Fortbildung/Nebentätigkeit"]
  C7B["7.3/7.4/7.5) Kombination mit Urlaub, Krankheit, Fahrten zur Dienststätte"]
  C7 --> C7A
  C7 --> C7B

  Q7A1["Buchung: Welche Besonderheiten gelten bei Versetzung,\nAbordnung oder Aufhebung einer Abordnung (Tagegeld/Übernachtung)?"]
  Q7A2["Buchung: Können Kosten für Fortbildungen erstattet werden,\nwenn sie teilweise dienstlich sind?"]
  C7A --> Q7A1
  C7A --> Q7A2

  Q7A3["Buchung: Haben Dienstreisende Anspruch auf Reisekosten-\\nvergütung für Nebentätigkeiten, wenn eine andere Stelle\nAuslagenerstattung gewährt?"]
  Q7A4["Buchung: Welche Abstimmungsregeln gelten zwischen\nStellen bei Mehrfachleistungen?"]
  C7A --> Q7A3
  C7A --> Q7A4

  Q7B1["Buchung: Wie wird die Vergütung bemessen, wenn Dienstreisen\nmit Urlaubs- oder Privatreise kombiniert werden?"]
  Q7B2["Buchung: Welche Sonderregel gilt, wenn die Dienstreise am\nUrlaubsort an- oder zu beenden ist und angeordnet wurde?"]
  C7B --> Q7B1
  C7B --> Q7B2

  Q7B3["Buchung: Wie werden Aufwendungen bei vorzeitiger Beendigung\nvon Urlaub/Privatreise auf Anordnung behandelt?"]
  Q7B4["Buchung: Werden bei Krankheit/Krankenhausaufnahme die\nnotwendigen Unterkunftsauslagen für jeden vollen Tag erstattet?"]
  C7B --> Q7B3
  C7B --> Q7B4

  Q7B5["Buchung: Können Fahrten Wohnung ↔ regelmäßige Dienststätte\naus besonderem dienstlichem Anlass erstattet werden?"]
  Q7B6["Buchung: Welche Nachweise sind bei solchen Fahrten\nerforderlich (Anordnung, Dienstanlass)?"]
  C7B --> Q7B5
  C7B --> Q7B6

  %% Category 8
  C8["8) Auslandsdienstreisen (Definition, Bemessung, Sonderregelungen)"]
  Root --> C8

  C8A["8.1/8.2) Begriff, Anwendungsbereich & Rechtsgrundlagen"]
  C8B["8.3/8.4) Zeitliche Bestimmung bei Flug/Schiff & Längerer Aufenthalt"]
  C8 --> C8A
  C8 --> C8B

  Q8A1["Buchung: Gelten besondere Regelungen für Auslandsdienstreisen\nund was ist darunter zu verstehen?"]
  Q8A2["Buchung: Für welches Land wird Tage- und Übernachtungsgeld\ngewährt, wenn vor Mitternacht zuletzt ein bestimmtes Land erreicht wurde?"]
  C8A --> Q8A1
  C8A --> Q8A2

  Q8A3["Erstattung: Nach welchen Regelungen werden Auslandstage- und\nAuslandsübernachtungsgelder bemessen (ARV/ARVVwV)?"]
  Q8A4["Erstattung: Wie ist die Bemessung konkret für typische Länder\n/ Pauschalen festgelegt?"]
  C8A --> Q8A3
  C8A --> Q8A4

  Q8B1["Buchung: Wie werden Zwischenlandungen bei Flug/Schiff für\ndie Länderbestimmung berücksichtigt?"]
  Q8B2["Erstattung: Wie ist zu verfahren, wenn Inland vor Mitternacht\nzuletzt erreicht wird (welches Auslandstagegeld gilt)?"]
  C8B --> Q8B1
  C8B --> Q8B2

  Q8B3["Buchung: Wann wird bei längeren Aufenthalten im Ausland\nab dem 15. Tag das Auslandstagegeld um 25% ermäßigt?"]
  Q8B4["Buchung: Wer kann in begründeten Fällen von der Ermäßigung\nabsehen und kann ab dem 15. Tag tatsächliche Übernachtungs-\\nkosten erstattet bekommen?"]
  C8B --> Q8B3
  C8B --> Q8B4

  %% Category 9
  C9["9) Trennungsgeld (Abordnung ohne Umzugskosten)"]
  Root --> C9

  C9A["9.1) Anspruchsvoraussetzungen"]
  C9B["9.2) Anwendbarkeit auf Auszubildende / Widerrufsdienstverhältnisse"]
  C9 --> C9A
  C9 --> C9B

  Q9A1["Buchung: Wann entsteht Anspruch auf Trennungsgeld bei\nAbordnung ohne Zusage von Umzugskostenvergütung?"]
  Q9A2["Buchung: Welche Faktoren bestimmen Höhe und Dauer des\nTrennungsgeldanspruchs?"]
  C9A --> Q9A1
  C9A --> Q9A2

  Q9B1["Buchung: Gilt Trennungsgeld auch für Beamtinnen/Beamte auf\nWiderruf im Vorbereitungsdienst bei bestimmten Abordnungen?"]
  Q9B2["Buchung: Welche Besonderheiten gelten für Auszubildende?"]
  C9B --> Q9B1
  C9B --> Q9B2

  %% Category 10
  C10["10) Erstattungspraxis, Anträge, Fristen, Belege, Anrechnung, Verzicht"]
  Root --> C10

  C10A["10.1/10.2) Antragstellung & Ausschlussfrist (6 Monate)"]
  C10B["10.3/10.4) Belege, Anrechnung Dritter, Verzicht"]
  C10 --> C10A
  C10 --> C10B

  Q10A1["Erstattung: Muss Reisekostenvergütung schriftlich oder\nelektronisch beantragt werden und wer erhält die Vergütung?"]
  Q10A2["Erstattung: Innerhalb welcher Frist (Ausschlussfrist) muss\ndie Vergütung nach Reiseende beantragt werden? Wann beginnt sie zu laufen?"]
  C10A --> Q10A1
  C10A --> Q10A2

  Q10B1["Erstattung: Können zuständige Stellen bis zu welchem\nZeitpunkt die Vorlage der Kostenbelege verlangen?"]
  Q10B2["Erstattung: Was passiert, wenn angeforderte Belege nicht\ninnerhalb eines Monats vorgelegt werden?"]
  C10B --> Q10B1
  C10B --> Q10B2

  Q10B3["Erstattung: Wie lange sind Kostenbelege nach Erstattung\naufzubewahren und vorzulegen (Aufbewahrungsfrist)?"]
  Q10B4["Erstattung: Werden Leistungen Dritter auf Reisekosten-\\nvergütung angerechnet und wie?"]
  C10B --> Q10B3
  C10B --> Q10B4

  Q10B5["Erstattung: Haben Dienstreisende Anspruch auf Vergütung\nfür Nebentätigkeiten, wenn eine andere Stelle Auslagenerstattung gewährt?"]
  Q10B6["Erstattung: Kann ganz oder teilweise auf Reisekostenvergütung\nverzichtet werden und in welcher Form muss das erfolgen?"]
  C10B --> Q10B5
  C10B --> Q10B6

  %% Category 11
  C11["11) Vorbereitungskosten, Nebenkosten und sonstige Erstattungen"]
  Root --> C11

  C11A["11.1) Vorbereitungsaufwand bei entfallener Dienstreise"]
  C11B["11.2) Sonstige notwendige Nebenkosten (§10)"]
  C11 --> C11A
  C11 --> C11B

  Q11A1["Buchung: Werden entstandene Vorbereitungsaufwendungen\nerstattet, wenn Dienstreisen aus Gründen entfallen, die nicht\nvon den Dienstreisenden zu vertreten sind?"]
  Q11A2["Erstattung: Unter welchen Bedingungen werden Kosten für\nVorbereitungen anerkannt (Nachweise, Ablehnungskriterien)?"]
  C11A --> Q11A1
  C11A --> Q11A2

  Q11B1["Buchung: Welche sonstigen notwendigen Auslagen (Nebenkosten)\nkönnen erstattet werden, wenn sie nicht unter §§ 4–9 fallen?"]
  Q11B2["Erstattung: Wie sind Abrechnungs- und Nachweispflichten\nfür Nebenkosten geregelt (Form, Betragshöhen)?"]
  C11B --> Q11B1
  C11B --> Q11B2

  %% Category 12
  C12["12) Administration, Verwaltungsvorschriften, Zuständigkeiten"]
  Root --> C12

  C12A["12.1) Befugnisse des Finanzministeriums & Anpassungen"]
  C12B["12.2/12.3) Zuständigkeiten für Ausnahmen, Pauschalen & Klima-\\nAusgleichspflichten"]
  C12 --> C12A
  C12 --> C12B

  Q12A1["Buchung: Welche Befugnisse hat das Finanzministerium zur\nAnpassung der in §§ 5 und 7 Abs. 1 festgesetzten Beträge?"]
  Q12A2["Buchung: Wer erlässt allgemeine Verwaltungsvorschriften und\nwie werden Sätze angepasst (Verfahren, Zuständigkeit)?"]
  C12A --> Q12A1
  C12A --> Q12A2

  Q12B1["Buchung: Wer kann Ausnahmen von der niedrigsten Klasse\noder Pauschalen zulassen (Zuständigkeiten, Fristen)?"]
  Q12B2["Buchung: Welche Pflichten haben Ministerien/Hochschulen\nbzgl. Klimaausgleichszahlungen (jährliche Ausgleichszahlungen)?"]
  C12B --> Q12B1
  C12B --> Q12B2

  Q12B3["Erstattung: Wie sind Melde- und Nachweispflichten für\nbesondere Vorgaben (z. B. Drittmittelfinanzierte Flüge) geregelt?"]
  Q12B4["Buchung: Wie können Dienststellen Ausnahmen begründen und\nprozesse zur Genehmigung gestalten?"]
  C12B --> Q12B3
  C12B --> Q12B4


  %% Answer leaves (kurze, gesetzesbasierte Antworten)

  Q1A1 --> A_Q1A1["Antwort: Ja. Dienstreisen sind schriftlich oder elektronisch anzuordnen/genehmigen (§2 Abs.1). Ausnahmen gelten nur, wenn Anordnung wegen Amt oder Wesen des Dienstgeschäfts nicht in Betracht kommt (§2 Abs.1)."]
  Q1A2 --> A_Q1A2["Antwort: Ja. Für Richter sowie bestimmte Beauftragte (z. B. Landesbeauftragte für Datenschutz, Beauftragte für Menschen mit Behinderungen) gilt keine Anordnungspflicht (§2 Abs.3)."]
  Q1A3 --> A_Q1A3["Antwort: Dienstreisen sollen nur erfolgen, wenn keine kostengünstigere Art der Erledigung möglich und sinnvoll ist (§2 Abs.1). Wirtschaftlichkeitsgrundsatz ist maßgeblich."]
  Q1A4 --> A_Q1A4["Antwort: Die Anordnung oder Genehmigung hat schriftlich oder elektronisch zu erfolgen; zuständigkeit liegt beim zuständigen Dienstvorgesetzten (§2 Abs.1). Ausnahmen nur wie im Gesetz geregelt."]

  Q1B1 --> A_Q1B1["Antwort: Für Dienstgänge besteht grundsätzlich kein Anspruch auf Tagegeld (§6 Abs.3). Bei Dienstgängen >8 Stunden werden notwendige Verpflegungsauslagen bis zur Höhe des Tagegeldes für gleich lange Dienstreisen ersetzt (§6 Abs.3)."]
  Q1B2 --> A_Q1B2["Antwort: Dienstgänge sind Erledigungen außerhalb der Dienststätte am Dienst- oder Wohnort und erfordern die Anordnung/Genehmigung durch den zuständigen Vorgesetzten (§2 Abs.2). Abgrenzung richtet sich nach Ort und Zweck."]
  Q1B3 --> A_Q1B3["Antwort: Ausgangs- und Endpunkt bestimmen die Dienstreisenden grundsätzlich selbst unter Beachtung der Wirtschaftlichkeit (§3 Abs.2)."]
  Q1B4 --> A_Q1B4["Antwort: Abweichend kann der Vorgesetzte die Dienststätte als Ausgang/Endpunkt anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt (§3 Abs.2)."]
  Q1B5 --> A_Q1B5["Antwort: Wenn die Reise an der Wohnung angetreten/ beendet wird, bemisst sich Fahrtkostenerstattung bzw. Wegstreckenentschädigung nach Entfernung von/bis Wohnung, sofern nicht die Dienststätte als Ausgang/Endpunkt angeordnet wurde (§3 Abs.2)."]
  Q1B6 --> A_Q1B6["Antwort: Bei mehreren Wohnungen gilt die der Dienststätte am nächsten gelegene Wohnung/Unterkunft als maßgeblich (§3 Abs.2)."]

  Q2A1 --> A_Q2A1["Antwort: Grundsätzlich herrscht Wahlfreiheit der Beförderungsmittel (§3 Abs.3), aber wirtschaftliche Gesichtspunkte und Klimaschutz sind zu beachten; sonstige Einschränkungen können dienstlich erfolgen."]
  Q2A2 --> A_Q2A2["Antwort: Ja. Bei Wahl des Beförderungsmittels sind neben Wirtschaftlichkeit insbesondere die Erfordernisse des Klimaschutzes zu beachten (§3 Abs.3)."]
  Q2A3 --> A_Q2A3["Antwort: Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann (§3 Abs.3)."]
  Q2A4 --> A_Q2A4["Antwort: Dienstinteresse und Wirtschaftlichkeit sind maßgebliche Kriterien; Dienstreisende müssen Auswahl unter Wirtschaftlichkeitsgesichtspunkten treffen (§2 Abs.1, §3 Abs.2–3)."]

  Q2B1 --> A_Q2B1["Antwort: Es werden die Kosten der niedrigsten Beförderungsklasse erstattet (§4 Abs.1 Satz1). Bei regelmäßig verkehrenden Verkehrsmitteln gilt dies ebenso (§4 Abs.1)."]
  Q2B2 --> A_Q2B2["Antwort: Ausnahmen können die oberste Dienstbehörde oder ermächtigte Behörde zulassen; Ausnahmen sind bei besonderen dienstlichen Gründen möglich (§4 Abs.1)."]
  Q2B3 --> A_Q2B3["Antwort: Flugkosten sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Flugnutzung gegenüber Klimaschutzbelangen überwiegen (§4 Abs.1). Die Wirtschaftlichkeitsberechnung muss dabei Ausgleichszahlungen berücksichtigen."]
  Q2B4 --> A_Q2B4["Antwort: Grundsätzlich werden die Kosten der niedrigsten Flugklasse erstattet; das Finanzministerium kann Ausnahmen per Verwaltungsvorschrift bestimmen (§4 Abs.1)."]

  Q2B5 --> A_Q2B5["Antwort: Bei GdB ≥ 50 wird die nächsthöhere Klasse erstattet; Gleiches kann bei anderem gesundheitlichen Zustand gewährt werden (§4 Abs.2)."]
  Q2B6 --> A_Q2B6["Antwort: Ja. Andere Dienstreisende können aus gesundheitlichen Gründen ebenfalls die nächsthöhere Klasse erhalten, wenn ihr Zustand das rechtfertigt (§4 Abs.2)."]

  Q2B7 --> A_Q2B7["Antwort: Mietwagen, Taxi oder Carsharing werden erstattet, wenn aus triftigem Grund benutzt (§4 Abs.3). Ohne triftigen Grund darf nicht mehr bezahlt werden als bei Nutzung öffentlicher Verkehrsmittel."]
  Q2B8 --> A_Q2B8["Antwort: Ohne triftigen Grund darf keine höhere Vergütung als beim ÖPNV gewährt werden (§4 Abs.3 Satz2). Wirtschaftlichkeit ist zu beachten."]
  Q2B9 --> A_Q2B9["Antwort: Bei Carsharing erfolgt keine Kürzung der Mitgliedsgebühr wegen privater Nutzung (§4 Abs.3 Satz3)."]
  Q2B10 --> A_Q2B10["Antwort: Ja. Die Kosten für Klimaausgleichszahlungen sind in die Wirtschaftlichkeitsbetrachtung einzubeziehen; zudem haben Behörden/Jede Berufseinrichtung jährliche Ausgleichszahlungen zu leisten (§4 Abs.1 Satz1; Abs.4)."]

  Q2B11 --> A_Q2B11["Antwort: Oberste Dienstbehörden und staatliche Hochschulen sind verpflichtet, jährliche Ausgleichszahlungen für dienstliche Flüge zu leisten; das gilt für Mitglieder der Landesregierung, Ministerien und nachgeordnete Behörden sowie Hochschulen (§4 Abs.4)."]
  Q2B12 --> A_Q2B12["Antwort: Ja. Bei Flügen, die von Projekten staatlicher Hochschulen aus Drittmitteln bezahlt werden, fällt eine Ausgleichszahlung an, sofern Drittmittelgeber dem nicht entgegenstehen (§4 Abs.4 Satz2)."]

  Q3A1 --> A_Q3A1["Antwort: Wegstreckenentschädigung für Privatkraftfahrzeug beträgt 30 Cent je Kilometer (§5 Abs.1)."]
  Q3A2 --> A_Q3A2["Antwort: Bei erheblichem dienstlichen Interesse erhöht sich die Entschädigung auf 35 Cent je km (§5 Abs.2)."]

  Q3B1 --> A_Q3B1["Antwort: Bei regelmäßigem Fahren auf unbefestigten oder schwer befahrbaren Wegen kann mit Zustimmung der obersten Dienstbehörde ein Zuschlag von 5 Cent/km gewährt werden (§5 Abs.2)."]
  Q3B2 --> A_Q3B2["Antwort: Der Zuschlag bedarf Zustimmung der obersten Dienstbehörde; Nachweise/Begründungen richten sich nach dienstlichen Vorgaben und der Zustimmungsvoraussetzung (§5 Abs.2)."]
  Q3B3 --> A_Q3B3["Antwort: Für Fahrten mit Fahrrad, E‑Bike oder Pedelec beträgt die Wegstreckenentschädigung 25 Cent je Kilometer (§5 Abs.3)."]
  Q3B4 --> A_Q3B4["Antwort: Bei häufiger Nutzung von Dienstfahrrädern oder Dienstradleasing können spezielle Regelungen der Dienststelle gelten; das Gesetz nennt hierfür keine besonderen Sätze außer §5 Abs.3."]

  Q4A1 --> A_Q4A1["Antwort: Das Tagegeld beträgt für jeden vollen Kalendertag 24 Euro (§6 Abs.1)."]
  Q4A2 --> A_Q4A2["Antwort: Für An-/Abreisetag: bei Dienstreisedauer >8 Std. 6 Euro, bei >14 Std. 12 Euro (§6 Abs.1)."]

  Q4B1 --> A_Q4B1["Antwort: Die Dauer richtet sich nach Abreise und Ankunft an der Wohnung, es sei denn die Reise beginnt/endet an der Dienststätte oder dies wurde so angeordnet (§6 Abs.2). Bei mehreren Wohnungen gilt die der Dienststätte nächste (§6 Abs.2)."]
  Q4B2 --> A_Q4B2["Antwort: Zeitzonen, Nachtfahrten und Zwischenlandungen sind gesetzlich nicht gesondert geregelt; maßgeblich bleiben Abreise/Ankunftszeitpunkte nach Ortszeit bzw. besondere Regeln bei Auslandsdienstreisen (§6, §12)."]
  Q4B3 --> A_Q4B3["Antwort: Bei unentgeltlicher Verpflegung wird das Tagegeld gekürzt: Frühstück 20 %, Mittag und Abendessen jeweils 40 % des vollen Tagegeldes (§6 Abs.4)."]
  Q4B4 --> A_Q4B4["Antwort: Für Dienstgänge besteht kein Anspruch auf Tagegeld; bei Dienstgängen >8 Std. werden nachgewiesene Verpflegungsauslagen bis zur Höhe des Tagegeldes für eine gleich lange Dienstreise ersetzt (§6 Abs.3)."]

  Q5A1 --> A_Q5A1["Antwort: Pauschales Übernachtungsgeld beträgt 20 Euro im Inland und 30 Euro im Ausland (§7 Abs.1)."]
  Q5A2 --> A_Q5A2["Antwort: Höhere notwendige Übernachtungskosten werden im notwendigen Umfang erstattet; Verwaltungsvorschrift legt fest, bis zu welcher Höhe Übernachtungskosten notwendig sind (§7 Abs.1)."]
  Q5A3 --> A_Q5A3["Antwort: Übernachtungsgeld wird nicht gewährt bei Benutzung von Beförderungsmitteln, Aufenthalt in eigener Wohnung, unentgeltlicher Amtsunterkunft oder wenn Unterkunftskosten im erstattungsfähigen Fahrpreis enthalten sind (Ausnahmen bei zusätzlicher Übernachtung) (§7 Abs.2)."]
  Q5A4 --> A_Q5A4["Antwort: Wenn Unterkunftskosten in Fahrt-/sonstigen Kosten enthalten sind, wird Übernachtungsgeld nicht gewährt, außer eine zusätzliche Übernachtung ist wegen sehr früher Ankunft/später Abfahrt notwendig (§7 Abs.2 Nr.4)."]

  Q5B1 --> A_Q5B1["Antwort: Dauert Aufenthalt an demselben auswärtigen Geschäftsort länger als 7 Tage, wird ab dem 8. Tag die Vergütung gezahlt, die bei einer Abordnung zu gewähren wäre (§8). Die Bemessung richtet sich nach §8 und ggf. §9."]
  Q5B2 --> A_Q5B2["Antwort: Im Ausland gilt ab dem 15. Tag, dass anstelle des pauschalen Übernachtungsgeldes die nachgewiesenen notwendigen Übernachtungskosten erstattet werden (§12 Abs.6)."]
  Q5B3 --> A_Q5B3["Antwort: Bei Auslandsaufenthalten ohne Hin-/Rückreisetage länger als 14 Tage wird das Auslandstagegeld ab dem 15. Tag um 25 % ermäßigt (§12 Abs.6)."]
  Q5B4 --> A_Q5B4["Antwort: Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann in begründeten Fällen von der Ermäßigung absehen; zudem kann statt Pauschale ab dem 15. Tag die tatsächliche Übernachtung erstattet werden (§12 Abs.6)."]

  Q6A1 --> A_Q6A1["Antwort: Ja. Dienstreisende, die erfahrungsgemäß geringere Aufwendungen haben, können anstelle einzelner Vergütungen mit Aufwandsvergütung abgefunden werden, nach näherer Bestimmung durch die oberste Dienstbehörde (§9 Abs.1)."]
  Q6A2 --> A_Q6A2["Antwort: Die Form der Regelung bestimmt die oberste Dienstbehörde; üblicherweise durch dienstliche Festlegung/Vereinbarung gemäß §9 Abs.1 (gesetzliche Pflicht zur näheren Bestimmung)."]
  Q6B1 --> A_Q6B1["Antwort: Ja. Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann bei regelmäßigen oder gleichartigen Dienstreisen Pauschvergütungen festlegen (§9 Abs.2)."]
  Q6B2 --> A_Q6B2["Antwort: Sonstige notwendige Nebenkosten, die nicht unter §§4–9 fallen, werden nach §10 erstattet, wenn sie zur Erledigung des Dienstgeschäfts notwendig sind (§10 Abs.1)."]
  Q6B3 --> A_Q6B3["Antwort: Zuständigkeiten zur Festsetzung von Pauschalen liegen bei der obersten Dienstbehörde bzw. ermächtigten nachgeordneten Behörden; Obergrenzen können durch Verwaltungsvorschrift geregelt werden (§9 Abs.2; §14)."]
  Q6B4 --> A_Q6B4["Antwort: Bei Pauschalvergütungen sind Nachweise und Prüfpflichten durch die zuständige Dienststelle zu regeln; das Gesetz verlangt Prüfungen und ggf. formale Vorgaben (§3 Abs.4, §10)."]

  Q7A1 --> A_Q7A1["Antwort: Bei Versetzung/Abordnung wird Tagegeld bis zur Ankunft am neuen Dienstort gewährt; Tagegeld bis Ablauf des Ankunftstages, wenn ab dem nächsten Tag Trennungsgeld gezahlt wird; zudem Übernachtungsgeld (§11 Abs.1)."]
  Q7A2 --> A_Q7A2["Antwort: Für Fortbildungen, die teilweise dienstlich sind, können Kosten bis zur Höhe der für Dienstreisen zustehenden Reisekostenvergütung erstattet werden (§11 Abs.2)."]
  Q7A3 --> A_Q7A3["Antwort: Bei Nebentätigkeiten haben Dienstreisende nur insoweit Anspruch nach diesem Gesetz, wie nicht eine andere Stelle Auslagenerstattung zu gewähren hat (§3 Abs.6)."]
  Q7A4 --> A_Q7A4["Antwort: Es gelten Abstimmungsregeln: Leistungen Dritter werden auf die Vergütung angerechnet; Abrechnungen sind abzustimmen (§3 Abs.5-6)."]

  Q7B1 --> A_Q7B1["Antwort: Wird die Dienstreise mit Urlaub/Privatreise kombiniert, wird die Vergütung so bemessen, als ob nur die Dienstreise durchgeführt worden wäre; sie darf die tatsächliche (günstigere) Vergütung nicht übersteigen (§11 Abs.3)."]
  Q7B2 --> A_Q7B2["Antwort: Wenn angeordnet/genehmigt ist, die Dienstreise am Urlaubsort anzutreten/zu beenden, wird die Vergütung abweichend nach Abreise/Ankunft an diesem Ort bemessen (§11 Abs.4)."]
  Q7B3 --> A_Q7B3["Antwort: Bei vorzeitiger Beendigung auf Anordnung gilt Rückreise vom Urlaubs-/Aufenthaltsort zur Dienststätte als Dienstreise; Aufwendungen sind angemessen zu erstatten (§11 Abs.5-6)."]
  Q7B4 --> A_Q7B4["Antwort: Bei Krankenhausaufnahme werden für jeden vollen Kalendertag die notwendigen Unterkunftsauslagen am Geschäftsort erstattet (§11 Abs.7)."]
  Q7B5 --> A_Q7B5["Antwort: Fahrten Wohnung↔regelmäßige Dienststätte können aus besonderem dienstlichen Anlass erstattet werden (§11 Abs.8)."]
  Q7B6 --> A_Q7B6["Antwort: Erforderliche Nachweise sind Anordnung oder Nachweis des dienstlichen Anlasses; konkrete Anforderungen richtet die Dienststelle (§11 Abs.8, §3)."]

  Q8A1 --> A_Q8A1["Antwort: Ja. Auslandsdienstreisen sind Dienstreisen zwischen Inland und Ausland oder im Ausland; es muss mindestens ein Geschäftsort im Ausland liegen (§12 Abs.1). §§1–11 gelten entsprechend (§12 Abs.2)."]
  Q8A2 --> A_Q8A2["Antwort: Das Tage- und Übernachtungsgeld wird für das Land gewährt, das vor Mitternacht Ortszeit zuletzt erreicht wurde; wird das Inland vor Mitternacht zuletzt erreicht, gilt das Land des letzten Geschäftsortes im Ausland (§12 Abs.4)."]
  Q8A3 --> A_Q8A3["Antwort: Auslandstage- und -übernachtungsgelder werden nach Maßgabe der Auslandsreisekostenverordnung (ARV) und der ARVVwV bemessen (§12 Abs.3)."]
  Q8A4 --> A_Q8A4["Antwort: Konkrete Pauschalen und Länderzuordnungen sind in der ARV und der ARVVwV festgelegt; die Dienststelle/Finanzministerium gibt die Zahlen vor (§12 Abs.3)."]

  Q8B1 --> A_Q8B1["Antwort: Zwischenlandungen bleiben unberücksichtigt, es sei denn, durch sie werden Übernachtungen notwendig; bei Flugreisen gilt ein Land als erreicht, wenn das Flugzeug dort landet (§12 Abs.5)."]
  Q8B2 --> A_Q8B2["Antwort: Wird bei Auslandsdienstreisen das Inland vor Mitternacht zuletzt erreicht, wird Auslandstagegeld für das Land des letzten Geschäftsortes im Ausland gewährt (§12 Abs.4 Satz2)."]
  Q8B3 --> A_Q8B3["Antwort: Bei Dauerauslandsaufenthalten ohne Hin-/Rückreisetage länger als 14 Tage ist das Auslandstagegeld ab dem 15. Tag um 25 % zu ermäßigen (§12 Abs.6)."]
  Q8B4 --> A_Q8B4["Antwort: Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann in begründeten Fällen von der Ermäßigung absehen; ab dem 15. Tag können nachgewiesene Übernachtungskosten erstattet werden (§12 Abs.6)."]

  Q9A1 --> A_Q9A1["Antwort: Anspruch entsteht bei Abordnung außerhalb des Dienst- oder Wohnortes ohne Zusage von Umzugskostenvergütung; Trennungsgeld deckt notwendige Auslagen unter Berücksichtigung häuslicher Ersparnis (§13 Abs.1)."]
  Q9A2 --> A_Q9A2["Antwort: Höhe und Dauer richten sich nach den hierdurch entstehenden notwendigen Auslagen und der häuslichen Ersparnis; das Finanzministerium kann eine Rechtsverordnung erlassen (§13 Abs.1 Satz2)."]
  Q9B1 --> A_Q9B1["Antwort: Ja. Absatz 1 gilt auch für Beamtinnen/Beamte auf Widerruf im Vorbereitungsdienst bei Abordnungen im Rahmen der Ausbildung (§13 Abs.2)."]
  Q9B2 --> A_Q9B2["Antwort: Für Auszubildende gelten die speziellen Regeln des Abs.2; der maßgebliche Ausbildungsdienstort wird durch die oberste Dienstbehörde bestimmt (§13 Abs.2)."]

  Q10A1 --> A_Q10A1["Antwort: Reisekostenvergütung ist schriftlich oder elektronisch zu beantragen; Vergütung wird den Dienstreisenden auf Antrag gezahlt (§3 Abs.1, Abs.4)."]
  Q10A2 --> A_Q10A2["Antwort: Ausschlussfrist 6 Monate nach Beendigung der Dienstreise; die Frist beginnt mit dem Tag nach Beendigung der Dienstreise (§3 Abs.4). In Fällen des §10 Abs.2 beginnt Frist mit dem Tag, an dem die Dienstreise geendet hätte."]

  Q10B1 --> A_Q10B1["Antwort: Zuständige Stellen können bis zum Ablauf von sechs Monaten nach Antragstellung die Vorlage der maßgeblichen Kostenbelege verlangen (§3 Abs.4)."]
  Q10B2 --> A_Q10B2["Antwort: Werden geforderte Belege nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden (§3 Abs.4)."]
  Q10B3 --> A_Q10B3["Antwort: Dienstreisende müssen Kostenbelege nach Erstattung bis zum Ablauf eines Jahres aufbewahren und auf Verlangen vorlegen (§3 Abs.4)."]
  Q10B4 --> A_Q10B4["Antwort: Leistungen Dritter, die Dienstreisende aus Anlass einer Dienstreise erhalten, sind auf die Reisekostenvergütung anzurechnen (§3 Abs.5)."]
  Q10B5 --> A_Q10B5["Antwort: Bei Nebentätigkeiten haben Dienstreisende nur insoweit Anspruch nach diesem Gesetz, wie nicht eine andere Stelle Auslagenerstattung gewährt (§3 Abs.6)."]
  Q10B6 --> A_Q10B6["Antwort: Auf die Reisekostenvergütung kann ganz oder teilweise verzichtet werden; der Verzicht ist schriftlich oder elektronisch zu erklären (§3 Abs.7)."]

  Q11A1 --> A_Q11A1["Antwort: Ja. Entstandene Vorbereitungsaufwendungen werden erstattet, wenn Dienstreisen aus Gründen entfallen, die nicht von den Dienstreisenden zu vertreten sind (§10 Abs.2)."]
  Q11A2 --> A_Q11A2["Antwort: Anerkennung erfordert, dass Aufwendungen notwendig und nach diesem Gesetz berücksichtigungsfähig sind; Nachweise sind vorzulegen; genaue Kriterien bestimmt die Dienststelle (§10 Abs.2)."]
  Q11B1 --> A_Q11B1["Antwort: Sonstige notwendige Auslagen, die nicht unter §§4–9 fallen, werden als Nebenkosten erstattet, sofern sie zur Erledigung des Dienstgeschäfts notwendig sind (§10 Abs.1)."]
  Q11B2 --> A_Q11B2["Antwort: Abrechnung und Nachweispflichten richten sich nach den Vorgaben der zuständigen Stellen; Belege sind vorzulegen, Fristen sind zu beachten (§3 Abs.4; §10)."]

  Q12A1 --> A_Q12A1["Antwort: Das Finanzministerium ist ermächtigt, durch Rechtsverordnung die in §§5 und 7 Abs.1 festgesetzten Beträge an veränderte wirtschaftliche Verhältnisse anzupassen (§14 Abs.1)."]
  Q12A2 --> A_Q12A2["Antwort: Die allgemeinen Verwaltungsvorschriften erlässt das Finanzministerium; Anpassungsverfahren und Zuständigkeiten regelt es ebenfalls (§14 Abs.2)."]

  Q12B1 --> A_Q12B1["Antwort: Ausnahmen von der niedrigsten Klasse kann die oberste Dienstbehörde oder die von ihr ermächtigte nachgeordnete Behörde zulassen; Zuständigkeiten sind gesetzlich geregelt (§4 Abs.1)."]
  Q12B2 --> A_Q12B2["Antwort: Ministerien und staatliche Hochschulen sind verpflichtet, jährliche Ausgleichszahlungen für dienstliche Flüge zu leisten (§4 Abs.4)."]
  Q12B3 --> A_Q12B3["Antwort: Melde- und Nachweispflichten (z. B. bei Drittmittelfinanzierten Flügen) sind durch die jeweiligen Vorgaben der Verwaltungen zu regeln; Gesetz nennt die Pflicht zur Leistung der Ausgleichszahlung (§4 Abs.4)."]
  Q12B4 --> A_Q12B4["Antwort: Dienststellen können Ausnahmen begründen (z. B. besondere dienstliche Gründe) und müssen dies dokumentieren; die oberste Dienstbehörde kann Ermächtigungen erteilen (§4 Abs.1, §12 Abs.6)."]
