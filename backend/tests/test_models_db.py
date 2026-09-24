"""数据库层面的模型测试：验证关系、级联与唯一约束。"""

from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    KnowledgePoint,
    Question,
    QuestionOption,
    QuizAnswer,
    QuizSession,
    User,
    UserKnowledgeStat,
)


def _sample_question(**overrides: object) -> Question:
    data: dict[str, object] = {
        "content": "1 + 1 = ?",
        "type": "single_choice",
        "difficulty": 1,
        "answer": {"key": "A"},
        "explanation": "1 + 1 = 2",
        "status": "published",
    }
    data.update(overrides)
    return Question(**data)


async def test_user_quiz_answer_relationships(db_session: AsyncSession) -> None:
    user = User(openid="openid-1", nickname="tester")
    question = _sample_question()
    question.options = [
        QuestionOption(key="A", content="2", sort_order=0),
        QuestionOption(key="B", content="3", sort_order=1),
    ]
    db_session.add_all([user, question])
    await db_session.flush()

    session = QuizSession(user_id=user.id, mode="daily", total_count=1)
    db_session.add(session)
    await db_session.flush()

    answer = QuizAnswer(
        session_id=session.id,
        user_id=user.id,
        question_id=question.id,
        answer={"key": "A"},
        is_correct=True,
    )
    db_session.add(answer)
    await db_session.flush()

    loaded = (
        await db_session.execute(
            select(User)
            .options(selectinload(User.quiz_sessions).selectinload(QuizSession.answers))
            .where(User.id == user.id)
        )
    ).scalar_one()

    assert len(loaded.quiz_sessions) == 1
    assert len(loaded.quiz_sessions[0].answers) == 1
    assert loaded.quiz_sessions[0].answers[0].is_correct is True


async def test_question_option_cascade_delete(db_session: AsyncSession) -> None:
    question = _sample_question()
    question.options = [QuestionOption(key="A", content="2", sort_order=0)]
    db_session.add(question)
    await db_session.flush()
    question_id = question.id

    await db_session.delete(question)
    await db_session.flush()

    remaining = (
        await db_session.execute(
            select(QuestionOption).where(QuestionOption.question_id == question_id)
        )
    ).scalars().all()
    assert remaining == []


async def test_knowledge_point_tree(db_session: AsyncSession) -> None:
    root = KnowledgePoint(name="Python", description="root")
    db_session.add(root)
    await db_session.flush()

    child = KnowledgePoint(name="List", description="list", parent_id=root.id)
    db_session.add(child)
    await db_session.flush()

    loaded_root = (
        await db_session.execute(
            select(KnowledgePoint)
            .options(selectinload(KnowledgePoint.children))
            .where(KnowledgePoint.id == root.id)
        )
    ).scalar_one()
    assert [c.name for c in loaded_root.children] == ["List"]

    loaded_child = (
        await db_session.execute(
            select(KnowledgePoint)
            .options(selectinload(KnowledgePoint.parent))
            .where(KnowledgePoint.id == child.id)
        )
    ).scalar_one()
    assert loaded_child.parent is not None
    assert loaded_child.parent.name == "Python"


async def test_question_knowledge_point_many_to_many(db_session: AsyncSession) -> None:
    kp1 = KnowledgePoint(name="List", description="list")
    kp2 = KnowledgePoint(name="Slice", description="slice")
    question = _sample_question()
    question.knowledge_points = [kp1, kp2]
    db_session.add(question)
    await db_session.flush()

    loaded = (
        await db_session.execute(
            select(Question)
            .options(selectinload(Question.knowledge_points))
            .where(Question.id == question.id)
        )
    ).scalar_one()
    assert {kp.name for kp in loaded.knowledge_points} == {"List", "Slice"}


async def test_user_openid_unique_constraint(db_session: AsyncSession) -> None:
    db_session.add(User(openid="dup", nickname="a"))
    await db_session.flush()
    db_session.add(User(openid="dup", nickname="b"))
    with pytest.raises(IntegrityError):
        await db_session.flush()


async def test_user_knowledge_stat_unique_constraint(db_session: AsyncSession) -> None:
    user = User(openid="stat-user", nickname="n")
    kp = KnowledgePoint(name="Dict", description="dict")
    db_session.add_all([user, kp])
    await db_session.flush()

    db_session.add(
        UserKnowledgeStat(user_id=user.id, knowledge_point_id=kp.id, mastery_score=0.5)
    )
    await db_session.flush()

    db_session.add(UserKnowledgeStat(user_id=user.id, knowledge_point_id=kp.id))
    with pytest.raises(IntegrityError):
        await db_session.flush()
