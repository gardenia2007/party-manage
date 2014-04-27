
# mv .git /tmp/git_tmp

rm *.pyc
rm *.wsgic
rm controllers/*.pyc

echo "start deploy..."

saecloud deploy

echo "deploy end."

# mv /tmp/git_tmp .git

