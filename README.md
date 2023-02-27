# Wikipedia Web Mining Project

### Packages required:

- os
- sys
- requests
- datetime
- json
- pandas
- wikipedia

### Use:

1. Add events, their dates, and a category to the eventsList.csv file, then run WikiPrimaryEvents.py to generate a list of contained links and a CSV file of views for those events.

2. Run WikiLinkedPages.py with _python3 WikiLinkedPages.py {category}_ to get pageview data on all links within events in a category.

3. When adding new categories, create new directories /{category}/Views/ and /{category}/Links/.

4. The WikiAnalyzeLinks.py script can be run with _python3 WikiAnalyzeLinks.py {category}_. It calculates an average baseline of views, a peak number of views, and the percent increase between them. These numbers are the average of the 5 dates surrounding the minimum for baseline, and the average of 5 dates surrounding the maximum for peak. This can and probably should be changed but gets a rough estimate for the % increase in traffic to those pages.
