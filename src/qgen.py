import torch
import pdfplumber
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import List, Dict
import json  # Import json module

class EducationalPDFProcessor:
    def __init__(self, model_name="google/flan-t5-base"):
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

    def generate_questions(self, text: str, max_questions: int = 3, temperature: float = 0.8, top_k: int = 200, use_beam_search: bool = False) -> List[str]:
        # Generate questions based on the input text with the option for beam search or sampling
        input_text = "Generate questions: " + text
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True)
        
        # Select generation method
        if use_beam_search:
            outputs = self.model.generate(
                inputs['input_ids'],
                max_length=50,
                num_beams=3,
                num_return_sequences=max_questions,
                early_stopping=True
            )
        else:
            outputs = self.model.generate(
                inputs['input_ids'],
                max_length=50,
                num_return_sequences=max_questions,
                do_sample=True,
                temperature=temperature,
                top_k=top_k
            )
        
        questions = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        return questions

    def find_top_answers(self, input_ids, num_answers=4, max_answer_length=50, temperature=0.995, top_k=300, use_beam_search: bool = False) -> List[str]:
        # Generate top candidate answers with either beam search or sampling
        candidate_answers = []
        
        for _ in range(num_answers):
            if use_beam_search:
                output = self.model.generate(
                    input_ids,
                    max_length=max_answer_length,
                    num_beams=3,
                    num_return_sequences=1,
                    early_stopping=True
                )
            else:
                output = self.model.generate(
                    input_ids,
                    max_length=max_answer_length,
                    do_sample=True,
                    temperature=temperature,
                    top_k=top_k
                )
            answer_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            candidate_answers.append(answer_text)
        
        return candidate_answers

    def find_answers(self, text: str, questions: List[str], use_beam_search: bool = False) -> List[Dict[str, str]]:
        # Use T5 model to find possible answers to each generated question
        qa_pairs = []
        for question in questions:
            input_text = f"question: {question} context: {text}"
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True)
            candidate_answers = self.find_top_answers(inputs['input_ids'], num_answers=4, use_beam_search=use_beam_search)

            # Filter out single-number answers and ensure uniqueness
            filtered_answers = {ans for ans in candidate_answers if not ans.isdigit()}
            qa_pairs.append((question, list(filtered_answers)))  # Convert back to list
        return qa_pairs

    def generate_explanation(self, question: str, context: str, answer: str, use_beam_search: bool = False) -> str:
        # Generate an explanation for the provided answer
        input_text = f"Explain why the answer to the question '{question}' is '{answer}' based on the context: {context}"
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True)
        
        # Select generation method
        if use_beam_search:
            output = self.model.generate(
                inputs['input_ids'],
                max_length=100,
                num_beams=3,
                num_return_sequences=1,
                early_stopping=True
            )
        else:
            output = self.model.generate(
                inputs['input_ids'],
                max_length=100,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7,
                top_k=150
            )
        
        explanation = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return explanation

    def process_pdf_and_generate_qa(self, pdf_paths: List[str], max_questions: int = 3, use_beam_search: bool = False) -> List[Dict[str, str]]:
        # Process entire workflow: extract text, generate questions, find answers, and generate explanations
        all_text = self.extract_text_from_multiple_pdfs(pdf_paths)
        questions = self.generate_questions(all_text, max_questions=max_questions, use_beam_search=use_beam_search)
        qa_pairs = self.find_answers(all_text, questions, use_beam_search=use_beam_search)
        
        # Format the output as quiz questions
        quiz_questions = []
        for question, answers in qa_pairs:
            entry = {"question": question}
            options = [f"{chr(65 + i)}) {answer}" for i, answer in enumerate(answers[:4])]  # Limit to 4 options for A-D
            entry["options"] = options
            entry["correct"] = options[0] if options else "No valid answer options available."
            entry["explanation"] = self.generate_explanation(question, all_text, answers[0], use_beam_search=use_beam_search) if options else "No valid explanation available."
            quiz_questions.append(entry)

        return quiz_questions

# Usage
pdf_paths = ["../example.pdf"]
processor = EducationalPDFProcessor()
quiz_questions = processor.process_pdf_and_generate_qa(pdf_paths, max_questions=3, use_beam_search=False)

# Save the formatted output to a JSON file
with open("quiz_questions.json", "w") as json_file:
    json.dump(quiz_questions, json_file, indent=4)

# Display the formatted output
for question in quiz_questions:
    print(question)












