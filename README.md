# python_algo_project

Django app using SQLite and Bootstrap

### User Story

Search collection of algorithms by tag, language, or title

Challenge yourself with a random algorithm

Show and hide the solution

### Technical Points of Interest

Model relationships defined such that algorithms can have many tags and many solutions in different languages

The database has four tables: Algorithms, Solutions, Tags, and Languages
- Algorithms have a many-to-many relationship with tags
- Algorithms have a one-to-many relationship with solutions
- Languages have a one-to-many relationship with solutions

CRUD operations are handled with Django admin, replacing the original manually coded CRUD operations (original design remains commented in codebase)
