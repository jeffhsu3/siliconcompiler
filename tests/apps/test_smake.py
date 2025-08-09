import pytest
import os

from siliconcompiler.apps import smake


@pytest.mark.parametrize('target', ('asic', 'lint'))
def test_smake(target, monkeypatch, capfd, datadir):
    '''Test smake'''

    monkeypatch.setattr('sys.argv', [
        'smake', '-C', datadir, target])
    assert smake.main() == 0
    assert f"{target.upper()} MAKE" in capfd.readouterr().out


def test_smake_default(monkeypatch, capfd, datadir):
    '''Test smake'''

    monkeypatch.setattr('sys.argv', [
        'smake', '-C', datadir])
    assert smake.main() == 0
    assert "LINT MAKE" in capfd.readouterr().out


def test_smake_default_missing(monkeypatch, capfd):
    '''Test smake'''

    monkeypatch.setattr('sys.argv', ['smake'])
    assert smake.main() == 1
    assert "Error: Unable to load makefile 'make.py'" in capfd.readouterr().out


def test_smake_default_dir_missing(monkeypatch, capfd):
    '''Test smake'''

    monkeypatch.setattr('sys.argv', ['smake', '-C', 'testdir'])
    assert smake.main() == 1
    assert "Unable to change directory to testdir" in capfd.readouterr().out


@pytest.mark.parametrize('target', ('target0', 'target1'))
def test_smake_with_argument(target, monkeypatch, capfd, datadir):
    '''Test smake'''

    monkeypatch.setattr('sys.argv', [
        'smake', '-C', datadir, 'has_arg', '--target', target])
    assert smake.main() == 0
    assert f"target {target}" in capfd.readouterr().out


@pytest.mark.parametrize('target', ('target0', 'target1'))
def test_smake_with_argument2(target, monkeypatch, capfd, datadir):
    '''Test smake'''

    monkeypatch.setattr('sys.argv', [
        'smake', '-C', datadir, 'has_arg2', '--target', target, '--count', '5'])
    assert smake.main() == 0
    assert f"target {target} 5" in capfd.readouterr().out


def test_smake_help(monkeypatch, capfd, datadir):
    '''Test smake'''

    monkeypatch.setattr('sys.argv', ['smake', '-C', datadir, '-h'])
    with pytest.raises(SystemExit):
        assert smake.main() == 0
    output = capfd.readouterr()
    assert "LOOK FOR THIS TEXT IN HELP" in output.out
    assert "lint" in output.out
    assert "asic" in output.out
    assert "LINT HELP" in output.out


def test_smake_file(monkeypatch, capfd, datadir):
    '''Test smake with -f'''

    monkeypatch.setattr('sys.argv', [
        'smake', '-C', datadir, '-f', 'make_other.py', 'asic'])
    assert smake.main() == 0
    assert "ASIC OTHER" in capfd.readouterr().out


def test_smake_file_with_import(monkeypatch, capfd, datadir):
    '''Test smake with -f'''

    monkeypatch.setattr('sys.argv', [
        'smake', '-C', datadir, '-f', 'make_with_import.py', 'asic_here'])
    assert smake.main() == 0
    output = capfd.readouterr()
    assert "ASIC MAKE" in output.out
    assert "ASIC IMPORT" in output.out


def test_smake_file_decorated(monkeypatch, capfd, datadir):
    '''Test smake with -f'''

    exec_file = os.path.join(datadir, 'make_decorated.py')
    monkeypatch.setattr('sys.argv', [exec_file, 'asic'])
    assert smake.main(exec_file) == 0
    output = capfd.readouterr()
    assert "ASIC MAKE DECORATED" in output.out
