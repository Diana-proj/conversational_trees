from openai import OpenAI

OPENAI_API_KEY ="x"
client = OpenAI(api_key=OPENAI_API_KEY)

models = client.models.list()
for m in models.data:
    print(m.id)


# Access the document
with open("/Users/diana/Desktop/MasterThesis/PHA_SMART.txt", "r", encoding="utf-8") as f:
    document = f.read()
# Access the document
with open("/Users/diana/Desktop/BW_Gesetz.txt", "r", encoding="utf-8") as f:
    document = f.read()

with open("/Users/diana/Desktop/MasterThesis/Improved.md", "r", encoding="utf-8") as f:
    flow = f.read()



def merge_flow_multi (flow, multiturndialog):
    prompt = f"""
Mermaid Flow Integration Prompt (Final Polished Version)
You are given:
the existing Mermaid flow {flow}
one multi-turn dialog {multiturndialog}
🎯 GOAL
Integrate {multiturndialog} into {flow}.
Expand only the dialog’s main statutory topic into Question and Answer nodes.
Handle any side topic as an Xref only (no new Question/Answer tree).
Always anchor edits under the relevant Question or Answer in the existing flow, not at section roots.
Reuse existing node IDs when they match intent or paragraph; otherwise propose short, consistent new IDs.
🧩 EDIT OPTIONS (choose the smallest fitting type)
REPLACE —
If the dialog reveals a statutory condition:
Convert the existing Answer into a Question with conditional Answer(s).
Only create multiple Answers when the statute defines distinct outcomes (e.g., “über 7 Tage / unter 7 Tage”).
If the law yields one outcome, use a single factual Answer — no split.
BRANCH —
Add a follow-up Question under an Answer when the dialog clarifies the same topic.
XREF —
If the dialog mentions a side topic (another section or paragraph), insert only a cross-reference node (no new logic).
Do not duplicate existing siblings. Refer to them with Xref.
Do not create new top-level S* sections.
⚖️ STRUCTURAL RULES
Node types
Question — conditional or factual check (binary or A/B).
Label it with the condition, not “Kann …?” or “Darf …?”.
Answer — one sentence, statute-based, includes the citation (e.g., “§2 Abs.1”).
Xref — short pointer to another section (e.g., “→ S12”).
Deterministic vs. Conditional logic
Deterministic rule → Single Answer.
If the statute fixes the answer (“ist / gilt / bedarf”), output only one Answer node.
Do not create “Ja/Nein” branches.
Example:
A2_1["Dienstreisen bedürfen einer schriftlichen oder elektronischen Genehmigung. (§2 Abs.1)"]
Default + Exception pattern → One condition gate.
If the law states a default rule and an exception:
Model the default as an Answer (A) node.
Add one Question (Q) under it for the exception condition.
Create Ja/Nein edges only for the exception outcomes.
Example:
A2_1["Dienstreisen bedürfen grundsätzlich einer Genehmigung. (§2 Abs.1)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen Amt/Wesen nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Genehmigung erforderlich. (§2 Abs.1)"]
Scope / Applicability questions → Conditional allowed.
Use binary (Ja/Nein) only if the statute depends on a factual state (e.g., “liegt Auslandsgeschäftsort vor?”).
Never ask vague permission questions.
Avoid “Kann …? (Ja/Nein)” or “Darf …? (Ja/Nein)”.
Phrase as a statutory condition or a factual check.
Label and style rules
German only.
Present tense.
No “(Ja/Nein)” inside labels — only on edges.
Keep every Answer concise and normative.
Cite section numbers briefly (“§3 Abs.2”).
One sentence per Answer node.
🧱 TEXT INTEGRATION RULES
Attach new content under the closest related Question or Answer of the same statutory paragraph.
Prefer updating an existing Answer → Question (REPLACE) to inserting a sibling.
Only create a new node when no existing anchor fits.
When summarizing multiple items of the same legal kind (e.g., costs), keep them in one Answer sentence, not multiple nodes.
🧾 OUTPUT FORMAT
Return only the relevant Mermaid section in full (e.g., %% 3.2) where the update applies.
Do not repeat the rest of the flow.
Output exactly one fenced code block:
%% section header
...nodes and edges...
No prose, no commentary.
💡 EXAMPLES
1) Deterministic → single Answer
%% 2.1 Genehmigung
A2_1["Dienstreisen bedürfen einer schriftlichen oder elektronischen Genehmigung. (§2 Abs.1)"]
2) Default + exception
%% 2.1 Genehmigung mit Ausnahme
A2_1["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Genehmigung. (§2 Abs.1)"]
A2_1 --> Q2_1_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen Amt/Wesen nicht in Betracht)?"]
Q2_1_exc -->|"Ja"| A2_1_exc_yes["Keine Genehmigung erforderlich. (§2 Abs.1 S.2)"]
Q2_1_exc -->|"Nein"| A2_1_exc_no["Genehmigung erforderlich. (§2 Abs.1)"]
3) Scope condition (legitimate binary)
%% 1.1 Ausland
A1_1["Auslandsdienstreisen: §§1–11 LRKG gelten entsprechend. (§12 Abs.2–3)"]
A1_1 --> Q1_1a["Liegt mindestens ein auswärtiger Geschäftsort im Ausland?"]
Q1_1a -->|"Ja"| A1_1a_yes["Auslandsdienstreise: §§1–11 LRKG gelten entsprechend. (§12 Abs.2–3)"]
Q1_1a -->|"Nein"| A1_1a_no["Keine Auslandsdienstreise → Inlandsvorschriften (§§6,7)."]
4) Example fix for §3 Abs.2 (your earlier case)
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start/Ziel angeordnet?"]
Q3_2a -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Start/Zielpunkt. (§3 Abs.2)"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
🔒 Summary Ruleset (for the model)
Only branch when the statute creates a real conditional outcome.
Never branch “Ja/Nein” for fixed legal statements.
Strip “(Ja/Nein)” from labels.
Keep edges labeled “Ja” and “Nein” only when both outcomes exist.
Prefer factual conditions (“liegt vor?”, “wurde angeordnet?”) to permission questions (“darf?”, “kann?”).
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
        "id": 0,
        "title": "Gilt LRKG auch für Auslandsdienstreisen?",
        "turns": [
            {"role": "USER", "text": "Hallo, gilt das LRKG auch bei Auslandsdienstreisen — zum Beispiel wenn ich für eine Konferenz nach Frankreich fahre? Und wie ist dann die Regelung für Tagegeld und Übernachtungskosten?"},
            {"role": "SYSTEM", "text": "Enthält Ihre Reise mindestens einen Geschäftsort im Ausland (z. B. die Konferenz in Frankreich)?"},
            {"role": "USER", "text": "Ja, die Reise enthält eine Konferenz in Frankreich. Gilt das LRKG dann auch für Auslandsdienstreisen und wie sind Tagegeld sowie Übernachtungskosten in dem Fall zu berechnen?"},
            {"role": "SYSTEM", "text": "Ja — das LRKG gilt auch für Auslandsdienstreisen (§12 Abs.2); Tagegeld und Übernachtungsgeld werden dabei abweichend von §§6 und 7 nach der jeweils gültigen Fassung des §3 der Auslandsreisekostenverordnung (ARV) und der ARVVwV gewährt, wobei das Land nach §12 Abs.4–5 dasjenige ist, das vor Mitternacht Ortszeit zuletzt erreicht wird."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 1,
        "title": "Wer ist vom Gesetz erfasst (Anwendungsbereich)?",
        "turns": [
            {"role": "USER", "text": "Ich fahre nächste Woche zu einer Konferenz nach München und habe danach einen Kundentermin. Gilt das neue Landesreisekostengesetz für mich als befristet Beschäftigte im öffentlichen Dienst und auch für Dienstreisen mit der Bahn?"},
            {"role": "SYSTEM", "text": "Sind Sie verbeamtet oder sind Sie als befristet Beschäftigte/r (Angestellte/r) beim Land, einer Gemeinde, einem Landkreis oder einer sonstigen unter staatlicher Aufsicht stehenden Körperschaft tätig?"},
            {"role": "USER", "text": "Ich bin befristet angestellt beim Land. Gilt das neue Landesreisekostengesetz für mich und für Dienstreisen mit der Bahn?"},
            {"role": "SYSTEM", "text": "Das LRKG gilt nach §1 Absatz 1 ausdrücklich für Beamtinnen und Beamte sowie Richter; befristet Beschäftigte/Angestellte werden im Text nicht genannt — das LRKG gilt daher nicht für Sie als befristet Angestellte/r."},
            {"role": "USER", "text": "Ich fahre nächste Woche nach München zur Konferenz und habe danach einen Kundentermin — gelten für meine Bahntickets und das Tagegeld dann andere Regelungen? An wen wende ich mich dafür, an HR oder an die Reisekostenstelle?"},
            {"role": "SYSTEM", "text": "Nach §1 LRKG gilt das Gesetz nur für Beamtinnen/Beamte und Richter; als befristet Angestellte/r beim Land fällt Ihr Fall nicht unter das LRKG — die Regelungen zu Fahrt- und Flugkostenerstattung (§4) und Tagegeld (§6) gelten deshalb nicht für Sie."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 2,
        "title": "Nach welchen Vorschriften werden Auslandstage-/Übernachtungsgelder geregelt?",
        "turns": [
            {"role": "USER", "text": "Ich fahre nächste Woche zu einer Konferenz in Frankreich.  Nach welchen Vorschriften werden Auslandstage- und Übernachtungsgelder geregelt?"},
            {"role": "SYSTEM", "text": "Für Ihre Dienstreise nach Frankreich gilt § 12 Abs. 3 LRKG: Auslandstage- und Auslandsübernachtungsgelder werden nach der jeweils gültigen Fassung des § 3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 3,
        "title": "Braucht eine Dienstreise Anordnung/Genehmigung?",
        "turns": [
            {"role": "USER", "text": "Ich plane eine eintägige Dienstreise per Zug nach München für einen Kundentermin und müsste dafür Zugtickets buchen. Braucht so eine Dienstreise eine formelle Anordnung/Genehmigung, und darf ich die Tickets schon vorab kaufen oder brauche ich die Freigabe zuerst?"},
            {"role": "SYSTEM", "text": "Sind Sie Richter/in oder eine der in §2 genannten ausgenommenen Personen, oder haben Sie bereits eine schriftliche oder elektronische Anordnung/Genehmigung für die Dienstreise?"},
            {"role": "USER", "text": "Ich bin keine Richterin/kein Richter und gehöre nicht zu den in §2 genannten Ausnahmen, und ich habe noch keine schriftliche oder elektronische Anordnung.  Brauche ich trotzdem eine formelle Dienstreiseanordnung oder reicht die mündliche Zustimmung meines Vorgesetzten, und kann ich die Zugtickets jetzt schon kaufen und später zur Erstattung einreichen?"},
            {"role": "SYSTEM", "text": "Nach §2 Abs.1 LRKG bedarf eine Dienstreise grundsätzlich einer schriftlichen oder elektronischen Anordnung/Genehmigung (mündliche Zustimmung genügt nicht, es sei denn, eine Anordnung käme wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht); und nach §3 Abs.1 besteht ein Anspruch auf Erstattung nur für dienstlich veranlasste notwendige Auslagen — Tickets vorab ohne die erforderliche schriftliche/elektronische Anordnung zu kaufen ist daher rechtlich riskant, da ohne diese Anordnung der Erstattungsanspruch entffallen kann."},
            {"role": "USER", "text": "Ich fahre einmal per Zug nach München zu einem Kundentermin und müsste die Tickets bald buchen. Reicht eine einfache E-Mail meines Vorgesetzten als schriftliche/e-Anordnung, damit ich die Tickets vorher kaufen kann, oder muss das über ein bestimmtes Reiseportal/Formular laufen?"},
            {"role": "SYSTEM", "text": "Nach §2 Abs.1 LRKG genügt eine schriftliche oder elektronische Anordnung — eine einfache E-Mail Ihres zuständigen Dienstvorgesetzten ist damit ausreichend; das Gesetz schreibt kein bestimmtes Reiseportal oder Formular vor."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 4,
        "title": "In welcher Form muss die Anordnung erfolgen?",
        "turns": [
            {"role": "USER", "text": "Ich plane eine Dienstreise nach München Ende Oktober zu einer Konferenz und müsste Bahn- und Hotelbuchungen vornehmen. Reicht dafür eine E-Mail vom Vorgesetzten als Anordnung oder braucht es ein unterschriebenes Formular/ausgedruckte Anordnung?"},
            {"role": "SYSTEM", "text": "Kommt die E-Mail vom zuständigen Dienstvorgesetzten und enthält sie ausdrücklich eine Anordnung oder Genehmigung der Dienstreise?"},
            {"role": "USER", "text": "Ja, die E-Mail kommt vom Bereichsleiter und enthält explizit „Dienstreise angeordnet“ sowie Datum und Zweck (Konferenz), ich muss Bahn und Hotel buchen.  Reicht das für Buchung und Abrechnung, oder braucht HR trotzdem eine unterschriebene/ausgedruckte Anordnung?"},
            {"role": "SYSTEM", "text": "Nach § 2 Abs. 1 LRKG genügt eine schriftliche oder elektronische Anordnung — eine E-Mail des zuständigen Bereichsleiters mit der Formulierung „Dienstreise angeordnet“ plus Datum und Zweck ist damit für Buchung und Abrechnung ausreichend; eine eigenhändige Unterschrift oder gedruckte Anordnung ist gesetzlich nicht vorgeschrieben."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 5,
        "title": "Gibt es Ausnahmen von der Genehmigungspflicht?",
        "turns": [
            {"role": "USER", "text": "Ich plane eine eintägige Dienstreise per Zug zu einem Kundentermin in derselben Region (inkl. Bahnticket). Gibt es dafür Ausnahmen von der Genehmigungspflicht?"},
            {"role": "SYSTEM", "text": "Sind Sie Richter/in oder Landesbeauftragte/r für den Datenschutz bzw. Beauftragte/r der Landesregierung für die Belange von Menschen mit Behinderungen?"},
            {"role": "USER", "text": "Nein, das bin ich nicht. Muss ich für die eintägige Zugfahrt zum Kundentermin vorher eine Genehmigung einholen, oder reicht eine nachträgliche Abrechnung/Meldung?"},
            {"role": "SYSTEM", "text": "Wurde die Dienstreise vorab schriftlich oder elektronisch von Ihrer zuständigen Dienstvorgesetzten angeordnet oder genehmigt?"},
            {"role": "USER", "text": "Nein, das wurde nicht schriftlich oder elektronisch genehmigt. Reicht eine nachträgliche Abrechnung/Meldung, oder muss ich jetzt noch eine Genehmigung einholen?"},
            {"role": "SYSTEM", "text": "Liegt ein Fall vor, in dem nach Ihrem Amt oder dem Wesen des Dienstgeschäfts eine schriftliche oder elektronische Anordnung bzw. Genehmigung nicht in Betracht kommt?"},
            {"role": "USER", "text": "Nein, das trifft nicht zu. Muss ich dann noch vorab eine Genehmigung einholen, oder kann ich die eintägige Zugfahrt (inkl. Bahnticket) einfach nachträglich abrechnen/melden?"},
            {"role": "SYSTEM", "text": "Wurde die Reise insgesamt – also auch mündlich oder anderweitig bestätigt – von Ihrer zuständigen Dienstvorgesetzten angeordnet oder genehmigt?"},
            {"role": "USER", "text": "Nein, es gab keine mündliche Bestätigung.  Gibt es in solchen Fällen eine Ausnahme für eintägige Zugfahrten in derselben Region, sodass ich das Bahnticket nachträglich abrechnen kann, oder muss ich jetzt noch eine Genehmigung einholen?"},
            {"role": "SYSTEM", "text": "Nach § 2 LRKG müssen Dienstreisen schriftlich oder elektronisch angeordnet oder genehmigt sein; da bei Ihrer eintägigen Zugfahrt keine solche Anordnung/Genehmigung vorlag und keine der in § 2 genannten Ausnahmen zutrifft, wird die Fahrt nicht als Dienstreise im Sinne des Gesetzes angesehen und nach § 3 besteht damit grundsätzlich kein Anspruch auf Reisekostenvergütung."},
            {"role": "USER", "text": "Verstehe — kann meine Vorgesetzte die Fahrt jetzt noch nachträglich genehmigen, damit ich das Bahnticket abrechnen kann?  Falls das nicht möglich ist, gibt es eine Regelung, wie ich die Kosten privat erstattet bekomme?"},
            {"role": "SYSTEM", "text": "Da bei Ihrer eintägigen Zugfahrt keine schriftliche oder elektronische Anordnung vorlag und keine der Ausnahmen des § 2 einschlägig ist, besteht nach § 3 LRKG grundsätzlich kein Anspruch auf Erstattung; das Gesetz enthält keine ausdrückliche Regelung zur nachträglichen Genehmigung oder zur privaten Erstattung."},
            {"role": "USER", "text": "Gibt es in unserer Behörde eine interne Kulanzregelung, dass Vorgesetzte Reisen nachträglich genehmigen oder Bahntickets erstatten können? An wen wende ich mich dafür konkret — HR, Reisekostenstelle oder meine Vorgesetzte?"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },

        {
        "id": 6,
        "title": "Woran unterscheidet man Dienstreise und Dienstgang?",
        "turns": [
            {"role": "USER", "text": "Ich habe nächste Woche eine zweitägige Konferenz in einer anderen Stadt und übernachte dort. Woran unterscheidet sich das von einem kurzen Dienstgang (z. B. Tagesbesuch beim Kunden ohne Übernachtung) und welche Folgen hat das für Fahrtkosten und Tagegeld?"},
            {"role": "SYSTEM", "text": "Treten Sie die Reise von Ihrer Wohnung aus an und kehren Sie dorthin zurück, oder beginnt/endet die Reise an Ihrer Dienststätte?"},
            {"role": "USER", "text": "Ich trete die Reise von meiner Wohnung aus an und kehre dorthin zurück.  Bekomme ich dann Tagegeld für Übernachtung/Verpflegung und wie reiche ich Bahntickets sowie Hotelrechnung korrekt ein?"},
            {"role": "SYSTEM", "text": "Um wie spät brechen Sie von Ihrer Wohnung zur Konferenz auf und wann kehren Sie an welchem Tag zurück?"},
            {"role": "USER", "text": "Ich fahre am Montag um 7:30 Uhr von zu Hause los und komme am Dienstag gegen 19:00 Uhr wieder zurück.  Ist das in meinem Fall eine Dienstreise oder ein Dienstgang?"},
            {"role": "SYSTEM", "text": "Das ist eine Dienstreise (§2 Abs.1 LRKG), weil es sich um eine mehrtägige Reise außerhalb des Dienstortes mit Übernachtung handelt; Voraussetzung ist, dass sie angeordnet oder genehmigt ist."},
            {"role": "USER", "text": "Muss die Dienstreise schriftlich (z. B. per E-Mail) von der Dienststelle genehmigt werden, damit ich Tagegeld und Fahrtkosten abrechnen kann?  Und wie reiche ich Bahntickets und die Hotelrechnung korrekt bei der Reisekostenstelle ein?"},
            {"role": "SYSTEM", "text": "Wurde die Dienstreise schriftlich oder elektronisch von Ihrer zuständigen Dienstvorgesetzten angeordnet oder genehmigt?"},
            {"role": "USER", "text": "Nein, es liegt noch keine schriftliche Genehmigung vor.  Reicht eine E-Mail als Genehmigung oder braucht es eine formelle Reiseanordnung?  Kann ich Bahn- und Hotelbelege per Scan an die Reisekostenstelle schicken?"},
            {"role": "SYSTEM", "text": "Eine E-Mail genügt: Die Anordnung oder Genehmigung muss schriftlich oder elektronisch erfolgen (§2 Abs.1 LRKG)."},
            {"role": "USER", "text": "Für meine Konferenzreise: Kann ich Bahn- und Hotelbelege als Scan per E-Mail an die Reisekostenstelle schicken, oder benötigen Sie die Originalbelege?  Muss die Genehmigung vor der Buchung vorliegen, damit die Kosten erstattet werden, oder reicht die nachträgliche schriftliche Anordnung?"},
            {"role": "SYSTEM", "text": "Wollen Sie die Bahn- und Hotelbelege bereits jetzt zusammen mit dem Abrechnungsantrag elektronisch (als Scan) einreichen, oder möchten Sie nur den Antrag stellen und die Originalbelege auf Anforderung der zuständigen Stelle vorlegen?"},
            {"role": "USER", "text": "Ich schicke die Bahn- und Hotelbelege jetzt gern als Scan zusammen mit dem Abrechnungsantrag.  Müssen die Originalbelege trotzdem aufbewahrt und auf Verlangen vorgelegt werden, und an welche E-Mail-Adresse soll ich die Scans schicken?"},
            {"role": "SYSTEM", "text": "Nach § 3 Abs. 4 LRKG müssen Sie die Originalbelege nach Erstattung bis zum Ablauf eines Jahres aufbewahren und auf Verlangen vorlegen; das Gesetz nennt keine E-Mail-Adresse für die Übermittlung von Scans."},
            {"role": "USER", "text": "An welche E-Mail-Adresse soll ich die eingescannten Bahn- und Hotelbelege schicken?  Soll ich dabei die Genehmigungs-E-Mail der Dienststelle mitschicken oder nur die Belege?"},
            {"role": "SYSTEM", "text": "Das LRKG nennt keine E-Mail-Adresse für die Einsendung von Scans; eine solche Adresse wird nicht geregelt. Ebenfalls schreibt das Gesetz nicht vor, die Genehmigungs-E-Mail der Abrechnung beizufügen; die Anordnung/Genehmigung muss jedoch schriftlich oder elektronisch vorliegen (§2 Abs.1). Die zuständige Stelle kann bis sechs Monate nach Antragstellung die Vorlage der Belege verlangen; werden diese auf Anforderung nicht innerhalb eines Monats vorgelegt, kann der Vergütungsantrag insoweit abgelehnt werden, und nach Erstattung sind die Belege bis zum Ablauf eines Jahres aufzubewahren (§3 Abs.4)."}
        ]
    },
    {
        "id": 7,
        "title": "Wer bestimmt Ausgangs-/Endpunkt grundsätzlich?",
        "turns": [
            {"role": "USER", "text": "Ich fahre nächste Woche dienstlich zu einer Konferenz und will die Zugtickets buchen. Wer bestimmt grundsätzlich den Ausgangs-/Endpunkt — mein Wohnort oder die Dienststelle, und muss ich das vorher klären?"},
            {"role": "SYSTEM", "text": "Wirst du die Dienstreise von deiner Wohnung antreten/beenden oder von der Dienststelle — bzw. hat deine oder dein zuständige Vorgesetzte bereits eine Anordnung darüber getroffen?"},
            {"role": "USER", "text": "Ich fahre von meiner Wohnung los und komme auch dorthin zurück; eine Anordnung meiner Vorgesetzten gibt es noch nicht. Muss ich das vorher mit der Dienststelle klären, damit der Wohnort als Ausgangspunkt anerkannt wird, bevor ich das Zugticket buche?"},
            {"role": "SYSTEM", "text": "Nach § 3 Abs. 2 LRKG kannst du grundsätzlich selbst deine Wohnung als Ausgangs- und Endpunkt bestimmen; eine vorherige Klärung ist nicht erforderlich, es sei denn, die zuständige Vorgesetzte ordnet abweichend die Dienststätte als Ausgangs- oder Endpunkt an (z. B. wenn die Fahrtstrecke unmittelbar an der Dienststätte vorbeiführt)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 8,
        "title": "Kann die Dienststelle verbindlich die Dienststätte als Start/Ziel anordnen?",
        "turns": [
            {"role": "USER", "text": "Ich fahre nächste Woche mit der Bahn zu einer Konferenz in Hannover und würde lieber von zu Hause aus starten statt erst ins Büro zu fahren.  Kann die Dienststelle verbindlich vorschreiben, dass Start/Ziel die Dienststätte sein müssen, und werden Fahrtkosten bzw. Anreisezeit in dem Fall trotzdem erstattet?"},
            {"role": "SYSTEM", "text": "Führt die von Ihnen geplante Zugverbindung unmittelbar an Ihrer Dienststätte vorbei?"},
            {"role": "USER", "text": "Nein — der Zug fährt nicht an der Dienststelle vorbei; ich müsste erst von zu Hause zum Bahnhof (ca. 15 Minuten).  Kann die Dienststelle trotzdem vorschreiben, dass Start/Ziel die Dienststätte sein muss, oder werden in diesem Fall Fahrtkosten und Anreisezeit ab meinem Wohnort erstattet?"},
            {"role": "SYSTEM", "text": "Da die Zugstrecke nicht unmittelbar an Ihrer Dienststätte vorbeiführt, darf die Dienststelle nach §3 Abs.2 nicht verbindlich die Dienststätte als Start-/Zielpunkt anordnen; starten Sie von Ihrer Wohnung, bemisst sich die Fahrtkosten- bzw. Wegstreckenvergütung nach der Entfernung von/zu Ihrer Wohnung und die Reisedauer für Tagegeld nach Abreise/Ankunft an der Wohnung (vgl. §§3 Abs.2, 4, 5, 6 LRKG)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 9,
        "title": "Wie wird Fahrkostenerstattung bemessen, wenn Reise an der Wohnung beginnt/endet?",
        "turns": [
            {"role": "USER", "text": "Ich habe nächste Woche eine Dienstreise per Bahn, Abfahrt von meiner Wohnung. Wird die Fahrkostenerstattung ab meiner Wohnung berechnet und werden Kosten für Bus/Taxi zum Bahnhof ersetzt?"},
            {"role": "SYSTEM", "text": "Wenn Sie die Dienstreise an Ihrer Wohnung antreten, bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung (§3 Abs.2); Fahrkosten für regelmäßig verkehrende Beförderungsmittel (z. B. Bus zum Bahnhof) werden bis zur Höhe der niedrigsten Beförderungsklasse erstattet (§4 Abs.1), Taxikosten nur bei triftigem Grund (§4 Abs.3)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 10,
        "title": "Bin ich frei in Wahl des Beförderungsmittels?",
        "turns": [
            {"role": "USER", "text": "Ich habe nächste Woche eine Inlands-Dienstreise zu einer ganztägigen Konferenz in Köln (Abfahrt aus Frankfurt).  Kann ich frei zwischen Bahn, Auto oder Flug wählen, oder muss ich die günstigste Option nehmen bzw. vorher genehmigen lassen?"},
            {"role": "SYSTEM", "text": "Hat Ihre zuständige Dienstvorgesetzte oder Ihr Dienstvorgesetzter bereits eine bestimmte Beförderungsart angeordnet oder genehmigt?"},
            {"role": "USER", "text": "Nein, bisher hat niemand etwas angeordnet oder genehmigt.  Muss ich vorher um Genehmigung bitten oder kann ich frei zwischen Bahn, Auto und Flug wählen — und muss ich dabei immer die günstigste Option nehmen?"},
            {"role": "SYSTEM", "text": "Da keine Anordnung vorliegt, dürfen Sie nach §3 Abs.3 grundsätzlich das Beförderungsmittel frei wählen; dabei sind Wirtschaftlichkeits- und Klimaschutzgesichtspunkte zu beachten—Fahrtkosten werden nur bis zur niedrigsten Beförderungsklasse erstattet (§4 Abs.1) und Flugreisen nur, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen; unentgeltliche Beförderung wird nicht erstattet."},
            {"role": "USER", "text": "Ich fahre nächste Woche von Frankfurt nach Köln zur ganztägigen Konferenz.  Muss ich eine Flugbuchung vorher genehmigen lassen oder kann ich selbst buchen und nachträglich abrechnen, und werden Flugkosten dann nur bis zur günstigsten Zugverbindung erstattet?"},
            {"role": "SYSTEM", "text": "Sind Sie Richter/in oder eine der in §2 Abs.3 genannten Personen (z. B. Landesbeauftragte für Datenschutz oder für Belange von Menschen mit Behinderungen), für die keine Anordnung oder Genehmigung nötig ist?"},
            {"role": "USER", "text": "Nein, ich gehöre nicht dazu. Für meine Fahrt nächste Woche von Frankfurt nach Köln: Muss eine Flugreise vorher genehmigt werden oder kann ich selbst buchen und hinterher abrechnen?"},
            {"role": "SYSTEM", "text": "Gibt es dienstliche oder wirtschaftliche Gründe, die die Flugnutzung gegenüber der Bahn rechtfertigen (z. B. erhebliche Zeitersparnis oder zwingende Termine)?"},
            {"role": "USER", "text": "Nein, es gibt keinen besonderen Zeitdruck — es ist eine ganztägige Konferenz in Köln.  Muss ich dann zwingend den günstigsten Zugtarif (Sparpreis) buchen, und bräuchte ich vorab eine Genehmigung, falls ich trotzdem fliegen möchte?"},
            {"role": "SYSTEM", "text": "Da kein besonderer Zeitdruck und keine Anordnung vorliegt: Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse (bei der Bahn üblicherweise 2. Klasse); Flugkosten sind nur erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen."},
            {"role": "USER", "text": "Brauche ich eine vorherige Genehmigung durch meine Vorgesetzte bzw. meinen Vorgesetzten, damit ein Flug später erstattet wird?  Oder kann ich selbst buchen und nachträglich abrechnen, auch ohne besonderen dienstlichen Anlass?"},
            {"role": "SYSTEM", "text": "Nach dem LRKG ist keine ausdrückliche vorherige Genehmigung für eine Flugbuchung vorgeschrieben; Sie können grundsätzlich das Beförderungsmittel wählen, aber Flugkosten werden nur erstattet, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen — sonst wird nur die Kostenhöhe der niedrigsten Beförderungsklasse (z. B. Zug 2. Klasse) erstattet (§§3 Abs.3, 4 Abs.1)."},
            {"role": "USER", "text": "Ich fahre nächste Woche zur ganztägigen Konferenz Frankfurt–Köln.  Wenn ich trotzdem einen Flug buche und der teurer ist als die Zugfahrt, muss ich die Differenz dann privat zahlen oder wird das im Einzelfall geprüft und erstattet?"},
            {"role": "SYSTEM", "text": "Da keine dienstlichen oder wirtschaftlichen Gründe vorliegen, werden Flugkosten nach §4 Abs.1 nur bis zur Höhe der Kosten der niedrigsten Beförderungsklasse erstattet — Sie müssten die Differenz privat zahlen."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },

        {
        "id": 11,
        "title": "Kann die Dienststelle ein Verkehrsmittel vorschreiben?",
        "turns": [
            {"role": "USER", "text": "Ich muss zur Konferenz nach München (Dienstreise, innerdeutsch). Kann mir die Dienststelle vorschreiben, welches Verkehrsmittel ich nehme — zum Beispiel verpflichtend das Auto statt der Bahn?"},
            {"role": "SYSTEM", "text": "Gemäß § 3 Abs. 3 LRKG sind Dienstreisende grundsätzlich frei in der Wahl des Beförderungsmittels; die Dienststelle kann ihnen also nicht generell vorschreiben, mit dem Auto statt der Bahn zu fahren, wobei bei der Wahl wirtschaftliche Gesichtspunkte und insbesondere die Erfordernisse des Klimaschutzes zu beachten sind und Fahrtkosten nicht erstattet werden, wenn eine unentgeltliche Beförderungsmöglichkeit genutzt werden kann."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 12,
        "title": "Welche Klasse wird erstattet?",
        "turns": [
            {"role": "USER", "text": "Ich fahre nächste Woche zu einer Konferenz nach München und buche mit der Bahn. Welche Klasse wird erstattet — 1. oder 2. Klasse, und gilt das für Flüge (Economy vs. Premium Economy) genauso?"},
            {"role": "SYSTEM", "text": "Haben Sie einen Grad der Behinderung von mindestens 50 oder einen gesundheitlichen Grund, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"},
            {"role": "USER", "text": "Nein, ich habe keinen GdB ≥50 und es gibt keinen gesundheitlichen Grund.  Bedeutet das, dass bei Zugfahrten grundsätzlich nur die 2. Klasse erstattet wird und bei Flügen nur Economy?"},
            {"role": "SYSTEM", "text": "Ja. Nach § 4 Absatz 1 werden Fahrtkosten nur bis zur Höhe der niedrigsten Beförderungsklasse erstattet — bei Zugreisen also grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy). Flugkosten sind zudem nur erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Flugnutzung gegenüber den Belangen des Klimaschutzes überwiegen; die Dienstbehörde kann in Ausnahmefällen abweichen."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 13,
        "title": "Sind Flugkosten erstattungsfähig?",
        "turns": [
            {"role": "USER", "text": "Ich plane eine Inlands-Dienstreise nach München für eine Konferenz. Werden Flugkosten dafür erstattet und gibt es Einschränkungen (z. B. nur bei signifikanter Zeitersparnis oder nur Economy-Tarife)?"},
            {"role": "SYSTEM", "text": "Liegt für Ihre Reise ein dienstlicher oder wirtschaftlicher Grund vor, der die Flugbenutzung rechtfertigt (z. B. erhebliche Zeitersparnis gegenüber der Bahn)?"},
            {"role": "USER", "text": "Ja — ich habe einen engen Zeitplan und durch den Flug spare ich mehrere Stunden gegenüber der Bahn. Muss ich die Flugbuchung vorab genehmigen lassen und sind nur Economy-Tarife erstattungsfähig?"},
            {"role": "SYSTEM", "text": "Da die Flugbenutzung wegen erheblicher Zeitersparnis dienstlich/wirtschaftlich begründet ist, sind Flugkosten erstattungsfähig, vorausgesetzt die Dienstreise wurde schriftlich oder elektronisch angeordnet bzw. genehmigt; erstattet werden grundsätzlich die Kosten der niedrigsten Flugklasse (Economy), Ausnahmen nur bei besonderen dienstlichen Gründen oder bei medizinischer Notwendigkeit."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 14,
        "title": "Wie hoch ist Entschädigung Privat-KFZ?",
        "turns": [
            {"role": "USER", "text": "Ich fahre mit meinem privaten Auto zur Dienstreise (Konferenz in München, Hin- und Rückfahrt). Wie hoch ist die Entschädigung pro Kilometer nach dem Landesreisekostengesetz und werden Park- oder Mautgebühren zusätzlich erstattet?"},
            {"role": "SYSTEM", "text": "Liegt an der Benutzung Ihres privaten Kraftfahrzeugs ein erhebliches dienstliches Interesse (z. B. weil ein anderes Verkehrsmittel nicht zumutbar oder die dienstliche Erledigung dies erfordert)?"},
            {"role": "USER", "text": "Ja — ich muss technische Geräte und Poster mitnehmen und bin zeitlich sehr gebunden, daher ist der Zug nicht zumutbar.  Welche km-Pauschale gilt in diesem Fall und werden Park- bzw. Mautkosten zusätzlich erstattet?"},
            {"role": "SYSTEM", "text": "Da aufgrund des erheblichen dienstlichen Interesses die höhere Pauschale gilt, beträgt die Wegstreckenentschädigung 0,35 Euro/km (§5 Abs.2 LRKG); notwendige Park- und Mautgebühren sind als Nebenkosten erstattungsfähig (§10 Abs.1 LRKG)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 15,
        "title": "Wie hoch ist Tagegeld für vollen Kalendertag?",
        "turns": [
            {"role": "USER", "text": "Ich fahre zu einer zweitägigen Konferenz in ein anderes Bundesland und reise mit der Bahn – wie hoch ist das Tagegeld für einen vollen Kalendertag? Gilt der Satz bundesweit gleich oder hängt er vom Bundesland ab?"},
            {"role": "SYSTEM", "text": "Wurde die Konferenzreise von Ihrer zuständigen Dienstvorgesetzten schriftlich oder elektronisch als Dienstreise angeordnet oder genehmigt?"},
            {"role": "USER", "text": "Ja, die Reise wurde schriftlich von meiner Dienstvorgesetzten genehmigt.  Steht mir dann für jeden vollen Kalendertag das volle Tagegeld zu und wo finde ich den aktuellen Pauschalsatz?"},
            {"role": "SYSTEM", "text": "Ja — bei schriftlich genehmigter Dienstreise steht Ihnen für jeden vollen Kalendertag das volle Tagegeld in Höhe von 24 Euro zu (§6 Abs. 1 LRKG)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 16,
        "title": "Wie viel Tagegeld am An-/Abreisetag bei >8 Std / >14 Std?",
        "turns": [
            {"role": "USER", "text": "Ich reise dienstlich innerhalb Deutschlands zu einer Konferenz und fahre mit dem Zug. Wie viel Tagegeld bekomme ich am An- bzw. Abreisetag, wenn meine Reisedauer über 8 Std. bzw. über 14 Std. liegt?"},
            {"role": "SYSTEM", "text": "Bei einer innerdeutschen Dienstreise erhalten Sie an An- und Abreisetagen: bei mehr als 8 Stunden Reisedauer 6 Euro, bei mehr als 14 Stunden 12 Euro (§ 6 Abs. 1 LRKG)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 17,
        "title": "Wie wird Tagegeld bei unentgeltlicher Verpflegung gekürzt?",
        "turns": [
            {"role": "USER", "text": "Ich fahre nächste Woche zu einer zweitägigen Konferenz in ein anderes Bundesland, Anreise mit der Bahn, das Mittagessen wird vom Veranstalter kostenlos gestellt. Wie wird dann mein Tagegeld gekürzt — gibt es feste Pauschalen/Prozentwerte für unentgeltliche Mahlzeiten oder zieht ihr feste Eurobeträge ab, und muss ich dafür Belege einreichen?"},
            {"role": "SYSTEM", "text": "Handelt es sich bei den beiden Konferenztagen um volle Kalendertage (Anspruch auf das volle Tagegeld von 24 €), oder sind An- bzw. Abreisetag kürzere Dienstreisetage (mit 6 € bzw. 12 € Tagegeld)?"},
            {"role": "USER", "text": "Ja — beide Konferenztage sind volle Kalendertage.  Wenn mir am Mittag eine Mahlzeit kostenlos gestellt wird, wie genau wird dann mein Tagegeld gekürzt?"},
            {"role": "SYSTEM", "text": "Bei unentgeltlichem Mittagessen wird nach § 6 Abs. 4 40 % des vollen Tagegeldes (24 €) einbehalten — also 9,60 € pro vollem Kalendertag; das gilt auch bei von dritter Seite bereitgestellter Verpflegung oder wenn unentgeltliche Verpflegung ohne triftigen Grund nicht in Anspruch genommen wird."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 18,
        "title": "Wie hoch ist pauschales Übernachtungsgeld Inland?",
        "turns": [
            {"role": "USER", "text": "Ich fahre nächste Woche zu einer zweitägigen Konferenz innerhalb Deutschlands.  Wie hoch ist das pauschale Übernachtungsgeld Inland und muss ich trotzdem Hotelrechnungen einreichen?"},
            {"role": "SYSTEM", "text": "Für Ihre zweitägige Inlands-Konferenz beträgt das pauschale Übernachtungsgeld 20 Euro pro notwendiger Übernachtung (§ 7 Abs. 1 LRKG)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    },
    {
        "id": 19,
        "title": "Bis wann muss Reisekostenvergütung beantragt werden (Ausschlussfrist)?",
        "turns": [
            {"role": "USER", "text": "Ich war letzte Woche dienstlich in München (Konferenz) und habe Zugtickets sowie Hotelrechnungen. Bis wann muss ich die Reisekostenvergütung beantragen, damit sie nicht verfällt — gibt es da eine Ausschlussfrist?"},
            {"role": "SYSTEM", "text": "Für Ihre Dienstreise nach München müssen Sie die Reisekostenvergütung schriftlich oder elektronisch spätestens innerhalb von sechs Monaten nach dem Tag nach Beendigung der Dienstreise beantragen (§ 3 Abs. 4 LRKG)."},
            {"role": "USER", "text": "Danke, Tschüss"},
            {"role": "SYSTEM", "text": "Goodbye."}
        ]
    }
]

from pathlib import Path

IMPROVED_PATH = Path("/Users/diana/Desktop/MasterThesis/Improved_Flow.md")

 


extension = """
% 1.1 Geltungsbereich (split concise questions)
S1A --> Q1_1["Gilt LRKG auch für Auslandsdienstreisen?"]
S1A --> Q1_2["Wer ist vom Gesetz erfasst (Anwendungsbereich)?"]
S1A --> Q1_3["Nach welchen Vorschriften werden Auslandstage-/Übernachtungsgelder geregelt?"]
S1A --> Q1_4["Wer erlässt Verwaltungsvorschriften / Besonderheiten?"]

