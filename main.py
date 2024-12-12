from fastapi import FastAPI,Request
from fastapi.responses import RedirectResponse,Response
from textblob import TextBlob
from twilio.twiml.messaging_response import MessagingResponse

app=FastAPI(title="Sentiment Analysis App")

@app.get("/",include_in_schema=False)
def index():
    return RedirectResponse("/docs",status_code=308)

@app.get("/sentiment-analysis/{text}")
def sentiment_analysis(text:str):
    blob=TextBlob(text)
    polarity=blob.sentiment.polarity
    subjectivity=blob.sentiment.subjectivity

    if polarity>0:
        sentiment="positive"
    elif polarity<0:
        sentiment="negative"
    else:
        sentiment="neutral"


    return {
        "text":text,
        "sentiment":sentiment,
        "polarity":polarity,
        "subjectivity":subjectivity
    }

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    incoming_msg = form_data.get("Body")  # User's WhatsApp message

    # Perform sentiment analysis
    blob = TextBlob(incoming_msg)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Create a response for WhatsApp
    response = MessagingResponse()
    response.message(
        f"Sentiment Analysis Result:\n"
        f"Text: {incoming_msg}\n"
        f"Sentiment: {sentiment}\n"
        f"Polarity: {polarity:.2f}\n"
        f"Subjectivity: {subjectivity:.2f}"
    )

    return Response(content=str(response), media_type="application/xml")