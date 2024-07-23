import logging
from fastapi import APIRouter, HTTPException
from typing import List

from qa_api.models import Question, QuestionResponse, QuestionEntity, Answer, AnswerResponse, AnswerEntity, Comment, CommentResponse, CommentEntity

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Temporary storage for questions, answers, and comments
questions = []
answers = []
comments = []

# Questions
@router.post("/questions/", response_model=QuestionResponse)
def create_question(question: Question):
    question_id = len(questions) + 1
    question_entity = QuestionEntity(id=question_id, **question.model_dump())
    questions.append(question_entity)
    logger.info(f"Created question: {question_entity}")
    return QuestionResponse(id=question_entity.id, **question.model_dump())

@router.get("/questions/", response_model=List[QuestionResponse])
def get_questions():
    logger.info("Fetching all questions")
    return [QuestionResponse(id=question.id, title=question.title, description=question.description) for question in questions]

@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int):
    logger.info(f"Fetching question with id: {question_id}")
    for question in questions:
        if question.id == question_id:
            return QuestionResponse(id=question.id, title=question.title, description=question.description)
    logger.error(f"Question with id {question_id} not found")
    raise HTTPException(status_code=404, detail="Question not found")

# Answers
@router.post("/answers/", response_model=AnswerResponse)
def create_answer(answer: Answer):
    answer_id = len(answers) + 1
    answer_entity = AnswerEntity(id=answer_id, **answer.model_dump())
    answers.append(answer_entity)
    logger.info(f"Created answer: {answer_entity}")
    return AnswerResponse(id=answer_entity.id, **answer.model_dump())

@router.get("/questions/{question_id}/answers/", response_model=List[AnswerResponse])
def get_answers(question_id: int):
    logger.info(f"Fetching answers for question id: {question_id}")
    return [AnswerResponse(id=answer.id, question_id=answer.question_id, content=answer.content) for answer in answers if answer.question_id == question_id]

# Comments
@router.post("/comments/", response_model=CommentResponse)
def create_comment(comment: Comment):
    comment_id = len(comments) + 1
    comment_entity = CommentEntity(id=comment_id, **comment.model_dump())
    comments.append(comment_entity)
    logger.info(f"Created comment: {comment_entity}")
    return CommentResponse(id=comment_entity.id, **comment.model_dump())

@router.get("/answers/{answer_id}/comments/", response_model=List[CommentResponse])
def get_comments(answer_id: int):
    logger.info(f"Fetching comments for answer id: {answer_id}")
    return [CommentResponse(id=comment.id, answer_id=comment.answer_id, content=comment.content) for comment in comments if comment.answer_id == answer_id]