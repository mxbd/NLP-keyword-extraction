import json
import os
from helpers.file_processing import process_files_in_folder, filter_zero_frequency
from helpers.visualization import create_wordcloud, create_bar_plot, create_txt_file

def load_config(config_path):
    """
    Load the configuration settings from a JSON file.
    """
    with open(config_path, 'r') as file:
        return json.load(file)

def main():
    """
    Main function to execute the script.
    """
    # Load config
    config = load_config("config.json")

    # Extract config settings
    input_folder = config["input_folder"]
    output_folder = config["output_folder"]
    ignore_words = config["ignore_words"]
    generate_outputs = config["generate_outputs"]
    num_keywords_per_file = config["num_keywords_per_file"]
    num_keywords_total = config["num_keywords_total"]
    adjust_unigrams = config["adjust_unigrams_based_on_bigrams"]

    # Process files and get unigrams, bigrams, combined keywords and analysis log
    result = process_files_in_folder(input_folder, num_keywords_per_file, num_keywords_total, ignore_words, adjust_unigrams)

    unigrams = result["unigrams"]
    bigrams = result["bigrams"]
    combined_keywords = result["combined_keywords"]
    analysis_log = result["log"]

    # Filter out zero frequency entries (can happens if "adjust_unigrams_based_on_bigrams": true)
    unigrams = filter_zero_frequency(unigrams)
    bigrams = filter_zero_frequency(bigrams)
    combined_keywords = filter_zero_frequency(combined_keywords)

    # Generate outputs based on user configuration
    if generate_outputs.get("wordcloud"):
        wordcloud_path_unigrams = os.path.join(output_folder, '30_wordcloud_unigrams.png')
        create_wordcloud(unigrams, wordcloud_path_unigrams)

        wordcloud_path_bigrams = os.path.join(output_folder, '31_wordcloud_bigrams.png')
        create_wordcloud(bigrams, wordcloud_path_bigrams)

        wordcloud_path_bigrams = os.path.join(output_folder, '32_wordcloud_combined.png')
        create_wordcloud(combined_keywords, wordcloud_path_bigrams)

    if generate_outputs.get("barplot"):
        barplot_path_unigrams = os.path.join(output_folder, '20_barplot_unigrams.png')
        create_bar_plot(unigrams, barplot_path_unigrams)

        barplot_path_bigrams = os.path.join(output_folder, '21_barplot_bigrams.png')
        create_bar_plot(bigrams, barplot_path_bigrams)

        barplot_path_bigrams = os.path.join(output_folder, '22_barplot_combined.png')
        create_bar_plot(combined_keywords, barplot_path_bigrams)

    if generate_outputs.get("txt_file"):
        txt_path = os.path.join(output_folder, '10_keywords.txt')
        create_txt_file(unigrams, bigrams, combined_keywords, txt_path)

    if generate_outputs.get("analysis_log"):
        log_path = os.path.join(output_folder, '00_analysis_log.txt')
        with open(log_path, 'w') as log_file:
            for pdf_file, pages in analysis_log.items():
                log_file.write(f"{pdf_file}: Pages used for analysis - {pages}\n")

if __name__ == "__main__":
    main()
