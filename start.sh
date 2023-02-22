if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Azanpopz/hagadmansa.git /hagadmansa
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /hagadmansa
fi
cd /hagadmansa
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
