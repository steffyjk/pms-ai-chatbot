import os
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from groq import Groq
from sqlalchemy import text
from constants import prompts
from tabulate import tabulate

# Corrected the connection string format
# Example of correct usage
engine = create_engine(
    "postgresql://MarsIntelAdmin:India%402023@mars-intel.postgres.database.azure.com:5432/earth-pm-ci"
)
db = SQLDatabase(engine=engine)

client = Groq(
    api_key="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",
)

completion = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {"role": "system", "content": prompts["earthpm_sql_generator_1"]},
        {"role": "user", "content": "Please tell me the details about Project where name is 123."},
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)
sql_query = ""
for chunk in completion:
    sql_query += (
        chunk.choices[0].delta.content
        if chunk.choices[0].delta.content is not None
        else ""
    )

# Execute the query and fetch results
if sql_query != "":
    breakpoint()
    with engine.connect() as connection:
        result = connection.execute(text(sql_query))
        # Fetch all rows from the executed query
        rows = result.fetchall()
        columns = result.keys()

    # Print the results
    print("Query Results:")
    for row in rows:
        print(row)
    print(tabulate(rows, headers=columns, tablefmt="grid"))
