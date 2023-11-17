import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_wordcloud(keywords, output_path):
    """
    Create a word cloud from the provided keywords.
    """

    # Convert bigrams (tuples) to strings and build the frequency dictionary
    word_freq_dict = { ' '.join(key) if isinstance(key, tuple) else key: value for key, value in keywords}

    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq_dict)

    # Plot the WordCloud image                        
    plt.figure(figsize=(8, 8), facecolor=None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad=0) 
    
    # Save the fig
    plt.savefig(output_path)
    plt.close()


def create_bar_plot(keywords, output_path):
    """
    Create a horizontal bar plot for the provided keywords.
    """
    
    # Convert tuples to strings
    keywords = sorted([(' '.join(key) if isinstance(key, tuple) else key, value) for key, value in keywords], key=lambda x: x[1], reverse=True)

    words, frequencies = zip(*keywords)

    plt.figure(figsize=(10, 10))
    plt.barh(words, frequencies)
    plt.xlabel('Frequency')
    plt.ylabel('Keywords')
    plt.yticks(fontsize=8)
    plt.title('Keyword Frequencies')
    plt.gca().invert_yaxis()

    # Save the fig
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def create_txt_file(unigrams, bigrams, combined_keywords, output_path):
    """
    Create a txt file words and respective frequency for unigrams, bigrams, and combined_keywords.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        # Write Unigrams section
        file.write("Unigram Frequency\n\n")
        for unigram, freq in unigrams:
            file.write(f"{unigram}: {freq}\n")
        file.write("\n")

        # Write Bigrams section
        file.write("Bigram Frequency\n\n")
        for bigram, freq in bigrams:
            bigram = ' '.join(bigram)  # Convert tuple to string
            file.write(f"{bigram}: {freq}\n")
        file.write("\n")

        # Write Combined Keywords section
        file.write("Combined Keyword Frequency\n\n")
        for keyword, freq in combined_keywords:
            file.write(f"{keyword}: {freq}\n")
        file.write("\n")

