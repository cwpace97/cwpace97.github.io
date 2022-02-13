@REM run python scripts
python "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\scripts\update_strava.py"
python "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\scripts\update_robinhood.py"
python "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\scripts\update_untappd.py"

@REM push data to github
cd "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io"
git add ".\data"
git commit -m "automatic data update..."
git push