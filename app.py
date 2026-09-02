from flask import Flask, render_template, request, redirect, url_for

import csv
import os
import random
app = Flask(__name__)

CSV_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "movies.csv"
)

print("CSV location:", os.path.abspath(CSV_FILE))
print("File exists:", os.path.exists(CSV_FILE))
print("Can write:", os.access(CSV_FILE, os.W_OK))

# ============================================================
# LOAD MOVIES
# ============================================================

def load_movies():

    movies = []

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            movie = dict(row)

            # Make sure these fields exist
            movie.setdefault("series", "")
            movie.setdefault("series_order", "")
            movie.setdefault("director", "")

            # Clean text fields
            text_columns = [
                "title",
                "series",
                "director",
                "genre",
                "own_it",
                "mood",
                "watched",
                "so_bad_its_good"
            ]

            for column in text_columns:

                movie[column] = str(
                    movie.get(column, "")
                ).strip()

            # Normalize Genre and Mood capitalization
            movie["genre"] = (
                movie["genre"].title()
                if movie["genre"]
                else ""
            )

            movie["mood"] = (
                movie["mood"].title()
                if movie["mood"]
                else ""
            )

            # Numeric fields
            for column in [
                "movie_id",
                "runtime",
                "year",
                "series_order"
            ]:

                value = movie.get(
                    column,
                    ""
                ).strip()

                if value == "":
                    movie[column] = None
                    continue

                try:

                    number = float(value)

                    if number.is_integer():
                        movie[column] = int(number)
                    else:
                        movie[column] = number

                except ValueError:

                    movie[column] = None

            movies.append(movie)

    return movies

movies = load_movies()

