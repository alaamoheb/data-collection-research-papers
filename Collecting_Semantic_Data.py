import requests
import csv
import time

url = 'https://api.semanticscholar.org/graph/v1/paper/batch'
query_params = {"fields": "title,authors,citationCount,references,url,fieldsOfStudy,year,isOpenAccess,externalIds,paperId,publicationDate,embedding"}

api_key = "your_api_key"
headers = {"x-api-key": api_key}

csv_file_path = 'C:\\Users\\alaay\\Documents\\Programs\\DATA\\Semantic Scholar Data\\Graph Analysis\\scr\\data\\sample.csv'
output_csv_path = 'C:\\Users\\alaay\\Documents\\Programs\\DATA\\Semantic Scholar Data\\Graph Analysis\\scr\\data\\fetched_data.csv'


papers_dois = []
with open(csv_file_path, mode='r', encoding='ISO-8859-1') as file:
    reader = csv.DictReader(file)
    column_names = [name.strip() for name in reader.fieldnames]
    if 'doi' in column_names:
        for row in reader:
            doi = row['doi']
            if doi:
                papers_dois.append(doi)


with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
    fieldnames = ['Paper Id','doi', 'title', 'authors', 'citationCount', 'references', 'year', 'isOpenAccess', 'externalIds', 'publicationDate', 'embedding']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

   
    batch_size = 500
    for i in range(0, len(papers_dois), batch_size):
        
        papers_details_response = requests.post(
            url,
            params=query_params,
            json={"ids": papers_dois[i:i + batch_size]},
            headers=headers
        )

        
        try:
            papers_details = papers_details_response.json()
        except ValueError as e:
            print(f"Error parsing JSON at batch {i}: {e}")
            continue

        if not isinstance(papers_details, list):
            print(f"Unexpected response format at batch {i}: {papers_details}")
            continue

        for paper in papers_details:
            if paper:
                extracted_doi = paper.get("externalIds", {}).get("DOI", doi)
                data_to_save = {
                    'Paper Id': paper.get("paperId", ""),
                    'doi': extracted_doi,
                    'title': paper.get("title", ""),
                    'authors': ', '.join([author['name'] for author in paper.get("authors", [])]),
                    'citationCount': paper.get("citationCount", ""),
                    'references': paper.get("references", []),
                    'year': paper.get("year", ""),
                    'isOpenAccess': paper.get("isOpenAccess", ""),
                    'externalIds': paper.get("externalIds", {}),
                    'publicationDate': paper.get("publicationDate", ""),
                    'embedding': paper.get("embedding", "")
                }
                writer.writerow(data_to_save)

        print(f"Processed {min(i + batch_size, len(papers_dois))} papers out of {len(papers_dois)}")

        
        time.sleep(1)

print(f"Fetched data saved to {output_csv_path}")
