# Documentation
## Project structure
The GASearcher project has the following structure:

* gas/: The main application directory.
  * models.py: Loads data processed by the CLIP neural network.
  * views.py: Handles user requests and send the search results to templates.
  * urls.py: Maps URLs to views.
  
* templates/: HTML templates for the user interface.
* static/: Static files such as CSS and JavaScript.
* start_server: Shell script to start the Django development server on Linux.
* start_server.bat: Batch script to start the Django development server on Windows.
* requirements.txt: A list of required Python packages.

## Preprocessed data
GASearcher includes part of preprocessed data for two dataset (nounlist dictionaries and classification):

* v3c_nounlist.txt: A dataset containing 6,800 common nouns.
* sea_nounlist.txt: A dataset containing the names of various sea creatures.

## Used dictionaries
GASearcher uses the following additional python libraries:

* Django Debug Toolbar: A panel that displays various debug information when running Django applications. 
* ftfy: Fixes text that has been mangled by inconsistent encoding. 
* NumPy: A library for working with arrays and matrices. 
* Pandas: A library for data analysis and manipulation. 
* regex: A regular expression library. 
* sklearn_som: A self-organizing map library. 
* tqdm: A library for displaying progress bars. 
* Torch: A machine learning library. 
* torchaudio: A library for audio processing in Torch. 
* torchvision: A library for computer vision tasks in Torch.

