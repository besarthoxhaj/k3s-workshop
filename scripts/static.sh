PLATFORM=linux/amd64
TAG=besartshyti/workshop-static
PATH_APP=src
FILE=$PATH_APP/Dockerfile.static


docker buildx build    \
  --platform $PLATFORM \
  --tag $TAG           \
  --file $FILE         \
  --push $PATH_APP
