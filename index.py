import urllib.request
from flask import Flask, render_template, request, url_for, redirect, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itunes2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# global temp var to show tracks list
Tracks = []


class ItunesArtist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistName = db.Column(db.String(50), nullable=False)
    trackName = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return 'ItunesArtist %r' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tracks_list', methods=['GET'])
def tracks_list():
    # tracks = '136975'
    return render_template('tracks.html', tracks=Tracks)


@app.route('/show_tracks', methods=['POST'])
def show_tracks():
    id = request.form['id']
    # url = f'https://itunes.apple.com/lookup?id={id}&entity=musicTrack'

    url = f'https://itunes.apple.com/lookup?id={id}&entity=song&limit=200'  # max limit is 200 >:-(
    response = urllib.request.urlopen(url)
    artists = response.read()
    data = json.loads(artists)

    global Tracks
    # result = []
    Tracks = []

    for track in data["results"]:
        if track['wrapperType'] == 'track':
            Tracks.append(track)
    # print(result)

    return redirect(url_for('tracks_list'))

    # return render_template('index.html', tracks=tracks)


#print(Tracks)

# @app.route('/add_tracks', methods=['POST', 'GET'])
# def add_tracks():
#     if request.method == "POST":
#         atistName = Traks


# TO DO: def for parsing artist ID by artistName

# def getArtistID(term, media="all", country="us", limit=10):
#     url = "https://itunes.apple.com/search"
#     payload = {"term": term, "media": media, "country": country, "limit": limit}
#     response = requests.get(url, params=payload)
#     response.raise_for_status()
#     results = response.json().get("results", [])
#     assert isinstance(results, object)
#     return results


# def __getTracks(collectionId, country):
#     url = f'https://itunes.apple.com/lookup?id={str(collectionId)}&entity=song&country={str(country)}'
#
#     with urllib.request.urlopen(url) as r:
#         data: object = json.loads(
#             r.read().decode(
#                 r.info().get_param('charset') or 'utf-8'))
#
#     return data
#
# @app.route("/")
# def iTunesGetTracks(collectionId, country="us"):
#     data = __getTracks(collectionId, country=country)
#
#     results = []
#
#     for item in data['results']:
#         if item['wrapperType'] == 'track':
#             result = {
#                 "name": item["trackName"],
#                 "track": item["trackNumber"],
#                 "artist": item["artistName"],
#                 "trackId": item["trackId"],
#                 "disc": item["discNumber"],
#                 "totalDiscs": item["discCount"],
#             }
#             results.append(result)
#
#     results.sort(key=lambda v: v["track"])
#
#     return render_template('index.html', tracks=results)

if __name__ == "__main__":
    app.run(debug=True)
