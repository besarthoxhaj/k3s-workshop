PLATFORM=linux/amd64
TAG=besartshyti/workshop-predictor
PATH_APP=src
FILE=$PATH_APP/Dockerfile.predictor


docker buildx build    \
  --platform $PLATFORM \
  --tag $TAG           \
  --file $FILE         \
  --push $PATH_APP
