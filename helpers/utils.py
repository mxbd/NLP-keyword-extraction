import re

# function not ideal as it removes also pages wiht 50% content and 50% references
# TO DO: function to identify start of references section and ignore subsequent text
def is_reference_page(text):
    """
    Determine if a page is a reference page based on certain indicators.
    """

    # Count occurrences of certain patterns
    year_count = len(re.findall(r'\b\d{4}\b', text))
    doi_count = len(re.findall(r'doi:', text))
    arxiv_count = len(re.findall(r'arXiv', text))
    url_count = len(re.findall(r'https?:', text))

    # Use a threshold to decide if it's a reference page
    if year_count > 5 and (doi_count > 5 or arxiv_count > 5 or url_count > 5):
        return True

    return False