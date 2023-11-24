from typing import Any, List, Optional, Union
import flet as ft
from flet_core.buttons import ButtonStyle
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, CrossAxisAlignment, MainAxisAlignment, OffsetValue, PaddingValue, ResponsiveNumber, RotateValue, ScaleValue, ScrollMode
import constants as C
from time import sleep

songs : dict
father : ft.Page

def seconds_to_minutes(secs : int) -> str:
    if secs < 10: return f"0:0{int(secs)}"
    if secs < 60: return f"0:{int(secs)}"
    elif secs >= 60: 
        mins = int(secs/60)
        ssecs =  f"0{int(secs-mins*60)}" if int(secs-mins*60) < 10 else str(int(secs-mins*60))
        return f"{mins}:{ssecs}"


class SongDisplay(ft.ListTile):
    def __init__(self, name : str, song_id : str, change_songs_atributes, play_song_func, ref: Ref | None = None, key: str | None = None, width: OptionalNumber = None, height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None, right: OptionalNumber = None, bottom: OptionalNumber = None, expand: bool | int | None = None, col: ResponsiveNumber | None = None, opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None, offset: OffsetValue = None, aspect_ratio: OptionalNumber = None, animate_opacity: AnimationValue = None, animate_size: AnimationValue = None, animate_position: AnimationValue = None, animate_rotation: AnimationValue = None, animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None, tooltip: str | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, content_padding: PaddingValue = None, leading: Control | None = None, title: Control | None = None, subtitle: Control | None = None, trailing: Control | None = None, is_three_line: bool | None = None, selected: bool | None = None, dense: bool | None = None, autofocus: bool | None = None, toggle_inputs: bool | None = None, url: str | None = None, url_target: str | None = None, on_click=None, on_long_press=None):
        super().__init__(ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, content_padding, leading, title, subtitle, trailing, is_three_line, selected, dense, autofocus, toggle_inputs, url, url_target, on_click, on_long_press)
        


        def play_audio(e):
            song_obj : SongObj = songs.get(song_id)
            print(song_obj)
            if song_obj.path == "PLACEHOLDER__.mp3": return
            play_song_func(song_id)

        
        def fav(e):
            fav = False
            if e.control.icon == ft.icons.FAVORITE_BORDER:
                e.control.icon = ft.icons.FAVORITE
                change_songs_atributes(song_id, True)
            else:
                e.control.icon = ft.icons.FAVORITE_BORDER
                change_songs_atributes(song_id, False)
            
            e.control.update()
        
        self.title  = ft.Text(value=name.replace(".mp3", ""))
        self.leading = leading=ft.Image(src_base64=C.DEFAULT_COVER, border_radius=150, width=75, height=75)
        self.on_click = play_audio
        self.content_padding = 5
        self.subtitle = ft.Text(value=f"Del Album")
        print(songs.get(song_id))
        fav_button = ft.IconButton(icon=ft.icons.FAVORITE_BORDER if songs.get(song_id).fav == False else ft.icons.FAVORITE, on_click=fav)
        self.trailing = fav_button

class SongSearchResult(ft.ListTile):
    def __init__(self, name : str, cover : str, author : str, link : str, launch_url , download_func, ref: Ref | None = None, key: str | None = None, width: OptionalNumber = None, height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None, right: OptionalNumber = None, bottom: OptionalNumber = None, expand: bool | int | None = None, col: ResponsiveNumber | None = None, opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None, offset: OffsetValue = None, aspect_ratio: OptionalNumber = None, animate_opacity: AnimationValue = None, animate_size: AnimationValue = None, animate_position: AnimationValue = None, animate_rotation: AnimationValue = None, animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None, tooltip: str | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, content_padding: PaddingValue = None, leading: Control | None = None, title: Control | None = None, subtitle: Control | None = None, trailing: Control | None = None, is_three_line: bool | None = None, selected: bool | None = None, dense: bool | None = None, autofocus: bool | None = None, toggle_inputs: bool | None = None, url: str | None = None, url_target: str | None = None, on_click=None, on_long_press=None):
        super().__init__(ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, content_padding, leading, title, subtitle, trailing, is_three_line, selected, dense, autofocus, toggle_inputs, url, url_target, on_click, on_long_press)

        def download(e):
            self.ic.disabled = True
            self.disabled = True
            self.update()
            download_func(e=None, song_name=name)
            


        self.on_long_press = lambda x: launch_url(e=None, url=link)
        self.ic = ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=download)

      


        self.title  = ft.Text(value=name)
        self.leading = leading=ft.Image(src=cover, border_radius=150, width=75, height=75)
        #self.on_click = download_song
        self.content_padding = 5
        self.subtitle = ft.Text(value=f"By {author}")
        #fav_button = ft.IconButton(icon=ft.icons.FAVORITE_BORDER if songs.get(song_id).fav == False else ft.icons.FAVORITE, on_click=fav)
        self.trailing = self.ic
        

