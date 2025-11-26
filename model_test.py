from transformers import pipeline

# Use a multilingual zero-shot classifier
# This allows you to define your own labels without training a new model!
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def analyze_message(text):
    candidate_labels = ["urgent financial scam", "phishing attempt", "normal conversation", "safe transaction"]
    
    result = classifier(text, candidate_labels)
    
    # Return the top label and score
    top_label = result['labels'][0]
    confidence = result['scores'][0]
    
    return top_label, confidence