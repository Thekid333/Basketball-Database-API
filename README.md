
# Basketball API Project

This project demonstrates how to set up and interact with a basketball-related API backend. You can use the provided PostgreSQL database exports to quickly load a database with preloaded data or start from scratch and load data using the provided tools.

---

## Database Setup

### 1. Install and Configure PostgreSQL
1. Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/).
2. Ensure PostgreSQL is running, and in a terminal, run the following commands to create a user and a database:
   ```bash
   createuser bballuser --createdb
   createdb bballdata
   ```
3. Connect to the `bballdata` database and configure the schema and permissions:
   ```bash
   psql -U postgres -d bballdata
   ```
   Inside the PostgreSQL shell, run:
   ```sql
   CREATE SCHEMA app;
   ALTER USER bballuser WITH PASSWORD 'Basketball';
   GRANT ALL ON SCHEMA app TO bballuser;
   ```

---

## Using the Provided Database Exports

### Option 1: Preloaded Database with Data
1. The file `dbexportFilledwithData.pgsql` contains preloaded data. To use it:
   ```bash
   psql -U bballuser -d bballdata -f path/to/dbexportFilledwithData.pgsql
   ```
2. This will populate your database with sample data, allowing you to immediately view API responses.

### Option 2: Empty Database
1. If you want to start with an empty database, load the provided `dbexportEmptydb.pgsql` file:
   ```bash
   psql -U bballuser -d bballdata -f path/to/dbexportEmptydb.pgsql
   ```
2. To load your own data into the database, run the following Django management command:
   ```bash
   python manage.py load_data
   ```
   This command will populate the database from the JSON files located in `backend/raw_data/`.

3. **Raw Data Files**:
   - **`teams.json`**: Defines the teams, with `id` and `name` fields.
   - **`players.json`**: Lists players with `id`, `name`, and `teamId` to associate them with teams.
   - **`games.json`**: Includes game details (e.g., `id`, `date`, home and away teams, player stats, and shots).

---

## Backend Setup

### 1. Install Python Environment Tools
1. Install [pyenv](https://github.com/pyenv/pyenv) for managing Python versions.
2. (Optional) Install `virtualenv` for managing isolated Python environments.

### 2. Install Dependencies
1. Navigate to the root of the project and install Python 3.10.1 using `pyenv`. If your system does not support this version, use a compatible Python version (you may need to update parts of the codebase for compatibility):
   ```bash
   pyenv install 3.10.1
   pyenv virtualenv 3.10.1 Basketball
   eval "$(pyenv init -)"  # May not be necessary on all systems
   ```
2. Install the required Python packages:
   ```bash
   pip install -r backend/requirements.txt
   ```

### 3. Start the Backend
1. Navigate to the `backend` directory and start the development server:
   ```bash
   cd /path/to/project/backend
   python manage.py runserver
   ```
2. The backend will run on [http://localhost:8000](http://localhost:8000).

---

## API Implementation and Viewing

### PlayerSummary API
- The skeleton for the `PlayerSummary` API view can be found in `backend/app/views/players.py`. This view is designed to return player summary data in the structure provided in `backend/app/views/sample_response/sample_response.json`.

- **Response Structure**:
  ```json
  {
      "name": "Michael Jordan",
      "team": "Tune Squad",
      "games": [
          {
              "date": "2022-12-19",
              "isStarter": true,
              "minutes": 40,
              "points": 25,
              "assists": 5,
              "offensiveRebounds": 3,
              "defensiveRebounds": 7,
              "steals": 2,
              "blocks": 1,
              "turnovers": 4,
              "defensiveFouls": 2,
              "offensiveFouls": 1,
              "freeThrowsMade": 5,
              "freeThrowsAttempted": 6,
              "twoPointersMade": 7,
              "twoPointersAttempted": 12,
              "threePointersMade": 2,
              "threePointersAttempted": 4,
              "shots": [
                  {
                      "isMake": true,
                      "locationX": 10,
                      "locationY": 20
                  }
              ]
          }
      ]
  }
  ```

- You can view the API output by navigating to:
  ```
  http://localhost:8000/api/v1/playerSummary/<PLAYER_ID>
  ```
- Replace `<PLAYER_ID>` with a valid player ID from your database.

---

## Deployment

### 1. Deployment on Heroku
1. The project uses the `Procfile` and `.buildpacks` for deployment on Heroku.
   - **Procfile**: Defines `gunicorn` as the WSGI server for running the backend.
   - **Buildpacks**:
     - Python: Handles the backend with `heroku-buildpack-python`.
     - Node.js: Placeholder for potential frontend.

2. To deploy:
   - Set the `DATABASE_URL` and any required environment variables in the Heroku settings.

3. Static Files:
   - Managed by `Whitenoise` for production.

---

## Recommendations for Improvement

- **Testing**: Add automated tests for API validation.
- **Environment Variables**: Include a `.env` file for local development.
- **Documentation**: Expand API usage examples and add Swagger or Postman documentation.

---

This README provides everything you need to get started with the Basketball API project. Feel free to customize and extend as needed!
