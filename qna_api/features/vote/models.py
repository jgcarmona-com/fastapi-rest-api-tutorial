from pydantic import BaseModel

class VoteCreate(BaseModel):
    vote_value: int  # 1 for upvote, -1 for downvote

class Vote(BaseModel):
    id: int
    vote_value: int
    user_id: int
    question_id: int | None
    answer_id: int | None

    class Config:
        from_attributes = True
