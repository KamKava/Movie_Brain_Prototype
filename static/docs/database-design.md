# Movie Brain — Data Design

Movie Brain currently uses a CSV file as its data store rather than a database.

## Movie Data

The main file is:

```text
movies.csv
```

Each movie contains information such as:

| Field             | Purpose                                    |
| ----------------- | ------------------------------------------ |
| `movie_id`        | Unique movie identifier                    |
| `title`           | Movie title                                |
| `series`          | Series name, if applicable                 |
| `series_order`    | Position within a series                   |
| `director`        | Director                                   |
| `genre`           | Movie genre                                |
| `year`            | Release year                               |
| `own_it`          | Whether the movie is owned                 |
| `runtime`         | Runtime in minutes                         |
| `mood`            | Mood/category                              |
| `watched`         | Whether the movie has been watched         |
| `so_bad_its_good` | Whether it is marked as "so bad it's good" |

## Why CSV?

CSV was chosen because the project currently has a small dataset and does not require a database server.

It also makes the data easy to inspect, edit and back up.

## Future Database

If Movie Brain grows, the CSV could be replaced with a relational database such as PostgreSQL.

The movie data could then be separated into related tables, for example:

```text
Movies
Series
Genres
Directors
```

This would make the project more suitable for larger datasets and more advanced querying.
