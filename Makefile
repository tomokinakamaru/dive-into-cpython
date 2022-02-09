.PHONY: all
all: cpython.ast cpython.min/.vscode/c_cpp_properties.json

.PHONY: pull
pull:
	git -C cpython pull

.PHONY: clean
clean:
	rm -rf cpython* tmp

cpython/.git/refs/heads/main:
	git clone --depth 1 https://github.com/python/cpython $(SRC)

cpython.min: tmp/minify.sh
	sh tmp/minify.sh cpython cpython.min

cpython.ast: tmp/astdump.sh
	sh tmp/astdump.sh cpython cpython.ast

cpython/.vscode/c_cpp_properties.json: tmp/log.json create-vscode-setting.py
	mkdir -p cpython/.vscode
	python3 create-vscode-setting.py cpython < tmp/log.json > cpython/.vscode/c_cpp_properties.json || rm cpython/.vscode/c_cpp_properties.json

cpython.min/.vscode/c_cpp_properties.json: cpython.min cpython/.vscode/c_cpp_properties.json
	mkdir -p cpython.min/.vscode
	cp cpython/.vscode/c_cpp_properties.json cpython.min/.vscode/c_cpp_properties.json

tmp:
	mkdir tmp

tmp/log.txt: cpython/.git/refs/heads/main | tmp
	git -C cpython clean -dfX .
	cd cpython && ./configure
	make -C cpython EXTRA_CFLAGS=-H 2>&1 | tee tmp/log.txt || rm tmp/log.txt

tmp/log.json: tmp/log.txt analyze-log.py
	python3 analyze-log.py cpython < tmp/log.txt > tmp/log.json || rm tmp/log.json

tmp/minify.sh: tmp/log.json create-minify-script.py
	python3 create-minify-script.py < tmp/log.json > tmp/minify.sh || rm tmp/minify.sh

tmp/astdump.sh: tmp/log.json create-astdump-script.py
	python3 create-astdump-script.py < tmp/log.json > tmp/astdump.sh || rm tmp/astdump.sh
