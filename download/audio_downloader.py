import audioscrape, os
from shutil import move
from youtubesearchpython import VideosSearch
from pydub import AudioSegment

class SongObj():
    def __init__(self, name : str, path : str,  fav : bool, author : str | None = None, album : str | None = None, cover : str | None = None) -> None:

        self.name = name
        self.path = path
        self.fav = fav
        self.author = author
        self.album = album
        self.cover = cover



def move_file(file: str, path: str):
    os.rename(file, f"{path}/{file}")

def download_song(name : str, ids: str) -> SongObj:

    before_dirs = os.listdir("./")
    audioscrape.download(
        query=name,
        include=["remix"],
        exclude=["guitar"],
        quiet=False,
        overwrite=False,
        limit=1,
        verbose=True
    )
    after_dirs = os.listdir("./")
    new_dirs = []
    for dir in after_dirs:
        if dir in before_dirs:continue
        new_dirs.append(dir)
    
    song_name = ""
    cover_path = ""
    os.mkdir(f"./download/{ids}")
    for item in new_dirs:
        name = str(item)

        if name.endswith(".description") or name.endswith(".json"):
            os.remove(name)
            continue
        
        if name.endswith(".ogg"):
            a = AudioSegment.from_ogg(name)
            song_name = name.replace(".ogg", ".mp3")
            a.export(song_name, format="mp3")
            os.remove(name)
            move(song_name, f"./download/{ids}")
            

        if name.endswith(".webp"):
            cover_path = name
            move(item, f"./download/{ids}/cover.webp")
    
    return SongObj(name=song_name, path=f"./download/{ids}/{song_name}", fav=False, author="Unknown", album="Unknown", cover=f"./download/{ids}/{cover_path}")

def search_song(song_name : str) -> list:
    limit = 5

    videosSearch = VideosSearch(song_name, limit = limit)
    lista = []
    for i in range(limit):
        data = videosSearch.result()['result'][i]
        dic = {
            "title": data['title'],
            "channel": data['channel']['name'],
            "link": data['link'],
            "cover": data['thumbnails'][0]['url']
            }
        lista.append(dic)
    return lista
