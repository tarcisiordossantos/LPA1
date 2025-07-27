import datetime
import sys

import pygame
from pygame import Surface, Rect, K_RETURN, KEYDOWN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from code.const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE, C_ORANGE
from code.dbProxy import DBProxy


class Score:

    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBscore')
        name = ''
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(48, 'YOU WIN!!!', C_ORANGE, SCORE_POS['Title'])
            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'Enter Player 1 name (4 characters):'
            if game_mode == MENU_OPTION[1]:
                score = player_score[0] + player_score[1] / 2
                text = 'Enter Team name(4 characters):'
            if game_mode == MENU_OPTION[2]:
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                    text = 'Enter Player 1 name (4 characters):'
                else:
                    score = player_score[1]
                    text = 'Enter Player 2 name (4 characters):'
            self.score_text(20, text, C_YELLOW, SCORE_POS['EnterName'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4:
                            name += event.unicode
            self.score_text(20, name, C_YELLOW, SCORE_POS['Name'])
            pygame.display.flip()


    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        self.score_text(48, 'TOP 10 SCORE', C_ORANGE, SCORE_POS['Title'])
        self.score_text(20, 'NAME     SCORE          DATE', C_ORANGE, SCORE_POS['Label'])
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for ps in list_score:
            id_, name, score, date = ps
            self.score_text(20, f'{name} {score :05d} {date}', C_YELLOW, SCORE_POS[list_score.index(ps)])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        tex_font: Font = pygame.font.SysFont(name='Lucida Sans Typewriter', size=text_size)
        text_surf: Surface = tex_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


def get_formatted_date():
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.strftime('%H:%M')
    current_date = current_datetime.strftime('%d/%m/%y')
    return f'{current_time} - {current_date}'