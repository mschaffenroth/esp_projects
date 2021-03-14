DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
sudo docker run --rm -v $DIR/files:/usr/src/app/files/ esp_frame:latest
cp files/* $DIR/../webfacade/static_files/
