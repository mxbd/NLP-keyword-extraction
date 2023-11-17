import os
import PyPDF2
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
from .utils import is_reference_page


# necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

def extract_keywords_from_pdf(pdf_path, num_keywords, ignore_words):
    """
    Extract keywords from a PDF file, excluding reference pages.
    Returns a tuple of (unigrams, bigrams, pages_used)
    """

    unigram_freq = Counter()
    bigram_freq = Counter()
    pages_used = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        stop_words = set(stopwords.words('english'))

        for i, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if is_reference_page(page_text):
                continue

            words = word_tokenize(page_text.lower())

            # Filtering for unigrams
            filtered_unigrams = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words and word not in ignore_words]
            unigram_freq.update(filtered_unigrams)

            # Filtering for bigrams
            filtered_bigrams = bigrams(filtered_unigrams)
            filtered_bigrams = [bigram for bigram in filtered_bigrams if not any(word in ignore_words for word in bigram)]
            bigram_freq.update(filtered_bigrams)

            pages_used.append(i)

    # Select top N unigrams and bigrams
    top_unigrams = unigram_freq.most_common(num_keywords)
    top_bigrams = bigram_freq.most_common(num_keywords)

    # Adjust unigram frequencies based on bigram occurrences
    for bigram, freq in top_bigrams:
        words = bigram
        for word in words:
            if word in unigram_freq:
                unigram_freq[word] = max(0, unigram_freq[word] - freq)

    # Get adjusted top unigrams after reduction
    top_unigrams_adjusted = unigram_freq.most_common(num_keywords)

    return top_unigrams_adjusted, top_bigrams, pages_used



def process_files_in_folder(input_folder, num_keywords_per_file, num_keywords_total, ignore_words=None, adjust_unigrams=False):
    cumulative_unigram_freq = Counter()
    cumulative_bigram_freq = Counter()
    cumulative_combined_freq = Counter()
    analysis_log = {}

    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, pdf_file)
            unigrams, bigrams, pages_used = extract_keywords_from_pdf(pdf_path, num_keywords_per_file, ignore_words)

            if adjust_unigrams:
                # Adjust unigram frequencies based on bigram occurrences for the individual file
                unigrams = adjust_unigram_frequencies(unigrams, bigrams)

            # Combine adjusted unigrams and bigrams for the individual file
            combined_keywords = dict(unigrams + bigrams)

            # Accumulate data from each file
            cumulative_unigram_freq += Counter(dict(unigrams))
            cumulative_bigram_freq += Counter(dict(bigrams))
            cumulative_combined_freq += Counter(combined_keywords)
            analysis_log[pdf_file] = pages_used

    # Get the most common unigrams, bigrams, and combined keywords across all texts
    top_unigrams = cumulative_unigram_freq.most_common(num_keywords_total)
    top_bigrams = cumulative_bigram_freq.most_common(num_keywords_total)
    top_combined_keywords = cumulative_combined_freq.most_common(num_keywords_total)

    return {
        "unigrams": top_unigrams, 
        "bigrams": top_bigrams,
        "combined_keywords": top_combined_keywords,
        "log": analysis_log
    }


# Adjustment logic: sum of unigrams always = or > than sum of bigrams
def adjust_unigram_frequencies(unigrams, bigrams):
    """
    Adjust the frequencies of unigrams based on the occurrence of corresponding bigrams.
    """
    unigram_dict = dict(unigrams)
    bigram_dict = dict([(" ".join(pair), freq) for pair, freq in bigrams])

    # Adjust unigram frequencies based on bigram occurrences
    for bigram, freq in bigram_dict.items():
        words = bigram.split(' ')
        for word in words:
            if word in unigram_dict:
                unigram_dict[word] = max(0, unigram_dict[word] - freq)

    adjusted_unigrams = [(word, freq) for word, freq in unigram_dict.items() if freq > 0]
    return adjusted_unigrams


def filter_zero_frequency(keywords):
    """ Remove entries with zero frequency. """
    return [(word, freq) for word, freq in keywords if freq > 0]


