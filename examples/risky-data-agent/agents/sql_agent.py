from openai import OpenAI


client = OpenAI()


def customer_agent(question, connection):
    prompt = f"Write SQL for this business question: {question}"
    response = client.responses.create(model="gpt-4.1", input=prompt)
    sql = response.output_text
    cursor = connection.cursor()
    return cursor.execute(sql).fetchall()

