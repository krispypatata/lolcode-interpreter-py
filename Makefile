project:
	python3 lolcode.py

parser:
	python3 lolcode.py test1.lol

lex:
	python3 lolcode_lexer_driver.py test1.lol

test_lex:
	python3 lolcode_lexer_driver.py test_lex1.lol

t2:
	python3 lolcode_lexer_driver.py ../tests/10_functions.lol

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +