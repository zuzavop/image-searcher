# GASearcher

GASearcher is a search engine that utilizes a neural network CLIP to process and retrieve images. The data is
loaded from [the models file](gas/models.py) upon server startup.

Searching through datasets is performed by querying [the server](gas/view.py).

All user interface data is separated into [html](templates), [css](static/css)
a [javascript](static/js) files.

The project includes two dictionaries of classes:

1. [dictionary](static/data/v3c_nounlist.txt) - containing 6,800 nouns (preprocessed for v3c).

2. [dictionary](static/data/sea_nounlist.txt) - containing names of sea creatures (preprocessed for Marine Video Kit).

## Requirements

* Python 3
* pip package manager

## Installation
1. Clone the repository.

    ```commandline
    git clone git@gitlab.mff.cuni.cz:vopalkoz/term-project.git
    ```

2. To run whole project, including the virtual environment and required Python libraries,
use [start_server.bat](start_server.bat) for Windows or [start_server](start_server) for Linux.
   For repeated start of project is possible used only this command:
   ```commandline
   python manage.py runserver
   ```

3. Open your web browser and go to http://localhost:8000/ to access the GASearcher.

## Using
Once you have the GASearcher running, you can use it to search in sample image dataset using text queries.

To search using text:

1. Enter a query in the text search box and click "Search" or "Enter".
2. The results will be displayed alongside their classes.
3. To view context of a specific image, click on its thumbnail.

More information about using searcher is shown on welcome page.
