import os
from flask import Flask, request
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

# ---------------- Load Environment Variables ---------------- #
load_dotenv()

# ---------------- Create Flask App ---------------- #
app = Flask(__name__)
CORS(app)

# ---------------- Supabase Connection ---------------- #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

# ---------------- Default Image ---------------- #
NO_IMAGE_URL = "https://via.placeholder.com/400x200"

# ---------------- Base Route ---------------- #
@app.route("/")
def home():
    return {
        "status": "🎵 Musicify Backend Running Successfully"
    }

# ============================================================
# READ ALL MUSIC
# GET -> http://localhost:5001/music
# ============================================================
@app.route("/music", methods=["GET"])
def get_all_music():

    if not supabase:
        return {"error": "Supabase not configured"}, 500

    res = supabase.table("music").select("*").execute()

    return {
        "music": res.data
    }

# ============================================================
# CREATE NEW SONG
# POST -> http://localhost:5001/music
# ============================================================
@app.route("/music", methods=["POST"])
def create_music():

    if not supabase:
        return {"error": "Supabase not configured"}, 500

    data = request.get_json()

    # ---------------- Validation ---------------- #
    if not data or not data.get("title"):
        return {"error": "Title is required"}, 400

    if not data.get("artist"):
        return {"error": "Artist is required"}, 400

    # ---------------- Create Song Object ---------------- #
    new_song = {
        "title": data["title"],
        "artist": data["artist"],
        "album": data.get("album", "Unknown Album"),
        "genre": data.get("genre", "Unknown"),
        "image": data.get("image", NO_IMAGE_URL),
        "url": data.get("url", "")
    }

    # ---------------- Insert into Supabase ---------------- #
    res = supabase.table("music").insert(new_song).execute()

    return {
        "message": "Song added successfully 🎵",
        "song": res.data
    }, 201

# ============================================================
# DELETE SONG
# DELETE -> http://localhost:5001/music/1
# ============================================================
@app.route("/music/<int:music_id>", methods=["DELETE"])
def delete_music(music_id):

    if not supabase:
        return {"error": "Supabase not configured"}, 500

    # Check if song exists
    check = supabase.table("music").select("*").eq("id", music_id).execute()

    if not check.data:
        return {"error": "Song not found"}, 404

    # Delete song
    res = supabase.table("music").delete().eq("id", music_id).execute()

    return {
        "message": "Song deleted successfully",
        "song": res.data
    }

# ============================================================
# UPDATE SONG
# PUT/PATCH -> http://localhost:5001/music/1
# ============================================================
@app.route("/music/<int:music_id>", methods=["PUT", "PATCH"])
def update_music(music_id):

    if not supabase:
        return {"error": "Supabase not configured"}, 500

    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    # Check if song exists
    check = supabase.table("music").select("*").eq("id", music_id).execute()

    if not check.data:
        return {"error": "Song not found"}, 404

    # Update song
    res = supabase.table("music").update(data).eq("id", music_id).execute()

    return {
        "message": "Song updated successfully 🎵",
        "song": res.data
    }

# ============================================================
# SEARCH MUSIC
# GET -> http://localhost:5001/search?query=eminem
# ============================================================
@app.route("/search")
def search_music():

    if not supabase:
        return {"error": "Supabase not configured"}, 500

    query = request.args.get("query", "").lower()

    res = supabase.table("music").select("*").execute()

    music = res.data

    filtered_music = []

    for song in music:

        if (
            query in str(song.get("title", "")).lower()
            or query in str(song.get("artist", "")).lower()
            or query in str(song.get("album", "")).lower()
            or query in str(song.get("genre", "")).lower()
        ):
            filtered_music.append(song)

    return {
        "music": filtered_music
    }

# ============================================================
# FILTER BY GENRE
# GET -> http://localhost:5001/genre/pop
# ============================================================
@app.route("/genre/<genre_name>")
def filter_by_genre(genre_name):

    if not supabase:
        return {"error": "Supabase not configured"}, 500

    res = (
        supabase
        .table("music")
        .select("*")
        .ilike("genre", genre_name)
        .execute()
    )

    return {
        "music": res.data
    }

# ---------------- Run Flask App ---------------- #
if __name__ == "__main__":
    app.run(port=5001, debug=True)