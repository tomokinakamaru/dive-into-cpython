.PHONY: setup
setup: \
	cpython/.astdump \
	cpython/.vscode/c_cpp_properties.json \
	cpython/.vscode/settings.json \

.PHONY: clean
clean:
	git clean -dfX .
	rm -rf cpython

.PHONY: update
update: cpython/.git/refs/heads/main
	git -C cpython pull

cpython/.git/refs/heads/main:
	git clone --depth 1 https://github.com/python/cpython

build.log: cpython/.git/refs/heads/main
	git -C cpython clean -dfX .
	cd cpython && ./configure
	make -C cpython | tee build.log || rm build.log

build.json: build.log generate-build.json.py
	python3 generate-build.json.py < build.log > build.json || rm build.json

astdump.sh: build.json generate-astdump.sh.py
	python3 generate-astdump.sh.py < build.json > astdump.sh || rm astdump.sh

cpython/.astdump: astdump.sh
	sh astdump.sh || rm -rf cpython/.astdump

cpython/.vscode: cpython/.git/refs/heads/main
	mkdir cpython/.vscode

cpython/.vscode/c_cpp_properties.json: build.json generate-c_cpp_properties.json.py | cpython/.vscode
	python3 generate-c_cpp_properties.json.py < build.json > cpython/.vscode/c_cpp_properties.json

cpython/.vscode/settings.json: build.json generate-settings.json.py | cpython/.vscode
	python3 generate-settings.json.py < build.json > cpython/.vscode/settings.json
