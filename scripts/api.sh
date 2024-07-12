PLATFORM=linux/amd64
TAG=besartshyti/workshop-api
PATH_APP=src
FILE=$PATH_APP/Dockerfile.api


docker buildx build    \
  --platform $PLATFORM \
  --tag $TAG           \
  --file $FILE         \
  --push $PATH_APP
