
import time
import sys
import pygame
from pygame.sprite import Sprite
import random

# 创建常量
BULLETS_SHOOT_FPS = pygame.USEREVENT
BOSS_BULLETS_SHOOT_FPS = pygame.USEREVENT + 1
BOSS_BIG_SHOOT_FPS = pygame.USEREVENT + 2


# 这里是英雄飞机
class Hero(Sprite):
	"""docstring for Hero"""
	def __init__(self, screen):
		super().__init__()
		self.image = pygame.image.load("./feiji/hero1.png")
		self.rect = self.image.get_rect()
		self.screen = screen # 设置变量screen	

		self.rect.centerx = 240
		self.rect.bottom = 852

		self.speed = 11
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		# 英雄发射子弹的精灵组
		self.bullets_group = pygame.sprite.Group()
		# 英雄发射炸弹的精灵组
		self.shoot_bomb_group = pygame.sprite.Group()
		# 英雄升级显示小文字的精灵组
		self.bullets_level_up_group = pygame.sprite.Group()
		# 回复血量精灵组
		self.hero_blood_up_group = pygame.sprite.Group()

		self.hero_on_off = True # 控制飞机坠毁后停止发射子弹
		self.hited = False # 判断飞机是否坠毁触发坠毁特效
		self.broken_picture_list = [] # 坠机图片列表
		self.__broken_picture() # 在初始化中先将图片保存进去，以方便后续调用
		self.image_num = 0 # 记录当前显示的图片是哪张
		self.image_show_time = 0 # 显示随着刷新，多少次的刷新更新出一张爆炸图片
		# 控制当飞机吃到子弹补给后升级子弹
		self.bullets_level_up = 0
		# 英雄血条
		self.blood = 30 # 定义英雄初始血量
		self.bomb_save = 3 # 炸弹的初始储存数量
		self.hit_box = (self.rect.x + 11, self.rect.y - 10, 29, 52)
		

	def update(self):
		if not self.hited:
			if self.moving_right:
				self.rect.centerx += self.speed
				if self.rect.centerx >= 430:
					self.moving_right = False
			if self.moving_left:
				self.rect.centerx -= self.speed
				if self.rect.centerx <= 50:
					self.moving_left = False
			if self.moving_up:
				self.rect.y -= self.speed
				if self.rect.y <= 0:
					self.moving_up = False
			if self.moving_down:
				self.rect.y += self.speed
				if self.rect.y >= 728:
					self.moving_down = False

			# 显示英雄血条坐标
			self.hit_box = (self.rect.x + 11, self.rect.y - 10, 29, 52)
	        # 血条(头顶的绿色背景矩形）
			pygame.draw.rect(self.screen, (0, 128, 0), (self.hit_box[0], self.hit_box[1] - 10, 90, 8))
	        # 血条(头顶的红色背景矩形，即：消耗的血）
			pygame.draw.rect(self.screen, (255, 0, 0), (self.hit_box[0] + self.blood * 3, self.hit_box[1] - 10, 90 - self.blood * 3, 8))
			# 这里显示被击毁之后的特效
		else:
			# 为了防止出现list index out of range错误
			if self.image_show_time <= 10:
				if self.image_show_time % 2 == 0:
					self.image = self.broken_picture_list[self.image_num]
					self.image_num += 1
				self.image_show_time += 1
			else:
				# 删除飞机
				self.kill()

	# def __del__(self):
		# print("123")

	def shoot(self):
		# 没有迟到补给
		if self.bullets_level_up == 0:
			bullet = Bullet()
			bullet.rect.centerx = self.rect.centerx
			bullet.rect.bottom = self.rect.y - 3
			self.bullets_group.add(bullet)
		# 吃到一个补给
		elif self.bullets_level_up == 1:
			bullet1 = Bullet()
			bullet1.rect.centerx = self.rect.centerx + 30
			bullet1.rect.bottom = self.rect.y - 3
			bullet2 = Bullet()
			bullet2.rect.centerx = self.rect.centerx - 30
			bullet2.rect.bottom = self.rect.y - 3
			self.bullets_group.add(bullet1, bullet2)
		# 吃到大于等于两个补给
		else:
			bullet_c = Bullet()
			bullet_r = BulletRight()
			bullet_l = BulletLeft()
			bullet_c.rect.centerx = self.rect.centerx
			bullet_c.rect.bottom = self.rect.y - 3
			bullet_r.rect.centerx = self.rect.centerx + 10
			bullet_r.rect.bottom = self.rect.y - 3
			bullet_l.rect.centerx = self.rect.centerx - 10
			bullet_l.rect.bottom = self.rect.y - 3
			self.bullets_group.add(bullet_c, bullet_r, bullet_l)


	def power_bomb(self):
		hero_power_bomb = HeroShootBomb()
		self.shoot_bomb_group.add(hero_power_bomb)


	def level_up(self):
		bullets_level_up = LevelUpFont()
		bullets_level_up.rect.centerx = 240
		bullets_level_up.rect.y = 250
		self.bullets_level_up_group.add(bullets_level_up)

	def blood_up(self):
		hero_blood_up = BloodUpFond()
		hero_blood_up.rect.centerx = 240
		hero_blood_up.rect.y = 250
		self.hero_blood_up_group.add(hero_blood_up)

	def __broken_picture(self):
		self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n1.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n2.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n3.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n1.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n2.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n3.png"))
		# self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n2.png"))
		# self.broken_picture_list.append(pygame.image.load("./feiji/hero_blowup_n3.png"))


