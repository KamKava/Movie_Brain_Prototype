# Movie Brain — Testing

Testing was carried out manually while developing the application.

## Features Tested

| Feature                   | Result |
| ------------------------- | ------ |
| Add movie                 | Passed |
| Edit movie                | Passed |
| Delete movie              | Passed |
| Mark movie as watched     | Passed |
| Search movies             | Passed |
| Apply filters             | Passed |
| Random movie picker       | Passed |
| Series-order restrictions | Passed |
| CSV data persistence      | Passed |
| Android APK launch        | Passed |
| Android styling           | Passed |

## Android Testing

The application was built as an Android APK and tested on an Android device.

During testing, the application initially had issues loading the HTML templates and CSS. The Buildozer configuration was updated to include the required files.

After rebuilding, the application successfully loaded the interface with its styling and could access the movie data.

## Current Testing Approach

Testing is currently manual rather than automated.

Future development could introduce automated tests for the movie filtering, series-order and random-selection logic.
