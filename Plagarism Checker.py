
from google_search_results import GoogleSearchResults
import docx
import fitz  # PyMuPDF

def read_word_file(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def read_pdf_file(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text += page.get_text()
    return text

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]

def calculate_similarity(text1, text2):
    distance = levenshtein_distance(text1, text2)
    max_length = max(len(text1), len(text2))
    similarity_percentage = 100 * (1 - distance / max_length)
    return similarity_percentage

def check_plagiarism_on_internet(query):
    params = {
        "q": query,
        "api_key": "a943e187bc05a6d05571917125b6a8d9293cedf4b06f47b30571dd6e490418e7"  # Replace with your SerpAPI key
    }

    try:
        serp_api = GoogleSearchResults(params)
        serp_api.get_json()
        organic_results = serp_api.organic_results
        if organic_results:
            first_result = organic_results[0]
            snippet = first_result.get('snippet', '')
            return snippet
        else:
            return "No search results found."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Enter the path of the document (Word or PDF):")
    file_path = input()

    try:
        document = read_word_file(file_path) if file_path.endswith('.docx') else read_pdf_file(file_path)
        internet_snippet = check_plagiarism_on_internet(document)

        print("\nInternet Search Result:")
        print(internet_snippet)
    except Exception as e:
        print(f"Error: {e}")
