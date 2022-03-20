git pull origin master
 case "$OSTYPE" in
   msys*)    venv/Scripts/pip-sync ;;
   cygwin*)  venv/Scripts/pip-sync ;;
   *) venv/bin/pip-sync ;;
 esac