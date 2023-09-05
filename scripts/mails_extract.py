import requests
import re
import json
import sys
import os

def extract_emails_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        
        email_pattern = r"[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,4}(?<!\.png)(?<!\.jpg)(?<!\.jpeg)(?<!\.gif)(?<!\.pn)(?<!\.svg)"
        emails = re.findall(email_pattern, content)
        
        emails = list(set(emails))
        
        return emails
    
    except requests.RequestException as e:
        print(f"Une erreur s'est produite lors de la récupération de la page: {e}")
        return []

def enrich_data_with_emails(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)

    for entry in data:
        website = entry.get("website")
        if website:
            emails = extract_emails_from_url(website)
            if emails:
                entry["liste_mails"] = emails

    # Ajout du suffixe -mails.json pour sauvegarder le fichier enrichi
    base, ext = os.path.splitext(filepath)
    output_filepath = f"{base}-mails{ext}"

    with open(output_filepath, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    # Vérifie si au moins un argument est fourni
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    enrich_data_with_emails(json_file)
