from src.components.text_summarization import TextSummarizer

if __name__ == '__main__':
    text = "The quick brown fox jumps over the lazy dog."
    summarizer = TextSummarizer()
    summary = summarizer.third_summarize(text)
    print(summary)