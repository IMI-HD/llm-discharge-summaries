
#creating the prompt by using ehr data
def create_prompt(ehr_data):
    prompt = [
        {"role": "system", "content": "Du bist Stationsarzt im Universitätsklinikum und schreibst Entlassungsbriefe für den Hausarzt des Patienten. Dabei verwendest du korrekte medizinische Terminologie. Du sprichst ausschließlich Deutsch.\n"},
        {"role": "user", "content": f"Schreibe die Abschnitte \"Anamnese und Befund\" und \"Therapie und Verlauf\" des Entlassungsbriefs für einen Patienten. Der Abschnitt \"Anamnese und Befund\" soll die Vorgeschichte des Patienten enthalten und erklären, warum der Patient die Operation erhalten hat. Der Abschnitt \"Therapie und Verlauf\" beschreibt den Verlauf der Operation und Informationen über die stationäre Behandlung des Patienten, die nach der Entlassung für den Hausarzt relevant sind.\nAlle anderen Abschnitte (\"Diagnose\", \"Therapie\", \"Histologie\", \"Procedere\" und \"Medikation\") werden automatisch erstellt und sollen nicht von dir geschrieben werden. Um die Abschnitte \"Anamnese und Befund\" und \"Therapie und Verlauf\" zu schreiben, stehen dir Informationen aus der Patientenakte zur Verfügung. Verwende ausschließlich die gegebenen Informationen und erfinde nichts dazu.\nHier sind die Daten aus der Patientenakte:\n{ehr_data}\n\nAnamnese und Befund:\nTherapie und Verlauf:"}
    ]
    
    return prompt