## Mobile Accessories
In order to run this application locally, you need to change the following configuration:
1. Install the requirements.txt by running `pip install -r requirements.txt` 
2. update the `.env` with your own `DB_URI`
3. `database.py` on line `6`, change the `DB_URI` accordingly. 
4. now to run the alembic migrations, please do: `alembic upgrade head`

## If you want to create another migration file for a new `DatabaseModel`, please run the following command in terminal:
`PYTHONPATH=. alembic revision --autogenerate -m "Added Store Table"`