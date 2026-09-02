# Movie Brain — Architecture

Movie Brain is a small Flask web application for managing a personal movie library and selecting movies to watch.

## Application Structure

```text
User
 │
 ▼
HTML / CSS
 │
 ▼
Flask (`app.py`)
 │
 ├── Search & Filters
 ├── Movie Management
 ├── Random Picker
 └── Series Logic
 │
 ▼
`movies.csv`
```

### Main Components

**`app.py`**
Contains the Flask application, routes, movie logic, filtering and CSV handling.

**`templates/`**
Contains the HTML pages used by the application.

**`static/style.css`**
Contains the application's styling.

**`movies.csv`**
Stores the movie library and acts as the current persistence layer.

**`main.py`**
Starts the Flask application when the project is packaged for Android.

**`buildozer.spec`**
Contains the configuration required to build the Android APK.

## Data Flow

Movie data is loaded from the CSV into Python when required. Changes such as adding, editing, deleting or marking a movie as watched are then written back to the CSV.

The random picker first applies the availability and filtering rules before selecting a movie.

## Android

The Android version uses the same Flask application packaged with Buildozer and python-for-android. This allows the web interface and application logic to be reused rather than creating a separate mobile application.
