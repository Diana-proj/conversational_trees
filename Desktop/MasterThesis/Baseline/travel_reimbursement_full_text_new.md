```mermaid
graph TD
%%{ init: { "theme": "default", "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "linear" } } }%%
 %% Bot start (greeting)
  B0["B: Begrüßung & Frage: Hallo! Wie kann ich helfen? Was möchten Sie?"]:::bot
  U1["U: Nennen Sie kurz Ihr Anliegen / Auswahl"]:::user
  B0 --> U1
  U1 --> B1["B: Bereich wählen (Transport / Tagegeld / Übernachtung / Ausland / Fristen / Sonstiges)"]:::bot

  %% Main choice branches (user selects area)
  B1 --> U2a["U: Transport wählen (kurz)"]:::user
  B1 --> U2b["U: Tagegeld-Typ wählen (kurz)"]:::user
  B1 --> U2c["U: Übernachtung wählen (kurz)"]:::user
  B1 --> U2d["U: Längerer Aufenthalt / Abordnung (kurz)"]:::user
  B1 --> U2e["U: Fristen & Belege (kurz)"]:::user
  B1 --> U2f["U: Ich möchte, dass Sie meine Erstattung berechnen (Schnellwahl)"]:::user
  B1 --> U2g["U: Sonstiges / Keine passende Option"]:::user

  %% Transport branch: bot prompts short transport options -> user chooses
  U2a --> B2a["B: Transportart wählen (kurz: PKW / Fahrrad / ÖPNV / Flug / Taxi/Carsharing / Gemischt)"]:::bot
  B2a --> U3a1["U: PKW (Privat)"]:::user
  B2a --> U3a2["U: Fahrrad / E‑Bike / Pedelec"]:::user
  B2a --> U3a3["U: ÖPNV oder Flug"]:::user
  B2a --> U3a4["U: Taxi / Mietwagen / Carsharing"]:::user
  B2a --> U3a5["U: Gemischte Transportarten (z. B. Auto + Zug)"]:::user

  U3a1 --> B3a1_c["B FINAL – PKW (Kurz): Kernaussage: 0,30 €/km. Next steps: Kilometrierung + Fahrtenliste. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot
  U3a2 --> B3a2_c["B FINAL – Fahrrad / E‑Bike (Kurz): Kernaussage: 0,25 €/km. Next steps: Kilometrierung + ggf. Reparaturnachweise. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot
  U3a3 --> B3a3_c["B FINAL – ÖPNV / Flug (Kurz): Erstattung bis Kosten niedrigster Klasse; Flug nur bei dienstl./wirtschaftl. Grund. Next steps: Fahr-/Flugtickets sammeln. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot
  U3a4 --> B3a4_c["B FINAL – Taxi / Mietwagen / Carsharing (Kurz): Nur bei triftigem Grund; Erstattung höchstens ÖPNV-Kosten. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot
  U3a5 --> B3a5_c["B FINAL – Gemischte Verkehrsmittel (Kurz): Kombinierte Fahrt dokumentieren (Strecke, Kosten je Segment). Next steps: Einzeln auflisten + Belege. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot

  %% Tagegeld branch
  U2b --> B2b["B: Tagegeld-Typ wählen (kurz: voller Tag / Teil-/Anreisetag / Dienstgang)"]:::bot
  B2b --> U3b1["U: Tagegeld volle Tage"]:::user
  B2b --> U3b2["U: Tagegeld An-/Abreisetag (Teil)"]:::user
  B2b --> U3b3["U: Dienstgang (Mehraufwand)"]:::user

  U3b1 --> B3b1_c["B FINAL – Tagegeld volle Tage (Kurz): Pauschale für volle Kalendertage (z. B. 24 €). Next steps: Reisedauer prüfen, Verpflegungsabzüge prüfen. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot
  U3b2 --> B3b2_c["B FINAL – Tagegeld An-/Abreisetag (Kurz): Staffelung nach Dauer (z. B. >8h/ >14h). Next steps: Ab-/Anreisezeiten notieren. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot
  U3b3 --> B3b3_c["B FINAL – Dienstgang (Kurz): Kein reguläres Tagegeld; Erstattung nachgewiesener Mehraufwendungen möglich. Aktionen: Berechnen | Checkliste | Rechtsinfo"]:::bot

  %% Übernachtung branch
  U2c --> B2c["B: Übernachtung wählen (kurz: Inland / Ausland)"]:::bot
  B2c --> U3c1["U: Übernachtung Inland"]:::user
  B2c --> U3c2["U: Übernachtung Ausland"]:::user

  U3c1 --> B3c1_c["B FINAL – Übernachtung Inland (Kurz): Pauschale / notwendige höhere Kosten erstattungsfähig. Next steps: Rechnungen sammeln, Amtsunterkünfte prüfen. Aktionen: Checkliste | Rechtsinfo"]:::bot
  U3c2 --> B3c2_c["B FINAL – Übernachtung Ausland (Kurz): Auslandssätze / Zuordnungsregelung beachten (Mitternachtsregel). Next steps: Land & Datum dokumentieren, Rechnungen sammeln. Aktionen: Checkliste | Rechtsinfo"]:::bot

  %% Längerer Aufenthalt / Trennungsgeld
  U2d --> B2d["B: Längerer Aufenthalt / Abordnung (kurz)"]:::bot
  B2d --> U3d1["U: Längerer Aufenthalt (Abordnung)"]:::user
  B2d --> U3d2["U: Trennungsgeld (Abordnung/Trennung)"]:::user

  U3d1 --> B3d1_c["B FINAL – Längerer Aufenthalt (Kurz): Ab Tag 8 gelten abordnungsähnliche Regeln; detaillierte Fristen beachten. Aktionen: Checkliste | Rechtsinfo"]:::bot
  U3d2 --> B3d2_c["B FINAL – Trennungsgeld (Kurz): Sonderregelung für Abordnung/Trennung; Anspruchsvoraussetzungen prüfen. Aktionen: Checkliste | Rechtsinfo"]:::bot

  %% Fristen & Belege
  U2e --> B2e["B: Fristen & Belege (kurz)"]:::bot
  B2e --> U3e1["U: Antragsfrist prüfen"]:::user
  B2e --> U3e2["U: Belege & Aufbewahrung"]:::user

  U3e1 --> B3e1_c["B FINAL – Antragsfrist (Kurz): Antrag i.d.R. innerhalb 6 Monate nach Dienstreise; Belege ggf. nachfordern. Aktionen: Checkliste | Rechtsinfo"]:::bot
  U3e2 --> B3e2_c["B FINAL – Belege & Aufbewahrung (Kurz): Belege 1 Jahr aufbewahren; bei fehlenden Belegen Frist-/Nachweisregeln beachten. Aktionen: Checkliste | Rechtsinfo"]:::bot

  %% From concise final nodes -> common user actions (quick replies)
  B3a1_c --> U_request_calc["U: Berechnung anfordern (Eingabemaske)"]:::user
  B3a1_c --> U_request_checklist["U: Checkliste / Formular anfordern"]:::user
  B3a1_c --> U_request_rechtsinfo["U: Mehr Details / Ausführliche Rechtsinfo"]:::user

  B3a2_c --> U_request_calc
  B3a2_c --> U_request_checklist
  B3a2_c --> U_request_rechtsinfo

  B3a3_c --> U_request_calc
  B3a3_c --> U_request_checklist
  B3a3_c --> U_request_rechtsinfo

  B3a4_c --> U_request_calc
  B3a4_c --> U_request_checklist
  B3a4_c --> U_request_rechtsinfo

  B3a5_c --> U_request_calc
  B3a5_c --> U_request_checklist
  B3a5_c --> U_request_rechtsinfo

  B3b1_c --> U_request_calc
  B3b1_c --> U_request_checklist
  B3b1_c --> U_request_rechtsinfo

  B3b2_c --> U_request_calc
  B3b2_c --> U_request_checklist
  B3b2_c --> U_request_rechtsinfo

  B3b3_c --> U_request_calc
  B3b3_c --> U_request_checklist
  B3b3_c --> U_request_rechtsinfo

  B3c1_c --> U_request_checklist
  B3c1_c --> U_request_rechtsinfo

  B3c2_c --> U_request_checklist
  B3c2_c --> U_request_rechtsinfo

  B3d1_c --> U_request_checklist
  B3d1_c --> U_request_rechtsinfo

  B3d2_c --> U_request_checklist
  B3d2_c --> U_request_rechtsinfo

  B3e1_c --> U_request_checklist
  B3e1_c --> U_request_rechtsinfo

  B3e2_c --> U_request_checklist
  B3e2_c --> U_request_rechtsinfo

  %% User action nodes -> central bot responses (shared)
  U_request_calc --> B_calc_res["B FINAL – Berechnungsergebnis: Ausgabeformat für Berechnung (z. B. km × Satz = Betrag); ggf. Übergabeformular zum Herunterladen."]:::bot
  U_request_checklist --> B_formular["B FINAL – Formular & Checkliste: Downloadlinks + kompakte Checkliste (Kilometerliste, Tickets, Hotelrechnungen, Verpflegungshinweise)."]:::bot
  U_request_rechtsinfo --> B_rechtsinfo["B: Rechtsinfo (zentrale Sammlung: §§, ausführliche Texte & Ausnahmen; 'Möchten Sie Details?')"]:::bot

  %% Direct main-menu quick paths
  U2f --> B_calc_res
  U2g --> B_fallback["B FINAL – Sonstiges / Fallback: Bitte kurz beschreiben (Beispiele angeboten: gemischte Verkehrsmittel, Widerspruch, Behinderung). Wir bieten passende Pfade an."]:::bot

  %% Ensure user action nodes have labels and outputs
  U_request_calc:::user
  U_request_checklist:::user
  U_request_rechtsinfo:::user

  %% Styling: bot nodes vs user nodes
  classDef bot fill:#E8F0FF,stroke:#1E4DB7,stroke-width:1px;
  classDef user fill:#FFF7E6,stroke:#B25A00,stroke-width:1px;

