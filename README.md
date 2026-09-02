# Movie Brain

A personal movie library and random movie picker built with **Python and Flask**.

![Movie Brain main interface](docs/images/image_1.png)

![Random movie choice](docs/images/image_2.png)

Movie Brain lets me manage my movie collection, search and filter it, and randomly select something to watch. It allows me manage my movie collection and optimizes my choice process.


## Features

* Add, edit and delete movies
* Mark movies as watched
* Search by title, series and director
* Filter by genre, series, mood, year, runtime and other attributes
* Random movie picker
* Prevent repeated picks during a picker session
* Series-order logic for movies watched in sequence
* CSV-based data storage
* Responsive dark-themed interface
* Android APK packaging

## Technology

* Python
* Flask
* HTML / CSS
* CSV
* Buildozer
* python-for-android
* Git / GitHub

## Running Locally

Clone the repository:

```bash
git clone https://github.com/KamKava/Movie_Brain_Prototype.git
cd Movie_Brain_Prototype
```

Create a virtual environment and install Flask:

```powershell
python -m venv venv
venv\Scripts\activate
pip install flask
```

Run the application:

```powershell
python app.py
```

The application will be available in your browser at:

```text
http://127.0.0.1:5000
```

## Documentation

More information about the project is available in the `docs/` folder:

* [Architecture](docs/architecture.md)
* [Data Design](docs/database-design.md)
* [Testing](docs/testing.md)

## Project Status

Movie Brain is a functional personal project developed as a portfolio project.

The current version uses CSV storage and has been packaged and tested as an Android APK.
