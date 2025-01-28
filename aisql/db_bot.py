import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)


def getPath(fname):
    return os.path.join(fdir, fname)


# SQLITE
sqliteDbPath = getPath("aidb.sqlite")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath)  # create new db
sqliteCursor = sqliteCon.cursor()
with (
    open(setupSqlPath) as setupSqlFile,
    open(setupSqlDataPath) as setupSqlDataFile
):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript)  # setup tables and keys
sqliteCursor.executescript(setupSQlDataScript)  # setup tables and keys


def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result


# OPENAI
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(api_key=config["openaiKey"])


def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result


# strategies
commonSqlOnlyRequest = "\n\nGive me a sqlite select statement that answers the question. I have given you the SQL database table creation script above. Only respond with sqlite syntax. If there is an error do not explain it!"
doubleShotIntro = "I am going to give you a SQL database schema through the table creation script. I am then going to provide you an example of a query successfully interacting with the database.\n"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (doubleShotIntro + setupSqlScript +
                                  " Which player has had the most semifinal appearances? " +
                                  " SELECT fullName, COUNT(*) AS sfAppearances FROM Player INNER JOIN Match ON playerId IN (winningPlayerId, losingPlayerId) WHERE round = 'SF' GROUP BY playerId ORDER BY sfAppearances DESC LIMIT 1;" +
                                  commonSqlOnlyRequest)
}

questions = [
    "Which player has won the most grand slams?",
    "Which clothing brand sponsors the most players?",
    "What happened to Madison Keys at the 2025 Australian Open?",
    "Which court type is Nadal the best on?",
    "What is the head to head record between Federer and Nadal?",
    "Which tennis player has switched racket brands?",
    "Which player has the best overall record?",
    "How many players has Iga Swiatek bageled?"
]


def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value


for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = getChatGptResponse(
                strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question + "\" based on this database schema\n" + setupSqlScript + "\nand the response was \""+queryRawResponse + \
                "\" Please, just give a concise response in a more friendly way? Please do not give any other suggestions or chatter."
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent=2)


sqliteCursor.close()
sqliteCon.close()
print("Done!")
