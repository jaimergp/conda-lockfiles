def test_cli_help(conda_cli):
    conda_cli("lockfiles", "--help", raises=SystemExit)
