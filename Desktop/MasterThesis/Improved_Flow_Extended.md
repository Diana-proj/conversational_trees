```mermaid
%%{ init: { "theme": "default", "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "linear" } } }%%
%%{init: { "flowchart": { "htmlLabels": true },
           "themeVariables": { "fontSize": "12px" } }}%%
graph TD
  R["Was möchten Sie zur Planung, Durchführung oder Abrechnung von Dienstreisen wissen?"]

  %% Top-level sections (unchanged)
  R --> S1["1 Rechtsrahmen & Grundbegriffe"]
  R --> S2["2 Anordnung, Ausgangs-/Endpunkt, Wohnortregelung"]
  R --> S3["3 Wirtschaftlichkeit & Klimaschutz bei Verkehrsmitteln"]
  R --> S4["4 Fahrt- und Flugkosten (§4)"]
  R --> S5["5 Wegstreckenentschädigung (§5)"]
  R --> S6["6 Tagegeld (Verpflegungspauschale) (§6)"]
  R --> S7["7 Übernachtungsgeld (Unterkunftspauschale) (§7)"]
  R --> S8["8 Längerer Aufenthalt & Abschläge (§8, §12 Abs.6)"]
  R --> S9["9 Aufwands- und Pauschvergütung (§9) / Nebenkosten (§10)"]
  R --> S10["10 Spezielle Fälle: Versetzung, Fortbildung, Krankheit, Urlaub"]
  R --> S11["11 Auslandsdienstreisen — Bemessung & Zeitpunkte (§12)"]
  R --> S12["12 Verwaltung, Fristen, Belege, Anrechnung, Verzicht (§3 Abs.4–7)"]
  R --> S13["13 Querverweise & Sonderauslegungen"]

  %% ---------------------------
  %% 1 Rechtsrahmen & Grundbegriffe
  S1 --> S1A["1.1 Geltungsbereich"]
  S1 --> S1B["1.2 Dienstreise vs. Dienstgang"]

  %% 1.1 Geltungsbereich (split concise questions)
  S1A --> Q1_1["Gilt LRKG auch für Auslandsdienstreisen?"]
  S1A --> Q1_2["Wer ist vom Gesetz erfasst (Anwendungsbereich)?"]
  S1A --> Q1_3["Nach welchen Vorschriften werden Auslandstage-/Übernachtungsgelder geregelt?"]
  S1A --> Q1_4["Wer erlässt Verwaltungsvorschriften / Besonderheiten?"]

  Q1_1 --> A1_1["Grundsatz: §§1–11 gelten entsprechend für Auslandsdienstreisen. (§12 Abs.2–3)"]
  A1_1 --> Q1_1a["Liegt mindestens ein auswärtiger Geschäftsort im Ausland (Definition §12 Abs.1)?"]
  Q1_1a -->|"Ja"| A1_1a_yes["Auslandsdienstreise: §§1–11 LRKG gelten; Auslandstage‑/Übernachtungsgelder nach ARV/ARVVwV. (§12 Abs.1–3)"]
  Q1_1a -->|"Nein"| A1_1a_no["Keine Auslandsdienstreise; Inlandssätze und -vorschriften gelten. (§12 Abs.2–3)"]
  A1_1a_yes --> Q1_1a_dayrules["Welche Vorschriften gelten für Auslandstage‑/Übernachtungsgelder und welches Land bestimmt die Bemessung?"]
  Q1_1a_dayrules --> A1_1a_day["Auslandstage-/Übernachtungsgelder nach §3 ARV und ARVVwV; Bemessung nach dem Land, das vor Mitternacht Ortszeit zuletzt erreicht wurde; ab Tag 15 Ermäßigung 25 %. (§12 Abs.3–6)"]
  A1_1a_day --> X1_1_day15["→ S11C"]

  Q1_2 --> A1_2["Erfasst: Beamtinnen/Beamte des Landes, Gemeinden, Gemeindeverbände, Landkreise, unterstellte KÖR/Anstalten/Stiftungen, Richter sowie abgeordnete Personen. (§1 Abs.1)"]
  Q1_3 --> A1_3["Auslandstage-/Übernachtungsgelder richten sich nach §3 ARV und ARVVwV. (§12 Abs.3)"]
  Q1_4 --> A1_4["Finanzministerium erlässt allgemeine Verwaltungsvorschriften; oberste Dienstbehörden können Bereichsregelungen treffen. (§14 Abs.2; §4 Abs.1 Satz2)"]

  %% 1.2 Dienstreise vs Dienstgang
  S1B --> Q1B_1["Braucht eine Dienstreise Anordnung/Genehmigung?"]
  S1B --> Q1B_2["In welcher Form muss die Anordnung erfolgen?"]
  S1B --> Q1B_3["Gibt es Ausnahmen von der Genehmigungspflicht?"]
  S1B --> Q1B_4["Besteht Tagegeldanspruch bei Dienstgang >8 Stunden?"]
  S1B --> Q1B_5["Woran unterscheidet man Dienstreise und Dienstgang?"]

  Q1B_1 --> A1B_1["Ja. Dienstreisen sind anzuordnen oder zu genehmigen, außer wenn es nach Amt oder Wesen des Geschäfts nicht erforderlich ist. (§2 Abs.1)"]
  Q1B_2 --> A1B_2["Schriftlich oder elektronisch. (§2 Abs.1)"]
  Q1B_3 --> A1B_3["Ausnahmen z. B. für Richter bei richterlichen Amtsgeschäften und bestimmte Beauftragte. (§2 Abs.3)"]
  Q1B_4 --> A1B_4["Bei Dienstgängen besteht kein Tagegeld; bei Dienstgängen >8 Std werden nachgewiesene Verpflegungsaufwendungen bis zur Höhe des entsprechenden Tagegeldes erstattet. (§6 Abs.3)"]
  Q1B_5 --> A1B_5["Abgrenzung nach Dienstort vs. Dienststätte, Anordnung und Zweck: Dienstreise = außerhalb des Dienstortes; Dienstgang = außerhalb der Dienststätte am Dienst- oder Wohnort. (§2)"]

  %% ---------------------------
  %% 2 Anordnung, Ausgangs-/Endpunkt, Wohnortregelung
  S2 --> S2A["2.1 Ausgangs-/Endpunkt"]
  S2 --> S2B["2.2 Maßgebliche Wohnung"]
  S2 --> S2C["2.3 Genehmigung / Anordnung von Dienstreisen"]

  %% 2.1 Ausgangs-/Endpunkt split
  S2A --> Q2A_1["Wer bestimmt Ausgangs-/Endpunkt grundsätzlich?"]
  S2A --> Q2A_2["Kann die Dienststelle verbindlich die Dienststätte als Start/Ziel anordnen?"]
  S2A --> Q2A_3["Wie wird Fahrkostenerstattung bemessen, wenn Reise an der Wohnung beginnt/endet?"]
  S2A --> Q2A_4["Gibt es Sonderregeln für An-/Abreisezeiten oder Zwischentransfers?"]
  S2A --> Q2A_5["Darf die Wohnung als Ausgangs- und Endpunkt gewählt werden (Prüfung)?"]

  Q2A_1 --> A2A_1["Dienstreisende bestimmen Ausgangs-/Endpunkt grundsätzlich unter Wirtschaftlichkeitsgesichtspunkten. (§3 Abs.2)"]
  Q2A_2 --> A2A_2["Ja; die Dienststelle kann die Dienststätte als Ausgangs-/Endpunkt anordnen, z. B. wenn die Strecke unmittelbar an der Dienststätte vorbeiführt. (§3 Abs.2)"]
  Q2A_3 --> A2A_3["Bei Antritt/Beendigung an der Wohnung bemisst sich Erstattung nach Entfernung Wohnung–Ziel (Wegstrecke §5 oder Fahrtkostenerstattung §4). (§3 Abs.2)"]
  Q2A_4 --> A2A_4["Die Dauerbemessung richtet sich nach Abreise/Ankunft an Wohnung oder Dienststätte; Zwischentransfers sind nicht speziell geregelt. (§6 Abs.2; §3 Abs.2)"]

  %% 2.1.5 Wohnung vs. Dienststätte (integrated extension)
  Q2A_5 --> A3_2["Prüfung: Darf die/der Dienstreisende die Wohnung als Ausgangs- und Endpunkt bestimmen? (§3 Abs.2)"]
  A3_2 --> Q3_2a["Hat die zuständige Dienstvorgesetzte die Dienststätte verbindlich als Start- oder Endpunkt angeordnet?"]
  Q3_2a -->|"Ja"| Q3_2_route["Führt die Fahrtstrecke unmittelbar an der Dienststätte vorbei?"]
  Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
  Q3_2_route -->|"Ja"| A3_2_route_yes["Dann gilt die Dienststätte als Start- bzw. Zielpunkt. (§3 Abs.2)"]
  Q3_2_route -->|"Nein"| A3_2_route_no["Dann bleibt die Wohnung Ausgangs- und Endpunkt; eine verbindliche Anordnung fehlt. (§3 Abs.2)"]
  A3_2_route_yes --> X2_1_formref["→ Form der Anordnung prüfen → Q2_1_form"]
  A3_2_route_no --> X3_2_who["→ Wer legt Ausgangs-/Endpunkt fest? → A3_2"]
  A3_2a_no --> Q3_2a_no_calc["Welche Bemessung der Fahrkostenerstattung gilt bei Fahrt ab/zu der Wohnung?"]
  Q3_2a_no_calc --> Q3_2a_no_calc_rate["Besteht an der Benutzung des privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse?"]
  Q3_2a_no_calc_rate -->|"Ja"| A3_2a_no_calc_yes["Bei erheblichem dienstlichen Interesse: 0,35 € je km. (§3 Abs.2; §5 Abs.2)"]
  Q3_2a_no_calc_rate -->|"Nein"| A3_2a_no_calc_no["Ohne erhebliches dienstliches Interesse: 0,30 € je km. (§3 Abs.2; §5 Abs.1)"]
  A3_2a_no_calc_yes --> X3_2a_no_calc_xref["→ Keine nähere Definition des „erheblichen dienstlichen Interesses“ im LRKG; nähere Regelungen durch die oberste Dienstbehörde. (§5 Abs.2)"]

  %% 2.2 Maßgebliche Wohnung
  S2B --> Q2B_1["Welche Wohnung ist maßgeblich bei mehreren Wohnungen?"]
  S2B --> Q2B_2["Welche Kriterien bestimmen die maßgebliche Wohnung?"]
  S2B --> Q2B_3["Was gilt bei gleichwertigen/wechselnden Wohnsitzen?"]
  S2B --> Q2B_4["Wie werden Dienstwohnungen/vorübergehende Unterkünfte behandelt?"]

  Q2B_1 --> A2B_1["Maßgeblich ist die der Dienststätte am nächsten gelegene Wohnung oder Unterkunft. (§3 Abs.2)"]
  Q2B_2 --> A2B_2["Kriterium ist Nähe zur Dienststätte; weitere praktische Kriterien kann die Dienststelle festlegen. (§3 Abs.2)"]
  Q2B_3 --> A2B_3["Bei mehreren gleichwertigen Wohnungen ist in der Regel die der Dienststätte nächste Wohnung maßgebend; Einzelfallentscheidungen obliegen der Dienststelle. (§3 Abs.2)"]
  Q2B_4 --> A2B_4["Dienstwohnungen oder vorübergehende Unterkünfte werden wie Wohnungen/Unterkünfte behandelt; bei Unklarheiten entscheidet die Dienststelle. (§3 Abs.2; §§7,8)"]

  %% 2.3 Genehmigung / Anordnung (INTEGRATED EXTENSION)
  S2C --> A2_1["Grundsatz: Dienstreisen bedürfen schriftlicher oder elektronischer Anordnung/Genehmigung. (§2 Abs.1 LRKG)"]
  A2_1 --> Q2_1_exc["Trifft Ausnahme §2 Abs.1 S.2 (Anordnung nicht erforderlich wegen Amt/Wesen des Geschäfts) zu?"]
  Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Anordnung/Genehmigung erforderlich. (§2 Abs.1 S.2)"]
  Q2_1_exc -->|"Nein"| A2_1_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1)"]
  A2_1 --> Q2_1_loc["Liegt Fortbildungs-/Geschäftsort außerhalb Ihres Dienstortes?"]
  Q2_1_loc -->|"Ja"| A2_1_loc_yes["Handelt es sich um eine Dienstreise; prüfen, ob Teilnahme angeordnet/genehmigt wurde. (§2 Abs.1)"]
  Q2_1_loc -->|"Nein"| A2_1_loc_no["Kein Auswärtiger Geschäftsort → kein Dienstreisebegriff (Dienstgang). (§2 Abs.1)"]
  A2_1_loc_yes --> X2_1_formref["→ Form der Anordnung prüfen → Q2_1_form"]
  A2_1_loc_no --> X2_1_tg["→ Tagegeldanspruch bei Dienstgang prüfen → S6"]
  A2_1 --> Q2_1_form["In welcher Form muss die Anordnung erfolgen?"]
  Q2_1_form --> A2_1_form["Schriftlich oder elektronisch (z. B. dienstliche E‑Mail oder internes System); mündliche Zustimmung genügt nicht. (§2 Abs.1)"]
  A2_1_form --> X2_1_mail["→ Zuständigkeit/Vertretung bei der Anordnung prüfen (wer sendet/zeichnet) → S2.3"]
  A2_1_form --> X2_1_oral["→ Mündliche Zustimmung genügt nicht; Ausnahmen prüfen → Q2_1_exc"]
  A2_1 --> X2_1_spec["→ Sonderregel prüfen: Richter/innen und bestimmte Landesbeauftragte benötigen keine Genehmigung (§2 Abs.3) → S2.3"]

  %% ---------------------------
  %% 3 Wirtschaftlichkeit & Klimaschutz
  S3 --> S3A["3.1 Wirtschaftlichkeitprinzip"]
  S3 --> S3B["3.2 Wahl des Beförderungsmittels & Klimaschutz"]

  %% 3.1
  S3A --> Q3A_1["Dürfen Dienstreisen nur bei fehlender kostengünstiger Alternative erfolgen?"]
  S3A --> Q3A_2["Welche Prüfpflichten bestehen vor Antritt (Alternativen)?"]
  S3A --> Q3A_3["Werden Fahrtkosten erstattet bei unentgeltlicher Beförderung?"]
  S3A --> Q3A_4["Wie sind vergünstigte/interne Beförderungen zu behandeln?"]

  Q3A_1 --> A3A_1["Ja. Dienstreisen sollen nur erfolgen, wenn keine kostengünstigere Art der Erledigung möglich und sinnvoll ist. (§2 Abs.1 letzter Satz)"]
  Q3A_2 --> A3A_2["Vor Antritt sind kostengünstige Alternativen (Telefon/Video) zu prüfen; Wirtschaftlichkeit ist zu berücksichtigen. (§2 Abs.1)"]
  Q3A_3 --> A3A_3["Fahrtkosten werden nicht erstattet, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann. (§3 Abs.3 Satz2)"]
  Q3A_4 --> A3A_4["Vergünstigte oder interne Beförderungsmöglichkeiten sind unter Wirtschaftlichkeit zu berücksichtigen; konkrete Handhabung regelt die Dienststelle. (§3 Abs.1 u.3)"]

  %% 3.2 Wahl des Beförderungsmittels & Klimaschutz (integrated)
  S3B --> Q3B_1["Bin ich frei in Wahl des Beförderungsmittels?"]
  S3B --> Q3B_2["Kann die Dienststelle ein Verkehrsmittel vorschreiben?"]
  S3B --> Q3B_3["Muss CO2-Emissionen dokumentiert werden?"]
  S3B --> Q3B_4["Wie wirken Klimaziele mit Wirtschaftlichkeit zusammen?"]
  S3B --> A3_3["Prüfung: Freiheit der Wahl des Beförderungsmittels vs. wirtschaftliche/klimatische Vorgaben"]

  Q3B_1 --> A3B_1["Dienstreisende sind grundsätzlich frei in der Wahl des Verkehrsmittels, müssen jedoch Wirtschaftlichkeit und Klimaschutz berücksichtigen. (§3 Abs.3)"]
  Q3B_2 --> A3B_2["Ja; die Dienststelle bzw. oberste Dienstbehörde kann ein Verkehrsmittel vorschreiben, insbesondere aus dienstlichen Gründen. (§4 Abs.1; §3 Abs.3)"]
  Q3B_3 --> A3B_3["Keine ausdrückliche gesetzliche Dokumentationspflicht zu CO2-Emissionen; Klimaschutz ist bei der Wahl zu beachten. (§3 Abs.3; §4 Abs.1 letzter Satz)"]
  Q3B_4 --> A3B_4["Klimaschutzanforderungen sind neben Wirtschaftlichkeit zu berücksichtigen; bei Flugentscheidungen müssen dienstliche/wirtschaftliche Gründe Klimabelange überwiegen. (§3 Abs.3; §4 Abs.1)"]

  %% nodes linking S2 and S3 considerations
  A3_2 --> A3_3

  A3_3 --> Q3_3a["Liegt eine unentgeltliche Beförderungsmöglichkeit vor (z. B. Dienstfahrkarte)?"]
  Q3_3a -->|"Ja"| A3_3a_yes["Fahrtkosten werden nicht erstattet. (§3 Abs.3)"]
  Q3_3a -->|"Nein"| A3_3a_no["Wahl bleibt frei; Erstattung richtet sich nach §§4–5 (Bahn: niedrigste Klasse; Privat‑PKW: 0,30 €/km bzw. 0,35 €/km bei erheblichem dienstlichen Interesse; Mietwagen/Taxi nur bei triftigem Grund). (§3 Abs.3; §§4–5)"]
  A3_3 --> Q3_3b["Hat die Dienststelle aus dienstlichen Gründen die Benutzung eines bestimmten Beförderungsmittels angeordnet?"]
  Q3_3b -->|"Ja"| A3_3b_yes["Dienstliche Anordnung gilt und schränkt die Wahl ein. (§3 Abs.3)"]
  Q3_3b -->|"Nein"| A3_3b_no["Wahl des Beförderungsmittels bleibt frei. (§3 Abs.3)"]
  A3_3 --> Q3_3c["Überwiegen dienstliche/wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
  Q3_3c -->|"Ja"| A3_3c_yes["Flugkosten erstattungsfähig; erstattet wird grundsätzlich der Preis der niedrigsten Flugklasse; Klimaausgleichskosten sind in die Wirtschaftlichkeitsprüfung einzubeziehen. (§4 Abs.1)"]
  Q3_3c -->|"Nein"| A3_3c_no["Flugkosten nicht erstattungsfähig, wenn Klimabelange überwiegen. (§4 Abs.1)"]
  A3_3c_yes --> Q3_3c_exc["Liegt ein Grad der Behinderung ≥50 oder gesundheitliche Notwendigkeit vor?"]
  Q3_3c_exc -->|"Ja"| A3_3c_exc_yes["Bei GdB ≥50 oder gesundheitlicher Notwendigkeit werden Kosten der nächsthöheren Flugklasse erstattet. (§4 Abs.2)"]
  Q3_3c_exc -->|"Nein"| A3_3c_exc_no["Keine Erstattung einer höheren Flugklasse; Erstattung bleibt auf niedrigste Flugklasse beschränkt. (§4 Abs.1)"]
  A3_3 --> X3_3_prescribe["→ Siehe Erstattungs- und Beschränkungsregeln (§§4–5)"]
  A3_3a_no --> Q3_3d["Welche Stelle entscheidet über Ausnahmen von Erstattung der niedrigsten Beförderungsklasse?"]
  Q3_3d --> A3_3d["Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann Ausnahmen zulassen; das Finanzministerium kann durch Verwaltungsvorschrift Ausnahmen bestimmen. (§4 Abs.1)"]
  A3_3 --> X3_3_tg["→ Tagegeld: Inland 24 € je voller Kalendertag; Übernachtungsgeld Inland 20 €, Ausland 30 €. (§6 Abs.1; §7 Abs.1; §12 Abs.3)"]

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

  %% ---------------------------
  %% 4 Fahrt- und Flugkosten (§4) — restructure into explicit choice nodes
  S4 --> S4A["4.1 Regel: niedrigste Beförderungsklasse"]
  S4 --> S4B["4.2 Ausnahmen / Flugbedingungen"]
  S4 --> S4C["4.3 Behinderung / gesundheitliche Gründe"]
  S4 --> S4D["4.4 Klimaausgleich & Pflichten"]
  S4 --> S4E["4.5 Mietwagen / Taxi / Carsharing"]

  %% 4.1
  S4A --> Q4A_1["Welche Klasse wird erstattet?"]
  Q4A_1 --> A4A_1["Erstattet werden Kosten der niedrigsten Beförderungsklasse. (§4 Abs.1 Satz1)"]

  S4A --> Q4A_2["Wie sind Reservierungen/Tarifunterschiede zu behandeln?"]
  Q4A_2 --> A4A_2["Reservierungen und Tarifunterschiede sind wirtschaftlich zu prüfen; grundsätzlich Erstattung bis zur niedrigsten Klasse. (§4 Abs.1)"]

  %% 4.2 Ausnahmen / Flüge split
  S4B --> Q4B_1["Wann sind Ausnahmen von Niedrigstklasse möglich?"]
  S4B --> Q4B_2["Wer entscheidet über Ausnahmen?"]
  S4B --> Q4B_3["Sind Flugkosten erstattungsfähig?"]
  S4B --> Q4B_4["Welche Flugklasse gilt grundsätzlich?"]

  Q4B_1 --> A4B_1["Ausnahmen bei besonderen dienstlichen Gründen; oberste Dienstbehörde kann Ausnahmen zulassen. (§4 Abs.1)"]
  Q4B_2 --> A4B_2["Oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde entscheidet; Finanzministerium kann per Verwaltungsvorschrift regeln. (§4 Abs.1; §14)"]
  Q4B_3 --> A4B_3["Flugkosten sind erstattungsfähig, wenn dienstliche/wirtschaftliche Gründe Klimabelange überwiegen. (§4 Abs.1)"]
  Q4B_4 --> A4B_4["Grundsätzlich werden die Kosten der niedrigsten Flugklasse erstattet; Ausnahmen per Verwaltungsvorschrift möglich. (§4 Abs.1)"]

  %% 4.3 health
  S4C --> Q4C_1["Grad der Behinderung ≥50: nächsthöhere Klasse?"]
  S4C --> Q4C_2["Andere gesundheitliche Gründe: nächsthöhere Klasse?"]

  Q4C_1 --> A4C_1["Ja; bei GdB ≥50 werden die Kosten der nächsthöheren Klasse erstattet. (§4 Abs.2)"]
  Q4C_2 --> A4C_2["Ja; andere gesundheitliche Gründe können Erstattung der nächsthöheren Klasse rechtfertigen. (§4 Abs.2)"]

  %% 4.4 Klimaausgleich
  S4D --> Q4D_1["Sind Klimaausgleichskosten in Wirtschaftlichkeits-Rechnung zu berücksichtigen?"]
  S4D --> Q4D_2["Gibt es Pflicht zu jährlichen Klimaausgleichszahlungen?"]

  Q4D_1 --> A4D_1["Ja; Kosten für Klimaausgleichszahlungen sind bei der Wirtschaftlichkeitsberechnung für Flugreisen einzubeziehen. (§4 Abs.1 letzter Satz)"]
  Q4D_2 --> A4D_2["Ja; oberste Dienstbehörden sind verpflichtet, jährliche Klimaausgleichszahlungen für bestimmte Gruppen zu leisten. (§4 Abs.4)"]

  %% 4.5 Mietwagen / Taxi / Carsharing
  S4E --> Q4E_1["Wann werden Mietwagen/Taxi/Carsharing erstattet?"]
  S4E --> Q4E_2["Darf ohne triftigen Grund höhere Vergütung als ÖPNV gezahlt werden?"]
  S4E --> Q4E_3["Wird Carsharing-Mitgliedsgebühr wegen Privatnutzung gekürzt?"]
  S4E --> Q4E_4["Wie ist Abrechnung/Nachweis beim Carsharing?"]

  Q4E_1 --> A4E_1["Bei triftigem Grund (dienstliche Notwendigkeit) werden notwendige Kosten erstattet. (§4 Abs.3)"]
  Q4E_2 --> A4E_2["Nein; ohne triftigen Grund darf nicht mehr vergütet werden als bei Benutzung öffentlichen Verkehrs. (§4 Abs.3)"]
  Q4E_3 --> A4E_3["Nein; bei Carsharing erfolgt keine Kürzung der Mitgliedsgebühr wegen privater Nutzung. (§4 Abs.3 letzter Satz)"]
  Q4E_4 --> A4E_4["Abrechnung nach tatsächlichem Aufwand; konkrete Nachweisregelungen legt die Dienststelle fest. (§4 Abs.3)"]

  %% ---------------------------
  %% 5 Wegstreckenentschädigung (§5) — explicit choices
  S5 --> S5A["5.1 Privat-KFZ Sätze"]
  S5 --> S5B["5.2 Erhöhter Satz / Zuschlag"]
  S5 --> S5C["5.3 Fahrrad / E‑Bike / Pedelec"]

  S5A --> Q5A_1["Wie hoch ist Entschädigung Privat-KFZ?"]
  Q5A_1 --> A5A_1["30 Cent pro Kilometer. (§5 Abs.1)"]

  S5A --> Q5A_2["Wann wird pauschal statt Einzelnachweis gezahlt?"]
  Q5A_2 --> A5A_2["Wegstreckenentschädigung ist pauschal je zurückgelegter Strecke; Abrechnungsmodalitäten regelt die Dienststelle. (§5 Abs.1)"]

  S5B --> Q5B_1["Wann gilt erhöhter Satz 35 Ct/km?"]
  S5B --> Q5B_2["Wer entscheidet über Anwendung des erhöhten Satzes?"]
  S5B --> Q5B_3["Gibt es Zuschlag für schlechte Fahrwege und wie hoch?"]
  S5B --> Q5B_4["Welche Nachweise sind für Zuschlag nötig?"]

  Q5B_1 --> A5B_1["Bei erheblichem dienstlichen Interesse kann die Wegstreckenentschädigung 35 Ct/km betragen. (§5 Abs.2 Satz1)"]
  Q5B_2 --> A5B_2["Anwendung des erhöhten Satzes bedarf der Zustimmung oder Regelung durch die oberste Dienstbehörde. (§5 Abs.2 Satz2)"]
  Q5B_3 --> A5B_3["Ein Zuschlag von 5 Ct/km kann gewährt werden bei regelmäßigen Fahrten auf unbefestigten/schwer befahrbaren Wegen. (§5 Abs.2 Satz2)"]
  Q5B_4 --> A5B_4["Für den Zuschlag sind Nachweise der regelmäßigen Nutzung solcher Wege erforderlich; die Dienststelle bestimmt die konkreten Nachweise. (§5 Abs.2)"]

  S5C --> Q5C_1["Wie hoch ist Entschädigung Fahrrad/E‑Bike/Pedelec?"]
  S5C --> Q5C_2["Gibt es Sonderregeln für Dienstfahrräder/Job-Bikes?"]

  Q5C_1 --> A5C_1["25 Cent pro Kilometer. (§5 Abs.3)"]
  Q5C_2 --> A5C_2["Sonderregelungen für Dienstfahrräder sind nicht ausdrücklich im Gesetz; Dienststelle kann Regelungen treffen. (§5; §9)"]

  %% ---------------------------
  %% 6 Tagegeld (§6) — split into explicit hour-based choices
  S6 --> S6A["6.1 Höhe & Staffelung"]
  S6 --> S6B["6.2 Reisedauer / Stichtage"]
  S6 --> S6C["6.3 Dienstgänge vs. Dienstreisen"]
  S6 --> S6D["6.4 Kürzungen bei unentgeltlicher Verpflegung"]

  S6A --> Q6A_1["Wie hoch ist Tagegeld für vollen Kalendertag?"]
  Q6A_1 --> A6A_1["24 € pro vollem Kalendertag. (§6 Abs.1 Satz1)"]

  S6A --> Q6A_2["Wie viel Tagegeld am An-/Abreisetag bei >8 Std / >14 Std?"]
  Q6A_2 --> A6A_2["Bei >8 Std: 6 €; bei >14 Std: 12 €. (§6 Abs.1 Satz2)"]

  S6A --> Q6A_3["Gibt es unterschiedliche Sätze Inland/Ausland?"]
  Q6A_3 --> A6A_3["Ja; Inland: gesetzlicher Satz (24 € Volltag), Auslandssätze richten sich nach ARV/ARVVwV. (§6 Abs.1; §12 Abs.3)"]

  S6A --> Q6A_4["Wie sind kurze Dienstreisen (Stunden) gestaffelt?"]
  Q6A_4 --> A6A_4["Für Kurzreisen gilt die Stundenstaffelung am An-/Abreisetag; konkrete Stundengrenzen siehe >8 Std / >14 Std. (§6 Abs.1)"]

  S6B --> Q6B_1["Nach welchen Zeitpunkten wird Reisedauer bestimmt?"]
  S6B --> Q6B_2["Gibt es Abweichungen bei Zeitverschiebungen/Grenzüberschreitungen?"]

  Q6B_1 --> A6B_1["Dauer bemisst sich nach Abreise/Ankunft an der Wohnung, es sei denn Beginn/Ende an der Dienststätte wurde angeordnet. (§6 Abs.2)"]
  Q6B_2 --> A6B_2["Abweichungen bei grenzüberschreitenden Reisen/Zeitzonen regelt ARV/ARVVwV; LRKG verweist hierauf. (§12 Abs.3–5)"]

  S6C --> Q6C_1["Besteht Tagegeldanspruch bei Dienstgang?"]
  S6C --> Q6C_2["Wie ist Grenze Tagegeld vs. Wegstreckenentschädigung gezogen?"]

  Q6C_1 --> A6C_1["Für Dienstgänge besteht kein Anspruch auf Tagegeld; bei Dienstgängen >8 Std werden Verpflegungsaufwendungen bis zur Höhe des Tagegeldes einer Dienstreise gleicher Dauer erstattet. (§6 Abs.3)"]
  Q6C_2 --> A6C_2["Tagegeld deckt Verpflegung; Wegstreckenentschädigung regelt Fahrten mit privatem KFZ; Abrechnung nach §§5,6."]

  S6D --> Q6D_1["Wie wird Tagegeld bei unentgeltlicher Verpflegung gekürzt?"]
  Q6D_1 --> A6D_1["Bei unentgeltlicher Verpflegung wird vom Tagegeld 20% für Frühstück und jeweils 40% für Mittag/Abendessen abgezogen. (§6 Abs.4)"]
  S6D --> Q6D_2["Wie sind Teilkostenzahlungen/Zwischenspeisungen zu behandeln?"]
  Q6D_2 --> A6D_2["Zwischenspeisungen oder in Kosten enthaltene Teilverpflegung gelten als unentgeltliche Verpflegung und sind entsprechend zu kürzen. (§6 Abs.4)"]

  %% ---------------------------
  %% 7 Übernachtungsgeld (§7) — explicit Inland/Ausland, exclusions
  S7 --> S7A["7.1 Pauschbeträge & Erstattung höherer Kosten"]
  S7 --> S7B["7.2 Fälle ohne Anspruch"]
  S7 --> S7C["7.3 Unterkunft bereits enthalten / zusätzliche Übernachtung"]

  S7A --> Q7A_1["Wie hoch ist pauschales Übernachtungsgeld Inland?"]
  S7A --> Q7A_2["Wie hoch ist pauschales Übernachtungsgeld Ausland?"]
  Q7A_1 --> A7A_1["Inland: 20 €. (§7 Abs.1)"]
  Q7A_2 --> A7A_2["Ausland: 30 € (Pauschalgrundsatz; länderspezifische Sätze durch ARV/ARVVwV). (§7 Abs.1; §12 Abs.3)"]

  S7A --> Q7A_3["Wer erlässt Höchstbeträge für erstattungsfähige höhere Übernachtungskosten?"]
  Q7A_3 --> A7A_3["Das Finanzministerium bestimmt per Verwaltungsvorschrift, bis zu welcher Höhe Übernachtungskosten als notwendig gelten. (§7 Abs.1; §14 Abs.1)"]

  S7B --> Q7B_1["In welchen Fällen wird Übernachtungsgeld nicht gewährt?"]
  Q7B_1 --> A7B_1["Nicht gewährt bei Benutzung von Reiseunterkunft, Aufenthalt in eigener Wohnung, unentgeltlicher Arbeitgeberunterkunft oder wenn Unterkunftskosten bereits in erstattungsfähigen Kosten enthalten sind. (§7 Abs.2 Nr.1–4)"]

  S7B --> Q7B_2["Wann entfällt Anspruch wegen Arbeitgebergestellung?"]
  Q7B_2 --> A7B_2["Kein Anspruch bei unentgeltlicher Bereitstellung einer Unterkunft durch den Dienstherrn; gilt auch, wenn Unterkunft ohne triftigen Grund nicht genutzt wird. (§7 Abs.2 Nr.3)"]

  S7C --> Q7C_1["Wird Übernachtungsgeld gezahlt, wenn Unterkunft bereits in Fahrt-/sonstigen Kosten enthalten ist?"]
  Q7C_1 --> A7C_1["Grundsätzlich nicht; Ausnahme: zusätzliche notwendige Übernachtung wegen zu früher Ankunft oder zu später Abfahrt. (§7 Abs.2 Nr.4)"]

  S7C --> Q7C_2["Wann rechtfertigt zusätzliche Übernachtung gesonderte Erstattung?"]
  Q7C_2 --> A7C_2["Wenn Übernachtung aufgrund zu früher Ankunft am Geschäftsort oder zu später Abfahrt zusätzlich erforderlich ist. (§7 Abs.2 Nr.4)"]

  %% ---------------------------
  %% 8 Längerer Aufenthalt (§8 & §12 Abs.6)
  S8 --> S8A["8.1 Inland: längerer Aufenthalt (§8)"]
  S8 --> S8B["8.2 Ausland: Langzeitregelung (§12 Abs.6)"]

  S8A --> Q8A_1["Ab wann gelten besondere Sätze bei längerem Aufenthalt im Inland?"]
  Q8A_1 --> A8A_1["Bei Aufenthalt >7 Tage am selben auswärtigen Geschäftsort gilt ab dem 8. Tag die Vergütung wie bei Abordnung. (§8)"]

  S8A --> Q8A_2["Welche praktischen Folgen hat das für Dienstplanung?"]
  Q8A_2 --> A8A_2["Ab dem 8. Tag sind abordnungsähnliche Sätze anzuwenden; Dienststellen sollten Dienstpläne entsprechend berücksichtigen. (§8)"]

  S8B --> Q8B_1["Ab wann wird Auslandstagegeld ab 15. Tag ermäßigt?"]
  Q8B_1 --> A8B_1["Bei Auslandsaufenthalt ohne Hin-/Rückreisetage länger als 14 Tage wird das Auslandstagegeld ab dem 15. Tag um 25% ermäßigt. (§12 Abs.6)"]

  S8B --> Q8B_2["Wer kann von der Ermäßigung absehen?"]
  Q8B_2 --> A8B_2["Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann in begründeten Fällen von der Ermäßigung absehen. (§12 Abs.6)"]

  S8B --> Q8B_3["Ab dem 15. Tag: Übernachtungspauschale oder nachgewiesene Kosten?"]
  Q8B_3 --> A8B_3["Ab dem 15. Tag werden anstelle des Pauschalübernachtungsgeldes die nachgewiesenen notwendigen Übernachtungskosten erstattet. (§12 Abs.6)"]

  %% ---------------------------
  %% 9 Aufwands- & Pauschvergütung (§9) / Nebenkosten (§10)
  S9 --> S9A["9.1 Aufwandsvergütung statt Einzelleistungen"]
  S9 --> S9B["9.2 Pauschvergütung bei regelmäßigen Reisen"]
  S9 --> S9C["9.3 Sonstige Nebenkosten (§10)"]
  S9 --> S9D["9.4 Erstattung Vorbereitungsaufwand bei Entfall"]

  S9A --> Q9A_1["Kann statt Tage-/Übernachtungs- und Auslagenerstattung eine Aufwandsvergütung gezahlt werden?"]
  Q9A_1 --> A9A_1["Ja; Dienstreisende mit erfahrungsgemäß geringeren Aufwendungen können eine Aufwandsvergütung erhalten; nähere Bestimmungen durch die oberste Dienstbehörde. (§9 Abs.1)"]

  S9A --> Q9A_2["Wie wird Höhe/Umfang der Aufwandsvergütung bestimmt?"]
  Q9A_2 --> A9A_2["Höhe und Umfang werden nach näherer Bestimmung der obersten Dienstbehörde oder ermächtigten nachgeordneten Behörde festgelegt. (§9 Abs.1)"]

  S9B --> Q9B_1["Kann es Pauschvergütung bei regelmäßigen Reisen geben?"]
  Q9B_1 --> A9B_1["Ja; die oberste Dienstbehörde kann bei regelmäßigen oder gleichartigen Reisen eine Pauschvergütung anstelle der Reisekostenvergütung oder einzelner Teile gewähren. (§9 Abs.2)"]

  S9B --> Q9B_2["Wie ist Pauschale zu bemessen?"]
  Q9B_2 --> A9B_2["Die Pauschale ist nach dem Durchschnitt der sonst anfallenden Einzelvergütungen zu bemessen. (§9 Abs.2)"]

  S9C --> Q9C_1["Wer erstattet sonstige notwendige Auslagen (z. B. Park, Telekom)?"]
  Q9C_1 --> A9C_1["Notwendige Auslagen, die nicht unter §§4–9 fallen, werden als Nebenkosten erstattet. (§10 Abs.1)"]

  S9C --> Q9C_2["Welche Beispiele zählen zu Nebenkosten?"]
  Q9C_2 --> A9C_2["Beispiele: Telekommunikation, Parkgebühren, Internetnutzung; Einzelfallregelung durch die Dienststelle. (§10 Abs.1)"]

  S9D --> Q9D_1["Werden Vorbereitungsaufwendungen bei nicht zu vertretendem Entfall erstattet?"]
  Q9D_1 --> A9D_1["Ja; notwendige Vorbereitungsaufwendungen werden erstattet, wenn die Dienstreise aus Gründen entfällt, die Dienstreisende nicht zu vertreten haben. (§10 Abs.2)"]

  S9D --> Q9D_2["Welche Nachweise gelten für diese Erstattung?"]
  Q9D_2 --> A9D_2["Nachweise und Umfang richtet die zuständige Stelle; das Gesetz verlangt Erstattung nur notwendiger, berücksichtigungsfähiger Aufwendungen. (§10 Abs.2)"]

  %% ---------------------------
  %% 10 Spezielle Fälle
  S10 --> S10A["10.1 Versetzung/Abordnung & Trennungsgeld (§13)"]
  S10 --> S10B["10.2 Fortbildung / Nebentätigkeit"]
  S10 --> S10C["10.3 Dienstliche Anordnung während Urlaub/privater Reise"]
  S10 --> S10D["10.4 Krankheit / Krankenhaus während Dienstreise"]
  S10 --> S10E["10.5 Fahrten Wohnung–Dienststätte aus besonderem Anlass"]

  %% 10.1
  S10A --> Q10A_1["Wann besteht Anspruch auf Trennungsgeld bei Abordnung?"]
  S10A --> Q10A_2["Gilt Trennungsgeld für Beamtinnen und Beamte auf Widerruf im Vorbereitungsdienst?"]
  S10A --> Q10A_3["Wird Tagegeld bei Versetzung/Abordnung bis Ankunft gezahlt?"]
  S10A --> Q10A_4["Wie sind Kombinationen (Umzug + Dienstreise) zu behandeln?"]

  Q10A_1 --> A10A_1["Trennungsgeld wird bei Abordnung ohne Zusage der Umzugskostenvergütung für notwendige Auslagen gezahlt; Details per Rechtsverordnung. (§13 Abs.1)"]
  Q10A_2 --> A10A_2["Ja; Regelungen gelten auch für Beamtinnen/Beamte auf Widerruf im Vorbereitungsdienst bei Abordnungen. (§13 Abs.2)"]
  Q10A_3 --> A10A_3["Ja; Tagegeld wird bis zur Ankunft am neuen Dienstort gewährt (bis Ablauf des Ankunftstages, ggf. ergänzend Trennungsgeld/Übernachtungsgeld). (§11 Abs.1; §13)"]
  Q10A_4 --> A10A_4["Kombinationen sind nach einschlägigen Vorschriften zu behandeln; Details regelt die Dienststelle bzw. die Verordnung zum Trennungsgeld. (§11 Abs.1; §13)"]

  %% 10.2
  S10B --> Q10B_1["Werden Fortbildungskosten erstattet?"]
  S10B --> Q10B_2["Welche Nachweise sind für Fortbildungskosten nötig?"]
  S10B --> Q10B_3["Besteht Anspruch bei Nebentätigkeit mit anderer Stelle?"]
  S10B --> Q10B_4["Wie erfolgt Koordination mit anderer zahlender Stelle?"]

  Q10B_1 --> A10B_1["Ja; Kosten für Fortbildungen im dienstlichen Interesse können bis zur Höhe der Reisekostenvergütung erstattet werden. (§11 Abs.2)"]
  Q10B_2 --> A10B_2["Voraussetzungen/Nachweise müssen das dienstliche Interesse belegen; Anforderungen legt die Dienststelle/Verwaltungsvorschrift fest. (§11 Abs.2)"]
  Q10B_3 --> A10B_3["Anspruch besteht nur insoweit, wie nicht eine andere Stelle Auslagenerstattung zu gewähren hat. (§3 Abs.6)"]
  Q10B_4 --> A10B_4["Koordination erfolgt durch Anrechnung oder Vereinbarungen; Dienstreisende haben nur Teilanspruch, wenn andere Stellen leisten. (§3 Abs.6)"]

  %% 10.3
  S10C --> Q10C_1["Wie wird Vergütung bemessen, wenn Dienstreise mit Urlaub verbunden?"]
  S10C --> Q10C_2["Was gilt, wenn Dienstreise am Urlaubsort angeordnet wird?"]
  S10C --> Q10C_3["Ist Rückreise bei dienstlicher vorzeitiger Beendigung erstattungsfähig?"]
  S10C --> Q10C_4["Wer trägt Aufwendungen durch Unterbrechung/Stornokosten?"]

  Q10C_1 --> A10C_1["Reisekostenvergütung wird so bemessen, als ob nur die Dienstreise durchgeführt worden wäre; sie darf die nach tatsächlichem Verlauf entstehende Vergütung nicht übersteigen. (§11 Abs.3)"]
  Q10C_2 --> A10C_2["Wenn Dienstreise am Urlaubsort angeordnet/genehmigt wird, bemisst sich die Vergütung nach Abreise/Ankunft an diesem Ort abweichend. (§11 Abs.4)"]
  Q10C_3 --> A10C_3["Ja; Rückreise vom Urlaubs-/Aufenthaltsort zur Dienststätte gilt als Dienstreise und wird vergütet. (§11 Abs.5)"]
  Q10C_4 --> A10C_4["Aufwendungen durch Unterbrechung oder vorzeitige Beendigung werden in angemessenem Umfang erstattet; Stornokosten können ersetzt werden, soweit dienstlich veranlasst und notwendig. (§11 Abs.6)"]

  %% 10.4
  S10D --> Q10D_1["Wer trägt Kosten bei Krankenhausaufnahme während Dienstreise?"]
  S10D --> Q10D_2["Welche Nachweise sind erforderlich?"]

  Q10D_1 --> A10D_1["Bei Krankenhausaufnahme werden für jeden vollen Kalendertag die notwendigen Auslagen für Unterkunft am Geschäftsort erstattet. (§11 Abs.7)"]
  Q10D_2 --> A10D_2["Ärztliche Bescheinigungen bzw. Krankenhausunterlagen sind als Nachweise erforderlich; genaue Anforderungen legt die zuständige Stelle fest. (§11 Abs.7)"]

  %% 10.5
  S10E --> Q10E_1["Können Fahrten Wohnung–Dienststätte aus besonderem Anlass erstattet werden?"]
  S10E --> Q10E_2["Beispiele für besondere Anlässe?"]

  Q10E_1 --> A10E_1["Ja; bei besonderen dienstlichen Anlässen können die entstandenen notwendigen Fahrtkosten erstattet werden. (§11 Abs.8)"]
  Q10E_2 --> A10E_2["Beispiele: Einsätze außerhalb üblicher Arbeitszeit, dringende Nachrückdienste; Entscheidung liegt bei der Dienststelle. (§11 Abs.8)"]

  %% ---------------------------
  %% 11 Auslandsdienstreisen (§12) — explicit choices
  S11 --> S11A["11.1 Landeszuordnung / Mitternachtsregel"]
  S11 --> S11B["11.2 Landekriterium bei Flug/Schiff; Zwischenlandungen"]
  S11 --> S11C["11.3 Ermäßigung ab Tag 15 (Langzeit) — cross-ref zu §8/§12"]

  S11A --> Q11A_1["Für welches Land wird Tage-/Übernachtungsgeld bemessen (Mitternachtsregel)?"]
  Q11A_1 --> A11A_1["Das Tage- und Übernachtungsgeld wird für das Land gewährt, das vor Mitternacht Ortszeit zuletzt erreicht wurde; erreicht das Inland vor Mitternacht zuletzt, gilt das Land des letzten Auslandsgeschäftsortes. (§12 Abs.4)"]

  S11A --> Q11A_2["Wie sind Zeitverschiebungen/Transitländer zu behandeln?"]
  Q11A_2 --> A11A_2["Zeitverschiebungen und Transitländer sind nach der Mitternachtsregel zu behandeln; detaillierte Fragen regelt ARV/ARVVwV. (§12 Abs.4; §12 Abs.3)"]

  S11B --> Q11B_1["Wann gilt ein Land bei Flugreisen als erreicht?"]
  S11B --> Q11B_2["Wie werden Zwischenlandungen behandelt?"]
  Q11B_1 --> A11B_1["Bei Flugreisen gilt ein Land als erreicht mit der Landung; bei Schiffsreisen gilt Entsprechendes. (§12 Abs.5)"]
  Q11B_2 --> A11B_2["Zwischenlandungen bleiben unberücksichtigt, es sei denn, durch sie werden Übernachtungen erforderlich. (§12 Abs.5)"]

  S11C --> Q11C_1["Ab wann wird Auslandstagegeld ab dem 15. Tag ermäßigt?"]
  S11C --> Q11C_2["Wer kann in begründeten Fällen hiervon absehen?"]
  Q11C_1 --> A11C_1["Bei Aufenthalt im Ausland ohne Hin-/Rückreisetage länger als 14 Tage wird das Auslandstagegeld ab dem 15. Tag um 25% ermäßigt. (§12 Abs.6)"]
  Q11C_2 --> A11C_2["Die oberste Dienstbehörde oder ermächtigte nachgeordnete Behörde kann in begründeten Fällen von der Ermäßigung absehen; Anträge dort zu stellen. (§12 Abs.6)"]

  %% ---------------------------
  %% 12 Verwaltung, Fristen, Belege, Anrechnung, Verzicht (§3 Abs.4–7)
  S12 --> S12A["12.1 Antrags- / Ausschlussfristen"]
  S12 --> S12B["12.2 Vorlage- & Aufbewahrungspflichten für Belege"]
  S12 --> S12C["12.3 Anrechnung / Koordination mit Dritten"]
  S12 --> S12D["12.4 Verzicht auf Vergütung"]

  S12A --> Q12A_1["Bis wann muss Reisekostenvergütung beantragt werden (Ausschlussfrist)?"]
  S12A --> Q12A_2["Wann beginnt die sechsmonatige Frist?"]

  Q12A_1 --> A12A_1["Spätestens innerhalb von sechs Monaten nach Beendigung der Dienstreise schriftlich oder elektronisch zu beantragen. (§3 Abs.4)"]
  Q12A_2 --> A12A_2["Die Frist beginnt mit dem Tag nach Beendigung der Dienstreise; in Fällen des §10 Abs.2 mit Ablauf des Tages, an dem die Dienstreise geendet hätte. (§3 Abs.4)"]

  S12B --> Q12B_1["Bis wann können Stellen Belege verlangen und Folgen bei Nichtvorlage?"]
  S12B --> Q12B_2["Wie lange sind Belege nach Erstattung aufzubewahren?"]

  Q12B_1 --> A12B_1["Die zuständigen Stellen können bis sechs Monate nach Antragstellung Belege verlangen; werden sie nicht innerhalb eines Monats vorgelegt, kann der Antrag insoweit abgelehnt werden. (§3 Abs.4)"]
  Q12B_2 --> A12B_2["Belege sind nach Erstattung bis zum Ablauf eines Jahres zur Rechnungsprüfung aufzubewahren und auf Verlangen vorzulegen. (§3 Abs.4)"]

  S12C --> Q12C_1["Werden Leistungen Dritter auf Reisekosten angerechnet?"]
  S12C --> Q12C_2["Wie ist Anspruch bei Nebentätigkeit mit anderen Stellen geregelt?"]

  Q12C_1 --> A12C_1["Ja; Leistungen, die Dienstreisende ihres Amtes wegen von Dritten erhalten, sind auf die Reisekostenvergütung anzurechnen. (§3 Abs.5)"]
  Q12C_2 --> A12C_2["Bei Dienstreisen für eine vom Dienstherrn veranlasste Nebentätigkeit besteht Anspruch nur, soweit nicht eine andere Stelle Auslagenerstattung zu leisten hat. (§3 Abs.6)"]

  S12D --> Q12D_1["Kann auf Reisekostenvergütung verzichtet werden?"]
  S12D --> Q12D_2["Welche Rechtsfolgen hat ein Widerruf des Verzichts?"]

  Q12D_1 --> A12D_1["Ja; ganz oder teilweise kann verzichtet werden; der Verzicht ist schriftlich oder elektronisch zu erklären. (§3 Abs.7)"]
  Q12D_2 --> A12D_2["Widerruf und Rechtsfolgen bestimmen sich nach allgemeinem Verwaltungsrecht und dienststelleninternen Regelungen; das Gesetz regelt die Form des Verzichts. (§3 Abs.7)"]

  %% ---------------------------
  %% 13 Querverbindungen & Sonderauslegungen
  S13 --> S13A["13.1 Kombination Dienstreise + Privat/Urlaub"]
  S13 --> S13B["13.2 Erstattung Vorbereitungsaufwand bei Entfall — cross-ref §10"]

  S13A --> Q13A_1["Wie wird Vergütung bemessen bei Verbindung mit Privat-/Urlaubsreise?"]
  S13A --> Q13A_2["Wird Rückreise bei dienstlich angeordneter vorzeitiger Rückkehr vergütet?"]

  Q13A_1 --> A13A_1["Die Vergütung wird so bemessen, als ob nur die Dienstreise durchgeführt worden wäre; darf tatsächliche Vergütung nicht übersteigen. (§11 Abs.3)"]
  Q13A_2 --> A13A_2["Ja; die Rückreise vom Urlaubs-/Aufenthaltsort zur Dienststätte gilt bei dienstlicher Anordnung als Dienstreise und wird vergütet. (§11 Abs.5)"]

  S13B --> Q13B_1["Werden Vorbereitungsaufwendungen bei Entfall erstattet (Verbindung zu §10.2)?"]
  Q13B_1 --> A13B_1["Ja; notwendige Vorbereitungsaufwendungen werden erstattet, wenn die Dienstreise aus Gründen entfällt, die Dienstreisende nicht zu vertreten haben. (§10 Abs.2)"]

  S13B --> Q13B_2["Welche Nachweise sind erforderlich und wie ist Umfang?"]
  Q13B_2 --> A13B_2["Nachweise und Umfang richten sich nach §10 Abs.2 und den Vorgaben der zuständigen Stelle; erstattet werden nur notwendige, nachgewiesene Aufwendungen. (§10 Abs.2)"]

  %% ---------------------------
  %% NOTES: Cross-reference edges (linking instead of duplication)
  A1_3 -.-> A11A_1
  A6A_3 -.-> A11C_1
  A7A_2 -.-> A14_note["Verwaltungsrechtsverweis: vgl. §14 Abs.1 (Ermächtigung Finanzministerium)"]
  A14_note --> A7A_3

  style R fill:#f9f,stroke:#333,stroke-width:2px
  style S1 fill:#eef,stroke:#333
  style S2 fill:#eef,stroke:#333
  style S3 fill:#eef,stroke:#333
  style S4 fill:#eef,stroke:#333
  style S5 fill:#eef,stroke:#333
  style S6 fill:#eef,stroke:#333
  style S7 fill:#eef,stroke:#333
  style S8 fill:#eef,stroke:#333
  style S9 fill:#eef,stroke:#333
  style S10 fill:#eef,stroke:#333
  style S11 fill:#eef,stroke:#333
  style S12 fill:#eef,stroke:#333
  style S13 fill:#eef,stroke:#333
```