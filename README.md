# FilmRec
Course project repository for 5003, containing our group project code and related materials.

### Dataset
The project uses the **MovieLens ml-latest-small** dataset, which includes over 600 users, approximately 9,700 movies, and around 100,000 rating entries.

### Movie Details
The ml-latest-small package provides a CSV file that contains IMDb IDs for each movie. These identifiers are used to fetch additional movie information through web scraping.

### Technology Stack
- **Django** as the backend web framework  
- **MySQL** as the database (managed via DataGrip)  
- **Bootstrap** for frontend page rendering  
- **Python** for backend logic and algorithm implementation  

### Algorithm
The system adopts **User-Based Collaborative Filtering (UserCF)** to generate personalized recommendations.  
Given the dataset size (~600 users), UserCF performs efficiently.  

**ItemCF** similarity is also calculated and used in the “Similar Movies” section on movie detail pages.

---

## Detailed Version

1. Django 2.0  
2. Python 3.6  

---

## How to Run

This project requires a MySQL database. A full database backup is provided in the `database` folder.

1. Import the database backup and ensure the database name is **movie_recommend_db**.  
2. Configure the database connection in the Django settings file.  
3. Make sure your Django environment is properly set up, then start the project.

---
