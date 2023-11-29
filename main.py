import pygame, time, math, random
import firstgame
from firstgame import Block, Player, Button
from datetime import datetime


def main():
    # window constants
    global keys
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 500

    # Init screen
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("my first build game")

    # Fill screen with pic
    IMAGE = r'C:\Users\netan\Downloads\back_ground_for_soccer_game.png'
    img = pygame.image.load(IMAGE)
    screen.blit(img, (0, 0))
    pygame.display.update()

    # קורדינטות התחלתיות של אובייקט השחקן
    x, y = 350, 470

    # מגדיר רשימה חדשה על מנת לבדוק איזה מלבנים נוגעים בשחקן
    new_block_list = pygame.sprite.Group()

    # קצב עידכון המסך
    REFRESH_RATE = 60
    clock = pygame.time.Clock()

    # פונקציה שקובעת שלא יראו את מצביע העכבר על המסך
    pygame.mouse.set_visible(0)

    # יצירת שחקן
    player = pygame.sprite.Group()
    player.add(Player(x, y))

    # יצירת כפתורים למשחק
    restart_button = Button(325, 400, 50, 30, "RESTART", (0, 0, 0), 36)

    # רשימה של הניקוד הטוב ביותר לאותו משחק
    scores_in_game = []

    # יצירת בלוקים חדשים על ידי המחלקה Block
    block_list = pygame.sprite.Group()
    blocks_row_num = 20
    for u in range(1, blocks_row_num + 1):
        for i in range(7):
            block = Block(i * 80, (-blocks_row_num * 70 - 300) + (u * 90))
            block_list.add(block)

    # נותן מהירות התחלתית לתזוזת הבלוקים
    counter_for_v = 1 * blocks_row_num * 6 + 20
    for i in block_list:
        vx = random.choice([-1, 1]) * ((counter_for_v / 25) + 1)
        vy = 1
        i.update_v(vx, vy)
        counter_for_v -= 1

    # משתנה בוליאני ששומר האם המשתמש הפסיד
    do_lost = False

    # אוגר בתוכו את הרשימה של הניקוד
    scores_in_game_line = []

    # משתנה ל BACKGROUND כשמפסידים
    background_color = (0, 0, 0)
    background_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    # משתנה שמחזיק את כמות הניקוד של השחקן
    player_score = 0

    # משתנה שסופר כמות פריימים על מנת לעדכן את הבלוקים על ציר הY כל מספר תמונות מסויים
    frame_counter_for_y_movment = 0
    number_of_frame_to_update = 3

    # משיג את הY של כל שורת בלוקים לטובת הניקוד
    y_list_blocks_for_score = pygame.sprite.Group()
    counter = 0
    for i in block_list:
        if counter == 6:
            y_list_blocks_for_score.add(i)
            counter = 0
        else:
            counter += 1

    # הגדרת טקסט ניקוד
    score_font = pygame.font.Font(None, 36)
    score_massege = f"YOUR SCORE IS {player_score}"
    score_text = score_font.render(score_massege, True, (255, 255, 255))
    score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))

    # verb check if finish
    finis = False
    while not finis and not do_lost or not finis:
        # בודק איזה מקשים לחוצים בזמן הנתון
        keys = pygame.key.get_pressed()

        # מנגנון סגירה של התכנית
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                finis = True

        while not do_lost and not finis:
            # בודק איזה מקשים לחוצים בזמן הנתון
            keys = pygame.key.get_pressed()

            # מעדכן את תזוזת הבלוקים
            for i in block_list:
                i.update_loc_x()
            if frame_counter_for_y_movment == number_of_frame_to_update:
                for i in block_list:
                    i.update_loc_y()
                frame_counter_for_y_movment = 0
            else:
                frame_counter_for_y_movment += 1

            # מדפיס את כל האובייקטים של המשחק עם המסך
            screen.blit(img, (0, 0))
            block_list.draw(screen)
            player.draw(screen)
            pygame.display.update()

            # מנגנון סגירה של התכנית
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    finis = True

                # מזיז את האובייקט הראשי לפי החצים
                elif event.type == pygame.KEYDOWN:
                    for i in player:
                        i.update_place_by_x_y(firstgame.arrows_movment_x(keys, i.get_pos_x(), WINDOW_WIDTH),
                                              firstgame.arrows_movment_y(keys, i.get_pos_y(), WINDOW_HEIGHT))

            # בודק האם הבלוקים נוגעים בפריים של חלון המשחק
            for block in block_list:
                block.touch_frame_block(WINDOW_WIDTH)

            # בודק האם השחקן נוגע בבלוקים
            new_block_list.empty()
            for play in player:
                player_hit_blocks = pygame.sprite.spritecollide(play, block_list, False)
                if 0 < len(player_hit_blocks):
                    do_lost = True

            # בודק את הניקוד של השחקן, לפי האם השחקן גבוה יותר במיקום על המסך מהבלוקים
            for pl in player:
                for i in y_list_blocks_for_score:
                    if pl.get_pos_y() < i.get_pos()[1]:
                        player_score += 1
                        y_list_blocks_for_score.remove(i)

            # מדפיס את הניקוד של השחקן
            score_massege = f"YOUR SCORE IS {player_score}"
            score_text = score_font.render(score_massege, True, (255, 255, 255))
            score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 20))
            screen.blit(score_text, score_text_rect)
            pygame.display.update()

            # כמות פריימים במסך
            clock.tick(REFRESH_RATE)

            # קובע את הדיליי אם וכאשר נלחץ כפתור לזמן ממושך
            pygame.key.set_repeat(10, 4)

        # אם השחקן מפסידת מכאן מתחיל מסך ההפסד \ ממשק הבית
        font = pygame.font.Font(None, 36)
        massege = f"""YOU LOST!  YOUR SCORE IS {player_score}"""
        text = font.render(massege, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 100))
        real_date_time = datetime.now()
        screen.fill(background_color)
        screen.blit(text, text_rect)
        bigger_then_nine = False
        for line_to_print in scores_in_game_line:
            if len(scores_in_game_line) <= 45:
                line_to_print.draw(screen)
            else:
                bigger_then_nine =  True
        if bigger_then_nine:
            for t in range(45):
                scores_in_game_line[t].draw(screen)
        restart_button.draw(screen)
        pygame.display.update()
        pygame.mouse.set_visible(1)

        # מרסט את המשחק
        if restart_button.is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)) or keys[pygame.K_SPACE]:
            pygame.mouse.set_visible(0)
            scores_in_game.append([player_score, str(real_date_time)[:19]])
            do_lost = False
            finis = False
            player_score = 0

            # נותן מיקום ראשוני ומהירות לבלוקים
            counter_u = 1
            counter_i = 0
            counter_for_v = 1 * blocks_row_num * 6 + 20
            for block in block_list:
                vx = random.choice([-1, 1]) * ((counter_for_v / 25) + 1)
                vy = 1
                block.update_v(vx, vy)
                counter_for_v -= 1
                if counter_u < blocks_row_num + 1:
                    if counter_i <= 6:
                        block.update_loc_x_v(counter_i * 80, (-blocks_row_num * 70 - 300) + (counter_u * 90))
                        counter_i += 1
                    else:
                        counter_u += 1
                        counter_i = 0
                        block.update_loc_x_v(counter_i * 80, (-blocks_row_num * 70 - 300) + (counter_u * 90))
                        counter_i += 1
                else:
                    counter_u = 0

            # יוצר את רשימת הניקוד פלוס זמן
            counter_line_space = 20
            scores_in_game.sort(key=lambda p: p[0], reverse=True)
            for line in scores_in_game:
                one_line = Button(310, 200 + counter_line_space, 100, 20, (str(counter_line_space // 20) + "." + "SCORE - " + str(line[0]) + "   " + line[1]), (0, 0, 0), 20)
                scores_in_game_line.append(one_line)
                counter_line_space += 20

            if len(scores_in_game_line) == 55:
                scores_in_game_line.pop(0)
                counter_line_space -= 20

            # נותן מיקום ראשוני לשחקן
            for pl in player:
                pl.update_place_by_x_y(350, 470)

            # מקבךל את מיקומי הY מחדש של כל הבלוקים
            counter = 0
            for i in block_list:
                if counter == 6:
                    y_list_blocks_for_score.add(i)
                    counter = 0
                else:
                    counter += 1

        if finis and not do_lost:
            time.sleep(3)

    pygame.quit()


if __name__ == '__main__':
    main()
