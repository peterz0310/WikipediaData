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

1. Add events, their dates, and a category to the eventsList.csv file, then run WikiPrimaryEvents.py to generate a list of contained links and a CSV of views for those events.

2. Run WikiLinkedPages.py with _python3 WikiLinkedPages.py {category}_ to get pageview data on all links within events in a category.

3. When adding new categories, create new directories /{category}/Views/ and /{category}/Links/.
