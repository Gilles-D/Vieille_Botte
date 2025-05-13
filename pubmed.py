# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:00:01 2025

@author: Gil
"""

from Bio import Entrez

# Ton adresse email (requis par NCBI)
Entrez.email = "ton.email@exemple.com"

def search_pubmed(query, max_results=5):
    """
    Recherche les articles PubMed en fonction d'une requête (mot-clé ou auteur).
    Retourne une liste de tuples (titre, lien).
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="most recent")
    record = Entrez.read(handle)
    ids = record.get("IdList", [])[:max_results]  # Sécurité pour ne jamais dépasser max_results

    if not ids:
        return []

    handle = Entrez.esummary(db="pubmed", id=",".join(ids))
    summary_records = Entrez.read(handle)

    results = []
    for item in summary_records:
        title = item.get("Title", "Sans titre")
        url = f"https://pubmed.ncbi.nlm.nih.gov/{item['Id']}/"
        results.append((title, url))

    return results[:max_results]  # Sécurité bis