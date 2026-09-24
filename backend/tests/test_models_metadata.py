"""模型元数据层面的测试：不依赖数据库连接。"""

from __future__ import annotations

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import configure_mappers

from app.models import (
    Base,
    KnowledgePoint,
    Question,
    QuestionKnowledgePoint,
    UserKnowledgeStat,
)

EXPECTED_TABLES = {
    "users",
    "questions",
    "question_options",
    "knowledge_points",
    "question_knowledge_points",
    "quiz_sessions",
    "quiz_answers",
    "user_knowledge_stats",
    "review_items",
}


def test_all_tables_registered() -> None:
    assert EXPECTED_TABLES <= set(Base.metadata.tables)


def test_mappers_configure_without_error() -> None:
    # 若关系配置有误（例如 self-referential / back_populates 不匹配）此处会抛异常。
    configure_mappers()


def _unique_constraint_columns(table) -> list[frozenset[str]]:
    return [
        frozenset(c.name for c in constraint.columns)
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    ]


def test_user_openid_is_unique() -> None:
    from app.models import User

    assert frozenset({"openid"}) in _unique_constraint_columns(User.__table__)


def test_user_knowledge_stat_unique_constraint() -> None:
    combos = _unique_constraint_columns(UserKnowledgeStat.__table__)
    assert frozenset({"user_id", "knowledge_point_id"}) in combos


def test_question_check_constraints_exist() -> None:
    names = {c.name for c in Question.__table__.constraints if c.name}
    assert {
        "ck_questions_type",
        "ck_questions_difficulty_range",
        "ck_questions_status",
    } <= names


def test_question_knowledge_point_composite_pk() -> None:
    pk_columns = {c.name for c in QuestionKnowledgePoint.__table__.primary_key.columns}
    assert pk_columns == {"question_id", "knowledge_point_id"}


def test_knowledge_point_is_self_referential() -> None:
    rels = KnowledgePoint.__mapper__.relationships
    assert "parent" in rels
    assert "children" in rels
    # parent/children 都指向 KnowledgePoint 自身。
    assert rels["parent"].mapper.class_ is KnowledgePoint
    assert rels["children"].mapper.class_ is KnowledgePoint


def test_expected_indexes_present() -> None:
    def index_names(table_name: str) -> set[str]:
        return {ix.name for ix in Base.metadata.tables[table_name].indexes}

    assert {"ix_questions_status", "ix_questions_difficulty"} <= index_names("questions")
    assert "ix_knowledge_points_parent_id" in index_names("knowledge_points")
    assert {
        "ix_quiz_answers_user_id",
        "ix_quiz_answers_question_id",
        "ix_quiz_answers_answered_at",
    } <= index_names("quiz_answers")
    assert {
        "ix_review_items_user_id",
        "ix_review_items_scheduled_at",
        "ix_review_items_status",
    } <= index_names("review_items")
