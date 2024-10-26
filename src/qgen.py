import torch
import pdfplumber
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import List, Tuple

class EducationalPDFProcessor:
    def __init__(self, model_name="google/flan-t5-small"):
        # Initialize the model and tokenizer for text generation and question answering
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        # Extract text from a single PDF
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Ensure the text is not None
                    text += page_text + "\n"
        return text

    def extract_text_from_multiple_pdfs(self, pdf_paths: List[str]) -> str:
        # Combine text from multiple PDFs
        all_text = ""
        for pdf_path in pdf_paths:
            all_text += self.extract_text_from_pdf(pdf_path)
        return all_text

    def generate_questions(self, text: str, max_questions: int = 5, temperature: float = 0.7, top_k: int = 100) -> List[str]:
        # Generate questions based on the input text with sampling
        input_text = "Generate questions: " + text
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True)
        
        # Generate questions with sampling to add variety
        outputs = self.model.generate(
            inputs['input_ids'],
            max_length=50,
            num_return_sequences=max_questions,
            do_sample=True,           # Enable sampling to add randomness
            temperature=temperature,   # Set a high temperature for more diverse questions
            top_k=top_k                # Sample from the top K tokens for increased variability
        )
        
        questions = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        return questions

    def find_top_answers(self, input_ids, num_answers=4, max_answer_length=50, temperature=0.995, top_k=200) -> List[str]:
        # Generate top candidate answers with sampling for more variety
        candidate_answers = []
        
        for _ in range(num_answers):
            output = self.model.generate(
                input_ids,
                max_length=max_answer_length,
                do_sample=True,  # Enable sampling to introduce randomness
                temperature=temperature,  # Controls the creativity of the output (higher = more random)
                top_k=top_k  # Limit sampling to the top K tokens to control diversity
            )
            answer_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            candidate_answers.append(answer_text)
        
        return candidate_answers

    def find_answers(self, text: str, questions: List[str]) -> List[Tuple[str, List[str]]]:
        # Use T5 model to find 4 possible answers to each generated question
        qa_pairs = []
        for question in questions:
            input_text = f"question: {question} context: {text}"
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True)
            candidate_answers = self.find_top_answers(inputs['input_ids'], num_answers=4)
            qa_pairs.append((question, candidate_answers))
        return qa_pairs

    def process_pdf_and_generate_qa(self, pdf_paths: List[str], max_questions: int = 5):
        # Process entire workflow: extract text, generate questions, and find answers
        all_text = self.extract_text_from_multiple_pdfs(pdf_paths)
        questions = self.generate_questions(all_text, max_questions=max_questions)
        qa_pairs = self.find_answers(all_text, questions)
        return qa_pairs

# Usage
pdf_paths = ["../data/L1a - History.pdf"]  # List your PDF files here
processor = EducationalPDFProcessor()
qa_pairs = processor.process_pdf_and_generate_qa(pdf_paths, max_questions=5)

# Display the questions and answer options
for question, answers in qa_pairs:
    print(f"Question: {question}")
    for i, answer in enumerate(answers, 1):
        print(f"Answer Option {i}: {answer}")
    print()




