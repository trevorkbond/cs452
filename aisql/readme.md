**config.json** should not be shared or committed. :)

**setup.sql** setups up the database.

**db_bot.py** initializes the database, connects to openai, provides prompts and questions.

**strategies** attempting to try out the three strategies “zero-shot, single-domain, and cross-domain” as outlined in this paper: https://arxiv.org/abs/2305.11853

**responses_\<strategy>_\<time>.json** records the provided prompts and questions, as well as the generated SQL queries and responses.

**description** This database represents the mock data to manage an upcoming dogshow.