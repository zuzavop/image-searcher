# Video retrieval

GASearcher (where GAS stands for "Generic Annotation System") is a Django-based software that allows users to search in
an image database using a text query. System show the results alongside their predefined classes, which
are intended to assist users in selecting suitable word combinations for formulating queries that more likely describe
the desired image. In addition to text search, the program also allows similarity search based on a selected image
from the currently displayed images.

The software allows logging the search progress of individual users and changing the experiment settings within the
framework of changing the collections of images used.

Text queries to the database and classification is implemented using
[the CLIP neural network](https://beta.openai.com/).

The GASearcher web application project is located in [this folder](gasearcher) with a description of its functionality.

Helper code for processing images and their classification is included in [the src folder](src). The folder contains
[code](src/parse_video.py) for processing videos into individual frames, [classification](src/top_classes.py) of frames
into classes, and [code](src/images_to_clip.py) for obtaining feature frames from the CLIP network.

The current version of the work associated with this software is available
at [this link](https://www.overleaf.com/read/ffjzxjyhtznc). Detailed software documentation is available in
[the docs](docs) folder within information about reusing software with different dataset.
