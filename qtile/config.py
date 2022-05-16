# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun"), desc="Launch terminal"),
    Key([mod,"shift"], "n", lazy.spawn("nmd"), desc="Launch rofi network manager"),
    Key([mod,"shift"], "b", lazy.spawn("blueman-manager"), desc="Launch rofi network manager"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # ~ Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
# INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

# INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

    
]

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", ]
# ~ group_labels = ["  ", "  ", " " ", "  " , " " ", " " ", "  " , "  ", "  ", "  ",]
group_labels = ["Web","Edit/chat", "Image", "Gimp", "Meld", "Video", "Files",]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),





# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

	# ~ groups = [Group(i) for i in "123456789"]

	# ~ for i in groups:
		# ~ keys.extend(
			# ~ [
				# ~ # mod1 + letter of group = switch to group
				# ~ Key(
					# ~ [mod],
					# ~ i.name,
					# ~ lazy.group[i.name].toscreen(),
					# ~ desc="Switch to group {}".format(i.name),
				# ~ ),
				# ~ # mod1 + shift + letter of group = switch to & move focused window to group
				# ~ Key(
					# ~ [mod, "shift"],
					# ~ i.name,
					# ~ lazy.window.togroup(i.name, switch_group=True),
					# ~ desc="Switch to & move focused window to group {}".format(i.name),
				# ~ ),
			 
			# ~ ]
		# ~ )
		
def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#FFFFFF",
           # "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme() 
layouts = [
    layout.MonadTall(margin=4, border_width=1, border_focus="#5e81ac", border_normal="#4c566a"),
   # layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
   # layout.Matrix(**layout_theme),
   # layout.Bsp(**layout_theme),
   # layout.Floating(**layout_theme),
   # ~ layout.RatioTile(**layout_theme),
   # layout.Max(**layout_theme)
]

# ~ old code
# ~ layouts = [
    # ~ layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # ~ layout.Max(),
    # ~ # Try more layouts by unleashing below layouts.
    # ~ # layout.Stack(num_stacks=2),
    # ~ # layout.Bsp(),
    # ~ # layout.Matrix(),
    # ~ # layout.MonadTall(),
    # ~ # layout.MonadWide(),
    # ~ # layout.RatioTile(),
    # ~ # layout.Tile(),
    # ~ # layout.TreeTab(),
    # ~ # layout.VerticalTile(),
    # ~ # layout.Zoomy(),
# ~ ]

colors = [["#282c34", "#282c34"], #282c34 color description : Very dark grayish blue.[0]
          ["#1c1f24", "#1c1f24"], #1c1f24 color description : Very dark (mostly black) blue.[1]
          ["#dfdfdf", "#dfdfdf"], #dfdfdf color description : Very light gray.[2]
          ["#ff6c6b", "#ff6c6b"], #ff6c6b color description : Very light red.[3]
          ["#98be65", "#98be65"], #98be65 color description : Slightly desaturated green.[4]
          ["#da8548", "#da8548"], #da8548 color description : Soft orange.[5]
          ["#51afef", "#51afef"], #51afef color description : Soft blue.[6]
          ["#c678dd", "#c678dd"], #c678dd color description : Soft magenta.[7]
          ["#46d9ff", "#46d9ff"], #46d9ff color description : Light cyan.[8]
          ["#a9a1e1", "#a9a1e1"]] #a9a1e1 color description : Very soft blue[9]
          
colors2 = {
    "flamingo": "#F2CDCD",
    "mauve": "#DDB6F2",
    "pink": "#F5C2E7",
    "maroon": "#E8A2AF",
    "red": "#F28FAD",
    "peach": "#F8BD96",
    "yellow": "#FAE3B0",
    "green": "#ABE9B3",
    "teal": "#B5E8E0",
    "blue": "92CDFB",
    "sky": "#89DCEB",
    "white": "#D9E0EE",
    "gray0": "#6E6C7E",
    "black1": "#1A1826",
}

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())


