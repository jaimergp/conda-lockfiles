def test_cli_lockfiles_help(conda_cli):
    _, _, exception = conda_cli("lockfiles", "--help", raises=SystemExit)
    assert exception.value.code == 0


def test_cli_lockfiles_create_help(conda_cli):
    conda_cli("lockfiles", "create", "--help", raises=SystemExit)
    _, _, exception = conda_cli("lockfiles", "create", "--help", raises=SystemExit)
    assert exception.value.code == 0


def test_cli_lockfiles_export_help(conda_cli):
    _, _, exception = conda_cli("lockfiles", "export", "--help", raises=SystemExit)
    assert exception.value.code == 0
