import os
# from dotenv import load_dotenv
import instagrapi
from flask import Flask, render_template, request

app = Flask(__name__)
# load_dotenv()

cl = instagrapi.Client()
LOGIN = os.environ.get('LOGIN')
PASSWORD = os.environ.get('PASSWORD')
cl.login(LOGIN, PASSWORD)


@app.route('/')
def index():
    render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    url = request.form['url']
    media_pk = cl.media_pk_from_url(url)
    if media_pk is None:
        raise ValueError("Invalid URL")
    media_id = cl.media_id(media_pk)
    if media_id is None:
        raise ValueError("Failed to retrieve media ID")
    comments = cl.media_comments(media_id)
    comments_and_users = []
    pos = 1
    for comment in comments:
        username = comment.dict().get('user', {}).get('username')
        text = comment.dict().get('text')
        if username and text:
            comments_and_users.append({'number': pos, 'username': username,
                                       'url': f'https://instagram.com/{username}/', 'text': text})
            pos += 1

    if not comments_and_users:
        return f"No comments found for this post"
    return render_template('result.html', result=comments_and_users)



if __name__ == '__main__':
    app.run()
