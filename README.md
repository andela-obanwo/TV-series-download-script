# TV-series-download-script
Script to download TVshows

## Setup
#### NB: Starred modules may already by installed or throw errors, Simply move on.
* Install python 2.7
* Install the following modules using pip. Run:
  `pip install bs4 clint requests fake_useragent`
  
* Edit the file tvSeriesScraper.py
* Modify the 'name' and 'folderpath' variables to indicate path for file storage

* Also modify the list of Shows to your liking (with names as found on on o2tvseries.com)


## Usage
* Run 'python tvSeriesScraper.py'

* Type "New" and then enter the name of the show you want to download.
or
* Type "update" to update all currently followed shows

TVshows currently recognized by 'Update':
        `'Arrow','Legends of tomorrow',
        'Blindspot','Agents of shield','Empire',
        'Daredevil','Game of Thrones', 'Gotham',
        'Greys Anatomy','How to get away with murder',
        'Heroes Reborn','Mistresses', 'Orange is the new black',
        'Modern family', 'Reign', 'Quantico', 'The flash',
        'Scandal','Vikings','Jessica Jones', 'Luke Cage'`
        



