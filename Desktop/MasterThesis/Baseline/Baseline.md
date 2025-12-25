```mermaid
%%{ init: { "theme": "default", "flowchart": { "useMaxWidth": false, "htmlLabels": true, "curve": "linear" } } }%%
%%{init: { "flowchart": { "htmlLabels": true },
           "themeVariables": { "fontSize": "12px" } }}%%
graph TD

classDef bot fill:#cfe8ff,stroke:#036,stroke-width:1px;
classDef user fill:#e8ffd8,stroke:#063,stroke-width:1px;

%% ROOT
B_root_greeting["Was möchten Sie zur Reisekostenabrechnung wissen? Zu welchem Thema haben Sie Fragen?"]:::bot

U_choice_fahrt["Fahrt/Flugkostenerstattung (§4)"]:::user
U_choice_weg["Wegstreckenentschädigung (§5)"]:::user
U_choice_tage["Tagegeld / Verpflegung (§6)"]:::user
U_choice_ueber["Übernachtungsgeld (§7)"]:::user
U_choice_abroad["Auslandsdienstreisen (§12)"]:::user
U_choice_frists["Fristen, Belege, Antrag (§3)"]:::user
U_choice_trennung["Trennungsgeld / Abordnung (§13)"]:::user
U_fallback_offer_help["Hilfe / Glossar anzeigen?"]:::user

B_root_greeting --> U_choice_fahrt
B_root_greeting --> U_choice_weg
B_root_greeting --> U_choice_tage
B_root_greeting --> U_choice_ueber
B_root_greeting --> U_choice_abroad
B_root_greeting --> U_choice_frists
B_root_greeting --> U_choice_trennung
B_root_greeting --> U_fallback_offer_help

%% FIRST PRECISION QUESTIONS
B_ask_transport_mode["Welches Verkehrsmittel haben Sie verwendet? (ÖPNV/Flug/Mietwagen/Taxi/Carsharing)"]:::bot
B_ask_commute_mode["Welches Fortbewegungsmittel nutzen Sie zum Dienstort?"]:::bot
B_ask_duration["Ganztag oder Teilzeit? (Stunden/Tage)"]:::bot
B_ask_inland_or_abroad["Inland oder Ausland? Erstattung gegen Beleg?"]:::bot
B_ask_deadline_topic["Geht es um Frist, Belegvorlage oder Aufbewahrung?"]:::bot
B_ask_separation_topic["Trennungsgeld bei Abordnung oder Ausbildung?"]:::bot

U_choice_fahrt --> B_ask_transport_mode
U_choice_weg --> B_ask_commute_mode
U_choice_tage --> B_ask_duration
U_choice_ueber --> B_ask_inland_or_abroad
U_choice_abroad --> B_ask_inland_or_abroad
U_choice_frists --> B_ask_deadline_topic
U_choice_trennung --> B_ask_separation_topic

%% USER REPLIES
U_mode_public_flight["ÖPNV / Flug"]:::user
U_mode_car_taxi["Mietwagen / Taxi / Carsharing"]:::user
U_mode_other["Anderes / Kombination"]:::user

B_ask_transport_mode --> U_mode_public_flight
B_ask_transport_mode --> U_mode_car_taxi
B_ask_transport_mode --> U_mode_other

U_pkw_private_km["Privat-PKW (km-Angabe)"]:::user
U_special_duty_interest["Dienstliches Interesse / Fahrrad / schwierige Wege"]:::user

B_ask_commute_mode --> U_pkw_private_km
B_ask_commute_mode --> U_special_duty_interest

U_full_days["Volle Kalendertage"]:::user
U_partial_days["Teilweise Tage (An-/Abreise)"]:::user

B_ask_duration --> U_full_days
B_ask_duration --> U_partial_days

U_accommodation_inland["Inland – Pauschale / Beleg?"]:::user
U_accommodation_abroad["Ausland – Ziel/Tage / Beleg?"]:::user

B_ask_inland_or_abroad --> U_accommodation_inland
B_ask_inland_or_abroad --> U_accommodation_abroad

U_deadline_within6months["Antrag innerhalb 6 Monate"]:::user
U_receipts_and_retention["Belege / Aufbewahrung"]:::user

B_ask_deadline_topic --> U_deadline_within6months
B_ask_deadline_topic --> U_receipts_and_retention

U_abordnung_no_move["Abordnung ohne Umzugskostenzusage"]:::user
U_training_assignment["Abordnung im Rahmen der Ausbildung"]:::user

B_ask_separation_topic --> U_abordnung_no_move
B_ask_separation_topic --> U_training_assignment

%% TRIFTIGER GRUND, SLOTS, CONFIRMATION
B_triftiger_decision["Liegt ein triftiger Grund für Mietwagen/Taxi/Carsharing vor?"]:::bot
U_triftiger_yes["Ja, triftiger Grund"]:::user
U_triftiger_no["Nein"]:::user
B_restrict_to_public_transport["Ohne triftigen Grund nur Erstattung bis ÖPNV-Kosten (§4 Abs.3)"]:::bot

B_collect_trip_slots["Bitte angeben: Datum, Ziel, Dauer, Kosten, Belege vorhanden?"]:::bot
U_slot_provide["Angaben übermittelt"]:::user
U_slot_no_receipts["Keine Belege vorhanden"]:::user

B_help_receipts["So reichen Sie Kosten gegen Beleg ein: Foto + Betrag + Empfänger."]:::bot

B_confirm_action["Erstattung berechnen oder Zusammenfassung erstellen?"]:::bot
U_confirm_yes["Ja"]:::user
U_confirm_no["Nein / Abbrechen"]:::user

B_calc_and_summary["Erstattung berechnet / Antrag vorbereitet"]:::bot
B_exit["Beenden oder anderes Thema?"]:::bot

U_mode_public_flight --> B_collect_trip_slots
U_mode_other --> B_collect_trip_slots
U_mode_car_taxi --> B_triftiger_decision

B_triftiger_decision --> U_triftiger_yes
B_triftiger_decision --> U_triftiger_no

U_triftiger_yes --> B_collect_trip_slots
U_triftiger_no --> B_restrict_to_public_transport

B_collect_trip_slots --> U_slot_provide
B_collect_trip_slots --> U_slot_no_receipts

U_slot_provide --> B_confirm_action
U_slot_no_receipts --> B_help_receipts

B_confirm_action --> U_confirm_yes
B_confirm_action --> U_confirm_no

U_confirm_yes --> B_calc_and_summary
U_confirm_no --> B_exit

%% ATOMIC LEGAL INFO
B_flight_policy_basic["Flüge: niedrigste Klasse (§4 Abs.1)"]:::bot
B_flight_reimbursement_condition["Flugkosten nur bei dienstlichem/wirtschaftlichem Bedarf (§4 Abs.1)"]:::bot
B_flight_climate_note["Dienststelle kann klimafreundliche Alternative verlangen"]:::bot

U_choice_fahrt --> B_flight_policy_basic
U_choice_fahrt --> B_flight_reimbursement_condition
U_choice_fahrt --> B_flight_climate_note

B_mileage_triftiger_condition["Mietwagen/Taxi/Carsharing nur bei triftigem Grund (§4 Abs.3)"]:::bot
B_carsharing_policy["Carsharing: Mitgliedsgebühr nicht gekürzt (§4 Abs.3)"]:::bot
B_mileage_special_interest["0,35 €/km bei erhebl. dienstl. Interesse (§5 Abs.2)"]:::bot
B_mileage_difficult_road_surcharge["+0,05 €/km bei schwierigen Wegen (§5 Abs.3)"]:::bot
B_bicycle_rate["0,25 €/km für Fahrrad/E-Bike (§5 Abs.3)"]:::bot

U_pkw_private_km --> B_mileage_triftiger_condition
U_special_duty_interest --> B_mileage_special_interest
U_special_duty_interest --> B_mileage_difficult_road_surcharge
U_special_duty_interest --> B_bicycle_rate

B_daily_full["Tagegeld: 24 € (§6 Abs.1)"]:::bot
B_daily_partial_thresholds[">8h = 6 €; >14h = 12 € (§6 Abs.1)"]:::bot
B_daily_meal_deductions["Kürzungen: Frühstück 20%, Mittag/Abend je 40%"]:::bot

U_full_days --> B_daily_full
U_partial_days --> B_daily_partial_thresholds
U_choice_tage --> B_daily_meal_deductions

B_accommodation_inland["Inland: 20 € oder tatsächliche Kosten (§7 Abs.1)"]:::bot
B_accommodation_abroad_basic["Ausland: 30 € (§7 Abs.1)"]:::bot
B_accommodation_abroad_higher_costs["Höhere Kosten bei Nachweis"]:::bot
B_accommodation_abroad_exclusions["Kein Geld bei eigener Wohnung/Amtsunterkunft (§7 Abs.2)"]:::bot

U_accommodation_inland --> B_accommodation_inland
U_accommodation_abroad --> B_accommodation_abroad_basic
U_accommodation_abroad --> B_accommodation_abroad_higher_costs
U_accommodation_abroad --> B_accommodation_abroad_exclusions

B_abroad_definition["Definition Auslandsdienstreise (§12)"]:::bot
B_abroad_last_country_rule["Land vor Mitternacht maßgeblich (§12 Abs.4)"]:::bot
B_abroad_long_stay_reduction["Ab 15. Tag 25 % weniger (§12 Abs.5–6)"]:::bot

U_choice_abroad --> B_abroad_definition
U_choice_abroad --> B_abroad_last_country_rule
U_choice_abroad --> B_abroad_long_stay_reduction

B_receipt_deadline["Anspruch erlischt nach 6 Monaten (§3 Abs.4)"]:::bot
B_receipts_request["Dienststelle kann Belege nachfordern"]:::bot
B_receipts_noncompliance_effects["Nichtvorlage: Ablehnung möglich"]:::bot
B_record_retention_requirements["Belege 1 Jahr aufbewahren"]:::bot

U_deadline_within6months --> B_receipt_deadline
U_receipts_and_retention --> B_receipts_request
U_receipts_and_retention --> B_receipts_noncompliance_effects
U_receipts_and_retention --> B_record_retention_requirements

B_trennung_general["Trennungsgeld ohne Umzugskostenzusage (§13 Abs.1)"]:::bot
B_trennung_training["Trennungsgeld bei Ausbildung (§13 Abs.2)"]:::bot

U_abordnung_no_move --> B_trennung_general
U_training_assignment --> B_trennung_training

%% HELP / FALLBACK
B_help_glossary["Glossar anzeigen"]:::bot
B_fallback["Bitte wiederholen — nicht verstanden"]:::bot
U_help_glossary_ack["Danke / Ende"]:::user

U_fallback_offer_help --> B_help_glossary
B_help_glossary --> U_help_glossary_ack
U_help_glossary_ack --> B_exit
B_fallback --> U_fallback_offer_help