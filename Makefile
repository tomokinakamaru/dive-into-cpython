.PHONY: setup
setup: \
	cpython/.vscode/c_cpp_properties.json \
	cpython/.vscode/settings.json \
	astdump

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

build.json: build.log build.json.py
	python3 build.json.py > build.json || build.json

c_cpp_properties.json: build.json c_cpp_properties.json.py
	python3 c_cpp_properties.json.py > c_cpp_properties.json || rm c_cpp_properties.json

settings.json: build.json settings.json.py
	python3 settings.json.py > settings.json || rm settings.json

cpython/.vscode:
	mkdir cpython/.vscode

cpython/.vscode/c_cpp_properties.json: c_cpp_properties.json | cpython/.vscode
	cd cpython/.vscode && ln -sf ../../c_cpp_properties.json

cpython/.vscode/settings.json: settings.json | cpython/.vscode
	cd cpython/.vscode && ln -sf ../../settings.json

astdump.sh: build.json astdump.sh.py
	python3 astdump.sh.py > astdump.sh || rm astdump.sh

astdump: astdump.sh
	sh astdump.sh || rm -rf astdump
