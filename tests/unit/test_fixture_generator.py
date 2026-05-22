"""Tests for deterministic questionnaire fixture generation."""

from __future__ import annotations

from dsw_document_template_tool.fixture_generator import generate_questionnaire_events


def test_generate_questionnaire_events_is_deterministic_and_path_aware() -> None:
    """Generated events should be stable and follow DSW questionnaire path rules."""

    questionnaire = _synthetic_questionnaire()

    first = generate_questionnaire_events(
        questionnaire,
        seed=20260522,
        case_index=2,
        max_events=50,
        max_items_per_list=2,
    )
    second = generate_questionnaire_events(
        questionnaire,
        seed=20260522,
        case_index=2,
        max_events=50,
        max_items_per_list=2,
    )

    assert first == second
    assert first.events
    assert first.events[0]["path"] == "chapter-1.q-options"
    assert first.events[0]["value"]["type"] == "AnswerReply"

    paths = [event["path"] for event in first.events]
    assert "chapter-1.q-options.answer-b.q-follow-up" in paths
    assert "chapter-1.q-list" in paths
    assert any(
        path.startswith("chapter-1.q-list.") and path.endswith(".q-list-value") for path in paths
    )

    list_event = next(event for event in first.events if event["path"] == "chapter-1.q-list")
    assert list_event["value"]["type"] == "ItemListReply"
    assert len(list_event["value"]["value"]) == 2


def test_generate_questionnaire_events_covers_different_option_answers_across_cases() -> None:
    """The fixed seed still varies branches by case index."""

    questionnaire = _synthetic_questionnaire()

    selected_answers = {
        generate_questionnaire_events(
            questionnaire,
            seed=20260522,
            case_index=case_index,
            max_events=50,
            max_items_per_list=1,
        ).events[0]["value"]["value"]
        for case_index in range(4)
    }

    assert selected_answers == {"answer-a", "answer-b"}


def _synthetic_questionnaire() -> dict[str, object]:
    return {
        "knowledgeModel": {
            "chapterUuids": ["chapter-1"],
            "entities": {
                "chapters": {
                    "chapter-1": {
                        "uuid": "chapter-1",
                        "questionUuids": ["q-options", "q-list", "q-multi"],
                    }
                },
                "questions": {
                    "q-options": {
                        "uuid": "q-options",
                        "title": "Choose a branch",
                        "questionType": "OptionsQuestion",
                        "answerUuids": ["answer-a", "answer-b"],
                    },
                    "q-follow-up": {
                        "uuid": "q-follow-up",
                        "title": "Explain the selected branch",
                        "questionType": "ValueQuestion",
                    },
                    "q-list": {
                        "uuid": "q-list",
                        "title": "Datasets",
                        "questionType": "ListQuestion",
                        "itemTemplateQuestionUuids": ["q-list-value"],
                    },
                    "q-list-value": {
                        "uuid": "q-list-value",
                        "title": "Dataset name",
                        "questionType": "ValueQuestion",
                    },
                    "q-multi": {
                        "uuid": "q-multi",
                        "title": "Methods",
                        "questionType": "MultiChoiceQuestion",
                        "choiceUuids": ["choice-a", "choice-b", "choice-c"],
                    },
                },
                "answers": {
                    "answer-a": {"uuid": "answer-a", "followUpUuids": []},
                    "answer-b": {"uuid": "answer-b", "followUpUuids": ["q-follow-up"]},
                },
            },
        }
    }
