```mermaid
%%{ init: { "theme": "default", "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "linear" } } }%%
flowchart LR
  Root["Was möchten Sie zur Planung, Durchführung oder Abrechnung von Dienstreisen wissen?"]

  %% Top-level categories (plain-language)
  Root --> BAS["A. Grundlagen (Begriff, Genehmigung, Abgrenzung, Ausgangs-/Endpunkt)"]
  Root --> TRA["B. Beförderung, Fahrt- und Flugkosten, Klimaauflagen"]
  Root --> WEG["C. Wegstreckenentschädigung (PKW, Fahrrad, Zuschläge)"]
  Root --> TAGE["D. Tagegeld (Sätze, Dauer, Kürzungen)"]
  Root --> UEBN["E. Übernachtung, Langzeitaufenthalte, höhere Kosten"]
  Root --> PAUS["F. Aufwands- und Pauschvergütung / sonstige Nebenkosten"]
  Root --> SPEZ["G. Besondere Fälle: Versetzung, Fortbildung, Urlaub, Krankheit, Fahrten zur Dienststätte"]
  Root --> AUSW["H. Auslandsdienstreisen (Definition, Länderregel, Langzeit)"]
  Root --> TRG["I. Trennungsgeld (Abordnung ohne Umzugskosten)"]
  Root --> ANTR["J. Anträge, Fristen, Belege, Anrechnung, Verzicht"]
  Root --> VORB["K. Vorbereitungsaufwand und sonstige notwendige Auslagen (§10)"]
  Root --> ADMIN["L. Verwaltung, Zuständigkeiten, Anpassungen"]

  %% A. Grundlagen
  BAS --> BAS_DEF["A.1 Begriff & Genehmigung"]
  BAS --> BAS_DIFF["A.2 Dienstreise vs. Dienstgang"]
  BAS --> BAS_POINT["A.3 Ausgangs- / Endpunkt; Wohnsitze"]

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

  %% A.3 Ausgangs- / Endpunkt; Wohnsitze
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

  %% B. Beförderung, Fahrt- und Flugkosten, Klimaauflagen
  TRA --> TRA_CHOICE["B.1 Wahl des Verkehrsmittels und Klimaschutz"]
  TRA --> TRA_COSTS["B.2 Fahrt- und Flugkosten: Klassen, Ausnahmen"]
  TRA --> TRA_TAXI["B.3 Mietwagen, Taxi, Carsharing und Ausgleichszahlungen"]

  %% B.1 Wahl & Klimaschutz
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

  %% B.2 Fahrt- und Flugkosten Detailregeln

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

  %% B.3 Mietwagen/Taxi/Carsharing und Klimaausgleich
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

  %% C. Wegstreckenentschädigung
  WEG --> WEG_PKW["C.1 Privates Kraftfahrzeug (Sätze)"]
  WEG --> WEG_ZUSCHLAG["C.2 Zuschläge für schwierige Wege"]
  WEG --> WEG_FAHRRAD["C.3 Fahrrad / E‑Bike / Pedelec"]

    WEG_PKW["C.1 Privates Kraftfahrzeug (Sätze)"]
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

  %% C.2 Zuschläge
  WEG_ZUSCHLAG --> Q_BAD_ROAD["Frage: Kann ein Zuschlag für unbefestigte oder schwer befahrbare Wege gewährt werden?"]
  Q_BAD_ROAD --> A_BAD_ROAD["Antwort: Ja, mit Zustimmung der obersten Dienstbehörde kann ein Zuschlag von 5 Cent/km gewährt werden, wenn regelmäßig Fahrten auf solchen Wegen erforderlich sind (§5 Abs.2)."]

  WEG_ZUSCHLAG --> Q_ZUSCHLAG_PROOF["Frage: Welche Nachweise gelten für den Zuschlag?"]
  Q_ZUSCHLAG_PROOF --> A_ZUSCHLAG_PROOF["Antwort: Die Zustimmung der obersten Dienstbehörde ist erforderlich; Nachweise und Begründungen richten sich nach dienstlichen Vorgaben (§5 Abs.2)."]

  %% C.3 Fahrrad
  WEG_FAHRRAD --> Q_BIKE_RATE["Frage: Wie hoch ist die Wegstreckenentschädigung für Fahrrad, E‑Bike oder Pedelec?"]
  Q_BIKE_RATE --> A_BIKE_RATE["Antwort: 25 Cent je Kilometer zurückgelegter Strecke (§5 Abs.3)."]

  WEG_FAHRRAD --> Q_BIKE_FREQUENT["Frage: Gilt Besonderes bei häufiger Nutzung von Dienstfahrrädern oder Dienstradleasing?"]
  Q_BIKE_FREQUENT --> A_BIKE_FREQUENT["Antwort: Das Gesetz nennt keine besonderen Sätze; Dienststellen können spezielle Regelungen treffen (§5 Abs.3)."]

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

  %% E. Übernachtung & Langzeitaufenthalte
  UEBN --> UEBN_BASIC["E.1 Pauschalbeträge und Ersatz höherer Übernachtungskosten"]
  UEBN --> UEBN_LONG["E.2 Langzeitregelungen (ab 8./15. Tag) und Auslandsbesonderheiten"]

  %% E.1 Pauschalbeträge & Ausschlüsse

  UEBN_BASIC --> Q_OVN_DOM_ABR["Frage: Wie hoch ist das pauschale Übernachtungsgeld im Inland und Ausland?"]
  Q_OVN_DOM_ABR --> A_OVN_DOM_ABR["Antwort: Pauschales Übernachtungsgeld: 20 Euro im Inland, 30 Euro im Ausland (§7 Abs.1)."]

  Q_OVN_DOM_ABR --> Q_OVN_EXCLUSIONS["Check: Wird Ihnen die Unterkunft vom Arbeitgeber unentgeltlich bereitgestellt?"]
  Q_OVN_EXCLUSIONS -->|"Ja"| A_OVN_EXCLUSIONS["Antwort: Der Anspruch entfällt u. a. bei unentgeltlich vom Dienstherrn bereitgestellter Unterkunft; ebenso entfällt er bei Benutzung von Beförderungsmitteln, bei Aufenthalt in eigener Wohnung oder wenn Unterkunftskosten im erstattungsfähigen Fahrpreis enthalten sind. Eine zusätzliche Übernachtung wird nur ersetzt, wenn sie wegen früher Ankunft oder später Abfahrt erforderlich ist (§7 Abs.2)."]
  Q_OVN_EXCLUSIONS -->|"Nein"| A_OVN_DOM_ABR

  Q_OVN_DOM_ABR --> Q_OVN_HIGHER["Frage: Wer legt die Höchstbeträge für erstattungsfähige höhere Übernachtungskosten fest, falls mein Hotel teurer ist als die Pauschale?"]
  Q_OVN_HIGHER --> A_OVN_HIGHER["Antwort: Höhere notwendige Übernachtungskosten werden im notwendigen Umfang erstattet; das Finanzministerium bestimmt per Verwaltungsvorschrift bis zu welcher Höhe (§7 Abs.1; §14)."]

  UEBN_BASIC --> Q_OVN_TICKET_INCLUDED["Frage: Was gilt, wenn Unterkunftskosten Teil eines Ticketpreises sind (z. B. Bahnreise mit Hotel)?"]
  Q_OVN_TICKET_INCLUDED --> A_OVN_TICKET_INCLUDED["Antwort: Übernachtungsgeld wird nicht gewährt, wenn Unterkunftskosten im erstattungsfähigen Fahrpreis enthalten sind, außer eine zusätzliche Übernachtung ist wegen früher Ankunft oder später Abfahrt erforderlich (§7 Abs.2 Nr.4)."]

  %% E.2 Langzeit & Ausland Besonderheiten
  UEBN_LONG --> Q_LONG_LOCAL_8["Frage: Wann werden Auslagenerstattungen ab dem 8. Tag gezahlt und wie bemessen?"]
  Q_LONG_LOCAL_8 --> A_LONG_LOCAL_8["Antwort: Dauert der Aufenthalt an demselben auswärtigen Geschäftsort länger als 7 Tage, wird ab dem 8. Tag die Vergütung gezahlt, die bei Abordnung zu gewähren wäre (§8)."]

  UEBN_LONG --> Q_ABROAD_15_COSTS["Frage: Können ab dem 15. Tag im Ausland statt pauschalem Übernachtungsgeld tatsächliche Übernachtungskosten erstattet werden?"]
  Q_ABROAD_15_COSTS --> A_ABROAD_15_COSTS["Antwort: Ja, ab dem 15. Tag im Ausland können anstelle der Pauschale die nachgewiesenen notwendigen Übernachtungskosten erstattet werden (§12 Abs.6)."]

  UEBN_LONG --> Q_ABROAD_15_REDUCE["Frage: Wann wird das Auslandstagegeld ab dem 15. Tag um 25% ermäßigt?"]
  Q_ABROAD_15_REDUCE --> A_ABROAD_15_REDUCE["Antwort: Bei Dauerauslandsaufenthalten ohne Hin-/Rückreisetage länger als 14 Tage ist das Auslandstagegeld ab dem 15. Tag um 25 % zu ermäßigen (§12 Abs.6)."]

  UEBN_LONG --> Q_ABROAD_15_WAIVER["Frage: Wer kann von der Ermäßigung absehen?"]
  Q_ABROAD_15_WAIVER --> A_ABROAD_15_WAIVER["Antwort: Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann in begründeten Fällen von der Ermäßigung absehen (§12 Abs.6)."]

  %% F. Aufwands- und Pauschvergütung / sonstige Nebenkosten
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

  %% G. Besondere Fälle
  SPEZ --> SPEZ_TRANSFER["G.1 Versetzung, Abordnung"]
  SPEZ --> SPEZ_TRAINING["G.2 Fortbildung und Nebentätigkeit"]
  SPEZ --> SPEZ_PRIVATE["G.3 Kombination mit Urlaub / Krankheit / Fahrten zur Dienststätte"]

  SPEZ_TRANSFER --> Q_TRANSFER_DAYS["Frage: Welche Vergütung gilt bei Versetzung/Abordnung (Tagegeld/Übernachtung)?"]
  Q_TRANSFER_DAYS --> A_TRANSFER_DAYS["Antwort: Bei Versetzung/Abordnung wird Tagegeld bis zur Ankunft am neuen Dienstort und Übernachtungsgeld gewährt; Tagegeld bis Ablauf des Ankunftstages, wenn ab dem nächsten Tag Trennungsgeld gezahlt wird (§11 Abs.1)."]

  SPEZ_TRAINING --> Q_TRAINING_PARTIAL["Frage: Können Kosten für Fortbildungen erstattet werden, wenn sie teilweise dienstlich sind?"]
  Q_TRAINING_PARTIAL --> A_TRAINING_PARTIAL["Antwort: Ja, für Fortbildungen mit zumindest teilweise dienstlichem Interesse können Kosten bis zur Höhe der dienstlichen Reisekostenvergütung erstattet werden (§11 Abs.2)."]

  SPEZ_TRAINING --> Q_SECONDARY_JOB["Frage: Haben Dienstreisende Anspruch auf Reisekosten, wenn eine andere Stelle Auslagenerstattung gewährt?"]
  Q_SECONDARY_JOB --> A_SECONDARY_JOB["Antwort: Nur insoweit, wie nicht eine andere Stelle Auslagenerstattung für dieselbe Reise gewährt; gilt auch bei Verzicht auf Ansprüche gegenüber dieser Stelle (§3 Abs.6)."]

  SPEZ_TRAINING --> Q_MULTIPLE_COORD["Frage: Welche Abstimmungsregeln gelten zwischen Stellen bei Mehrfachleistungen?"]
  Q_MULTIPLE_COORD --> A_MULTIPLE_COORD["Antwort: Leistungen Dritter sind auf die Vergütung anzurechnen; Abrechnung und Abstimmung zwischen Stellen sind erforderlich (§3 Abs.5–6)."]

  SPEZ_PRIVATE --> Q_PRIVATE_COMBINE["Frage: Wie wird Vergütung bemessen, wenn Dienstreise mit Urlaub kombiniert wird?"]
  Q_PRIVATE_COMBINE --> A_PRIVATE_COMBINE["Antwort: Die Vergütung bemisst sich so, als ob nur die Dienstreise durchgeführt worden wäre und darf die nach dem tatsächlichen Verlauf günstigere Vergütung nicht übersteigen (§11 Abs.3)."]

  SPEZ_PRIVATE --> Q_START_END_VAC["Frage: Was gilt, wenn die Dienstreise am Urlaubsort an- oder beendet wird (angeordnet)?"]
  Q_START_END_VAC --> A_START_END_VAC["Antwort: Dann wird die Vergütung abweichend nach Abreise von bzw. Ankunft an diesem Ort bemessen (§11 Abs.4)."]

  SPEZ_PRIVATE --> Q_PREMATURE_END["Frage: Wie werden Aufwendungen bei vorzeitiger Beendigung einer Urlaubsreise auf Anordnung behandelt?"]
  Q_PREMATURE_END --> A_PREMATURE_END["Antwort: Die Rückreise vom Urlaubs-/Aufenthaltsort zur Dienststätte gilt als Dienstreise; angemessene Aufwendungen werden erstattet (§11 Abs.5–6)."]

  SPEZ_PRIVATE --> Q_HOSPITAL["Frage: Werden bei Krankenhausaufnahme die Unterkunftsauslagen erstattet?"]
  Q_HOSPITAL --> A_HOSPITAL["Antwort: Ja, für jeden vollen Kalendertag des Krankenhausaufenthalts werden die notwendigen Unterkunftsauslagen am Geschäftsort erstattet (§11 Abs.7)."]

  SPEZ_PRIVATE --> Q_COMMUTE_SPECIAL["Frage: Können Fahrten Wohnung ↔ regelmäßige Dienststätte aus besonderem dienstlichen Anlass erstattet werden?"]
  Q_COMMUTE_SPECIAL --> A_COMMUTE_SPECIAL["Antwort: Ja, notwendige Fahrtkosten können bei besonderem dienstlichen Anlass erstattet werden; Nachweise und Anforderungen regelt die Dienststelle (§11 Abs.8; §3)."]

  SPEZ_PRIVATE --> Q_COMMUTE_PROOF["Frage: Welche Nachweise sind bei solchen Fahrten erforderlich?"]
  Q_COMMUTE_PROOF --> A_COMMUTE_PROOF["Antwort: Erforderlich sind Anordnung oder Nachweis des dienstlichen Anlasses; konkrete Anforderungen legt die Dienststelle fest (§11 Abs.8; §3)."]

  %% H. Auslandsdienstreisen
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

  %% I. Trennungsgeld
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


  %% J. Anträge, Fristen, Belege, Anrechnung, Verzicht
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

  %% K. Vorbereitungsaufwand & sonstige Auslagen (§10)
  VORB --> VORB_PREP["K.1 Vorbereitungsaufwand bei entfallener Dienstreise"]
  VORB --> VORB_OTHER["K.2 Sonstige notwendige Nebenkosten (§10)"]

  VORB_PREP --> Q_PREP_REIMBURSE["Frage: Werden entstandene Vorbereitungsaufwendungen erstattet, wenn Dienstreisen entfallen, die nicht von Dienstreisenden zu vertreten sind?"]
  Q_PREP_REIMBURSE --> A_PREP_REIMBURSE["Antwort: Ja, notwendige und nach diesem Gesetz berücksichtigungsfähige Vorbereitungsaufwendungen werden erstattet (§10 Abs.2)."]

  VORB_PREP --> Q_PREP_PROOF["Frage: Unter welchen Bedingungen werden Vorbereitungskosten anerkannt?"]
  Q_PREP_PROOF --> A_PREP_PROOF["Antwort: Anerkennung erfordert, dass Aufwendungen notwendig und nach dem Gesetz berücksichtigungsfähig sind; Nachweise sind vorzulegen und Kriterien bestimmt die Dienststelle (§10 Abs.2)."]

  VORB_OTHER --> Q_OTHER_COSTS_EXPLAIN["Frage: Welche sonstigen notwendigen Auslagen können erstattet werden?"]
  Q_OTHER_COSTS_EXPLAIN --> A_OTHER_COSTS_EXPLAIN["Antwort: Sonstige notwendige Auslagen, die nicht unter §§4–9 fallen, werden erstattet, wenn sie zur Erledigung des Dienstgeschäfts notwendig sind (§10 Abs.1)."]

  VORB_OTHER --> Q_OTHER_COSTS_ABRECHN["Frage: Wie sind Abrechnungs- und Nachweispflichten für Nebenkosten geregelt?"]
  Q_OTHER_COSTS_ABRECHN --> A_OTHER_COSTS_ABRECHN["Antwort: Abrechnung und Nachweispflichten regeln die zuständigen Dienststellen; Belege sind vorzulegen und Fristen zu beachten (§3 Abs.4; §10)."]

  %% L. Verwaltung, Zuständigkeiten, Anpassungen
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

```