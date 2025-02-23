# Job Portal ETL

## Overview
The **Job Portal ETL** project is designed to extract, transform, and load (ETL) job-related data into a structured database. The system processes user and membership information while ensuring efficient data management.

## Features
- **User Management:** Handles user data extraction and storage.
- **Membership System:** Tracks user memberships with activation and expiry dates.
- **Database Integration:** Uses MySQL for structured storage with foreign key relationships.
- **JSON Processing:** Reads and inserts data from JSON files.
- **Error Handling:** Ensures database consistency and prevents constraint violations.
- **CI/CD Support:** Integrated with GitHub and Jenkins for deployment.

## Project Structure
```
job-portal-etl/
├── config/
│   ├── db_config.py
├── db/
│   ├── db_connection.py
├── models/
│   ├── users.py
│   ├── membership.py
├── services/
│   ├── user_services.py
│   ├── membership_services.py
├── utils/
│   ├── common_utils.py
│   ├── file_utils.py
│   ├── json_util.py
├── json_data/
│   ├── users.json
│   ├── membership.json
├── main.py
├── README.md
```

## Installation & Setup
### Prerequisites
- Python 3.8+
- MySQL
- Git
- Virtual Environment (optional but recommended)

### Setup Instructions
1. **Clone the Repository**
   ```sh
   git clone git@github.com:NampelliSrilekha/job-portal-etl.git
   cd job-portal-etl
   ```
2. **Create a Virtual Environment (Optional)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Setup Database**
   - Update `config/db_config.py` with your database credentials.
   - Run SQL scripts to create tables (if required).

5. **Run the ETL Pipeline**
   ```sh
   python main.py
   ```

## Usage
- Modify JSON files under `json_data/` to include users and memberships.
- Run `main.py` to insert the data into the database.
- Extend services to include additional job-related information.

## Troubleshooting
- **Foreign Key Constraint Errors:** Ensure user IDs exist before inserting memberships.
- **Permission Issues with Git:** Configure SSH keys properly.

## Contributing
Pull requests are welcome! Please follow the project structure and coding standards.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