widget_defaults = dict(
    font="font awesome",
    fontsize = 10,
    padding = 2,
    # ~ background=colors2["gray0"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
			widget.TextBox(
				text=" 異 " ,
				fontsize = 12,
				# ~ mouse_callbacks={"Button1": lazy.spawn("")},
				mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("rofi -show run")},
				foreground=colors2["pink"],
				),
				widget.Sep(
                    linewidth=0,
                    padding=6
                ),
            
                
                widget.CurrentLayout(
                font = "Noto Sans Bold",
                foreground = colors[5],
                # ~ background = colors[1]
                ),
                
                widget.Sep(
                    linewidth=0,
                    padding=6
                ),
                widget.GroupBox(
					active=colors2["pink"],
                    rounded=False,
                    # ~ background=colors2["peach"],
                    # ~ highlight_color=colors2["peach"],
                    highlight_method="line",
                    borderwidth=3,
                    margin=4,
                    padding=1
                ),
                # ~ widget.TextBox(
					# ~ text="", 
					# ~ padding=0, 
					# ~ fontsize=20, 
					# ~ foreground=colors2["peach"]
					# ~ ),
                # ~ widget.Prompt(),
                 widget.Sep(
                    linewidth=0,
                    padding=6
                ),
                widget.WindowName(
					fontsize = 12,
                    foreground = "#0099e6",

                ),
            widget.TextBox(
                text="" ,
                fonts="MesloLGS NF",
                foreground=colors[4],
                # ~ background=colors[8],
                padding=4,
                fontsize=14
            ),
            
            widget.Backlight(
				foreground=colors[3],
				        # ~ foreground="1a1b26",
						backlight_name="intel_backlight",
						),
            widget.Sep(
                         linewidth = 1,
                         padding = 10,
                         foreground = colors[2],
                         ),
            widget.TextBox(
                text="" ,
                fonts="MesloLGS NF",
                foreground=colors[4],
                # ~ background=colors[8],
                padding=4,
                fontsize=14
            ),
            widget.PulseVolume(
                # ~ background=colors[8],
                foreground=colors[3],
                font="MesloLGS NF",
                fontsize=12,
                limit_max_volume = False,
                mouse_callbacks={'Button3': lambda: qtile.cmd_spawn("pavucontrol")},
                update_interval=0.01),
                widget.Sep(
                    linewidth=0,
                    padding=6
                ),
                widget.CheckUpdates(
                    display_format='{updates}',
                    no_update_string='[ No updates ]',
                    font="Source Code Pro",
                    fontsize=11,
					# ~ mouse_callbacks={'Button3': lambda: lazy.spawn("alacritty")},
                    foreground=colors[9],
                ),                
                widget.CapsNumLockIndicator(
                fmt="  {}", 
                fontsize=10,
                foreground=colors2["yellow"]
                
                ),
                
                widget.Memory(
                         font="Noto Sans",
                         # ~ format = {},
                         update_interval = 1,
                         fontsize = 12,
                         foreground = colors[5],
                         # ~ background = colors[1],
                        ),
                widget.Sep(
                    linewidth=0,
                    padding=6
                ),
                widget.TextBox(
                        font="FontAwesome",
                        text=" ",
                        foreground=colors[3],
                        padding = 0,
                        fontsize=10
                        ),
                widget.Clock(
                        foreground = colors[5],
                        fontsize = 11,
                        format="%Y-%m-%d %H:%M"
                        ),
                widget.Sep(
                         linewidth = 1,
                         padding = 10,
                         foreground = colors[2],
                         ),
                widget.Systray(),
                widget.QuickExit(
                    default_text="拉",
                    fontsize=20,
                    foreground="#e0def4",
                    timer_interval=0,
                    countdown_format="拉"
                ),
            ],
            size=22,
            # ~ background="#c6c6eb",
            border_width=[1, 0, 1, 0],
            opacity=0.8  # Draw top and bottom borders
            # ~ border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])
# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
