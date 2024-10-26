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

    def generate_questions(self, text: str, max_questions: int = 5) -> List[str]:
        # Generate questions based on the input text with beam search
        input_text = "Generate questions: " + text
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True)
        outputs = self.model.generate(
            inputs['input_ids'], max_length=50, num_return_sequences=max_questions, num_beams=max_questions
        )
        questions = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        return questions

    def find_answers(self, text: str, questions: List[str]) -> List[Tuple[str, str]]:
        # Use T5 model to find answers to the generated questions
        answers = []
        for question in questions:
            input_text = f"question: {question} context: {text}"
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True)
            outputs = self.model.generate(inputs['input_ids'], max_length=50)
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            answers.append((question, answer))
        return answers

    def process_pdf_and_generate_qa(self, pdf_paths: List[str], max_questions: int = 5):
        # Process entire workflow: extract text, generate questions, and find answers
        all_text = self.extract_text_from_multiple_pdfs(pdf_paths)
        questions = self.generate_questions(all_text, max_questions=max_questions)
        qa_pairs = self.find_answers(all_text, questions)
        return qa_pairs

# Usage
pdf_paths = ["../data/L2 - Algorithms_v2.pdf"]  # List your PDF files here
processor = EducationalPDFProcessor()
qa_pairs = processor.process_pdf_and_generate_qa(pdf_paths, max_questions=5)

# Display the questions and answers
for question, answer in qa_pairs:
    print(f"Question: {question}")
    print(f"Answer: {answer}\n")
