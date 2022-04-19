# Make environment from scratch
.PHONY : env
env :
	bash -ic make_scripts/envsetup.sh

# Remove environment
.PHONY : cleanenv
cleanenv :
	bash -ic 'make_scripts/envsetup.sh remove'

# Build the JupyterBook normally
.PHONY : html
html :
	jupyterbook build .

# Build the JupyterBook with URL Hub proxy
.PHONY : html-hub
html-hub :
	## TODO: edit to be specific for this (or confirm)
	jupyter-book config sphinx .
	sphinx-build  . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
	python -m http.server

# Clean everything
.PHONY : clean
clean :
	rm -rf figures/*
	rm -rf audio/*
	rm -rf _build/*
