from src.schemas.evidence import CodeEvidence


def test_code_evidence_creation():
    evidence = CodeEvidence(
        syntax_valid=True,
        ast_tree=None,
        syntax_error=None,
        static_issues=[],
    )

    assert evidence.syntax_valid is True
    assert evidence.syntax_error is None
    assert evidence.static_issues == []