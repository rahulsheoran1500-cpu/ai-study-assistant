"""AI SERVICE - OpenAI API integration for all AI features"""

import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AIService:
    """Service class for all AI operations using OpenAI GPT-4o"""
    
    MODEL = "gpt-4o"
    
    @staticmethod
    def check_api_key():
        """Check if API key is configured"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY not found")
            return False
        return True
    
    @staticmethod
    def answer_question(question):
        """Answer an academic question"""
        if not AIService.check_api_key():
            return "❌ API Key not configured. Add OPENAI_API_KEY to .env"
        
        try:
            response = client.chat.completions.create(
                model=AIService.MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert academic tutor. Provide clear, concise explanations suitable for college students."},
                    {"role": "user", "content": question}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def generate_notes(topic, detail_level="medium"):
        """Generate structured study notes"""
        if not AIService.check_api_key():
            return "❌ API Key not configured"
        
        try:
            prompt = f"""Generate comprehensive study notes on: {topic}
            
Include:
1. Introduction
2. Key Concepts with definitions
3. Detailed Explanation
4. Examples
5. Key Points
6. Quick Review

Detail Level: {detail_level}
Use clear formatting with bullet points."""
            
            response = client.chat.completions.create(
                model=AIService.MODEL,
                messages=[
                    {"role": "system", "content": "Create clear, well-structured study notes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def summarize_text(text, summary_length="medium"):
        """Summarize provided text"""
        if not AIService.check_api_key():
            return {"error": "❌ API Key not configured"}
        
        try:
            prompt = f"""Summarize this text. Create:
1. A concise summary
2. 5-7 key points in bullet format

Text: {text}

Summary Length: {summary_length}"""
            
            response = client.chat.completions.create(
                model=AIService.MODEL,
                messages=[
                    {"role": "system", "content": "Create clear, concise summaries with key points."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            parts = content.split('\n\n')
            
            return {
                "summary": parts[0] if parts else content,
                "key_points": '\n'.join(parts[1:]) if len(parts) > 1 else ""
            }
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": f"❌ Error: {str(e)}"}
    
    @staticmethod
    def generate_quiz(topic, num_questions=5):
        """Generate multiple-choice quiz questions"""
        if not AIService.check_api_key():
            return {"error": "❌ API Key not configured"}
        
        try:
            prompt = f"""Create {num_questions} multiple-choice questions on: {topic}
            
For each question provide:
1. Question text
2. Four options (A, B, C, D)
3. Correct answer
4. Explanation

Format as JSON array:
[{{
  "question": "text",
  "options": {{"A": "opt", "B": "opt", "C": "opt", "D": "opt"}},
  "correct_answer": "A",
  "explanation": "why"
}}]"""
            
            response = client.chat.completions.create(
                model=AIService.MODEL,
                messages=[
                    {"role": "system", "content": "Create clear, educational multiple-choice questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
            
            return {"raw_content": content}
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": f"❌ Error: {str(e)}"}
    
    @staticmethod
    def generate_flashcards(topic, num_cards=10):
        """Generate flashcard question-answer pairs"""
        if not AIService.check_api_key():
            return {"error": "❌ API Key not configured"}
        
        try:
            prompt = f"""Create {num_cards} flashcard pairs for: {topic}
            
Format as JSON: [{{"question": "Q", "answer": "A"}}]"""
            
            response = client.chat.completions.create(
                model=AIService.MODEL,
                messages=[
                    {"role": "system", "content": "Create concise flashcard question-answer pairs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
            
            return {"raw_content": content}
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": f"❌ Error: {str(e)}"}
    
    @staticmethod
    def generate_study_plan(subjects, exam_date, available_hours, difficulty_level):
        """Generate personalized study plan"""
        if not AIService.check_api_key():
            return "❌ API Key not configured"
        
        try:
            from datetime import datetime
            exam_date_obj = datetime.strptime(exam_date, '%Y-%m-%d')
            days_remaining = (exam_date_obj - datetime.now()).days
            
            prompt = f"""Create a personalized study plan:
Subjects: {subjects}
Exam Date: {exam_date}
Days Remaining: {days_remaining}
Daily Hours: {available_hours}
Difficulty: {difficulty_level}

Include:
1. Overview
2. Weekly breakdown
3. Daily schedule
4. Study tips
5. Milestones"""
            
            response = client.chat.completions.create(
                model=AIService.MODEL,
                messages=[
                    {"role": "system", "content": "Create personalized, realistic study plans."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"❌ Error: {str(e)}"
