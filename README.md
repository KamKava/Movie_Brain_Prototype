# Movie Brain

Movie Brain is a personal movie library and random movie picker built with Python and Flask.

The application allows movies to be stored, searched, filtered, edited and deleted, while also providing a random movie picker for deciding what to watch.

The project was developed as a small full-stack application and later packaged as an Android APK.

## Features

* Add movies to a personal movie library
* Edit existing movie information
* Delete movies
* Mark movies as watched
* Search movies by:

  * Title
  * Series
  * Director
* Filter movies by:

  * Genre
  * Series
  * Mood
  * Year
  * Runtime
  * Ownership
  * Watched status
  * "So bad it's good"
* Random movie picker
* Prevent the same movie being repeatedly selected during a picker session
* Series-order logic to prevent later films being suggested before earlier films have been watched
* Persistent movie data stored in CSV
* Responsive dark-themed web interface
* Android APK packaging using Buildozer

## How the Movie Picker Works

The random picker does more than simply choose a random row from the CSV file.

Movies that have already been watched are excluded, and movies in a series are checked against their viewing order.

For example:

```text
The Lord of the Rings 1 — watched
The Lord of the Rings 2 — available
The Lord of the Rings 3 — unavailable
```

Once the second film is watched, the third film becomes available.

The picker also keeps track of movies already selected during the current session, reducing repeated suggestions.

## Technology

* **Python** — application logic and data handling
* **Flask** — web application framework
* **HTML** — page structure and forms
* **CSS** — styling and responsive layout
* **CSV** — persistent movie data
* **Buildozer** — Android packaging
* **python-for-android** — Android application build system
* **Git / GitHub** — version control and project hosting

## Project Structure

```text
Movie_Brain_Prototype/
│
├── app.py
├── main.py
├── movies.csv
├── buildozer.spec
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    └── update.html
```

### Main Files

**`app.py`**

Contains the Flask application, routes, movie filtering, random selection, series-order logic and CSV handling.

**`main.py`**

Entry point used when packaging the Flask application for Android.

**`movies.csv`**

Stores the movie library and its associated information.

**`templates/`**

Contains the HTML templates used by Flask.

**`static/style.css`**

Contains the application's styling.

**`buildozer.spec`**

Contains the configuration used to package the application as an Android APK.

## Running Locally

Clone the repository and move into the project directory:

```bash
git clone https://github.com/KamKava/Movie_Brain_Prototype.git
cd Movie_Brain_Prototype
```

Create and activate a virtual environment:

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

Install Flask:

```powershell
pip install flask
```

Run the application:

```powershell
python app.py
```

The application will be available locally at:

```text
http://127.0.0.1:5000
```

## Android Packaging

The application can also be packaged as an Android APK using Buildozer.

The Android build uses Flask's web interface inside a Python-for-Android WebView bootstrap.

The project includes the HTML templates, CSS and CSV data required by the application through the Buildozer configuration.

The Android entry point is:

```text
main.py
```

The current Android build configuration targets:

```text
arm64-v8a
```

## Data Storage

Movie data is currently stored in a CSV file rather than a database.

This keeps the project lightweight and easy to inspect or modify manually.

The CSV contains fields including:

```text
movie_id
title
series
series_order
director
genre
year
own_it
runtime
mood
watched
so_bad_its_good
```

## Current Limitations

* Movie data is stored in CSV rather than a database.
* There is currently no user authentication.
* The application is designed primarily for personal use.
* The Android package is currently a debug build.
* The application does not currently use an external movie database or API.
* There is no AI recommendation system yet.

## Future Improvements

Possible future improvements include:

* Migrating movie storage from CSV to SQLite or PostgreSQL
* Adding an external movie database API for automatically retrieving movie information
* Improving recommendations based on viewing history and preferences
* Adding richer movie metadata such as posters, cast and descriptions
* Improving the Android experience
* Creating a more structured backend API

## Project Status

Movie Brain is a functional personal project and is currently being maintained as a portfolio/development project.

The application began as a simple movie-picker idea and evolved into a Flask application with persistent data, filtering, series logic and Android packaging.
