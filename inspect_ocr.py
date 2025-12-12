from src.extractor import Extractor

def inspect():
    extractor = Extractor("examples/IMG_1805.png")
    result = extractor.extract()
    print("--- FULL TEXT START ---")
    print(result['full_text'])
    print("--- FULL TEXT END ---")

if __name__ == "__main__":
    inspect()
