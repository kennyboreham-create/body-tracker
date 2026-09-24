# Body Tracker

Diet + workout tracker for recomp / athletic performance. Static app ready for **GitHub Pages**.

## What's included

- `index.html` — app UI (diet modals, workout days A/B/C, IndexedDB logging)
- `foods.json`, `workouts.json`, `workouttooltip.json` — catalog data loaded by the site
- `img/gobletsquat.png` — exercise image
- `data/app.db` and `scripts/build_db.py` — optional SQLite snapshot; the Pages app does not read them

## Edit data

1. Change `foods.json`, `workouts.json`, and/or `workouttooltip.json`.
2. Commit the JSON files and push.

The live site always loads those JSON files for foods, workouts, and optional exercise tips.

## Enable GitHub Pages

1. Push this repo to GitHub (e.g. `kennyboreham-create/body-tracker`).
2. Repo **Settings** → **Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Branch: **main**, folder: **/ (root)** → **Save**.
5. After a minute or two, open `https://kennyboreham-create.github.io/body-tracker/`.

## Local preview

Serve the folder over HTTP (not `file://`) so fetch of the JSON catalogs works, e.g.:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

Diet/workout logs stay in your browser (IndexedDB); they are not stored in the GitHub repo.
