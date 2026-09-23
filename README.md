# Body Tracker

Diet + workout tracker for recomp / athletic performance. Static app ready for **GitHub Pages**.

## What's included

- `index.html` — app UI (diet modals, workout days A/B/C, IndexedDB logging)
- `data/app.db` — SQLite data loaded in-browser via [sql.js](https://sql.js.org/)
- `foods.json`, `workouts.json`, `workouttooltip.json` — editable source data
- `img/gobletsquat.png` — exercise image
- `scripts/build_db.py` — rebuilds `data/app.db` from the JSON files

## Edit data

1. Change `foods.json`, `workouts.json`, and/or `workouttooltip.json`.
2. Rebuild the database:

```bash
python scripts/build_db.py
```

3. Commit the JSON files **and** `data/app.db`, then push.

The live site prefers `data/app.db`. If the DB fails to load, it falls back to the JSON files.

## Enable GitHub Pages

1. Push this repo to GitHub (e.g. `kennyboreham-create/body-tracker`).
2. Repo **Settings** → **Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Branch: **main**, folder: **/ (root)** → **Save**.
5. After a minute or two, open `https://kennyboreham-create.github.io/body-tracker/`.

## Local preview

Serve the folder over HTTP (not `file://`) so fetch/sql.js work, e.g.:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

Diet/workout logs stay in your browser (IndexedDB); they are not stored in the GitHub repo.
