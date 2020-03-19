# Email-Newsletter
Automatically sends emails to recipients with the latest news obtained from News API

# Setup
First, sign up for an API key at https://newsapi.org/ and replace the contents of the
text file apikey.txt with the API key

Enter the email (for example, a gmail address) you want to send the newsletter from in the text file sender_email.txt
Save the password for this email in password.txt

Enter the information for the intended recipients in the tab delimited text file client_summary.txt. The file is intended to work like a table where you can add new contacts by to send the newsletter to with different preferences. 

You can enter the recipient name under 'Name' and their respectively email under 'Email' separated by a tab. The value under 'News' for all recipients should either be TRUE or FALSE, which identifies whether the email should be sent to them (TRUE) or not (FALSE).

Parameters for 'Language', 'Country', 'Query', and 'Category' can take on the value FALSE to avoid filtering news to a specific language, country, keyword, or category respectively.

These parameters can also take on the following: (pulled from https://newsapi.org/docs/endpoints/sources)

'Language' can take on one of: ar, de, en, es, fr, he, it, nl, no, pt, ru, se, ud, zh.

'Country' allows the include FALSE (meaning the news will be from any country) but can also be from any of the countries from https://newsapi.org/sources

'Query' takes in a keyword for the news to filter by.

'Category' can take on one of: business, entertainment, health, science, sports, technology.

'Source' takes on a news source, such as bbc-news or the-verge.


# Usage
Running newsproject.py will send the email based on pulling data from the current time.

scheduler.py allows you to schedule the emails to be sent out at specified intervals. You can change the interval length by changing the variable 'frequency'.

