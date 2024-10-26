from utils import extract_text_from_pdf
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = T5ForConditionalGeneration.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

def get_question(answer, context, max_length=64):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'], 
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return tokenizer.decode(output[0])

context = "Manuel has created RuPERTa-base with the support of HF-Transformers and Google"
answer = "Manuel"

get_question(answer, context)

"""
path_pdf = "../data/L1a - History.pdf"
text = extract_text_from_pdf(path_pdf)
questions = generate_questions(text, model, tokenizer, num_questions=5)

for i, question in enumerate(questions, 1):
    print(f"Question {i}: {question}")
    """