import flet as ft
from time import sleep
import download.audio_downloader as AD
import controls_classes as cc


def main(page: ft.Page):

    songs = page.client_storage.get("songs") if page.client_storage.get("songs") else {"-1":"song.mp3"}
    cc.songs = songs
    cc.father = page
    songs = {"-1":"song.mp3"}
    page.client_storage.clear()

    last_audio_state = ""



    def hide_song_modifier(e):
        modify_song_dialog.open = False
        page.update()


    modify_song_dialog_song_name_input = ft.TextField(value="", width=200)
    modify_song_dialog_author = ft.TextField(value="", width=200)
    modify_song_dialog_album = ft.TextField(value="", width=200)
    modify_song_dialog_cover = ft.IconButton(icon=ft.icons.ADD_A_PHOTO)

    modify_song_dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Modify Song"),
    content=ft.Column([
            ft.Row(height=10),
            ft.Row([ft.Text("Name:"), modify_song_dialog_song_name_input]),
            ft.Row(height=10),
            ft.Row([ft.Text("Author:"), modify_song_dialog_author]),
            ft.Row(height=10),
            ft.Row([ft.Text("Album:"), modify_song_dialog_album]),
            ft.Row(height=10),
            ft.Row([ft.Text("Cover:"), ft.Text("Current cover: LLLLLLL"),modify_song_dialog_cover]),
            ft.Row(height=10),], expand=False
            
            ),
    actions=[ft.IconButton(icon=ft.icons.CANCEL, on_click=hide_song_modifier), ft.IconButton(icon=ft.icons.SAVE)],
    actions_alignment=ft.MainAxisAlignment.CENTER,
    on_dismiss=lambda x: print("Modal dialog dismissed!"),
    content_padding=5)

    def go_to_url(e, url: str):
        page.launch_url(url)

    def play_song(id : str):
        print(songs.get(id).path)
        song_path = songs[id].path
        if song_path == "PLACEHOLDER__.mp3": return
        if str(song_path).startswith("!"):
            pass
        
        current_audio.src = song_path
        current_audio.release()
        current_audio.resume()
        current_audio.update()

    
    def modify_songs(id : str, fav: bool):
        songs.get(id).fav = fav

    def audio_loaded(e):
        print(f"--Se ha cargado el audio {e.control.src}")
        if e.control.src == "PLACEHOLDER__.mp3": 
            music_slider.disabled = True
            return
        print(f"--Playing the audio {e.control.src}")
        music_slider.disabled = False
        print(current_audio.src)
        current_audio.play()
        
    def audio_postion_update(e):
        if current_audio.src == "PLACEHOLDER__.mp3": return
        music_slider.value = e.control.get_current_position() / e.control.get_duration()
        ms_start_text.value = cc.seconds_to_minutes(e.control.get_current_position() / 1000)
        ms_end_text.value = cc.seconds_to_minutes(current_audio.get_duration()/1000)
        music_slider.update()
        bottom_container.update()

    def audio_state_update(e):
        print(f"--Audio state changed: {e.data}")
        nonlocal last_audio_state
        nonlocal bt_play
        last_audio_state = e.data
        if e.data == "playing":
            bt_play.icon = ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED
        elif e.data == "stopped" or "paused":
            bt_play.icon = ft.icons.PLAY_CIRCLE_FILLED_SHARP 

        music_slider.disabled = False
            
        bottom_container.update()

    def refresh_songs_list():
        mm_songs_list.controls = []
        lllllll = []
        for id in songs:
            if id == "-1": continue
            songs_obj : cc.SongObj = songs[id]
            print(songs_obj)
            lllllll.append(cc.SongDisplay(name=songs_obj.name, song_id=id, play_song_func=play_song, 
                                          change_songs_atributes=modify_songs))
                
        mm_songs_list.controls = lllllll


    def play_button_clicked(e):
        nonlocal last_audio_state
        if last_audio_state == "playing":
            current_audio.pause()
        elif last_audio_state == "stopped" or "paused":
            current_audio.resume()

    
    def slider_changed(e):
        if current_audio.src == "PLACEHOLDER__.mp3": return
        current_audio.release()
        current_audio.seek(int(e.control.value * current_audio.get_duration()) - current_audio.get_current_position())
        current_audio.resume()
    
    def next_song(e):
        pass

    def previous_song(e):
        pass

    def add_song_filepicker(e):
        file_picker.pick_files(dialog_title="Select the Song Source", file_type=ft.FilePickerFileType.AUDIO)
    
    def add_song(obj : cc.SongObj):
        songs[get_next_free_song_id()] = obj
        page.client_storage.set("songs", songs)
        cc.songs = songs
        refresh_songs_list()
        page.overlay.append(current_audio)
        page.update()

    def download_song(e, song_name : str):
        add_song(AD.download_song(song_name, get_next_free_song_id()))
        

    def get_next_free_song_id() -> int:
        keys = []
        for item in list(songs.keys()):
            keys.append(int(item))
        keys.sort(reverse=True) if len(keys) != 1 else None
        return int(keys[0] + 2)

    def add_song_source(e : ft.FilePickerResultEvent):
        nonlocal songs
        if not e.files: return
        
        add_song(cc.SongObj(name=e.files[0].name, path=e.files[0].path, fav=False))
        

    def search_song(e):
        canciones = AD.search_song(dd_search_input.value)
        dd_songs_list.controls = []
        controls = []
        for item in canciones:
            controls.append(cc.SongSearchResult(name=item.get("title"), cover=item.get("cover"), author=item.get("channel") ,
                                                 link=item.get("link"), launch_url=go_to_url, download_func=download_song))
        dd_songs_list.controls = controls
        page.update()

    def change_page_to_add(e):
        if mid_container.content == add_page: 
            print("-----Going to main page")
            mid_container.content = main_page
            bt_add_song.style.color = ft.colors.AMBER_100
            bt_lists.style.color = ft.colors.AMBER_100
            dd_songs_list.controls = []
        else: 
            print("-----Going to lists add")
            mid_container.content = add_page
            bt_add_song.style.color = ft.colors.AMBER_500
            bt_lists.style.color = ft.colors.AMBER_100
        page.update()

    def change_lists_main_page(page : str):
        match page:
            case "lists":
                pass
            case "favs":
                pass
            case "albums":
                pass
            case "artist":
                pass

    def change_page_to_list(e):
        if mid_container.content == lists_page: 
            print("-----Going to main page")
            mid_container.content = main_page
            bt_lists.style.color = ft.colors.AMBER_100
            bt_add_song.style.color = ft.colors.AMBER_100
            

        else: 
            print("-----Going to lists page")
            mid_container.content = lists_page
            bt_lists.style.color = ft.colors.AMBER_500
            bt_add_song.style.color = ft.colors.AMBER_100
            refresh_songs_list()
        page.update()
        page.update()

    def change_lists_page(e, page: int):
        match page:
            case 0: lists_page.content = page_main_lists_page
            case 1: 
                lists_page.content = page_favs_1
                refresh_page_list(e=None, page=1)
            case 2: lists_page.content = page_playlists_2
            case 3: lists_page.content = page_albums_3
            case 4: pass
            case 5: lists_page.content = page_settings_5
        lists_page.update()

    def refresh_page_list(e, page: int):
        nonlocal songs
        match page:
            case 1:
                favs = []
                lsit = []
                for item in songs:
                    if int(item) == -1: continue
                    data = songs[item]
                    if data.fav == True: favs.append(item)
                for sss in favs:
                    lsit.append(cc.SongDisplay(name=songs[sss].name, song_id=sss, change_songs_atributes=modify_songs, play_song_func=play_song))
                page_favs_1.controls = [page_top_row] + lsit
                lists_page.update()


    current_audio = ft.Audio(src="PLACEHOLDER__.mp3", autoplay=False, volume=0.05, on_position_changed=audio_postion_update, on_loaded=audio_loaded, on_state_changed=audio_state_update)
    page.overlay.append(current_audio)
    page.update()

    #debug_button = ft.FloatingActionButton(icon=ft.icons.ADD, bgcolor=ft.colors.LIME_300)

    file_picker = ft.FilePicker(on_result=add_song_source)
    page.overlay.append(file_picker)

    
    page.title = "MusMode"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    dd_search_input = ft.TextField(expand=True, color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_GREY_800) 
    
    dd_search_button = ft.IconButton(icon=ft.icons.SEARCH, on_click=search_song)
    dd_add_song = ft.PopupMenuButton(items=[
        ft.PopupMenuItem(icon=ft.icons.STORAGE, text="Add local file", on_click=add_song_filepicker),]
        ,icon=ft.icons.ADD)
   
    dd_songs_list = ft.ListView(controls=[], spacing=10, auto_scroll=False, expand=True)

    mm_topbar = ft.SafeArea(content=[ft.Row([
        ft.Container(width=5),
        ft.IconButton(icon=ft.icons.SETTINGS, scale=1.5, on_click=lambda x: print("Ajustes")),
    ], alignment=ft.MainAxisAlignment.START, height=40)])
    mm_songs_list =ft.ListView([], horizontal=ft.CrossAxisAlignment.CENTER, spacing=4, expand=1)
    refresh_songs_list()
    main_page = ft.Column([mm_songs_list], alignment=ft.MainAxisAlignment.SPACE_EVENLY, expand=True)

    #----------------------------------------------------------------------------------------------------
    def test_func(e):
        print("hhhh")
        page.dialog = modify_song_dialog
        modify_song_dialog.open = True
        page.update()

    page_main_lists_page = ft.ListView([
        cc.OptionDisplay(textt="Favourites", on_click=lambda x: change_lists_page(e=None, page=1)), 
        cc.OptionDisplay(textt="PlayLists", on_click=lambda x: change_lists_page(e=None, page=2)), 
        cc.OptionDisplay(textt="Albums", on_click=lambda x: change_lists_page(e=None, page=3)), 
        cc.OptionDisplay(textt="Artists", on_click=lambda x: change_lists_page(e=None, page=4)), 
        cc.OptionDisplay(textt="Settings", on_click=test_func)
        ], spacing=10 )
    page_top_row = ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, scale=1.5, on_click=lambda x: change_lists_page(e=None, page=0)), ], alignment=ft.MainAxisAlignment.START)

    page_settings_5 =   ft.ListView([page_top_row], padding=10)
    page_favs_1 =       ft.ListView([page_top_row], padding=10)
    page_playlists_2 =  ft.ListView([page_top_row], padding=10)
    page_albums_3 =     ft.ListView([page_top_row], padding=10)


    #----------------------------------------------------------------------------------------------------

    lists_page = ft.Container(page_main_lists_page)

    add_page = ft.Column([  ft.SafeArea(content=    ft.Row([dd_search_input, dd_search_button, dd_add_song, ft.Container(width=5)], spacing=5, alignment=ft.MainAxisAlignment.CENTER)    ),
        dd_songs_list,
    ])

    ms_start_text = ft.Text("0:0")
    ms_end_text = ft.Text("0:0")

    bt_play = ft.IconButton(    icon=ft.icons.PLAY_CIRCLE_FILLED_SHARP,     scale=1.75, on_click=play_button_clicked)
    bt_next = ft.IconButton(    icon=ft.icons.SKIP_NEXT,                    scale=1.25)
    bt_previous = ft.IconButton(icon=ft.icons.SKIP_PREVIOUS,                scale=1.25)
    bt_add_song = ft.IconButton(icon=ft.icons.ADD_OUTLINED,                 scale=1.5, on_click=change_page_to_add, style=ft.ButtonStyle(color=ft.colors.AMBER_100))
    bt_lists = ft.IconButton(   icon=ft.icons.FORMAT_LIST_BULLETED_SHARP,   scale=1.5, on_click=change_page_to_list, style=ft.ButtonStyle(color=ft.colors.AMBER_100))

    top_container = ft.SafeArea(ft.Row([ft.IconButton(icon=ft.icons.SETTINGS)], height=25))
    mid_container = ft.Container(content=main_page,expand=True, bgcolor=ft.colors.BLACK12)
    music_slider = ft.Slider(height=20, expand=True, on_change=slider_changed)
    slider_container = ft.Row([
        ft.Container(width=10),
        ms_start_text,
        music_slider,
        ms_end_text,
        ft.Container(width=10)
    ],height=20, expand=True)

    buttons_container   = ft.Row(   [bt_lists, bt_previous, bt_play, bt_next, bt_add_song], height=50, alignment=ft.MainAxisAlignment.CENTER)
    bottom_container    = ft.Column([slider_container, buttons_container],                  height=80)

    
    
    page.add(mid_container, bottom_container)




main_obj = main
ft.app(target=main_obj)
#, view=ft.WEB_BROWSER