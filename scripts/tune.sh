PLATFORM=linux/amd64
TAG=besartshyti/workshop-tune
PATH_APP=src
FILE=$PATH_APP/Dockerfile.tune


docker buildx build    \
  --platform $PLATFORM \
  --tag $TAG           \
  --file $FILE         \
  --push $PATH_APP
