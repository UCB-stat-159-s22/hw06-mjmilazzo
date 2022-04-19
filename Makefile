# Make environment from scratch
.PHONY : env
env :
	bash -ic scripts/envsetup.sh

# Remove environment
.PHONY : cleanenv
cleanenv :
	bash -ic 'scripts/envsetup.sh remove'
