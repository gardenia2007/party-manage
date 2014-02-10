
mv .git /tmp/git_tmp

echo "start deploy..."

saecloud deploy

echo "deploy end."

mv /tmp/git_tmp .git