Q1_1 --> A1_1["Liegt mindestens ein auswärtiger Geschäftsort im Ausland?"]
A1_1 -->|"Ja"| A1_1_yes["Auslandsdienstreise: §§1–11 LRKG gelten entsprechend; Auslandstage- und Auslandsübernachtungsgelder richten sich nach der jeweils gültigen Fassung der ARV und der ARVVwV; maßgebliches Land nach der Mitternachtsregel. (§12 Abs.2–5)"]
A1_1 -->|"Nein"| A1_1_no["Keine Auslandsdienstreise: Es gelten die Inlandsregelungen (Tagegeld/Übernachtung nach §§6,7 LRKG). (§6, §7)"]

Q1_2 --> A1_2["Erfasst sind Beamtinnen/Beamte des Landes, Gemeinden, Gemeindeverbände, Landkreise, sonstige der Aufsicht des Landes unterstehende KÖR/Anstalten/Stiftungen, Richter sowie ab- oder zu diesen abgeordnete Personen, vgl. §1 Abs.1."]
Q1_3 --> A1_3["Auslandstage- und Auslandsübernachtungsgelder richten sich nach der jeweils gültigen Fassung des §3 ARV und der ARVVwV, vgl. §12 Abs.3."]
Q1_4 --> A1_4["Das Finanzministerium erlässt die allgemeinen Verwaltungsvorschriften; oberste Dienstbehörden können bereichsspezifische Regelungen treffen, vgl. §14 Abs.2 und §4 Abs.1 Satz2."]
Processed dialog 1/20
```mermaid
%% 1.1 Geltungsbereich (split concise questions)
Q1_2["Wer ist vom Gesetz erfasst (Anwendungsbereich)?"]
Q1_2 --> Q1_2a["Fällt die Dienstperson unter die in §1 Abs.1 genannten Gruppen (Beamtinnen/Beamte, Richter, Gemeinden, Gemeindeverbände, Landkreise, sonstige der Aufsicht des Landes unterstehende KÖR/Anstalten/Stiftungen)?"]
Q1_2a -->|"Ja"| A1_2_yes["Das LRKG gilt für Beamtinnen und Beamte des Landes, Gemeinden, Gemeindeverbände, Landkreise, sonstige der Aufsicht des Landes unterstehende Körperschaften, Anstalten und Stiftungen, Richter sowie ab- oder zu diesen abgeordnete Personen. (§1 Abs.1)"]
Q1_2a -->|"Nein"| A1_2_no["Das LRKG gilt nicht für befristet Beschäftigte/Angestellte, da diese im Wortlaut nicht genannt sind. (§1 Abs.1)"]
A1_2_no --> X1_2_xref["→ S4, S6"]
```
Processed dialog 2/20
```mermaid
%% 12 Auslandstage-/Übernachtungsgelder
Q12_3["Welche Vorschriften gelten für Auslandstage- und Auslandsübernachtungsgelder?"]
Q12_3 --> A12_3["Auslandstage- und Auslandsübernachtungsgelder werden nach der jeweils gültigen Fassung des §3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt. (§12 Abs.3 LRKG)"]
```
Processed dialog 3/20
```mermaid
%% 12 Auslandstage-/Übernachtungsgelder
Q12_3["Welche Vorschriften gelten für Auslandstage- und Auslandsübernachtungsgelder?"]
Q12_3 --> A12_3["Auslandstage- und Auslandsübernachtungsgelder werden nach der jeweils gültigen Fassung des §3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt. (§12 Abs.3 LRKG)"]
A12_3 --> A12_3a["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung/Genehmigung; eine einfache E‑Mail des zuständigen Vorgesetzten gilt als elektronische Anordnung, das Gesetz schreibt kein bestimmtes Reiseportal oder Formular vor. (§2 Abs.1 LRKG)"]
A12_3a --> Q12_3a_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q12_3a_exc -->|"Ja"| A12_3a_exc_yes["Keine Anordnung erforderlich. (§2 Abs.1 S.2 LRKG)"]
Q12_3a_exc -->|"Nein"| A12_3a_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1 LRKG)"]
A12_3a --> X12_3_ref3["→ §3 Abs.1 LRKG (Erstattung nur für dienstlich veranlasste notwendige Auslagen)"]
```
Processed dialog 4/20
```mermaid
%% 12 Auslandstage-/Übernachtungsgelder
Q12_3["Welche Vorschriften gelten für Auslandstage- und Auslandsübernachtungsgelder?"]
Q12_3 --> A12_3["Auslandstage- und Auslandsübernachtungsgelder werden nach der jeweils gültigen Fassung des §3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt. (§12 Abs.3 LRKG)"]
A12_3 --> A12_3a["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung/Genehmigung; eine einfache E‑Mail des zuständigen Vorgesetzten gilt als elektronische Anordnung, das Gesetz schreibt kein bestimmtes Reiseportal oder Formular vor. (§2 Abs.1 LRKG)"]
A12_3a --> Q12_3a_form["Kommt die E‑Mail vom zuständigen Dienstvorgesetzten und enthält sie ausdrücklich eine Anordnung/Genehmigung der Dienstreise?"]
Q12_3a_form -->|"Ja"| A12_3a_yes["Die E‑Mail vom zuständigen Vorgesetzten mit ausdrücklicher Formulierung ‚Dienstreise angeordnet‘ genügt für Buchung und Abrechnung. (§2 Abs.1 LRKG)"]
Q12_3a_form -->|"Nein"| A12_3a_no["Fehlt eine ausdrückliche Anordnung oder stammt die Nachricht nicht vom zuständigen Vorgesetzten, ist eine schriftliche oder elektronische Anordnung des Zuständigen erforderlich. (§2 Abs.1 LRKG)"]
A12_3a --> Q12_3a_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q12_3a_exc -->|"Ja"| A12_3a_exc_yes["Keine Anordnung erforderlich. (§2 Abs.1 S.2 LRKG)"]
Q12_3a_exc -->|"Nein"| A12_3a_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1 LRKG)"]
A12_3a --> X12_3_ref3["→ §3 Abs.1 LRKG (Erstattung nur für dienstlich veranlasste notwendige Auslagen)"]
```
Processed dialog 5/20
```mermaid
%% 12 Auslandstage-/Übernachtungsgelder
Q12_3["Welche Vorschriften gelten für Auslandstage- und Auslandsübernachtungsgelder?"]
Q12_3 --> A12_3["Auslandstage- und Auslandsübernachtungsgelder werden nach der jeweils gültigen Fassung des §3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt. (§12 Abs.3 LRKG)"]
A12_3 --> A12_3a["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung/Genehmigung; eine einfache E‑Mail des zuständigen Vorgesetzten gilt als elektronische Anordnung, das Gesetz schreibt kein bestimmtes Reiseportal oder Formular vor. (§2 Abs.1 LRKG)"]
A12_3a --> Q12_3a_form["Kommt die E‑Mail vom zuständigen Dienstvorgesetzten und enthält sie ausdrücklich eine Anordnung/Genehmigung der Dienstreise?"]
Q12_3a_form -->|"Ja"| A12_3a_yes["Die E‑Mail vom zuständigen Vorgesetzten mit ausdrücklicher Formulierung ‚Dienstreise angeordnet‘ genügt für Buchung und Abrechnung. (§2 Abs.1 LRKG)"]
Q12_3a_form -->|"Nein"| A12_3a_no["Fehlt eine ausdrückliche Anordnung oder stammt die Nachricht nicht vom zuständigen Vorgesetzten, ist eine schriftliche oder elektronische Anordnung des Zuständigen erforderlich. (§2 Abs.1 LRKG)"]
A12_3a --> Q12_3a_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q12_3a_exc -->|"Ja"| A12_3a_exc_yes["Keine Anordnung erforderlich. (§2 Abs.1 S.2 LRKG)"]
Q12_3a_exc -->|"Nein"| A12_3a_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1 LRKG)"]
A12_3a --> X12_3_ref3["→ §3 Abs.1 LRKG (Erstattung nur für dienstlich veranlasste notwendige Auslagen)"]
A12_3a --> A12_3a_post["Fehlt eine schriftliche oder elektronische Anordnung und greift keine Ausnahme, besteht nach §3 Abs.1 LRKG grundsätzlich kein Anspruch auf Erstattung; das LRKG enthält keine ausdrückliche Regelung zur nachträglichen Genehmigung. (§2 Abs.1, §3 Abs.1 LRKG)"]
A12_3a_post --> X12_3_kulanz["→ interne Kulanzregelung der Dienststelle (HR/Reisekostenstelle/Vorgesetzte) prüfen"]
```
Processed dialog 6/20
```mermaid
%% 12 Auslandstage-/Übernachtungsgelder
Q12_3["Welche Vorschriften gelten für Auslandstage- und Auslandsübernachtungsgelder?"]
Q12_3 --> A12_3["Auslandstage- und Auslandsübernachtungsgelder werden nach der jeweils gültigen Fassung des §3 der Auslandsreisekostenverordnung des Bundes (ARV) und der Allgemeinen Verwaltungsvorschrift (ARVVwV) gewährt. (§12 Abs.3 LRKG)"]
A12_3 --> A12_3a["Grundsatz: Dienstreisen bedürfen einer schriftlichen oder elektronischen Anordnung/Genehmigung; eine einfache E‑Mail des zuständigen Vorgesetzten gilt als elektronische Anordnung, das Gesetz schreibt kein bestimmtes Reiseportal oder Formular vor. (§2 Abs.1 LRKG)"]
A12_3a --> Q12_3a_form["Kommt die E‑Mail vom zuständigen Dienstvorgesetzten und enthält sie ausdrücklich eine Anordnung/Genehmigung der Dienstreise?"]
Q12_3a_form -->|"Ja"| A12_3a_yes["Die E‑Mail vom zuständigen Vorgesetzten mit ausdrücklicher Formulierung ‚Dienstreise angeordnet‘ genügt für Buchung und Abrechnung. (§2 Abs.1 LRKG)"]
Q12_3a_form -->|"Nein"| A12_3a_no["Fehlt eine ausdrückliche Anordnung oder stammt die Nachricht nicht vom zuständigen Vorgesetzten, ist eine schriftliche oder elektronische Anordnung des Zuständigen erforderlich. (§2 Abs.1 LRKG)"]
A12_3a --> Q12_3a_exc["Greift die Ausnahme nach §2 Abs.1 S.2 (Anordnung kommt wegen des Amtes oder des Wesens des Dienstgeschäfts nicht in Betracht)?"]
Q12_3a_exc -->|"Ja"| A12_3a_exc_yes["Keine Anordnung erforderlich. (§2 Abs.1 S.2 LRKG)"]
Q12_3a_exc -->|"Nein"| A12_3a_exc_no["Anordnung/Genehmigung erforderlich. (§2 Abs.1 LRKG)"]
A12_3a --> X12_3_ref3["→ §3 Abs.1 LRKG (Erstattung nur für dienstlich veranlasste notwendige Auslagen)"]
A12_3a --> A12_3a_post["Fehlt eine schriftliche oder elektronische Anordnung und greift keine Ausnahme, besteht nach §3 Abs.1 LRKG grundsätzlich kein Anspruch auf Erstattung; das LRKG enthält keine ausdrückliche Regelung zur nachträglichen Genehmigung. (§2 Abs.1, §3 Abs.1 LRKG)"]
A12_3a_yes --> X12_3_ref4["→ §3 Abs.4 LRKG (Belegaufbewahrung, Vorlagepflicht)"]
A12_3a_post --> X12_3_kulanz["→ interne Kulanzregelung der Dienststelle (HR/Reisekostenstelle/Vorgesetzte) prüfen"]
```
Processed dialog 7/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
```
Processed dialog 8/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> X3_2_costs["→ S4–S6"]
```
Processed dialog 9/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]
```
Processed dialog 10/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
Q3_3a -->|"Nein"| A3_3a_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse; ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
```
Processed dialog 11/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
Q3_3a -->|"Nein"| A3_3a_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse; ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> X3_3_costs["→ S4–S6"]
```
Processed dialog 12/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> X3_3_costs["→ S4–S6"]
```
Processed dialog 13/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
A3_3a_yes --> X3_3a_order["→ S2"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> X3_3_costs["→ S4–S6"]
```
Processed dialog 14/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
A3_3a_yes --> X3_3a_order["→ S2"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]

A3_3 --> Q3_3c["Liegt ein erhebliches dienstliches Interesse an der Benutzung eines privaten Kraftfahrzeugs vor (z. B. Transport technischer Geräte, zeitliche Bindung)?"]
Q3_3c -->|"Ja"| A3_3c_yes["Bei Vorliegen eines erheblichen dienstlichen Interesses beträgt die Wegstreckenentschädigung 0,35 €/km. (§5 Abs.2 LRKG)"]
Q3_3c -->|"Nein"| A3_3c_no["Bei Nichtvorliegen gilt die reguläre Wegstreckenentschädigung nach §5 Abs.1 LRKG. (§5 Abs.1 LRKG)"]
A3_3c_yes --> X3_3c_parks["→ S10 (Nebenkosten: Park- und Mautgebühren, §10 Abs.1)"]

A3_3 --> X3_3_costs["→ S4–S6"]
```
Processed dialog 15/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
A3_3a_yes --> X3_3a_order["→ S2"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]

A3_3 --> Q3_3c["Liegt ein erhebliches dienstliches Interesse an der Benutzung eines privaten Kraftfahrzeugs vor (z. B. Transport technischer Geräte, zeitliche Bindung)?"]
Q3_3c -->|"Ja"| A3_3c_yes["Bei Vorliegen eines erheblichen dienstlichen Interesses beträgt die Wegstreckenentschädigung 0,35 €/km. (§5 Abs.2 LRKG)"]
Q3_3c -->|"Nein"| A3_3c_no["Bei Nichtvorliegen gilt die reguläre Wegstreckenentschädigung nach §5 Abs.1 LRKG. (§5 Abs.1 LRKG)"]
A3_3c_yes --> X3_3c_parks["→ S10 (Nebenkosten: Park- und Mautgebühren, §10 Abs.1)"]

A3_3 --> Q3_6a["Wurde die Dienstreise schriftlich oder elektronisch angeordnet oder genehmigt?"]
Q3_6a -->|"Ja"| A3_6_yes["Bei schriftlich oder elektronisch genehmigter Dienstreise steht für jeden vollen Kalendertag Tagegeld in Höhe von 24 Euro zu. (§6 Abs.1 LRKG)"]
Q3_6a -->|"Nein"| X3_6_costs["→ S4–S6"]

A3_3 --> X3_3_costs["→ S4–S6"]
```
Processed dialog 16/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
A3_3a_yes --> X3_3a_order["→ S2"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]

A3_3 --> Q3_3c["Liegt ein erhebliches dienstliches Interesse an der Benutzung eines privaten Kraftfahrzeugs vor (z. B. Transport technischer Geräte, zeitliche Bindung)?"]
Q3_3c -->|"Ja"| A3_3c_yes["Bei Vorliegen eines erheblichen dienstlichen Interesses beträgt die Wegstreckenentschädigung 0,35 €/km. (§5 Abs.2 LRKG)"]
Q3_3c -->|"Nein"| A3_3c_no["Bei Nichtvorliegen gilt die reguläre Wegstreckenentschädigung nach §5 Abs.1 LRKG. (§5 Abs.1 LRKG)"]
A3_3c_yes --> X3_3c_parks["→ S10 (Nebenkosten: Park- und Mautgebühren, §10 Abs.1)"]

A3_3 --> Q3_6a["Wurde die Dienstreise schriftlich oder elektronisch angeordnet oder genehmigt?"]
Q3_6a -->|"Ja"| Q3_6b["Handelt es sich um einen vollen Kalendertag?"]
Q3_6a -->|"Nein"| X3_6_costs["→ S4–S6"]

Q3_6b -->|"Ja"| A3_6_yes["Bei schriftlich oder elektronisch genehmigter Dienstreise steht für jeden vollen Kalendertag Tagegeld in Höhe von 24 Euro. (§6 Abs.1 LRKG)"]
Q3_6b -->|"Nein"| Q3_6c["Übersteigt die Reisedauer am An- oder Abreisetag 14 Stunden?"]
Q3_6c -->|"Ja"| A3_6_14["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 14 Stunden Reisedauer 12 Euro. (§6 Abs.1 LRKG)"]
Q3_6c -->|"Nein"| Q3_6d["Übersteigt die Reisedauer am An- oder Abreisetag 8 Stunden?"]
Q3_6d -->|"Ja"| A3_6_8["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 8 Stunden Reisedauer 6 Euro. (§6 Abs.1 LRKG)"]
Q3_6d -->|"Nein"| A3_6_none["Am An- oder Abreisetag steht kein Tagegeld zu, wenn die Reisedauer höchstens 8 Stunden beträgt. (§6 Abs.1 LRKG)"]

A3_3 --> X3_3_costs["→ S4–S6"]
```
Processed dialog 17/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
A3_3a_yes --> X3_3a_order["→ S2"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]

A3_3 --> Q3_3c["Liegt ein erhebliches dienstliches Interesse an der Benutzung eines privaten Kraftfahrzeugs vor (z. B. Transport technischer Geräte, zeitliche Bindung)?"]
Q3_3c -->|"Ja"| A3_3c_yes["Bei Vorliegen eines erheblichen dienstlichen Interesses beträgt die Wegstreckenentschädigung 0,35 €/km. (§5 Abs.2 LRKG)"]
Q3_3c -->|"Nein"| A3_3c_no["Bei Nichtvorliegen gilt die reguläre Wegstreckenentschädigung nach §5 Abs.1 LRKG. (§5 Abs.1 LRKG)"]
A3_3c_yes --> X3_3c_parks["→ S10 (Nebenkosten: Park- und Mautgebühren, §10 Abs.1)"]

A3_3 --> Q3_6a["Wurde die Dienstreise schriftlich oder elektronisch angeordnet oder genehmigt?"]
Q3_6a -->|"Ja"| Q3_6b["Handelt es sich um einen vollen Kalendertag?"]
Q3_6a -->|"Nein"| X3_6_costs["→ S4–S6"]

Q3_6b -->|"Ja"| A3_6_yes["Bei schriftlich oder elektronisch genehmigter Dienstreise steht für jeden vollen Kalendertag Tagegeld in Höhe von 24 Euro. (§6 Abs.1 LRKG)"]
A3_6_yes --> Q3_6e["Wird an dem vollen Kalendertag unentgeltliche Verpflegung (z. B. Mittagessen) bereitgestellt?"]
Q3_6e -->|"Ja"| A3_6_meal_cut["Bei unentgeltlichem Mittagessen wird 40 % des vollen Tagegeldes einbehalten — 9,60 € pro vollem Kalendertag. (§6 Abs.4)"]
Q3_6e -->|"Nein"| A3_6_meal_no["Kein Abzug vom Tagegeld wegen unentgeltlicher Verpflegung. (§6 Abs.4)"]
A3_6_meal_cut --> X3_6_receipts["→ S4–S6"]

Q3_6b -->|"Nein"| Q3_6c["Übersteigt die Reisedauer am An- oder Abreisetag 14 Stunden?"]
Q3_6c -->|"Ja"| A3_6_14["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 14 Stunden Reisedauer 12 Euro. (§6 Abs.1 LRKG)"]
Q3_6c -->|"Nein"| Q3_6d["Übersteigt die Reisedauer am An- oder Abreisetag 8 Stunden?"]
Q3_6d -->|"Ja"| A3_6_8["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 8 Stunden Reisedauer 6 Euro. (§6 Abs.1 LRKG)"]
Q3_6d -->|"Nein"| A3_6_none["Am An- oder Abreisetag steht kein Tagegeld zu, wenn die Reisedauer höchstens 8 Stunden beträgt. (§6 Abs.1 LRKG)"]

A3_3 --> X3_3_costs["→ S4–S6"]
```
Processed dialog 18/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
A3_3a_yes --> X3_3a_order["→ S2"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]

A3_3 --> Q3_3c["Liegt ein erhebliches dienstliches Interesse an der Benutzung eines privaten Kraftfahrzeugs vor (z. B. Transport technischer Geräte, zeitliche Bindung)?"]
Q3_3c -->|"Ja"| A3_3c_yes["Bei Vorliegen eines erheblichen dienstlichen Interesses beträgt die Wegstreckenentschädigung 0,35 €/km. (§5 Abs.2 LRKG)"]
Q3_3c -->|"Nein"| A3_3c_no["Bei Nichtvorliegen gilt die reguläre Wegstreckenentschädigung nach §5 Abs.1 LRKG. (§5 Abs.1 LRKG)"]
A3_3c_yes --> X3_3c_parks["→ S10 (Nebenkosten: Park- und Mautgebühren, §10 Abs.1)"]

A3_3 --> Q3_6a["Wurde die Dienstreise schriftlich oder elektronisch angeordnet oder genehmigt?"]
Q3_6a -->|"Ja"| Q3_6b["Handelt es sich um einen vollen Kalendertag?"]
Q3_6a -->|"Nein"| X3_6_costs["→ S4–S6"]

Q3_6b -->|"Ja"| A3_6_yes["Bei schriftlich oder elektronisch genehmigter Dienstreise steht für jeden vollen Kalendertag Tagegeld in Höhe von 24 Euro. (§6 Abs.1 LRKG)"]
A3_6_yes --> Q3_6e["Wird an dem vollen Kalendertag unentgeltliche Verpflegung (z. B. Mittagessen) bereitgestellt?"]
Q3_6e -->|"Ja"| A3_6_meal_cut["Bei unentgeltlichem Mittagessen wird 40 % des vollen Tagegeldes einbehalten — 9,60 € pro vollem Kalendertag. (§6 Abs.4)"]
Q3_6e -->|"Nein"| A3_6_meal_no["Kein Abzug vom Tagegeld wegen unentgeltlicher Verpflegung. (§6 Abs.4)"]
A3_6_meal_cut --> X3_6_receipts["→ S4–S6"]

Q3_6b -->|"Nein"| Q3_6c["Übersteigt die Reisedauer am An- oder Abreisetag 14 Stunden?"]
Q3_6c -->|"Ja"| A3_6_14["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 14 Stunden Reisedauer 12 Euro. (§6 Abs.1 LRKG)"]
Q3_6c -->|"Nein"| Q3_6d["Übersteigt die Reisedauer am An- oder Abreisetag 8 Stunden?"]
Q3_6d -->|"Ja"| A3_6_8["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 8 Stunden Reisedauer 6 Euro. (§6 Abs.1 LRKG)"]
Q3_6d -->|"Nein"| A3_6_none["Am An- oder Abreisetag steht kein Tagegeld zu, wenn die Reisedauer höchstens 8 Stunden beträgt. (§6 Abs.1 LRKG)"]

A3_3 --> X3_3_costs["→ S4–S6"]
A3_3 --> A3_7["Pauschales Übernachtungsgeld Inland beträgt 20 € je notwendiger Übernachtung. (§7 Abs.1 LRKG)"]
A3_7 --> X3_7_receipts["→ S4–S6"]
```
Processed dialog 19/20
```mermaid
%% 3.2 Ausgangs-/Endpunkt (Wohnung vs. Dienststätte)
A3_2["Grundsatz: Die/der Dienstreisende darf die Wohnung als Ausgangs- und Endpunkt bestimmen. (§3 Abs.2)"]
A3_2 --> Q3_2a["Hat die Dienststelle abweichend die Dienststätte als Start- oder Zielpunkt angeordnet?"]
Q3_2a -->|"Ja"| Q3_2a_bypass["Führt die geplante Verkehrsverbindung unmittelbar an der Dienststätte vorbei?"]
Q3_2a -->|"Nein"| A3_2a_no["Wohnung bleibt Ausgangs- und Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Ja"| A3_2a_yes["Dann gilt die Dienststätte als Ausgangs- bzw. Endpunkt. (§3 Abs.2)"]
Q3_2a_bypass -->|"Nein"| A3_2a_no
A3_2a_no --> Q3_2a_bem["Bemisst sich die Fahrkostenerstattung nach der Entfernung von/bis zur Wohnung?"]
Q3_2a_bem --> A3_2a_bem_yes["Fahrkostenerstattung bemisst sich nach der Entfernung von/bis zur Wohnung. (§3 Abs.2)"]
A3_2a_bem_yes --> X3_2_costs["→ S4–S6"]

A3_2 --> A3_3["Grundsatz: Die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
A3_3 --> Q3_3a["Überwiegen dienstliche oder wirtschaftliche Gründe gegenüber Klimaschutzbelangen?"]
Q3_3a -->|"Ja"| A3_3a_yes["Flugreisen sind erstattungsfähig, wenn dienstliche oder wirtschaftliche Gründe die Klimaschutzbelange überwiegen. (§3 Abs.3; §4 Abs.1)"]
A3_3a_yes --> X3_3a_order["→ S2"]
Q3_3a -->|"Nein"| Q3_3a_exc["Liegt ein Grad der Behinderung ≥50 oder ein gesundheitlicher Grund vor, der die Nutzung einer höheren Beförderungsklasse rechtfertigt?"]
Q3_3a_exc -->|"Ja"| A3_3a_exc_yes["Bei Vorliegen eines Grad(es) der Behinderung ≥50 oder eines gesundheitlichen Grundes wird eine höhere Beförderungsklasse erstattet. (§4 Abs.1)"]
Q3_3a_exc -->|"Nein"| A3_3a_exc_no["Erstattet werden maximal die Kosten der niedrigsten Beförderungsklasse — bei Bahn grundsätzlich die 2. Klasse; bei Flugreisen grundsätzlich die niedrigste Flugklasse (Economy); ggf. zu zahlende Differenzen sind privat zu tragen. (§4 Abs.1)"]
A3_3 --> Q3_3b["Ordnet die Dienststelle verbindlich ein bestimmtes Beförderungsmittel an (z. B. Auto statt Bahn)?"]
Q3_3b -->|"Ja"| A3_3b_yes["Die Dienststelle darf nicht generell ein bestimmtes Verkehrsmittel vorschreiben; die/der Dienstreisende darf das Beförderungsmittel grundsätzlich frei wählen; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]
Q3_3b -->|"Nein"| A3_3b_no["Die/der Dienstreisende wählt das Beförderungsmittel grundsätzlich frei; Wirtschaftlichkeits- und Klimaschutzgesichtspunkte sind zu beachten. (§3 Abs.3)"]

A3_3 --> Q3_3c["Liegt ein erhebliches dienstliches Interesse an der Benutzung eines privaten Kraftfahrzeugs vor (z. B. Transport technischer Geräte, zeitliche Bindung)?"]
Q3_3c -->|"Ja"| A3_3c_yes["Bei Vorliegen eines erheblichen dienstlichen Interesses beträgt die Wegstreckenentschädigung 0,35 €/km. (§5 Abs.2 LRKG)"]
Q3_3c -->|"Nein"| A3_3c_no["Bei Nichtvorliegen gilt die reguläre Wegstreckenentschädigung nach §5 Abs.1 LRKG. (§5 Abs.1 LRKG)"]
A3_3c_yes --> X3_3c_parks["→ S10 (Nebenkosten: Park- und Mautgebühren, §10 Abs.1)"]

A3_3 --> Q3_6a["Wurde die Dienstreise schriftlich oder elektronisch angeordnet oder genehmigt?"]
Q3_6a -->|"Ja"| Q3_6b["Handelt es sich um einen vollen Kalendertag?"]
Q3_6a -->|"Nein"| X3_6_costs["→ S4–S6"]

Q3_6b -->|"Ja"| A3_6_yes["Bei schriftlich oder elektronisch genehmigter Dienstreise steht für jeden vollen Kalendertag Tagegeld in Höhe von 24 Euro. (§6 Abs.1 LRKG)"]
A3_6_yes --> Q3_6e["Wird an dem vollen Kalendertag unentgeltliche Verpflegung (z. B. Mittagessen) bereitgestellt?"]
Q3_6e -->|"Ja"| A3_6_meal_cut["Bei unentgeltlichem Mittagessen wird 40 % des vollen Tagegeldes einbehalten — 9,60 € pro vollem Kalendertag. (§6 Abs.4)"]
Q3_6e -->|"Nein"| A3_6_meal_no["Kein Abzug vom Tagegeld wegen unentgeltlicher Verpflegung. (§6 Abs.4)"]
A3_6_meal_cut --> X3_6_receipts["→ S4–S6"]

Q3_6b -->|"Nein"| Q3_6c["Übersteigt die Reisedauer am An- oder Abreisetag 14 Stunden?"]
Q3_6c -->|"Ja"| A3_6_14["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 14 Stunden Reisedauer 12 Euro. (§6 Abs.1 LRKG)"]
Q3_6c -->|"Nein"| Q3_6d["Übersteigt die Reisedauer am An- oder Abreisetag 8 Stunden?"]
Q3_6d -->|"Ja"| A3_6_8["Am An- oder Abreisetag beträgt das Tagegeld bei mehr als 8 Stunden Reisedauer 6 Euro. (§6 Abs.1 LRKG)"]
Q3_6d -->|"Nein"| A3_6_none["Am An- oder Abreisetag steht kein Tagegeld zu, wenn die Reisedauer höchstens 8 Stunden beträgt. (§6 Abs.1 LRKG)"]

A3_3 --> X3_3_costs["→ S4–S6"]
A3_3 --> A3_7["Pauschales Übernachtungsgeld Inland beträgt 20 € je notwendiger Übernachtung. (§7 Abs.1 LRKG)"]
A3_7 --> X3_7_receipts["→ S4–S6"]

A3_3 --> Q3_4a["Bis wann ist die Reisekostenvergütung schriftlich oder elektronisch zu beantragen (Ausschlussfrist)?"]
Q3_4a --> A3_4["Die Reisekostenvergütung ist schriftlich oder elektronisch spätestens innerhalb von sechs Monaten nach dem Tag nach Beendigung der Dienstreise zu beantragen. (§3 Abs.4 LRKG)"]"""



def merge_flow_multi_all (flow, extension):
    prompt = f"""
Mermaid Flow Integration Prompt (Final Polished Version)
You are given:
the existing Mermaid flow {flow}
extensions to some nodes of the dialogues {extension}
🎯 GOAL
Integrate {extension} into {flow} at the right node.
Output: The complete updated mermaid flow

"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content.strip()
    


if __name__ == "__main__":
    print("Printing Graph")

    """for i, multiturndialog in enumerate(dialogues, start=1):
        flow = merge_flow_multi(flow, multiturndialog)  # update flow in-place
        print(flow)
        print(f"Processed dialog {i}/{len(dialogues)}")

    IMPROVED_PATH.write_text(str(flow), encoding="utf-8")
    print(f"Saved final flow to: {IMPROVED_PATH.resolve()}")"""
    new = merge_flow_multi_all (flow, extension)
    print(new)
    IMPROVED_PATH.write_text(str(new), encoding="utf-8")
    print(f"Saved final flow to: {IMPROVED_PATH.resolve()}")