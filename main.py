
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.window import Window
from random import choice,randint
from kivy.uix.scatterlayout import Scatter
from functools import partial

Window.size = (300,600)
window_width , window_height = Window.size

x , y = 9,18
xy = ( window_width//x ) + (window_height // y)

image_size = (xy,xy)

correct_sound = SoundLoader.load('correct.wav')
wrong_sound = SoundLoader.load('wrong.wav')
second_sound = SoundLoader.load('mixkit-game-ball-tap-2073.wav')
class Manager(ScreenManager):
    pass
class Banner(Screen):
    pass

class Game(Screen):
    
    def play(self):
        self.clear_widgets()
        self.chances = []
        for i in range(1,4):
            image = Image(
                        source='green1.png',
                        size_hint=(None,None),
                        size=(xy/5,xy/5),
                        pos=((xy/3)*i,window_height-(xy/2)))
            self.chances.append(image)
            self.add_widget(image)
        
        self.score_label = Label(
                        text='0',
                        pos_hint={'center_x':0.5,'center_y':.92},
                        font_name='LANDEPZ GLITCH.ttf',
                        bold=1,
                        #font_name='SmallMemory.ttf',
                        font_size=window_width/9)
        self.score = 0
        self.speed = 5
        self.add_widget(self.score_label)
        self.make_shot()

    def animation_label1(self,*_):
        if self._label:
            self._size+=1
            self.label_banner.font_size+=(self._font_size/40)
        else:
            self._size-=1
            self.label_banner.font_size-=(self._font_size/40)



        if self._size%2:
            self.label_banner.pos[1]+=3
        else:
            self.label_banner.pos[1]-=3
        
    
        if self._size == 6:
            self._label = 0
        if self._size == 0:
            self._label = 1
    

    def on_enter(self):

        self.start('PLAY')
    def progress(self, *_):
        second = int( self.label_seconds.text )
        self.label_seconds.font_size = self._font_size
        Clock.unschedule(self.animation_label2)
        Clock.schedule_interval(self.animation_label2,0.01)
        if second > 1:
            second_sound.play()
            self.label_seconds.text = str(second-1)
            
        else:
            Clock.unschedule(self.progress)
            self.seconds = False
            self.play()
    def animation_label2(self,*_):
        self.label_seconds.font_size -= (self._font_size/90)

    def start_seconds(self ,*_):
        self.seconds = True
        self.clear_widgets()
        self._font_size = window_width/2
        
        self.label_seconds = Label(
                        text='3',
                        font_name='LANDEPZ GLITCH.ttf',
                        font_size=self._font_size)

        
        self.add_widget(self.label_seconds)
        
        Clock.schedule_interval(self.animation_label2,0.01)
        Clock.schedule_interval(self.progress,1)
        second_sound.play()
    def start(self,text):
        self.clear_widgets()
        self.banner = True
        self._font_size = window_width/7
        self.label_banner = Label(
                        text=text,
                        font_name='Kids Edition.ttf',
                        font_size=window_width/7)

        
        self.add_widget(self.label_banner)
        self._label = 1
        self._size =1
        
        Clock.unschedule(self.animation_label1)
        Clock.schedule_interval(self.animation_label1,.06)


    def rotating(self, *_):
        if not self.clicked_shot:
            self.shot.rotation += 3
        else:
            self.shot.rotation -= 50
    def moving(self, *_):
        if self.to_up:
            self.pos_y += self.speed
        else:
            self.pos_y -= self.speed

        self.shot.pos = self.pos_x ,self.pos_y
        
        
        if self.pos_y < -xy or self.pos_y >= window_height:
            if self.shot_type:
                self.lose_chance()
                
            else:
                self.update_score()
                self.make_new_shot()
    def lose_chance(self):
        self.remove_widget(self.chances.pop())
        if self.chances:
            self.make_new_shot()
        else:
            self.banner = True
            self.stop_moving()
            self.stop_rotating()
            self.start('TRY AGAIN')

    def update_score(self):
        self.score+=1
        self.score_label.text = str(self.score)
        if self.speed<45:
            self.speed += .2
        print('speed :' , self.speed)
    def make_new_shot(self):
        self.stop_moving()
        self.remove_widget(self.shot)
        self.make_shot()

    def stop_moving(self):
        Clock.unschedule(self.moving)
    def start_moving(self):
        Clock.schedule_interval(self.moving,0)
    
    def start_rotating(self):
        Clock.schedule_interval(self.rotating,0)
    def stop_rotating(self):
        Clock.unschedule(self.rotating)
    def make_shot(self):
        self.stop_rotating()
        self.start_rotating()
        self.shot_type = randint(0,1)
        if self.shot_type:
            self.make_image('green1.png')
        else:
            self.make_image('red1.png')

        self.to_up =  randint(0,1)
        self.pos_x =  randint(0,window_width-xy-(xy//3))
        self.pos_y =  -xy if self.to_up else window_height
        self.shot.pos =  self.pos_x ,self.pos_y

        self.size_xy = self.shot.size[0]

        self.start_moving()
        self.add_widget(self.shot)
        self.clicked_shot = False
 

    def make_image(self,source):

        self.shot = Scatter(
                        do_translation=False,
                        size_hint=(None,None),
                        size=image_size,
                        rotation=0)
        self.image = Image(
                        source=source,
                        size=image_size,
                        size_hint=(None,None))
        self.shot.add_widget(self.image)







    def on_touch_down(self, touch):

        if self.banner:
            self.clear_widgets()
            self.banner = False

            self.start_seconds()
            
            return
        if self.seconds:
            return 
        pos_x ,pos_y =  touch.pos
        if ( (self.pos_x-(x*6))<=(pos_x)<=(self.pos_x+xy+(x*6) )) and \
           ( (self.pos_y-(y*6))<=(pos_y)<=(self.pos_y+xy+(y*6))) :
           
            self.stop_moving()
            
            if self.shot_type:
                if not self.clicked_shot :
                    correct_sound.play()
                Clock.schedule_interval(self.correct,0)
            else:
                if not self.clicked_shot :
                    wrong_sound.play()
                self._wrong = 0
                Clock.schedule_interval(self.wrong,0)
            self.clicked_shot = True
    

    def correct(self, *_):

        if self.image.size[0]>0:
            self.image.size = [i-(xy/20) for i in self.image.size]
        else:
            
            Clock.unschedule(self.correct)
            self.make_new_shot()
            self.update_score()
            

    def wrong(self, *_):
        if self._wrong<20:
            self._wrong+=1
            self.image.size = (xy+(xy/2) if self.image.size[0] == xy else xy,)*2

        else:
            Clock.unschedule(self.wrong)
            self.lose_chance()



class MyApp(App):
    def build(self):
        game = Game()
        game.start('PLAY')
        screenManager = ScreenManager()
        screenManager.add_widget(game)
        return screenManager

MyApp().run()
