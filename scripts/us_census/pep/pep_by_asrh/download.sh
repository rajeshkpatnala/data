#Loading file_urls.txt file
urls=$(<file_urls.txt)

#Creating Input Directory
mkdir -p "input_data"
cd "input_data"
for url in $urls;do
    echo "downloading $url"
    curl -sS -O $url >> /dev/null
    if [[ $url =~ ".zip" ]];
    then 
      unzip *.zip
      rm *.zip
    fi
done