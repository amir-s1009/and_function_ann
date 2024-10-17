import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


from config import fontSize
from config import bg
import hebb
from matplotlib import pyplot as plt

class Main(BoxLayout):

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

        plt.xlabel("X1")
        plt.ylabel("X2")

        #main container:
        self.container = BoxLayout(orientation='vertical', size_hint=(1, 1))
        

        #nav bar:
        self.nav_bar = BoxLayout(orientation='horizontal', size_hint=(0.2, 0.05))
        self.train_nav = Button(text='Train >', size_hint=(1, 1), font_size=fontSize['nav_btn'], background_color=bg['nav_btn'])
        self.train_nav.bind(on_press=self.nav_train)
        self.test_nav = Button(text='Test >', size_hint=(1, 1), font_size=fontSize['nav_btn'], background_color=bg['nav_btn'])
        self.test_nav.bind(on_press=self.nav_test)
        self.nav_bar.add_widget(self.train_nav)
        self.nav_bar.add_widget(self.test_nav)

        #body:
        self.body = GridLayout(size_hint=(1, 0.95))
        self.body.cols = 2

        self.container.add_widget(self.nav_bar)
        self.container.add_widget(self.body)

        self.add_widget(self.container)

        self.showTrain()

    def nav_train(self, instance):
        self.showTrain()
    def nav_test(self, instance):
        self.showTest()

    def showTrain(self):
        self.body.clear_widgets()
        self.container.remove_widget(self.body)

        self.data = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=30, padding=50)

        self.item_x1 = BoxLayout(orientation='horizontal', size_hint=(1,0.1))
        self.x1_label = Label(text='enter X1:', size_hint=(1,0.8), font_size=fontSize['label'], halign='right')
        self.x1_input = TextInput(size_hint=(1,0.8), font_size=fontSize['input'])
        self.item_x1.add_widget(self.x1_label)
        self.item_x1.add_widget(self.x1_input)

        self.item_x2 = BoxLayout(orientation='horizontal', size_hint=(1,0.1))
        self.x2_label = Label(text='enter X2:', size_hint=(1,0.8), font_size=fontSize['label'])
        self.x2_input = TextInput(size_hint=(1,0.8), font_size=fontSize['input'])
        self.item_x2.add_widget(self.x2_label)
        self.item_x2.add_widget(self.x2_input)

        self.item_target = BoxLayout(orientation='horizontal', size_hint=(1,0.1))
        self.target_label = Label(text='enter target:', size_hint=(1,0.8), font_size=fontSize['label'])
        self.target_input = TextInput(size_hint=(1,0.8), font_size=fontSize['input'])
        self.item_target.add_widget(self.target_label)
        self.item_target.add_widget(self.target_input)

        self.btn = Button(text="Let's train!", size_hint=(0.5, 0.1), pos_hint={'x':0.5}, font_size=fontSize['form_btn'], background_color=bg['form_btn'])
        self.btn.bind(on_press=self.handle_train)

        self.data.add_widget(BoxLayout(size_hint=(1,0.3)))
        self.data.add_widget(self.item_x1)
        self.data.add_widget(self.item_x2)
        self.data.add_widget(self.item_target)
        self.data.add_widget(self.btn)
        self.data.add_widget(BoxLayout(size_hint=(1,0.3)))

        self.body.add_widget(self.data)
        self.plot_pane = FigureCanvasKivyAgg(plt.gcf())
        self.body.add_widget(self.plot_pane)

        self.container.add_widget(self.body)

    def showTest(self):
        self.container.remove_widget(self.body)
        self.body.remove_widget(self.data)
        self.body.remove_widget(self.plot_pane)

        self.data = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=30, padding=50)

        self.item_x1 = BoxLayout(orientation='horizontal', size_hint=(1,0.1))
        self.x1_label = Label(text='enter X1:', size_hint=(1,0.8), font_size=fontSize['label'], halign='right')
        self.x1_input = TextInput(size_hint=(1,0.8), font_size=fontSize['input'])
        self.item_x1.add_widget(self.x1_label)
        self.item_x1.add_widget(self.x1_input)

        self.item_x2 = BoxLayout(orientation='horizontal', size_hint=(1,0.1))
        self.x2_label = Label(text='enter X2:', size_hint=(1,0.8), font_size=fontSize['label'])
        self.x2_input = TextInput(size_hint=(1,0.8), font_size=fontSize['input'])
        self.item_x2.add_widget(self.x2_label)
        self.item_x2.add_widget(self.x2_input)

        self.btn = Button(text="Let's test!", size_hint=(0.5, 0.1), pos_hint={'x':0.5}, font_size=fontSize['form_btn'], background_color=bg['form_btn'])
        self.btn.bind(on_press=self.handle_test)

        self.data.add_widget(BoxLayout(size_hint=(1,0.3)))
        self.data.add_widget(self.item_x1)
        self.data.add_widget(self.item_x2)
        self.data.add_widget(self.btn)
        self.data.add_widget(BoxLayout(size_hint=(1,0.3)))

        self.body.add_widget(self.data)
        self.output = BoxLayout()
        self.output_label = Label(text='', font_size=100, halign='center')
        self.output.add_widget(self.output_label)
        self.body.add_widget(self.output)
        self.container.add_widget(self.body)
        

    def handle_train(self, instance):
        x1 = None
        x2 = None
        target = None
        try:
            x1 = int(self.x1_input.text)
            x2 = int(self.x2_input.text)
            target = int(self.target_input.text)

            res = hebb.train([x1, x2], target)        
            if res == 1:
                self.handle_plot()
                self.show_popup('Success', 'Your new sample fed to the model successfuly:)', 'greenyellow')
            elif res == 0:
                self.show_popup('Error', 'Your new sample did\'nt fed to the model successfuly:(', 'orangered')

        except:
            self.show_popup('Error', 'please enter a valid character!', 'orangered')

    def handle_test(self, instance):
        result = hebb.test([int(self.x1_input.text), int(self.x2_input.text)])
        if result:
            self.output_label.text = str(result)
        else:
            self.show_popup('Error', 'please train the model firstly:)', 'orangered')

    def show_popup(self, title, message, color):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, color=color))
        closeBtn = Button(text='got it!', size_hint=(1, 0.3), background_color='greenyellow')
        content.add_widget(closeBtn)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(600, 300))
        closeBtn.bind(on_press=popup.dismiss)
        popup.open()


    def get2pointsOfBoundry(self, w1, w2, b):
        if w1 == 0:
            return [[-3, 3], [-b/w2, -b/w2]]
        elif w2 == 0:
            return [[-b/w1, -b/w1], [3, -3]]
        else:
            return [[3, -3], [-w1/w2 * 3 - b/w2, -w1/w2 * (-3) - b/w2]]

    def handle_plot(self):
        self.body.remove_widget(self.plot_pane)
        plt.clf()
        self.init_plot()
        for sample in hebb.samples:
            plt.scatter(sample['x1'], sample['x2'])
        points = self.get2pointsOfBoundry(hebb.weights[0], hebb.weights[1], hebb.bias[0])
        plt.plot(points[0], points[1])
        self.plot_pane = FigureCanvasKivyAgg(plt.gcf())
        self.body.add_widget(self.plot_pane)

    def init_plot(self):
        plt.plot([0, 0], [-5, 5])
        plt.plot([-5, 5], [0, 0])

class And_Function(App):
    def build(self):
        return Main()

if(__name__ == "__main__"):
    And_Function().run()        