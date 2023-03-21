from typing import Dict, List

import plotly.express as px
import spotipy
from dash import Dash, html, dcc, Output, Input
from spotipy.oauth2 import SpotifyOAuth

from credentials import creds

scope = 'user-top-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=creds.client_id,
                                               client_secret=creds.client_secret,
                                               redirect_uri=creds.redirect_url,
                                               scope=scope))


def top_tracks(limit: int, time_range: str) -> Dict[str, List[str]]:
    """
    Gets the user's top tracks.
    :param limit: how many top tracks to return.
    :param time_range: the time range to query the top tracks.
    :return: a dictionary containing:
    'ttl' : the top tracks list,
    'al': the artists list,se
    'pl': the popularity list.
    """
    top_tracks_list = []
    artists_list = []
    popularity_list = []

    tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)

    for idx, track in enumerate(tracks['items']):
        track_name = track['name']
        top_tracks_list.append(track_name)
        popularity_list.append(track['popularity'])
        artists = []
        for art_idx in range(0, len(track['artists'])):
            artists.append(track['artists'][art_idx]['name'])
        artists_list.append(artists)

    return {'ttl': top_tracks_list, 'al': artists_list, 'pl': popularity_list}


def main():
    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Top Tracks on their Respective Popularity'),
        dcc.Dropdown(
            id="dropdown",
            options=["short_term", "medium_term", "long_term"],
            value="short_term",
            clearable=False, ),
        dcc.Graph(id="graph")
    ])

    @app.callback(
        Output("graph", "figure"),
        Input("dropdown", "value"))
    def update_bar_chart(time_range: str) -> px.bar:
        top_tracks_results = top_tracks(10, time_range)
        x = []
        y = []
        for idx, track in enumerate(top_tracks_results['ttl']):
            artists = ""
            for artist in top_tracks_results['al'][idx]:
                artists = artists + " " + artist

            x.append(track + " - " + artists)
            y.append(top_tracks_results['pl'][idx])

        fig = px.bar(x=x, y=y, labels={'x': 'Song', 'y': 'Popularity Score'})
        return fig

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
