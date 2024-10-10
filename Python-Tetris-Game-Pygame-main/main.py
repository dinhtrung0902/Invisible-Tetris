import pygame,sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Xếp gạch tàng hình")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# Thêm biến để theo dõi thời gian
time_counter = 0
blocks_visible = True

# Thêm hằng số cho kích thước và vị trí của khu vực chơi
PLAY_WIDTH = 300  # Chiều rộng khu vực chơi (10 ô * 30 pixel mỗi ô)
PLAY_HEIGHT = 600  # Chiều cao khu vực chơi (20 ô * 30 pixel mỗi ô)
PLAY_LEFT = 10  # Vị trí bên trái của khu vực chơi
PLAY_TOP = 10  # Vị trí trên cùng của khu vực chơi

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				game.game_over = False
				game.reset()
			if event.key == pygame.K_LEFT and game.game_over == False:
				game.move_left()
			if event.key == pygame.K_RIGHT and game.game_over == False:
				game.move_right()
			if event.key == pygame.K_DOWN and game.game_over == False:
				game.move_down()
				game.update_score(0, 1)
			if event.key == pygame.K_UP and game.game_over == False:
				game.rotate()
		if event.type == GAME_UPDATE and game.game_over == False:
			game.move_down()

	# Cập nhật bộ đếm thời gian
	time_counter += clock.get_time()
	
	# Kiểm tra và cập nhật trạng thái hiển thị của các block
	if time_counter >= 20000:  # 20 giây
		blocks_visible = True
		time_counter = 0
	elif time_counter >= 10000:  # 10 giây
		blocks_visible = False

	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)

	screen.fill(Colors.dark_blue)
	
	# Vẽ đường viền cho khu vực chơi
	pygame.draw.rect(screen, Colors.white, (PLAY_LEFT - 2, PLAY_TOP - 2, 
	                                            PLAY_WIDTH + 4, PLAY_HEIGHT + 4), 2)

	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 180, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 450, 50, 50))

	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, 
		centery = score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	game.draw(screen, blocks_visible)

	pygame.display.update()
	clock.tick(60)