@echo "{{{COPYING IMAGES INTO FOLDER}}}"
python "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\scripts\copy_images.py"
@echo "================================"

@echo "{{{RUNNING PYTHON SCRIPTS}}}"
python "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\scripts\update_strava.py"
python "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\scripts\update_untappd.py"
@echo "================================"

@echo "{{{PUSHING DATA TO GITHUB}}}"
cd "C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io"
git add ".\data"
git add ".\images"
git commit -m "automatic data update..."
git push
@echo "================================"
@echo "{{{PROCESS COMPLETE}}}"