# 这里是敌机坠毁后产生的子弹升级补记
class HeroLevelUp(Sprite):
	"""docstring for HeroLevelUp"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./feiji/prop_type_0.png")
		self.rect = self.image.get_rect()
		self.x_speed = random.randint(-5, 5)
		self.y_speed = random.randint(10, 15)

	def update(self):
		self.rect.y += self.y_speed
		self.rect.x += self.x_speed
		if self.rect.x < 0 or self.rect.x > 429:
			# 通过把速度值取反，获得飞机碰壁反弹效果
			self.x_speed = -self.x_speed
		if self.rect.y >= 852:
			self.rect.y = 0


# 升级之后显示字体
class LevelUpFont(Sprite):
	"""docstring for ClassName"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./feiji/level_up.png")
		self.rect = self.image.get_rect()
		self.n = 0

	def update(self):
		if self.n >= 15: # 控制出现时间
			self.kill()
		self.n += 1


class BloodUpFond(LevelUpFont):
	"""docstring for ClassName"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./feiji/blood_up.png")


# 这里是敌机坠毁后产生的子弹补记
class HeroBomb(Sprite):
	"""docstring for HeroBomb"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./feiji/prop_type_1.png")
		self.rect = self.image.get_rect()
		self.x_speed = random.randint(-5, 5)
		self.y_speed = random.randint(10, 15)

	def update(self):
		self.rect.y += self.y_speed
		self.rect.x += self.x_speed
		if self.rect.x < 0 or self.rect.x > 429:
			# 通过把速度值取反，获得飞机碰壁反弹效果
			self.x_speed = -self.x_speed
		if self.rect.y >= 852:
			self.rect.y = 0
	

