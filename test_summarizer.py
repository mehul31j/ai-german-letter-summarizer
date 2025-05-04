from summarizer import summarize_text, extract_key_points

def test_summarizer():
    # Sample German business letter
    german_text = """
    Sehr geehrte Damen und Herren,

    ich schreibe Ihnen bezüglich der unbezahlten Rechnung Nr. 12345 vom 15. März 2024.
    Die Zahlung sollte bis zum 30. März 2024 erfolgen, wurde aber bisher nicht geleistet.

    Die Rechnungssumme beträgt 1.234,56 € und ist für die gelieferten Büromaterialien.
    Bitte überweisen Sie den Betrag innerhalb der nächsten 7 Tage auf unser Konto:

    Kontoinhaber: Beispiel GmbH
    IBAN: DE12 3456 7890 1234 5678 90
    BIC: BEISDE12345

    Falls Sie die Rechnung bereits bezahlt haben, ignorieren Sie bitte dieses Schreiben.
    Bei Fragen können Sie uns unter +49 123 4567890 erreichen.

    Mit freundlichen Grüßen,
    Max Mustermann
    Geschäftsführer
    """

    print("Testing summarizer with DeepSeek...")
    print("\nOriginal German Text:")
    print(german_text)

    print("\nGenerating Summary...")
    summary = summarize_text(german_text)
    print("\nSummary:")
    print(summary)

    print("\nExtracting Key Points...")
    key_points = extract_key_points(german_text)
    print("\nKey Points:")
    for point in key_points:
        print(point)

if __name__ == "__main__":
    test_summarizer() 