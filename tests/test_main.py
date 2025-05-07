def test_cli_lockfiles_help(conda_cli):
    conda_cli("lockfiles", "--help", raises=SystemExit)


def test_cli_lockfiles_from_env_help(conda_cli):
    conda_cli("lockfiles", "--help", raises=SystemExit)
