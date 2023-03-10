if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Azanpopz/meemi.git /meemi
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /meemi
fi
cd /meemi
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
