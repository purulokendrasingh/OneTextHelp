Documentation for OneTextHelp

Please install the following NLTK models before running the app on your machine:
Punkt
the Perceptron Tagger
maxent_ne_chunker
words
wordnet
omw-1.4

pip install requests
pip install twilio
pip install nltk
pip install azure-cosmos

NLTK modules:
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
					 
Steps to run the backend project end to end:
1. Start the flask server (python -m flask run). The flask server will start on port 5000.
2. Create an ngrok tunnel (ngrok http 5000). Copy the forwarding url %URL%
3. Open Twilio Console > Messaging > Services > oth-messaging-service > Integration. Replace the webhook url with the forwarding url from ngrok (%URL%/sms) ***PLEASE MAKE SURE /sms IS APPENDED AT THE END***. SAVE SAVE SAVE
4. Run the twitter-reply-function-app (func start).