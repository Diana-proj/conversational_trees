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

  %% A.1 Definition & formal rules
  BAS_DEF --> Q_DEF["Frage: Was ist eine Dienstreise?"]
  Q_DEF --> A_DEF["Antwort: Dienstreisen sind Reisen zur Erledigung von Dienstgeschäften außerhalb des Dienstortes, die vom zuständigen Dienstvorgesetzten schriftlich oder elektronisch angeordnet oder genehmigt sind; Ausnahmen, wenn Anordnung unüblich ist (§2 Abs.1)."]

  BAS_DEF --> Q_APPROVAL["Frage: Muss eine Dienstreise schriftlich/e‑genehmigt werden?"]
  Q_APPROVAL --> A_APPROVAL["Antwort: Ja, die Anordnung oder Genehmigung hat schriftlich oder elektronisch zu erfolgen (§2 Abs.1)."]

  BAS_DEF --> Q_APPROXCEPT["Frage: Gelten für Richterinnen, Datenschutzbeauftragte oder die Behindertenbeauftragte Ausnahmen von der Anordnungspflicht?"]
  Q_APPROXCEPT --> A_APPROXCEPT["Antwort: Ja, für Richterinnen/Richter, den Landesbeauftragten für Datenschutz und die Landesbeauftragte für Belange von Menschen mit Behinderungen besteht keine Anordnungspflicht (§2 Abs.3)."]

  BAS_DEF --> Q_FORMAL["Frage: Welche formalen Regeln gelten für die Anordnung (Zuständigkeit, Form)?"]
  Q_FORMAL --> A_FORMAL["Antwort: Zuständig ist der zuständige Dienstvorgesetzte; Anordnung/Genehmigung schriftlich oder elektronisch; Ausnahmen nur wie gesetzlich geregelt (§2 Abs.1)."]

  %% A.2 Dienstgang vs Dienstreise
  BAS_DIFF --> Q_WHENDG["Frage: Wann ist ein Einsatz ein Dienstgang statt einer Dienstreise?"]
  Q_WHENDG --> A_WHENDG["Antwort: Dienstgänge sind dienstliche Erledigungen außerhalb der Dienststätte am Dienst- oder Wohnort, die angeordnet/genehmigt sind; Abgrenzung nach Ort und Zweck (§2 Abs.2)."]

  BAS_DIFF --> Q_TAGE_DG["Frage: Besteht bei Dienstgängen Anspruch auf Tagegeld?"]
  Q_TAGE_DG --> A_TAGE_DG["Antwort: Grundsätzlich kein Anspruch auf Tagegeld; bei Dienstgängen >8 Std. werden notwendige Verpflegungsauslagen bis zur Höhe des Tagegeldes für gleich lange Dienstreisen ersetzt (§6 Abs.3)."]

  %% A.3 Ausgangs- / Endpunkt; Wohnsitze
  BAS_POINT --> Q_CHOOSE_POINT["Frage: Kann ich Ausgangs‑ und Endpunkt meiner Dienstreise selbst wählen?"]
  Q_CHOOSE_POINT --> A_CHOOSE_POINT["Antwort: Ja, grundsätzlich bestimmt die/der Dienstreisende Ausgangs‑/Endpunkt unter Beachtung des Wirtschaftlichkeitsgrundsatzes (§3 Abs.2)."]

  BAS_POINT --> Q_FORCE_STATION["Frage: Kann die Dienststelle die Dienststätte als Ausgangs/Endpunkt anordnen?"]
  Q_FORCE_STATION --> A_FORCE_STATION["Antwort: Ja, der Vorgesetzte kann die Dienststätte anordnen, wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt (§3 Abs.2)."]

  BAS_POINT --> Q_TRAVEL_FROM_HOME["Frage: Wie wird die Fahrtkostenerstattung berechnet, wenn die Reise an der Wohnung beginnt oder endet?"]
  Q_TRAVEL_FROM_HOME --> A_TRAVEL_FROM_HOME["Antwort: Fahrtkostenerstattung oder Wegstreckenentschädigung bemisst sich nach der Entfernung von/bis Wohnung, sofern nicht die Dienststätte als Ausgangs-/Endpunkt angeordnet wurde (§3 Abs.2)."]

  BAS_POINT --> Q_MULTIPLE_HOME["Frage: Welche Wohnung gilt bei mehreren Wohnsitzen?"]
  Q_MULTIPLE_HOME --> A_MULTIPLE_HOME["Antwort: Maßgeblich ist die der Dienststätte am nächsten gelegene Wohnung oder Unterkunft (§3 Abs.2)."]

  %% B. Beförderung, Fahrt- und Flugkosten, Klimaauflagen
  TRA --> TRA_CHOICE["B.1 Wahl des Verkehrsmittels und Klimaschutz"]
  TRA --> TRA_COSTS["B.2 Fahrt- und Flugkosten: Klassen, Ausnahmen"]
  TRA --> TRA_TAXI["B.3 Mietwagen, Taxi, Carsharing und Ausgleichszahlungen"]

  %% B.1 Wahl & Klimaschutz
  TRA_CHOICE --> Q_FREE_CHOICE["Frage: Bin ich frei in der Wahl des Verkehrsmittels?"]
  Q_FREE_CHOICE --> A_FREE_CHOICE["Antwort: Grundsätzlich ja; Dienstreisende sind in der Wahl frei, müssen aber Wirtschaftlichkeitsgesichtspunkte und Klimaschutzanforderungen beachten (§3 Abs.3)."]

  TRA_CHOICE --> Q_CONSIDER_CLIMATE["Frage: Muss ich Klimaschutz bei der Verkehrsmittelwahl beachten (z. B. ÖPNV vor Auto)?"]
  Q_CONSIDER_CLIMATE --> A_CONSIDER_CLIMATE["Antwort: Ja, neben Wirtschaftlichkeit sind die Erfordernisse des Klimaschutzes bei der Wahl zu beachten (§3 Abs.3)."]

  TRA_CHOICE --> Q_FREE_TRANSPORT_NOT_REFUND["Frage: Werden Fahrtkosten erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit besteht?"]
  Q_FREE_TRANSPORT_NOT_REFUND --> A_FREE_TRANSPORT_NOT_REFUND["Antwort: Nein, Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann (§3 Abs.3)."]

  TRA_CHOICE --> Q_ROLE_ECONOMY["Frage: Welche Rolle spielen Dienstinteresse und Wirtschaftlichkeit?"]
  Q_ROLE_ECONOMY --> A_ROLE_ECONOMY["Antwort: Dienstinteresse und Wirtschaftlichkeit sind maßgeblich; die Auswahl hat wirtschaftlich zu sein (§2 Abs.1; §3 Abs.2–3)."]

  %% B.2 Fahrt- und Flugkosten Detailregeln
  TRA_COSTS --> Q_LOWEST_CLASS["Frage: Werden Kosten nur bis zur niedrigsten Beförderungsklasse ersetzt?"]
  Q_LOWEST_CLASS --> A_LOWEST_CLASS["Antwort: Ja, Kosten werden bis zur Höhe der niedrigsten Beförderungsklasse erstattet; Ausnahmen sind durch die oberste Dienstbehörde möglich (§4 Abs.1)."]

  TRA_COSTS --> Q_EXCEPT_LOWEST["Frage: Wann sind Ausnahmen von der niedrigsten Klasse möglich?"]
  Q_EXCEPT_LOWEST --> A_EXCEPT_LOWEST["Antwort: Ausnahmen können die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde bei besonderen dienstlichen Gründen zulassen (§4 Abs.1)."]

  TRA_COSTS --> Q_FLIGHT_ALLOWED["Frage: Sind Flugkosten grundsätzlich erstattungsfähig?"]
  Q_FLIGHT_ALLOWED --> A_FLIGHT_ALLOWED["Antwort: Flugkosten sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Flugnutzung gegenüber Klimaschutzbelangen überwiegen (§4 Abs.1)."]

  TRA_COSTS --> Q_LOWEST_FLIGHT["Frage: Werden bei Flügen nur Kosten der niedrigsten Flugklasse erstattet?"]
  Q_LOWEST_FLIGHT --> A_LOWEST_FLIGHT["Antwort: Grundsätzlich ja; das Finanzministerium kann per Verwaltungsvorschrift Ausnahmen bestimmen (§4 Abs.1)."]

  TRA_COSTS --> Q_HIGHER_CLASS_DISABILITY["Frage: Wann wird bei Grad der Behinderung ≥50 die höhere Klasse übernommen?"]
  Q_HIGHER_CLASS_DISABILITY --> A_HIGHER_CLASS_DISABILITY["Antwort: Dienstreisende mit Grad der Behinderung ≥50 erhalten die Auslagen für die nächsthöhere Klasse erstattet (§4 Abs.2)."]

  TRA_COSTS --> Q_HIGHER_CLASS_HEALTH["Frage: Können andere aus Gesundheitsgründen höhere Klassen erstattet bekommen?"]
  Q_HIGHER_CLASS_HEALTH --> A_HIGHER_CLASS_HEALTH["Antwort: Ja, andere Dienstreisende können bei entsprechendem gesundheitlichen Zustand die nächsthöhere Klasse erhalten (§4 Abs.2)."]

  %% B.3 Mietwagen/Taxi/Carsharing und Klimaausgleich
  TRA_TAXI --> Q_RENT_TAXI_CARSHARE["Frage: Werden Mietwagen-, Taxi- oder Carsharing‑Kosten ersetzt?"]
  Q_RENT_TAXI_CARSHARE --> A_RENT_TAXI_CARSHARE["Antwort: Ja, wenn aus triftigem Grund benutzt; sonst darf nicht mehr als beim ÖPNV gezahlt werden (§4 Abs.3)."]

  TRA_TAXI --> Q_PAY_MORE_THAN_OPNV["Frage: Dürfen ohne triftigen Grund höhere Vergütungen als ÖPNV gewährt werden?"]
  Q_PAY_MORE_THAN_OPNV --> A_PAY_MORE_THAN_OPNV["Antwort: Nein, ohne triftigen Grund darf keine höhere Vergütung als beim ÖPNV gewährt werden (§4 Abs.3 Satz2)."]

  TRA_TAXI --> Q_CARSHARE_MEMBER_FEE["Frage: Wird bei Carsharing die Mitgliedsgebühr wegen privater Nutzung gekürzt?"]
  Q_CARSHARE_MEMBER_FEE --> A_CARSHARE_MEMBER_FEE["Antwort: Nein, bei Carsharing erfolgt keine Kürzung der Mitgliedsgebühr wegen privater Nutzung (§4 Abs.3 Satz3)."]

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

  %% C.1 PKW
  WEG_PKW --> Q_PKW_RATE["Frage: Wie viel Wegstreckenentschädigung gilt für private PKW-Fahrten (Cent/km)?"]
  Q_PKW_RATE --> A_PKW_RATE["Antwort: 30 Cent je Kilometer zurückgelegter Strecke (§5 Abs.1)."]

  WEG_PKW --> Q_PKW_35["Frage: Wann erhöht sich die Entschädigung auf 35 Cent/km?"]
  Q_PKW_35 --> A_PKW_35["Antwort: Bei erheblichem dienstlichen Interesse beträgt die Wegstreckenentschädigung 35 Cent/km (§5 Abs.2)."]

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

  %% D. Tagegeld
  TAGE --> TAGE_RATES["D.1 Tagegeldsätze"]
  TAGE --> TAGE_DURATION["D.2 Bestimmung der Reisedauer und Kürzungen"]

  %% D.1 Sätze
  TAGE_RATES --> Q_FULL_DAY["Frage: Wie hoch ist das Tagegeld für jeden vollen Kalendertag?"]
  Q_FULL_DAY --> A_FULL_DAY["Antwort: Das Tagegeld beträgt 24 Euro für jeden vollen Kalendertag (§6 Abs.1)."]

  TAGE_RATES --> Q_ARR_DEP_DAY["Frage: Wie viel Tagegeld steht für An‑/Abreisetag bei mehrtägigen Reisen zu?"]
  Q_ARR_DEP_DAY --> A_ARR_DEP_DAY["Antwort: Bei Dienstreisedauer >8 Std. 6 Euro, bei >14 Std. 12 Euro für An‑/Abreisetag (§6 Abs.1)."]

  %% D.2 Dauer & Kürzung
  TAGE_DURATION --> Q_DETERMINE_DURATION["Frage: Nach welchen Zeitpunkten bestimmt sich die Dauer der Dienstreise (Abreise/Ankunft)?"]
  Q_DETERMINE_DURATION --> A_DETERMINE_DURATION["Antwort: Dauer richtet sich nach Abreise und Ankunft an der Wohnung, außer die Reise beginnt/endet an der Dienststätte oder dies wurde so angeordnet; bei mehreren Wohnungen gilt die der Dienststätte nächste (§6 Abs.2)."]

  TAGE_DURATION --> Q_TIMEZONE_NIGHT["Frage: Wie werden Zeitzonen, Nachtfahrten und Zwischenlandungen berücksichtigt?"]
  Q_TIMEZONE_NIGHT --> A_TIMEZONE_NIGHT["Antwort: Gesonderte Regeln fehlen; maßgeblich bleiben Abreise/Ankunftszeitpunkte nach Ortszeit und die besonderen Vorschriften bei Auslandsdienstreisen (§6; §12)."]

  TAGE_DURATION --> Q_UNPAID_MEALS["Frage: Wie wird das Tagegeld gekürzt, wenn unentgeltliche Verpflegung gewährt wird?"]
  Q_UNPAID_MEALS --> A_UNPAID_MEALS["Antwort: Frühstück: 20 %; Mittag und Abendessen: je 40 % des vollen Tagegeldes werden einbehalten (§6 Abs.4)."]

  TAGE_DURATION --> Q_TAGE_DG_RESTATE["Frage: Besteht für Dienstgänge Anspruch auf Tagegeld bzw. wie werden längere Dienstgänge vergütet?"]
  Q_TAGE_DG_RESTATE --> A_TAGE_DG_RESTATE["Antwort: Bei Dienstgängen besteht kein Tagegeldanspruch; bei Dienstgängen >8 Std. werden nachgewiesene Verpflegungsauslagen bis zur Höhe des Tagegeldes für die gleich lange Dienstreise erstattet (§6 Abs.3)."]

  %% E. Übernachtung & Langzeitaufenthalte
  UEBN --> UEBN_BASIC["E.1 Pauschalbeträge und Ersatz höherer Übernachtungskosten"]
  UEBN --> UEBN_LONG["E.2 Langzeitregelungen (ab 8./15. Tag) und Auslandsbesonderheiten"]

  %% E.1 Pauschalbeträge & Ausschlüsse
  UEBN_BASIC --> Q_OVN_DOM_ABR["Frage: Wie hoch ist das pauschale Übernachtungsgeld im Inland und Ausland?"]
  Q_OVN_DOM_ABR --> A_OVN_DOM_ABR["Antwort: Pauschales Übernachtungsgeld: 20 Euro im Inland, 30 Euro im Ausland (§7 Abs.1)."]

  UEBN_BASIC --> Q_OVN_HIGHER["Frage: Werden höhere notwendige Übernachtungskosten ersetzt und wer legt Höchstgrenzen fest?"]
  Q_OVN_HIGHER --> A_OVN_HIGHER["Antwort: Höhere notwendige Übernachtungskosten werden im notwendigen Umfang erstattet; das Finanzministerium bestimmt per Verwaltungsvorschrift bis zu welcher Höhe (§7 Abs.1)."]

  UEBN_BASIC --> Q_OVN_EXCLUSIONS["Frage: Wann wird Übernachtungsgeld nicht gewährt?"]
  Q_OVN_EXCLUSIONS --> A_OVN_EXCLUSIONS["Antwort: Kein Übernachtungsgeld bei Benutzung von Beförderungsmitteln, Aufenthalt in eigener Wohnung, unentgeltlicher Amtsunterkunft oder wenn Unterkunftskosten im erstattungsfähigen Fahrpreis enthalten sind (Ausnahme bei zusätzlicher Übernachtung) (§7 Abs.2)."]

  UEBN_BASIC --> Q_OVN_TICKET_INCLUDED["Frage: Was gilt, wenn Unterkunftskosten Teil eines Ticketpreises sind (z. B. Bahnreise mit Hotel)?"]
  Q_OVN_TICKET_INCLUDED --> A_OVN_TICKET_INCLUDED["Antwort: Übernachtungsgeld wird nicht gewährt, wenn Unterkunftskosten im erstattungsfähigen Fahrpreis enthalten sind, außer eine zusätzliche Übernachtung ist wegen früher Ankunft/später Abfahrt erforderlich (§7 Abs.2 Nr.4)."]

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
  PAUS --> PAUS_LUMP["F.1 Aufwandsvergütung statt Einzelvergütung"]
  PAUS --> PAUS_MISC["F.2 Pauschalen und sonstige Nebenkosten (§10)"]

  PAUS_LUMP --> Q_LUMP_INSTEAD["Frage: Können Dienstreisende statt Tagegeld/Übernachtung eine Aufwandsvergütung erhalten?"]
  Q_LUMP_INSTEAD --> A_LUMP_INSTEAD["Antwort: Ja, Dienstreisende mit erfahrungsgemäß geringeren Aufwendungen können nach näherer Bestimmung der obersten Dienstbehörde eine Aufwandsvergütung erhalten (§9 Abs.1)."]

  PAUS_LUMP --> Q_LUMP_FORM["Frage: Welche Form der Regelung/Vereinbarung ist nötig, um Aufwandsvergütung zu erhalten?"]
  Q_LUMP_FORM --> A_LUMP_FORM["Antwort: Die Form regelt die oberste Dienstbehörde; üblicherweise durch dienstliche Festlegung oder Vereinbarung (§9 Abs.1)."]

  PAUS_MISC --> Q_PAUCH_REGULAR["Frage: Kann die oberste Dienstbehörde Pauschvergütungen für regelmäßige oder gleichartige Dienstreisen festlegen?"]
  Q_PAUCH_REGULAR --> A_PAUCH_REGULAR["Antwort: Ja, die oberste Dienstbehörde kann Pauschvergütungen nach Durchschnitt der sonst anfallenden Einzelvergütungen festlegen (§9 Abs.2)."]

  PAUS_MISC --> Q_OTHER_NECESSARY["Frage: Welche sonstigen notwendigen Nebenkosten werden erstattet, wenn sie nicht unter §§4–9 fallen?"]
  Q_OTHER_NECESSARY --> A_OTHER_NECESSARY["Antwort: Notwendige Auslagen, die nicht unter §§4–9 fallen, werden als Nebenkosten erstattet, wenn sie zur Erledigung des Dienstgeschäfts notwendig sind (§10 Abs.1)."]

  PAUS_MISC --> Q_PAUCH_LIMITS["Frage: Gibt es Obergrenzen oder Zuständigkeiten zur Festsetzung von Pauschalen?"]
  Q_PAUCH_LIMITS --> A_PAUCH_LIMITS["Antwort: Zuständigkeit liegt bei der obersten Dienstbehörde bzw. ermächtigten Behörden; Obergrenzen können durch Verwaltungsvorschrift geregelt werden (§9 Abs.2; §14)."]

  PAUS_MISC --> Q_PAUCH_PROOF["Frage: Wie sind Nachweise bei Pauschalvergütungen zu handhaben?"]
  Q_PAUCH_PROOF --> A_PAUCH_PROOF["Antwort: Nachweise und Prüfpflichten regelt die zuständige Dienststelle; das Gesetz verlangt Prüfungen und formale Vorgaben (§3 Abs.4; §10)."]

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
  AUSW --> AUS_DEF["H.1 Begriff & Anwendungsbereich"]
  AUSW --> AUS_RATES["H.2 Bemessung, Länderregel, Zwischenlandungen"]
  AUSW --> AUS_LONG["H.3 Langzeit im Ausland (ab 15. Tag)"]

  AUS_DEF --> Q_ABROAD_DEF["Frage: Was ist eine Auslandsdienstreise?"]
  Q_ABROAD_DEF --> A_ABROAD_DEF["Antwort: Auslandsdienstreisen sind Dienstreisen zwischen Inland und Ausland sowie im Ausland; mindestens ein Geschäftsort im Ausland muss vorliegen (§12 Abs.1)."]

  AUS_DEF --> Q_APPLY_RULES["Frage: Gelten die Regeln der §§1–11 auch bei Auslandsdienstreisen?"]
  Q_APPLY_RULES --> A_APPLY_RULES["Antwort: Ja, die §§1–11 gelten entsprechend, soweit in §12 nicht abweichend geregelt (§12 Abs.2)."]

  AUS_RATES --> Q_ABROAD_RATES["Frage: Nach welchen Regelungen werden Auslandstage- und -übernachtungsgelder bemessen?"]
  Q_ABROAD_RATES --> A_ABROAD_RATES["Antwort: Auslandstage- und -übernachtungsgelder werden nach §3 der Auslandsreisekostenverordnung (ARV) und der ARVVwV bemessen (§12 Abs.3)."]

  AUS_RATES --> Q_COUNTRY_BY_MIDNIGHT["Frage: Für welches Land gilt Tage- und Übernachtungsgeld, wenn vor Mitternacht zuletzt ein Land erreicht wurde?"]
  Q_COUNTRY_BY_MIDNIGHT --> A_COUNTRY_BY_MIDNIGHT["Antwort: Das Tage‑ und Übernachtungsgeld gilt für das Land, das vor Mitternacht Ortszeit zuletzt erreicht wurde; wird Inland vor Mitternacht zuletzt erreicht, gilt das Land des letzten Geschäftsortes im Ausland (§12 Abs.4)."]

  AUS_RATES --> Q_STOP_OVERNIGHT["Frage: Wie werden Zwischenlandungen bei Flug/Schiff berücksichtigt?"]
  Q_STOP_OVERNIGHT --> A_STOP_OVERNIGHT["Antwort: Ein Land gilt beim Flug/Schiff als erreicht, wenn das Flugzeug/Schiff dort landet; Zwischenlandungen bleiben unberücksichtigt, es sei denn, sie erfordern Übernachtungen (§12 Abs.5)."]

  AUS_LONG --> Q_ABROAD_15_WHEN_REDUCE["Frage: Wann wird das Auslandstagegeld ab dem 15. Tag um 25% ermäßigt?"]
  Q_ABROAD_15_WHEN_REDUCE --> A_ABROAD_15_WHEN_REDUCE["Antwort: Dauert ein Auslandsaufenthalt ohne Hin‑/Rückreisetage länger als 14 Tage, ist das Auslandstagegeld ab dem 15. Tag um 25% zu ermäßigen (§12 Abs.6)."]

  AUS_LONG --> Q_ABROAD_15_WHO_WAIVE["Frage: Wer kann in begründeten Fällen von der Ermäßigung absehen oder tatsächliche Übernachtungskosten erstatten?"]
  Q_ABROAD_15_WHO_WAIVE --> A_ABROAD_15_WHO_WAIVE["Antwort: Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann absehen; ab dem 15. Tag können statt Pauschale nachgewiesene Übernachtungskosten erstattet werden (§12 Abs.6)."]

  %% I. Trennungsgeld
  TRG --> Q_TRG_WHEN["Frage: Wann entsteht Anspruch auf Trennungsgeld bei Abordnung ohne Umzugskosten?"]
  Q_TRG_WHEN --> A_TRG_WHEN["Antwort: Anspruch entsteht bei Abordnung außerhalb des Dienst‑ oder Wohnortes ohne Zusage von Umzugskostenvergütung; Trennungsgeld deckt notwendige Auslagen unter Berücksichtigung häuslicher Ersparnis (§13 Abs.1)."]

  TRG --> Q_TRG_AMOUNT["Frage: Wovon hängen Höhe und Dauer des Trennungsgeldes ab?"]
  Q_TRG_AMOUNT --> A_TRG_AMOUNT["Antwort: Höhe und Dauer richten sich nach den notwendigen Auslagen und der häuslichen Ersparnis; das Finanzministerium kann eine Rechtsverordnung erlassen (§13 Abs.1 Satz2)."]

  TRG --> Q_TRG_TRAINEES["Frage: Gilt Trennungsgeld für Beamtinnen/Beamte auf Widerruf im Vorbereitungsdienst und Auszubildende?"]
  Q_TRG_TRAINEES --> A_TRG_TRAINEES["Antwort: Ja, Absatz 1 gilt auch für Beamtinnen/Beamte auf Widerruf im Vorbereitungsdienst; spezielle Regeln für Auszubildende regelt Abs.2 (§13 Abs.2)."]

  %% J. Anträge, Fristen, Belege, Anrechnung, Verzicht
  ANTR --> ANTR_FILE["J.1 Antragstellung & Ausschlussfrist"]
  ANTR --> ANTR_BELEGE["J.2 Belege, Anrechnung, Verzicht"]

  ANTR_FILE --> Q_HOW_TO_APPLY["Frage: Muss Reisekostenvergütung schriftlich oder elektronisch beantragt werden und wer erhält die Vergütung?"]
  Q_HOW_TO_APPLY --> A_HOW_TO_APPLY["Antwort: Reisekostenvergütung ist schriftlich oder elektronisch zu beantragen; die Vergütung wird den Dienstreisenden auf Antrag gezahlt (§3 Abs.1, §3 Abs.4)."]

  ANTR_FILE --> Q_DEADLINE["Frage: Innerhalb welcher Frist muss die Vergütung beantragt werden und wann beginnt die Frist?"]
  Q_DEADLINE --> A_DEADLINE["Antwort: Ausschlussfrist 6 Monate nach Beendigung der Dienstreise; die Frist beginnt mit dem Tag nach Beendigung der Dienstreise (bei §10 Abs.2 mit dem Tag, an dem die Reise geendet hätte) (§3 Abs.4)."]

  ANTR_BELEGE --> Q_REQUEST_RECEIPTS["Frage: Bis zu welchem Zeitpunkt dürfen zuständige Stellen die Vorlage der Kostenbelege verlangen?"]
  Q_REQUEST_RECEIPTS --> A_REQUEST_RECEIPTS["Antwort: Zuständige Stellen können bis zum Ablauf von sechs Monaten nach Antragstellung die Vorlage der maßgeblichen Kostenbelege verlangen (§3 Abs.4)."]

  ANTR_BELEGE --> Q_NO_RECEIPT_REJECT["Frage: Was passiert, wenn angeforderte Belege nicht innerhalb eines Monats vorgelegt werden?"]
  Q_NO_RECEIPT_REJECT --> A_NO_RECEIPT_REJECT["Antwort: Werden Belege auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden (§3 Abs.4)."]

  ANTR_BELEGE --> Q_KEEP_RECEIPTS["Frage: Wie lange sind Kostenbelege nach Erstattung aufzubewahren und vorzulegen?"]
  Q_KEEP_RECEIPTS --> A_KEEP_RECEIPTS["Antwort: Dienstreisende müssen Kostenbelege nach Erstattung bis zum Ablauf eines Jahres aufbewahren und auf Verlangen vorlegen (§3 Abs.4)."]

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
  ADMIN --> ADMIN_FINMIN["L.1 Befugnisse des Finanzministeriums"]
  ADMIN --> ADMIN_EXCEPTIONS["L.2 Zuständigkeiten für Ausnahmen, Pauschalen & Klima"]

  ADMIN_FINMIN --> Q_ADAPT_RATES["Frage: Welche Befugnisse hat das Finanzministerium zur Anpassung der Beträge in §§5 und 7?"]
  Q_ADAPT_RATES --> A_ADAPT_RATES["Antwort: Das Finanzministerium darf durch Rechtsverordnung die in §§5 und 7 Abs.1 festgesetzten Beträge an veränderte wirtschaftliche Verhältnisse anpassen (§14 Abs.1)."]

  ADMIN_FINMIN --> Q_ADMIN_REGS["Frage: Wer erlässt die allgemeinen Verwaltungsvorschriften und wie werden Sätze angepasst?"]
  Q_ADMIN_REGS --> A_ADMIN_REGS["Antwort: Das Finanzministerium erlässt die allgemeinen Verwaltungsvorschriften zu diesem Gesetz und regelt Verfahren und Zuständigkeiten für Anpassungen (§14 Abs.2)."]

  ADMIN_EXCEPTIONS --> Q_WHO_ALLOW_EXCEPT["Frage: Wer kann Ausnahmen von der niedrigsten Klasse oder Pauschalen zulassen?"]
  Q_WHO_ALLOW_EXCEPT --> A_WHO_ALLOW_EXCEPT["Antwort: Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann Ausnahmen zulassen; Zuständigkeiten sind gesetzlich geregelt (§4 Abs.1)."]

  ADMIN_EXCEPTIONS --> Q_MIN_CLIMATE_OBLIG["Frage: Welche Pflichten haben Ministerien und Hochschulen bzgl. Klimaausgleichszahlungen?"]
  Q_MIN_CLIMATE_OBLIG --> A_MIN_CLIMATE_OBLIG["Antwort: Ministerien und staatliche Hochschulen sind verpflichtet, jährliche Ausgleichszahlungen für dienstliche Flüge zu leisten (§4 Abs.4)."]

  ADMIN_EXCEPTIONS --> Q_REPORT_DRM["Frage: Wie sind Melde- und Nachweispflichten für Drittmittelfinanzierte Flüge geregelt?"]
  Q_REPORT_DRM --> A_REPORT_DRM["Antwort: Melde‑ und Nachweispflichten regeln die Verwaltungen; das Gesetz nennt die Pflicht zur Leistung der Ausgleichszahlung, sofern Drittmittelvorgaben dem nicht entgegenstehen (§4 Abs.4)."]

  ADMIN_EXCEPTIONS --> Q_SERVICE_EXCEPTION_PROCESS["Frage: Wie können Dienststellen Ausnahmen begründen und Genehmigungsprozesse gestalten?"]
  Q_SERVICE_EXCEPTION_PROCESS --> A_SERVICE_EXCEPTION_PROCESS["Antwort: Dienststellen können Ausnahmen mit besonderem dienstlichen Grund begründen und müssen dies dokumentieren; die oberste Dienstbehörde kann Ermächtigungen erteilen (§4 Abs.1; §12 Abs.6)."]

```