def save_movies(movies):
    fieldnames = [
        "movie_id",
        "title",
        "series",
        "series_order",
        "director",
        "genre",
        "year",
        "own_it",
        "runtime",
        "mood",
        "watched",
        "so_bad_its_good"
    ]

    with open(CSV_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for movie in movies:
            writer.writerow({
                field: movie.get(field, "")
                for field in fieldnames
            })


# ============================================================
# MOVIES PICKED DURING CURRENT APP SESSION
# ============================================================

picked_movie_ids = set()


# ============================================================
# SERIES LOGIC
# ============================================================

def series_movie_is_available(movie, movies):

    """
    A standalone movie is available if it is unwatched.

    A series movie is available only when all earlier
    movies in that series have been watched.
    """

    series_name = str(movie.get("series", "")).strip()

    # Standalone movie
    if not series_name:
        return True

    # Need a series order
    current_order = movie.get("series_order")

    if current_order is None:
        return True

    # Find earlier movies in the same series
    for earlier_movie in movies:

        if (
            str(earlier_movie.get("series", "")).strip()
            == series_name
            and earlier_movie.get("series_order") is not None
            and earlier_movie.get("series_order") < current_order
        ):

            if str(
                earlier_movie.get("watched", "")
            ).lower() != "yes":

                return False

    return True


def get_series_available_movies(movies):

    available_movies = []

    for movie in movies:

        # Already watched
        if str(
            movie.get("watched", "")
        ).lower() == "yes":

            continue

        if series_movie_is_available(
            movie,
            movies
        ):

            available_movies.append(movie)

    return available_movies


# ============================================================
# FILTERS
# ============================================================

def apply_filters(movies):

    filtered = list(movies)

    genre = request.args.get(
        "genre",
        ""
    )

    series = request.args.get(
        "series",
        ""
    )

    mood = request.args.get(
        "mood",
        ""
    )

    year = request.args.get(
        "year",
        ""
    )

    runtime = request.args.get(
        "runtime",
        ""
    )

    own_it = request.args.get(
        "own_it",
        ""
    )

    watched = request.args.get(
        "watched",
        ""
    )

    so_bad = request.args.get(
        "so_bad_its_good",
        ""
    )


    # --------------------------------------------------------
    # GENRE
    # --------------------------------------------------------

    if genre:

        filtered = [
            movie for movie in filtered
            if movie.get("genre", "") == genre
        ]


    # --------------------------------------------------------
    # SERIES
    # --------------------------------------------------------

    if series:

        filtered = [
            movie for movie in filtered
            if movie.get("series", "") == series
        ]


    # --------------------------------------------------------
    # MOOD
    # --------------------------------------------------------

    if mood:

        filtered = [
            movie for movie in filtered
            if movie.get("mood", "") == mood
        ]


    # --------------------------------------------------------
    # YEAR
    # --------------------------------------------------------

    if year:

        filtered = [
            movie for movie in filtered
            if str(movie.get("year", "")) == year
        ]


    # --------------------------------------------------------
    # RUNTIME
    # --------------------------------------------------------

    if runtime == "quick":

        filtered = [
            movie for movie in filtered
            if movie.get("runtime") is not None
            and movie["runtime"] < 50
        ]

    elif runtime == "short":

        filtered = [
            movie for movie in filtered
            if movie.get("runtime") is not None
            and movie["runtime"] < 90
        ]

    elif runtime == "long":

        filtered = [
            movie for movie in filtered
            if movie.get("runtime") is not None
            and 90 <= movie["runtime"] <= 120
        ]

    elif runtime == "mega":

        filtered = [
            movie for movie in filtered
            if movie.get("runtime") is not None
            and movie["runtime"] > 120
        ]


    # --------------------------------------------------------
    # OWN IT
    # --------------------------------------------------------

    if own_it:

        filtered = [
            movie for movie in filtered
            if str(
                movie.get("own_it", "")
            ).lower() == own_it
        ]


    # --------------------------------------------------------
    # WATCHED
    # --------------------------------------------------------

    if watched:

        filtered = [
            movie for movie in filtered
            if str(
                movie.get("watched", "")
            ).lower() == watched
        ]


    # --------------------------------------------------------
    # SO BAD IT'S GOOD
    # --------------------------------------------------------

    if so_bad:

        filtered = [
            movie for movie in filtered
            if str(
                movie.get("so_bad_its_good", "")
            ).lower() == so_bad
        ]


    return filtered


# ============================================================
# FILTER VALUES
# ============================================================

def get_filter_values(movies):

    # --------------------------------------------------------
    # GENRES
    # --------------------------------------------------------

    genres = set()

    for movie in movies:

        value = movie.get("genre", "")

        if value:

            for genre in str(value).split(","):

                genre = genre.strip()

                if genre:
                    genres.add(genre)

    genres = sorted(genres)


    # --------------------------------------------------------
    # MOODS
    # --------------------------------------------------------

    moods = set()

    for movie in movies:

        value = movie.get("mood", "")

        if value:

            for mood in str(value).split(","):

                mood = mood.strip()

                if mood:
                    moods.add(mood)

    moods = sorted(moods)


    # --------------------------------------------------------
    # YEARS
    # --------------------------------------------------------

    years = sorted(
        {
            movie["year"]
            for movie in movies
            if movie.get("year") is not None
        },
        reverse=True
    )


    # --------------------------------------------------------
    # SERIES
    # --------------------------------------------------------

    series = sorted(
        {
            movie["series"]
            for movie in movies
            if movie.get("series", "")
        }
    )


    return genres, moods, years, series




# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    global movies

    search = request.args.get("search", "").strip()

    
    movies = load_movies()

    search_results = []

    if search:
        search_lower = search.lower()

        search_results = [
            movie for movie in movies
            if (
                search_lower in movie.get("title", "").lower()
                or search_lower in movie.get("series", "").lower()
                or search_lower in movie.get("director", "").lower()
            )
        ]

    filtered = apply_filters(movies)

    # Only movies currently available to watch
    available = get_series_available_movies(
        filtered
    )

    # Don't show movies already picked during this session
    available_for_picker = [
        movie for movie in available
        if movie.get("movie_id") not in picked_movie_ids
    ]
        # Get values for the filter menus
    genres, moods, years, series = get_filter_values(
        movies
    )

    # Get currently selected filters
    filters = {
        "genre": request.args.get("genre", ""),
        "series": request.args.get("series", ""),
        "mood": request.args.get("mood", ""),
        "year": request.args.get("year", ""),
        "runtime": request.args.get("runtime", ""),
        "own_it": request.args.get("own_it", ""),
        "watched": request.args.get("watched", ""),
        "so_bad_its_good": request.args.get(
            "so_bad_its_good",
            ""
        )
    }

    # --------------------------------------------------------
    # RANDOM PICK
    # --------------------------------------------------------

    winner = None

    if request.args.get("pick") == "1":

        # If everything has already been picked this session,
        # start a fresh cycle.
        if len(available_for_picker) == 0:

            picked_movie_ids.clear()

            available_for_picker = list(
                available
            )

        if len(available_for_picker) > 0:

            winner = random.choice(
                available_for_picker
            )

            picked_movie_ids.add(
                winner["movie_id"]
            )

    # --------------------------------------------------------
    # MOVIES NOT OWNED
    # --------------------------------------------------------

    not_owned = [
        movie for movie in movies
        if str(movie.get("own_it", "")).lower() == "no"
    ]

        # -------------------------------------------------------- 
    # WATCHED MOVIES 
    # -------------------------------------------------------- 
 
    watched_movies = [ 
        movie for movie in movies 
        if str(movie.get("watched", "")).lower() == "yes" 
    ]

    # --------------------------------------------------------
    # MESSAGE
    # --------------------------------------------------------

    message = request.args.get(
        "message",
        ""
    )

    # --------------------------------------------------------
    # DISPLAY PAGE
    # --------------------------------------------------------

    return render_template(
    "index.html",
    total_movies=len(movies),
    available=available,
    available_count=len(available),
    not_owned=not_owned,
    watched_movies=watched_movies,
    genres=genres,
    moods=moods,
    years=years,
    series=series,
    filters=filters,
    winner=winner,
    message=message,
    search=search,
    search_results=search_results
)

# ============================================================
# ADD NEW MOVIE
# ============================================================

@app.route(
    "/add_movie",
    methods=["POST"]
)
def add_movie():

    global movies


    movies = load_movies()

    # --------------------------------------------------------
    # GET FORM VALUES
    # --------------------------------------------------------

    title = request.form.get(
        "title",
        ""
    ).strip()

    if not title:

        return redirect(
            url_for(
                "home",
                message="Please enter a movie title."
            )
        )

    series_name = request.form.get(
        "series",
        ""
    ).strip()

    series_order = request.form.get(
        "series_order",
        ""
    ).strip()

    genre = request.form.get(
        "genre",
        ""
    ).strip()

    year = request.form.get(
        "year",
        ""
    ).strip()

    own_it = request.form.get(
        "own_it",
        "no"
    ).strip().lower()

    runtime = request.form.get(
        "runtime",
        ""
    ).strip()

    mood = request.form.get(
        "mood",
        ""
    ).strip()

    watched = request.form.get(
        "watched",
        "no"
    ).strip().lower()

    so_bad = request.form.get(
        "so_bad_its_good",
        "no"
    ).strip().lower()

    # --------------------------------------------------------
    # CREATE NEW MOVIE ID
    # --------------------------------------------------------

    if len(movies) == 0:

        new_id = 1

    else:

        existing_ids = [
            movie.get("movie_id")
            for movie in movies
            if movie.get("movie_id") is not None
        ]

        new_id = (
            max(existing_ids) + 1
            if existing_ids
            else 1
        )

    # --------------------------------------------------------
    # CONVERT NUMBERS
    # --------------------------------------------------------

    try:

        year_value = (
            int(year)
            if year
            else None
        )

    except ValueError:

        year_value = None


    try:

        runtime_value = (
            int(runtime)
            if runtime
            else None
        )

    except ValueError:

        runtime_value = None


    try:

        series_order_value = (
            float(series_order)
            if series_order
            else None
        )

    except ValueError:

        series_order_value = None

    # --------------------------------------------------------
    # CREATE NEW MOVIE
    # --------------------------------------------------------

    new_movie = {

        "movie_id": new_id,

        "title": title,

        "series": series_name,

        "series_order": series_order_value,

        "director": "",

        "genre": genre,

        "year": year_value,

        "own_it": own_it,

        "runtime": runtime_value,

        "mood": mood,

        "watched": watched,

        "so_bad_its_good": so_bad

    }

    # Add to current movie list
    movies.append(
        new_movie
    )

    # Save to CSV
    fieldnames = [
        "movie_id",
        "title",
        "series",
        "series_order",
        "director",
        "genre",
        "year",
        "own_it",
        "runtime",
        "mood",
        "watched",
        "so_bad_its_good"
    ]

    with open(
        CSV_FILE,
        "a",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writerow(
            new_movie
        )

    return redirect(
        url_for(
            "home",
            message=f"Movie added! ID #{new_id}"
        )
    )
    
 
 
 
# ============================================================
# UPDATE MOVIE
# ============================================================

@app.route(
    "/update_movie/<int:movie_id>",
    methods=["GET", "POST"]
)
def update_movie(movie_id):

    global movies

    movies = load_movies()

    # Find movie
    movie = next(
        (
            movie for movie in movies
            if movie.get("movie_id") == movie_id
        ),
        None
    )

    if movie is None:

        return redirect(
            url_for(
                "home",
                message="Movie not found."
            )
        )

    if request.method == "POST":

        # ----------------------------------------------------
        # GET UPDATED VALUES
        # ----------------------------------------------------

        movie["title"] = request.form.get(
            "title",
            ""
        ).strip()

        movie["series"] = request.form.get(
            "series",
            ""
        ).strip()

        series_order = request.form.get(
            "series_order",
            ""
        ).strip()

        try:

            movie["series_order"] = (
                float(series_order)
                if series_order
                else None
            )

        except ValueError:

            movie["series_order"] = None

        movie["genre"] = request.form.get(
            "genre",
            ""
        ).strip()

        year = request.form.get(
            "year",
            ""
        ).strip()

        try:

            movie["year"] = (
                int(year)
                if year
                else None
            )

        except ValueError:

            movie["year"] = None

        runtime = request.form.get(
            "runtime",
            ""
        ).strip()

        try:

            movie["runtime"] = (
                int(runtime)
                if runtime
                else None
            )

        except ValueError:

            movie["runtime"] = None

        movie["mood"] = request.form.get(
            "mood",
            ""
        ).strip()

        movie["own_it"] = request.form.get(
            "own_it",
            "no"
        ).lower()

        movie["watched"] = request.form.get(
            "watched",
            "no"
        ).lower()

        movie["so_bad_its_good"] = request.form.get(
            "so_bad_its_good",
            "no"
        ).lower()

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        save_movies(
            movies
        )

        return redirect(
            url_for(
                "home",
                message="Movie updated!"
            )
        )

    # --------------------------------------------------------
    # DISPLAY EDIT FORM
    # --------------------------------------------------------

    return render_template("update.html", movie=movie)


    
# ============================================================
# DELETE MOVIE
# ============================================================

@app.route(
    "/delete_movie/<int:movie_id>",
    methods=["POST"]
)
def delete_movie(movie_id):

    global movies

    movies = load_movies()

    # Check that movie exists
    movie_exists = any(
        movie.get("movie_id") == movie_id
        for movie in movies
    )

    if not movie_exists:

        return redirect(
            url_for(
                "home",
                message="Movie not found."
            )
        )

    # Remove the movie
    movies = [
        movie for movie in movies
        if movie.get("movie_id") != movie_id
    ]

    # Save updated CSV
    save_movies(
        movies
    )

    # Remove it from the current picker session too
    picked_movie_ids.discard(
        movie_id
    )

    return redirect(
        url_for(
            "home",
            message="Movie deleted."
        )
    )


# ============================================================
# MARK MOVIE AS WATCHED
# ============================================================

@app.route(
    "/watched",
    methods=["POST"]
)
def mark_watched():

    global movies

    movie_id = request.form.get(
        "movie_id"
    )

    movies = load_movies()

    # Find the movie
    movie = next(
        (
            movie for movie in movies
            if str(movie.get("movie_id"))
            == str(movie_id)
        ),
        None
    )

    if movie is None:

        return redirect(
            url_for(
                "home",
                message="Movie not found."
            )
        )

    # Mark as watched
    movie["watched"] = "yes"

    # Save back to CSV
    save_movies(
        movies
    )

    # It has now been dealt with
    picked_movie_ids.add(
        int(movie_id)
    )

    # Preserve filters
    filter_names = [
        "genre",
        "series",
        "mood",
        "year",
        "runtime",
        "own_it",
        "watched",
        "so_bad_its_good"
    ]

    redirect_arguments = {
        "message": "Movie marked as watched!"
    }

    for name in filter_names:

        value = request.form.get(
            name,
            ""
        )

        if value:

            redirect_arguments[name] = value

    return redirect(
        url_for(
            "home",
            **redirect_arguments
        )
    )


# ============================================================
# START MOVIE BRAIN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )