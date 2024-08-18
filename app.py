# app.py
from flask import Flask, jsonify, request
import nltk
from nltk.corpus import words
from flask_cors import CORS
from language_tool_python import LanguageTool
from nltk.tokenize import sent_tokenize

nltk.download('words')
nltk.download('punkt')

app = Flask(__name__)

# language_tool_python == 2.8
# Flask == 3.0.3
# nltk == 3.8.1
# flask_cors == 4.0.1

CORS(app)

@app.route('/favicon.ico')
def favicon():
    return "icon will be added soon"


# Route to get all items
@app.route('/', methods=['GET'])
def get_items():
    print("hello")
    return jsonify({"id": 1, "name": "Item 1"})

@app.route('/name', methods=['GET'])
def get_name():
    print("hello")
    return "Nitin Singh"

# Route to create a new item
@app.route('/', methods=['POST'])
def create_item():
    data = request.get_json()
    print(data)
    
    # tokens = nltk.word_tokenize(data['summary'].lower()) 
    # d = enchant.Dict("en_US")
    # misspelled = [word for word in tokens if not d.check(word)]
    
    grammerMistakes = check_grammar_with_languagetool(data['summary'])
    
    extracted_mistakes = []

    for mistake in grammerMistakes:
        extracted_mistake = {
            # 'ruleId': mistake.ruleId,
            'error': mistake.matchedText, 
            # 'message': mistake.message,
            # 'text': mistake.context['text'] if 'text' in mistake.context else None,
            'replacements': mistake.replacements,
            'context':mistake.context,
            # 'errorLength':mistake.errorLength,
            # 'ruleIssueType':mistake.ruleIssueType,
            # 'extracted_mistakes':mistake.extracted_mistakes
        }
        extracted_mistakes.append(extracted_mistake)
    
    
    mistakes = {
        'grammerMistakes': extracted_mistakes
    }
    
    
    finalData = jsonify(mistakes)
    print(finalData)
    return finalData, 201


def check_grammar_with_languagetool(text):
    mistakes = []
    tool = LanguageTool('en-US')
    sentences = sent_tokenize(text)
    for sentence in sentences:
        matches = tool.check(sentence)
        for match in matches:
            mistakes.append(match)
            # print(match)
    return mistakes        

if __name__ == '__main__':
    app.run(port=1234,debug=True)