class OptionDisplay(ft.ElevatedButton):
    def __init__(self, textt: str | None = None, ref: Ref | None = None, key: str | None = None, width: OptionalNumber = None, height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None, right: OptionalNumber = None, bottom: OptionalNumber = None, expand: bool | int | None = None, col: ResponsiveNumber | None = None, opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None, offset: OffsetValue = None, aspect_ratio: OptionalNumber = None, animate_opacity: AnimationValue = None, animate_size: AnimationValue = None, animate_position: AnimationValue = None, animate_rotation: AnimationValue = None, animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None, tooltip: str | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, color: str | None = None, bgcolor: str | None = None, elevation: OptionalNumber = None, style: ButtonStyle | None = None, icon: str | None = None, icon_color: str | None = None, content: Control | None = None, autofocus: bool | None = None, url: str | None = None, url_target: str | None = None, on_click=None, on_long_press=None, on_hover=None, on_focus=None, on_blur=None):
        super().__init__(textt, ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, color, bgcolor, elevation, style, icon, icon_color, content, autofocus, url, url_target, on_click, on_long_press, on_hover, on_focus, on_blur)

        self.text = textt

        content = ft.Container([
            ft.Column([
                ft.Text("Seccion"),
                ft.Icon(name=ft.icons.FAVORITE, color="pink")
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
        self.height = 125

        self.style = ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=50),
                    color={ft.MaterialState.DEFAULT: ft.colors.BLUE})
        
        
# class ListPage(ft.ListView):
#     def __init__(self, controlsa: List[Control] | None = None, ref: Ref | None = None, key: str | None = None, width: OptionalNumber = None, height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None, right: OptionalNumber = None, bottom: OptionalNumber = None, expand: bool | int | None = None, col: ResponsiveNumber | None = None, opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None, offset: OffsetValue = None, aspect_ratio: OptionalNumber = None, animate_opacity: AnimationValue = None, animate_size: AnimationValue = None, animate_position: AnimationValue = None, animate_rotation: AnimationValue = None, animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, auto_scroll: bool | None = None, on_scroll_interval: OptionalNumber = None, on_scroll: Any = None, horizontal: bool | None = None, spacing: OptionalNumber = None, item_extent: OptionalNumber = None, first_item_prototype: bool | None = None, divider_thickness: OptionalNumber = None, padding: PaddingValue = None):
#         super().__init__(controlsa, ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, auto_scroll, on_scroll_interval, on_scroll, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding)

#         self.controls = [ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK)], alignment=ft.MainAxisAlignment.START),
#                         controlsa]

class SongObj():
    def __init__(self, name : str, path : str,  fav : bool, author : str | None = None, album : str | None = None, cover : str | None = None) -> None:
        # self.data = {
        #     "name": name,
        #     "path": path,
        #     "fav": fav,
        #     "author": author,
        #     "album": album,
        #     "cover": cover
        # }
        self.name = name
        self.path = path
        self.fav = fav
        self.author = author
        self.album = album
        self.cover = cover

class AlbumObj():
    def __init__(self, name : str, songs : list, author : str | None = None, cover : str | None = None) -> None:
        self.data = {
            "name": name,
            "songs": songs,
            "author": author,
            "cover": cover}

class PlaylistObj():
    def __init__(self, songs : list, name : str, cover : str | None = None) -> None:
        self.data = {
            "name": name,
            "songs": songs,
            "cover": str
        }

class PlaylistView(ft.ListView):
    def __init__(self, PlayListDATA : PlaylistObj, SONGS_DICT : dict ,controls: List[Control] | None = None, ref: Ref | None = None, key: str | None = None, width: OptionalNumber = None, height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None, right: OptionalNumber = None, bottom: OptionalNumber = None, expand: bool | int | None = None, col: ResponsiveNumber | None = None, opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None, offset: OffsetValue = None, aspect_ratio: OptionalNumber = None, animate_opacity: AnimationValue = None, animate_size: AnimationValue = None, animate_position: AnimationValue = None, animate_rotation: AnimationValue = None, animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, auto_scroll: bool | None = None, on_scroll_interval: OptionalNumber = None, on_scroll: Any = None, horizontal: bool | None = None, spacing: OptionalNumber = None, item_extent: OptionalNumber = None, first_item_prototype: bool | None = None, divider_thickness: OptionalNumber = None, padding: PaddingValue = None):
        super().__init__(controls, ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, auto_scroll, on_scroll_interval, on_scroll, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding)




DEFAULT_SONG = SongObj("none", "PLACEHOLDER__.mp3", False, "", "", "")