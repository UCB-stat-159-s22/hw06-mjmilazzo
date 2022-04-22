# Make environment from scratch
.PHONY : env
env :
	chmod a+x make_scripts/envsetup.sh
	bash -ic make_scripts/envsetup.sh

# Remove environment
.PHONY : cleanenv
cleanenv :
	bash -ic 'make_scripts/envsetup.sh remove'

# Build the JupyterBook locally
.PHONY : html
html :
	chmod a+x make_scripts/bookgen.sh
	bash -ic make_scripts/bookgen.sh


# Build the JupyterBook with URL Hub proxy
.PHONY : html-hub
html-hub :
	pip install ghp-import
	ghp-import -n -p -f _build/html
	## TODO: edit to be specific for this (or confirm)
	
	#chmod a+x make_scripts/html-hub.sh
	#bash -ic make_scripts/html-hub.sh
	

# Clean everything
.PHONY : clean
clean :
	rm figures/*
	rm audio/*
	rm -rf _build