# 这里是英雄发射炸弹
class HeroShootBomb(Sprite):
	"""docstring for HeroShootBomb"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./feiji/bomb_groud0.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 240
		self.rect.bottom = 500
		self.y_speed = 1
		# 控制飞机炸弹背景出现的时间
		self.bomb_groud_time = 0

	def update(self):
		if self.bomb_groud_time <= 10:
			self.bomb_groud_time += 1
		else:
			self.kill()

	# def __del__(self):
		# print("sasa")


# 这里是英雄子弹
class Bullet(Sprite):
	"""docstring for Bullet"""
	def __init__(self):
		super().__init__()
		self.BULLET_TYPE = "./feiji/bullet1.png"
		self.image = pygame.image.load(self.BULLET_TYPE)
		self.rect = self.image.get_rect()
		self.y_speed = 16
		self.x_speed = 0

	def update(self):
		self.rect.y -= self.y_speed
		self.rect.x -= self.x_speed
		# 飞出屏幕范围时调用kill()，删除精灵（remove为从精灵组中删除精灵）
		if self.rect.bottom <= 30 or self.rect.x <= 0 or self.rect.x >= 845:
			self.kill()

	# def __del__(self):
		# print("子弹被删除")


# 飞机子弹升到三级时的子弹
class BulletRight(Bullet):
	"""docstring for Bullet_r"""
	def __init__(self):
		super().__init__()
		self.y_speed = 14
		self.x_speed = 8


# 飞机子弹升到三级时的子弹
class BulletLeft(Bullet):
	"""docstring for Bullet_r"""
	def __init__(self):
		super().__init__()
		self.y_speed = 14
		self.x_speed = -8


# 这里是敌机子弹
class EnemyBullet(Bullet):
	"""docstring for enemyBullet"""
	def __init__(self):
		super().__init__()
		self.BULLET_TYPE = "./feiji/bullet.png"
		self.image = pygame.image.load(self.BULLET_TYPE)
		self.rect = self.image.get_rect()
		# 产生子弹随机运动方向和速度
		# 这里是的初始位置和敌机有关联，因此暂不定义
		self.y_speed = random.randint(15, 20)
		self.x_speed = random.randint(-5, 5)

	def update(self):
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed
		# 飞出屏幕范围时调用kill()，删除精灵（remove为从精灵组中删除精灵）
		if self.rect.bottom >= 852 or self.rect.x < 0 or self.rect.x > 470:
			self.kill()

	# def __del__(self):
		# print("zidan")


# 这里是boss子弹
class BossBullet(Sprite):
	"""docstring for BossBullet"""
	def __init__(self):
		super().__init__()
		self.BULLET_TYPE = "./feiji/bullet2.png"
		self.image = pygame.image.load(self.BULLET_TYPE)
		self.rect = self.image.get_rect()
		# 产生子弹随机运动方向和速度
		# 这里是的初始位置和敌机有关联，因此暂不定义
		self.y_speed = 10
		self.x_speed = 0

	def update(self):
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed
		# 飞出屏幕范围时调用kill()，删除精灵（remove为从精灵组中删除精灵）
		if self.rect.bottom >= 852 or self.rect.x < 0 or self.rect.x > 470:
			self.kill()

	# def __del__(self):
		# print("1")


class BossBullet_r(BossBullet):
	"""docstring for BossBullet_r"""
	def __init__(self):
		super().__init__()
		self.y_speed = 8
		self.x_speed = 6

	# def __del__(self):
		# print("2")


class BossBullet_l(BossBullet):
	"""docstring for BossBullet_l"""
	def __init__(self):
		super().__init__()
		self.y_speed = 8
		self.x_speed = -6

	# def __del__(self):
		# print("3")


# 这里是boss技能子弹
class BossBigBullet(Sprite):
	"""docstring for BossBigBbullet"""
	def __init__(self):
		super().__init__()
		self.BULLET_TYPE = "./feiji/bullet.png"
		self.image = pygame.image.load(self.BULLET_TYPE)
		self.rect = self.image.get_rect()
		self.y_speed = 15
		self.x_speed = 0
		self.x_move = 0.5

	def update(self):
		self.rect.y += self.y_speed
		self.x_speed -= self.x_move
		self.rect.x += self.x_speed
		# 飞出屏幕范围时调用kill()，删除精灵（remove为从精灵组中删除精灵）
		if self.rect.bottom >= 852 or self.rect.bottom <= 0 or self.rect.x < 0 or self.rect.x > 470:
			self.kill()

	# def __del__(self):
		# print("111")
		

class BossBigBullet2(BossBigBullet):
	def __init__(self):
		super().__init__()
		self.x_move = -0.5	
		
	# def __del__(self):
		# print("222")

		
# 这里是敌机
class Enemy(Sprite):
	"""docstring for Enemy"""
	def __init__(self):
		super().__init__()
		self.ENEMY_TYPE = "./feiji/enemy0.png"
		self.image = pygame.image.load(self.ENEMY_TYPE)
		self.rect = self.image.get_rect()

		self.rect.x = random.randint(10, 420)
		self.rect.y = 0

		self.x_speed = random.randint(-6, 6)
		self.y_speed = random.randint(5, 10)

		self.blood = 2 # 敌机杂兵血量

	def update(self):
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed
		if self.rect.x < 0 or self.rect.x > 429:
			# 通过把速度值取反，获得飞机碰壁反弹效果
			self.x_speed = -self.x_speed
		if self.rect.y >= 852:
			self.rect.y = 0
		
	# def __del__(self):
		# print("enemy被消除")

		
"""这里的函数非常重要！！！！！
	将所有敌机的功能封装成一个模块"""
class Enemys(Sprite):
	"""docstring for Eenemys"""
	def __init__(self):
		super().__init__()
		self.enemys_group = pygame.sprite.Group()
		self.bullet_enemy_group = pygame.sprite.Group()
		self.enemy_hited_group = pygame.sprite.Group()
		# 敌机死后掉落飞机升级物品
		self.hero_leval_thing_group = pygame.sprite.Group()
		# 定义敌机爆炸之后掉落增加飞机炸弹物品
		self.hero_bomb_group = pygame.sprite.Group()
		self.RP_of_leval_thing = 0 # 飞机升级物品初始
		self.hero_add_bomb = 0 # 飞机增加炸弹初始
		self.hited = False
		self.n = 0
		self.enemy = Enemy()

	def add_enmey_and_shoot(self):
		
		if self.n % 35 == 0:
	
			self.enemys_group.add(self.enemy)
			# 两个函数无法确保初始位置都相同，暂不知如何解决，因此暂时合并成一个函数进行处理
			bullet_enemy = EnemyBullet()
			bullet_enemy.rect.centerx = self.enemy.rect.centerx
			bullet_enemy.rect.bottom = self.enemy.rect.bottom + 5
			self.bullet_enemy_group.add(bullet_enemy)
			self.n = 0
		# 找不到更好的方法，因此将敌机爆炸效果加入敌机精灵组尝试同步
		if self.hited:
			enemy_hited = EenemyHited()
			# 返回调用enemyhited时飞机的位置，因为刷新爆炸效果需要时间，因此会出现位置偏差
			enemy_hited.rect.centerx = self.enemy.rect.centerx
			enemy_hited.rect.bottom = self.enemy.rect.bottom
			self.enemy_hited_group.add(enemy_hited)
			self.hited = False
			# 每消灭n架敌机，产生一个弹药补给
			if self.RP_of_leval_thing >= 1:
				hero_leval_thing = HeroLevelUp()
				hero_leval_thing.rect.centerx = self.enemy.rect.centerx
				hero_leval_thing.rect.bottom = self.enemy.rect.bottom
				self.hero_leval_thing_group.add(hero_leval_thing)
				# 初始化为0，避免在main函数中RP_of_leval_thing三个循环内数值没有任何变化
				self.RP_of_leval_thing = 0
			if self.hero_add_bomb >= 1:
				hero_bomb = HeroBomb()
				hero_bomb.rect.centerx = self.enemy.rect.centerx
				hero_bomb.rect.bottom = self.enemy.rect.bottom
				self.hero_bomb_group.add(hero_bomb)
				self.hero_add_bomb = 0 # 初始化，以便后续循环操作
			# 重新产生一个敌机对象
			self.enemy = Enemy()
		# 控制n的值，控制敌机产生的时间频率
		self.n += 1
		# 返回敌机的位置坐标，给后续操作使用，这里的步骤非常重要！！！
		return self.enemy.rect.x, self.enemy.rect.y


# 这里是敌机被击落的特效
class EenemyHited(Enemy):
	"""docstring for EenemyHited"""
	def __init__(self):
		super().__init__()
		# self.hited = False # 判断敌机是否被击毁并触发坠机特效
		self.broken_picture_list = [] # 坠机图片列表
		self.__broken_picture() # 提前保存爆炸图片
		self.image_show_time = 0
		self.image_num = 0

	def update(self):
		if self.image_show_time <= 1:
			if self.image_show_time % 1 == 0:
				self.image = self.broken_picture_list[self.image_num]
				self.image_num += 1
			self.image_show_time += 1
		else:
			# 删除敌机
			self.kill()
			# self.hited = False
			print("-----")

	def __broken_picture(self):
		# self.broken_picture_list.append(pygame.image.load("./feiji/enemy0_down1.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy0_down2.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy0_down3.png"))
		# self.broken_picture_list.append(pygame.image.load("./feiji/enemy0_down4.png"))


# 这里是boss
class Boss(Sprite):
	"""docsring for Boss"""
	def __init__(self, screen):
		super().__init__()
		self.image = pygame.image.load("./feiji/enemy2.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 240
		self.rect.y = 10
		self.speed_x = random.randint(-5, 5)
		self.speed_y = random.randint(1, 5)
		self.boss_bullets_group = pygame.sprite.Group()
		self.boss_big_shoot_group = pygame.sprite.Group()

		self.screen = screen
		# 初始化血条位置
		self.hit_box = (self.rect.x + 8, self.rect.y + 11, 29, 52)

		self.boss_on_off = True # 控制飞机坠毁后停止发射子弹
		self.broken_picture_list = [] # 坠机图片列表
		self.__broken_picture() # 在初始化中先将图片保存进去，以方便后续调用
		self.blood = 50 # boss血量

	def update(self):
		if self.blood > 30:
			self.image = self.broken_picture_list[0]
		elif self.blood > 24:
			self.image = self.broken_picture_list[1]
		elif self.blood > 18:
			self.image = self.broken_picture_list[2]
		elif self.blood > 12:
			self.image = self.broken_picture_list[3]
		elif self.blood > 6:
			self.image = self.broken_picture_list[4]
		elif self.blood > 0:
			self.image = self.broken_picture_list[5]
		else:
			self.image = self.broken_picture_list[6]
		self.rect.centerx += self.speed_x
		self.rect.y += self.speed_y
		if self.rect.centerx <= 85 or self.rect.centerx >= 390:
			self.speed_x = -self.speed_x
		if self.rect.y <= 0 or self.rect.y >=160:
			self.speed_y = -self.speed_y
		
		# 血条坐标
		self.hit_box = (self.rect.x + 8, self.rect.y + 11, 29, 52)
        # 血条(头顶的绿色背景矩形）
		pygame.draw.rect(self.screen, (0, 128, 0), (self.hit_box[0], self.hit_box[1] - 10, 150, 8))
        # 血条(头顶的红色背景矩形，即：消耗的血）
		pygame.draw.rect(self.screen, (255, 0, 0), (self.hit_box[0] + self.blood * 3, self.hit_box[1] - 10, 150 - self.blood * 3, 8))


	def boss_shoot(self):
		boss_bullet0 = BossBullet()
		boss_bullet1 = BossBullet_r()
		boss_bullet2 = BossBullet_l()
		boss_bullet0.rect.centerx = self.rect.centerx
		boss_bullet1.rect.centerx = self.rect.centerx + 3
		boss_bullet2.rect.centerx = self.rect.centerx - 3
		boss_bullet0.rect.bottom = self.rect.bottom + 5
		boss_bullet1.rect.bottom = self.rect.bottom + 5
		boss_bullet2.rect.bottom = self.rect.bottom + 5
		self.boss_bullets_group.add(boss_bullet0, boss_bullet1, boss_bullet2)

	def big_shoot(self):
		boss_big_shoot = BossBigBullet()
		boss_big_shoot2 = BossBigBullet2()
		boss_big_shoot.rect.centerx = self.rect.right
		boss_big_shoot.rect.bottom = self.rect.bottom - 10
		boss_big_shoot2.rect.centerx = self.rect.left
		boss_big_shoot2.rect.bottom = self.rect.bottom - 10
		self.boss_big_shoot_group.add(boss_big_shoot, boss_big_shoot2)

	def __broken_picture(self):
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy2.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy2_down1.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy2_down2.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy2_down3.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy2_down4.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy2_down5.png"))
		self.broken_picture_list.append(pygame.image.load("./feiji/enemy2_down6.png"))


# 这里是游戏的酷炫边框
class CoolBackground(Sprite):
	"""docstring for CoolBackground"""
	def __init__(self,screen):
		super().__init__()
		self.image = pygame.image.load("./feiji/cool.png")
		self.rect = self.image.get_rect()
		self.screen = screen
		# 表示背景的坐标条
		self.cool_box = (330, 740, 29, 52)
		self.bomb_num = 3

	def update(self):
		# 表示炸弹的坐标条
        # 炸弹坐标条
		pygame.draw.rect(self.screen, (255, 0, 0), (self.cool_box[0], self.cool_box[1], self.bomb_num * 20, 20))
		




class MainGame(object):
	"""docstring for MainGame"""
	def __init__(self):
		# 初始化界面
		pygame.init()
		pygame.display.set_caption("飞机大战")
		# 显示窗口的图标
		self.ICON_SURFACE = pygame.image.load("./feiji/bomb.png")
		pygame.display.set_icon(self.ICON_SURFACE)
		# 设置窗口大小
		self.SCREEN_SIZE = (480, 852)
		self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
		# 设置背景图片,通过两张背景交替变换，实现背景的移动
		self.BG_IMAGE = pygame.image.load("./feiji/background.png")
		self.BG_IMAGE2 = pygame.image.load("./feiji/background.png")
		self.rect = self.BG_IMAGE.get_rect()
		self.rect2 = self.BG_IMAGE2.get_rect()
		self.screen.blit(self.BG_IMAGE, (0, 0))
		self.screen.blit(self.BG_IMAGE2, (0, -852))

		# 设置刷新帧率
		self.fps = 100
		self.fps_clock = pygame.time.Clock()
		self.geme_fps = self.fps_clock.tick(self.fps)

		# 设置定时器
		pygame.time.set_timer(BULLETS_SHOOT_FPS , 280)
		pygame.time.set_timer(BOSS_BULLETS_SHOOT_FPS , 800)
		pygame.time.set_timer(BOSS_BIG_SHOOT_FPS , 800)

		# 加入各个元素，创建精灵族，方便调用draw方法
		self.hero = Hero(self.screen) # 传入血条固定的屏幕
		self.heros_group = pygame.sprite.Group(self.hero)
		# self.enemy = Enemy()
		# self.enemy_group = pygame.sprite.Group(self.enemy)
		# 创建四组单独刷新的敌机群
		self.enemys = Enemys()
		self.enemys2 = Enemys()
		self.enemys3 = Enemys()
		self.enemys4 = Enemys()
		# 计算击落飞机数量
		self.boss_show_num = 0
		# 击落30架飞机后boss出现
		self.enmeys_die_before_boss = 30
		self.boss = Boss(self.screen)
		self.boss_group = pygame.sprite.Group(self.boss)
		# 设置酷炫的游戏背景
		self.cool_background = CoolBackground(self.screen)
		self.cool_background_group = pygame.sprite.Group(self.cool_background)


	def __event_handle(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					self.hero.moving_left = True
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					self.hero.moving_right = True
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					self.hero.moving_up = True
				if event.key == pygame.K_s or event.key == pygame.K_DOWN:
					self.hero.moving_down = True
				if event.key == pygame.K_SPACE:
					# 炸弹数大于0时才能发射炸弹
					if self.cool_background.bomb_num >= 1:
						self.hero.power_bomb()
						# 放一次炸弹减掉敌人10血
						if self.boss_show_num >= self.enmeys_die_before_boss:
							self.boss.blood -= 10
						else: # 对小兵一次秒杀,小兵死后和被子弹打子相同
							for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4]:
								# enemy_num.enemy.blood -= 3
								enemy_num.hited = True
								# 每次消灭敌机，让数量+1
								self.boss_show_num += 1
								# 记录消灭敌机数量，产生掉落飞机升级物品概率
								"""因为敌机精灵为三个精灵组共同出现，因此想要控制每击落n个敌机落下一个物资，
									必须在碰撞事件内部用其他方式记录"""
								if self.boss_show_num % 6 == 0:
									enemy_num.RP_of_leval_thing += 1
								if self.boss_show_num % 9 == 0:
									enemy_num.hero_add_bomb += 1
								# 发射炸弹之后，让当前出现的精灵个体消失，而不是让精灵组整体消失
								enemy_num.enemy.kill()
					if self.cool_background.bomb_num >= 1:
						self.cool_background.bomb_num -= 1


			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					self.hero.moving_left = False
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					self.hero.moving_right = False
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					self.hero.moving_up = False
				if event.key == pygame.K_s or event.key == pygame.K_DOWN:
					self.hero.moving_down = False

			if event.type == BULLETS_SHOOT_FPS:
				if self.hero.hero_on_off:
					self.hero.shoot()
				else:
					break

			if event.type == BOSS_BULLETS_SHOOT_FPS:
				if self.boss_show_num >= self.enmeys_die_before_boss:
					# 判断被击中降落时停止发射子弹
					if self.boss.boss_on_off:
						self.boss.boss_shoot()
					else:
						pass

			if event.type == BOSS_BIG_SHOOT_FPS:
				if self.boss_show_num >= self.enmeys_die_before_boss:
					if self.boss.boss_on_off:
						self.boss.big_shoot()
					else:
						pass
			

	def __collide(self):
		# 检测碰撞事件
		for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4]:
			# 单个子弹的血量判断
			if enemy_num.enemy.blood > 0:
				bullet_enemy_collide = pygame.sprite.groupcollide(enemy_num.enemys_group, self.hero.bullets_group, False, True)
				if bullet_enemy_collide:
					# 英雄每击中敌机一下，敌机杂兵血量-1，图片变为受损图片
					enemy_num.enemy.blood -= 1
					enemy_num.enemy.image = pygame.image.load("./feiji/enemy0_down1.png")
			else:
				bullet_enemy_collide = pygame.sprite.groupcollide(enemy_num.enemys_group, self.hero.bullets_group, True, True)
				if bullet_enemy_collide:
					enemy_num.hited = True
					# 每次消灭敌机，让数量+1
					self.boss_show_num += 1
					# 记录消灭敌机数量，产生掉落飞机升级物品概率
					"""因为敌机精灵为三个精灵组共同出现，因此想要控制每击落n个敌机落下一个物资，
						必须在碰撞事件内部用其他方式记录"""
					if self.boss_show_num % 6 == 0:
						enemy_num.RP_of_leval_thing += 1
					if self.boss_show_num % 9 == 0:
						enemy_num.hero_add_bomb += 1


			# 飞机吃到补记子弹的特效,仅子弹消失，飞机不消失
			hero_hero_leval_thing_collide = pygame.sprite.groupcollide(self.heros_group, enemy_num.hero_leval_thing_group, False, True)
			if hero_hero_leval_thing_collide:
				if self.hero.bullets_level_up <= 2:
					# 控制该变量，使的每次吃到补记，飞机子弹进化
					self.hero.bullets_level_up += 1
					# 创建升级图标
					self.hero.level_up()
				# 第三次吃到弹药升级之后改为增加血量
				if self.hero.bullets_level_up > 2:
					self.hero.blood_up()
					if self.hero.blood <= 27:
						self.hero.blood += 3
					else:
						self.hero.blood = 30


			# 飞机吃到补充炸弹时，仅炸弹标志消失，飞机不消失
			hero_hero_bomb_add_collide = pygame.sprite.groupcollide(self.heros_group, enemy_num.hero_bomb_group, False, True)
			if hero_hero_bomb_add_collide:
				# 使飞机的炸弹储藏量+1
				self.hero.bomb_save += 1
				# 控制cool background上的炸弹储存条
				if self.cool_background.bomb_num <= 5:
					self.cool_background.bomb_num += 1

			hero_enemy_collide = pygame.sprite.spritecollide(self.hero, enemy_num.enemys_group, True)
			# 改变hero_on_off的值，控制飞机发射子弹
			if hero_enemy_collide:
				self.hero.hero_on_off = False
				self.hero.hited = True

			# 分成血量>0不坠毁，和血量<=0坠毁
			if self.hero.blood > 0:	
				# 血量大时不坠毁，仅仅生命值, 将spritecollide改成groupcollide,否则没办法仅仅子弹消失飞机不消失
				bullet_hero_collide = pygame.sprite.groupcollide(self.heros_group, enemy_num.bullet_enemy_group, False, True)
				if bullet_hero_collide:
					self.hero.blood -= 1
			else:
				bullet_hero_collide = pygame.sprite.spritecollide(self.hero, enemy_num.bullet_enemy_group, True)
				if bullet_hero_collide:
					self.hero.hero_on_off = False
					self.hero.hited = True

		# 在达到条件后才生成boss，不然boss会提前生成，只不过没有刷新，但仍会被销毁
		if self.boss_show_num >= self.enmeys_die_before_boss:
			# boss 不同血量下的效果不同
			if self.boss.blood > 0:
				boss_hero_bullets_collide = pygame.sprite.groupcollide(self.boss_group, self.hero.bullets_group, False, True)
				if boss_hero_bullets_collide:
					# 每碰撞一下血量减1
					self.boss.blood -= 1
			else:
				boss_hero_bullets_collide = pygame.sprite.groupcollide(self.boss_group, self.hero.bullets_group, True, True)
				if boss_hero_bullets_collide:
					self.boss.boss_on_off = False

			# boss子弹与英雄碰撞
			if self.hero.blood > 0:	
				# 血量大时不坠毁，仅仅生命值, 将spritecollide改成groupcollide,否则没办法仅仅子弹消失飞机不消失
				boss_bullet_hero_collide = pygame.sprite.groupcollide(self.heros_group, self.boss.boss_bullets_group, False, True)
				if boss_bullet_hero_collide:
					self.hero.blood -= 1

				boss_big_bullet_hero_collide = pygame.sprite.groupcollide(self.heros_group, self.boss.boss_big_shoot_group, False, True)
				if boss_big_bullet_hero_collide:
					self.hero.blood -= 2

			else:
				boss_bullet_hero_collide = pygame.sprite.spritecollide(self.hero, self.boss.boss_bullets_group, True)
				if boss_bullet_hero_collide:
					self.hero.hero_on_off = False # 关闭英雄发射子弹
					self.hero.hited = True # 触发坠机特效

				boss_big_bullet_hero_collide = pygame.sprite.spritecollide(self.hero, self.boss.boss_big_shoot_group, True)
				if boss_big_bullet_hero_collide:
					self.hero.hero_on_off = False # 关闭英雄发射子弹
					self.hero.hited = True # 触发坠机特效
			

	def __update_elements(self):
		# 刷新页面

		# 设置动态背景
		self.rect.y += 3
		self.rect2.y += 3
		if self.rect.y >= 852:
			self.rect.y =0
		if self.rect2.y >= 852:
			self.rect2.y =0
		self.screen.blit(self.BG_IMAGE, (0, self.rect.y))
		self.screen.blit(self.BG_IMAGE2, (0, self.rect.y - 852))

		self.heros_group.update()
		self.heros_group.draw(self.screen)

		self.hero.bullets_group.update()
		self.hero.bullets_group.draw(self.screen)
		

		# 设置当boss出现后,多刷新几次，让剩下飞机被消灭，随后不再刷新敌机
		if self.boss_show_num <= self.enmeys_die_before_boss + 1:  # 10 = 2 + 8 ,多刷新了8次，使剩余敌机有时间被消灭
			# 刷新普通杂兵敌机
			for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4]:
				enemy_num.enemys_group.update()
				enemy_num.enemys_group.draw(self.screen)

				enemy_num.bullet_enemy_group.update()
				enemy_num.bullet_enemy_group.draw(self.screen)

				enemy_num.enemy_hited_group.update()
				enemy_num.enemy_hited_group.draw(self.screen)

				enemy_num.hero_leval_thing_group.update()
				enemy_num.hero_leval_thing_group.draw(self.screen)

				enemy_num.hero_bomb_group.update()
				enemy_num.hero_bomb_group.draw(self.screen)

				# print(self.boss_show_num)

		# 刷新boss,设定击落n架飞机后boss延迟刷新2次出现
		if self.boss_show_num >= self.enmeys_die_before_boss:
			self.boss_group.update()
			self.boss_group.draw(self.screen)

			self.boss.boss_bullets_group.update()
			self.boss.boss_bullets_group.draw(self.screen)

			self.boss.boss_big_shoot_group.update()
			self.boss.boss_big_shoot_group.draw(self.screen)


		# 这里刷新放炸弹时的背景，把所有元素挡住
		self.hero.shoot_bomb_group.update()
		self.hero.shoot_bomb_group.draw(self.screen)

		# 英雄升级、加血的精灵组更新
		self.hero.bullets_level_up_group.update()
		self.hero.bullets_level_up_group.draw(self.screen)

		self.hero.hero_blood_up_group.update()
		self.hero.hero_blood_up_group.draw(self.screen)

		# 游戏边框要在最上面，因此要最后刷新
		self.cool_background_group.update()
		self.cool_background_group.draw(self.screen)


		pygame.display.update()


	def run_game(self): 
		# 游戏主循环
		while True:
			# 消灭n台敌机后，不在生成新的敌机
			if self.boss_show_num < self.enmeys_die_before_boss:
				for enemy_num in [self.enemys, self.enemys2, self.enemys3, self.enemys4]:
					enemy_num.add_enmey_and_shoot()
			self.__collide()
			self.__event_handle()
			self.__update_elements()
	

if __name__ == '__main__':
	main_game = MainGame()
	main_game.run_game()





