#specifies the shell interpreter to be used for executing commands
SHELL := /bin/bash

#add a credential step when implementing in github pipelines
build-terraform:
	//print a message indicating the start of the build process
	@echo "Building Terraform configuration..."
	
	//remove any existing terraform.zip file in the build directory, ignoring errors if the file does not exist
	@rm $build/terraform.zip || exit 0
	//create the build/terraform directory if it does not exist
	@mkdir -p $build/terraform
	//copy the aws directory to the build/terraform directory
	@cp -r aws $build/terraform/
	//export the poetry dependencies to a requirements.txt file without hashes
	poetry export -f requirements.txt --without-hashes -o $build/terraform/requirements.txt
	//install the dependencies listed in requirements.txt to the build/terraform directory
	poetry run pip install -r $build/terraform/requirements.txt -t $build/terraform/
	//change to the build/terraform directory and create a zip file of its contents, excluding certain files and directories
	cd $build/terraform && zip -r ../terraform.zip * --exclude ".gitignore" "*__pycache__/*" "*tests/" 
	//remove the build/terraform directory to clean up
	rm -rf $build/terraform

	//once zip is made in build folder we do terraform init and plan to deploy it to aws

	//then remove the zip file to clean up
	@rm $build/terraform.zip
	@echo "built terraform.zip in $(build) directory"