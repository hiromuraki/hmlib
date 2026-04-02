from __future__ import annotations

from hmpy.hello import Hello


def test_hello_say_hello_prints_exact_message(capsys) -> None:
    Hello("tester").say_hello()

    assert capsys.readouterr().out == "Hello, tester!\n"