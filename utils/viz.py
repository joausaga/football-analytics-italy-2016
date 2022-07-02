from mplsoccer import Pitch, VerticalPitch

import matplotlib.pyplot as plt
import numpy as np


def draw_pass_network(title, lines, weights, positions, passes_by_player, 
                      pitch_color='white', pitch_line_color='black', 
                      pitch_type='wyscout', pitch_line_width=1, linezorder=0, 
                      color=[0, 0, 1, 1], fig_size=(20,12)):
    pitch = Pitch(pitch_type=pitch_type, line_zorder=linezorder, pitch_color=pitch_color, 
                  line_color=pitch_line_color, goal_type='box', goal_alpha=1, 
                  linewidth=pitch_line_width, spot_scale=0.006)
    fig, ax = pitch.draw(figsize=fig_size)
    # Set title
    ax.text(0, -1, title, fontsize=15)

    fill_adj = lambda x: 0.8 / (1 + np.exp(-(x-20)*0.2))
    weight_adj = lambda x: 15 / (1 + np.exp(-(x-10)*0.2))
    radius_adj =  lambda x: np.sqrt(x)*200

    # Draw passes (lines)
    color_passes = color.copy()
    for i, e in enumerate(lines):
        color_passes[3] = fill_adj(weights[i])
        pitch.lines(e[0], e[1], e[2], e[3], lw=weight_adj(weights[i]),
                    color=tuple(color_passes), zorder=1, ax=ax)

    # Draw players (circles)
    for k, xy in positions.items():
        radius = radius_adj(passes_by_player[k])
        pitch.scatter(xy[0], xy[1], s=radius, color=tuple(color), 
                      edgecolors=(0, 0, 0, 1), linewidth=2, alpha=1, ax=ax)


    # Print players' name
    for k, v in positions.items():
        player_name = f'{k}\n({passes_by_player[k]})'
        x,y = v
        ax.text(x, y+5, player_name, fontsize=15, ha='center', va='center',
                color='black')

    return fig, ax