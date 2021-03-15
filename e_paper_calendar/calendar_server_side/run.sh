DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
sudo docker run --rm -e TZ="Europe/Berlin" -v $DIR/files:/usr/src/app/files/ esp_frame:latest
cp $DIR/files/* $DIR/../../../webfacade/static_files/
