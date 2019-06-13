# Build a deployment package
$ sam build

# Run the build process inside an AWS Lambda-like Docker container
$ sam build --use-container

# Build and run your functions locally
$ sam build && sam local invoke
  
# Build and package for deployment
$ sam build && sam package --s3-bucket venafi-tpp-websdk-lambda-function-store
