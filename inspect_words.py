from src.extractor import Extractor

def inspect_words():
    extractor = Extractor("examples/IMG_1805.png")
    result = extractor.extract()
    print(f"Total words: {len(result['word_data'])}")
    for w in result['word_data']:
        # Print words that might be labels
        if len(w['text']) > 2:
            print(f"Text: {w['text']:<20} Conf: {w['conf']:<5} Top: {w['top']:<5} Left: {w['left']}")

if __name__ == "__main__":
    inspect_words()
