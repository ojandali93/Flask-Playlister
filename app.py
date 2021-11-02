from flask import Flask, render_template, request, redirect, url_for

from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        # We know that embedded YouTube videos always have this format
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
    return videos

# playlists = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#     { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
# ]

#     """Return homepage."""
# @app.route('/')
# def index():
#     return render_template('home.html', msg='Flask is Cool!!')

"""Show all playlists."""
@app.route('/')
def playlists_index():
    return render_template('playlists_index.html', playlists=playlists.find())

"""Create a new playlist."""
@app.route('/playlists/new')
def playlists_new():
    return render_template('playlists_new.html')

"""Submit a new playlist."""
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    # Grab the video IDs and make a list out of them
    video_ids = request.form.get('video_ids').split()
    # call our helper function to create the list of links
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))

if __name__ == '__main__':
    app.run(debug=True)