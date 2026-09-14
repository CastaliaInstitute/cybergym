from cybergym.core import score_case


def test_score_requires_exact_expectations():
    case = {"expect": {"tools": ["log_review"]}}
    assert score_case(case, {"tools": ["log_review"]}) == (1.0, "all expectations met")
    assert score_case(case, {"tools": []})[0] == 0.0
