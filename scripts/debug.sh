PLATFORM=linux/amd64
TAG=besartshyti/workshop-debug
PATH_APP=src
FILE=$PATH_APP/Dockerfile.debug


docker buildx build    \
  --platform $PLATFORM \
  --tag $TAG           \
  --file $FILE         \
  --push $PATH_APP
