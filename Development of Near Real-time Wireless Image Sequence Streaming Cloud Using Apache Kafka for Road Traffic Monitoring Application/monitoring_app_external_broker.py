import time
import wx
import cStringIO
from kafka import KafkaConsumer
import threading
import Queue
from datetime import datetime
#import simplejson
import pickle

local_consumer1 = KafkaConsumer('PhayaThai-1', bootstrap_servers = ['192.168.1.7:9092'], group_id = 'view1', consumer_timeout_ms = 300)

local_consumer2 = KafkaConsumer('PhayaThai-2', bootstrap_servers = ['192.168.1.7:9092'], group_id = 'view2', consumer_timeout_ms = 300)

local_consumer3 = KafkaConsumer('PhayaThai-3', bootstrap_servers = ['192.168.1.7:9092'], group_id = 'view3', consumer_timeout_ms = 300)

local_consumer4 = KafkaConsumer('PhayaThai-4', bootstrap_servers = ['192.168.1.7:9092'], group_id = 'view4', consumer_timeout_ms = 300)

local_consumer5 = KafkaConsumer('PhayaThai-5', bootstrap_servers = ['192.168.1.7:9092'], group_id = 'view5', consumer_timeout_ms = 300)

local_consumer6 = KafkaConsumer('PhayaThai-6', bootstrap_servers = ['192.168.1.7:9092'], group_id = 'view6', consumer_timeout_ms = 300)


local_consumer1.poll()
local_consumer2.poll()
local_consumer3.poll()
local_consumer4.poll()
local_consumer5.poll()
local_consumer6.poll()

local_consumer1.seek_to_end()
local_consumer2.seek_to_end()
local_consumer3.seek_to_end()
local_consumer4.seek_to_end()
local_consumer5.seek_to_end()
local_consumer6.seek_to_end()

my_queue1 = Queue.Queue()
my_queue2 = Queue.Queue()
my_queue3 = Queue.Queue()
my_queue4 = Queue.Queue()
my_queue5 = Queue.Queue()
my_queue6 = Queue.Queue()

start = time.time()

period_of_time = 120

latency_list_of_pi1 = []
latency_list_of_pi2 = []
latency_list_of_pi3 = []
latency_list_of_pi4 = []
latency_list_of_pi5 = []
latency_list_of_pi6 = []

unix_timestamp_of_pi1 = []
unix_timestamp_of_pi2 = []
unix_timestamp_of_pi3 = []
unix_timestamp_of_pi4 = []
unix_timestamp_of_pi5 = []
unix_timestamp_of_pi6 = []

image_list_pi1 = []
image_list_pi2 = []
image_list_pi3 = []
image_list_pi4 = []
image_list_pi5 = []
image_list_pi6 = []

class MyPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        background_image = 'new_one_1920_1080.png'
        bmp_background = wx.Image(background_image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap1 = wx.StaticBitmap(self, -1, bmp_background, (0, 0))
        parent.SetTitle('consumer application')

        self.font = wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.flashingText1 = wx.StaticText(self, label = 'Phaya Thai - 1', pos = (530, 610))
        self.flashingText2 = wx.StaticText(self, label = 'Phaya Thai - 2', pos = (950, 610))
        self.flashingText3 = wx.StaticText(self, label = 'Phaya Thai - 3', pos = (1360, 610))
        self.flashingText4 = wx.StaticText(self, label = 'Phaya Thai - 4', pos = (530, 360))
        self.flashingText5 = wx.StaticText(self, label = 'Phaya Thai - 5', pos = (950, 360))
        self.flashingText6 = wx.StaticText(self, label = 'Phaya Thai - 6', pos = (1360, 360))
        self.flashingText1.SetForegroundColour('red')
        self.flashingText2.SetForegroundColour('red')
        self.flashingText3.SetForegroundColour('red')
        self.flashingText4.SetForegroundColour('red')
        self.flashingText5.SetForegroundColour('red')
        self.flashingText6.SetForegroundColour('red')

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(50)
        # self.timer.Start(200)
        def save_list_pi1():
            global latency_list_of_pi1
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            # threading.Timer(300.0, save_list_pi1).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi1 latency list' + current_time + '.txt', 'w')
            # simplejson.dump(latency_list_of_pi1, f)
            # f.close()

            threading.Timer(300.0, save_list_pi1).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi1 latency list' + current_time + '.txt', 'w') as fp:
                pickle.dump(latency_list_of_pi1, fp)

            # fig, ax = plt.subplots()
            #
            # ax.plot(latency_list_of_pi1)
            #
            # ax.set(title="Latency per image vs messages (PhayaThai-1) at Local broker 2")
            #
            # ax.set(xlabel="Number of messages from PhayaThai-1", ylabel="Latency in ms")
            #
            # plt.show()

            latency_list_of_pi1 *= 0

        def save_list_pi2():
            global latency_list_of_pi2
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_list_pi2).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi2 latency list' + current_time + '.txt', 'w')
            # simplejson.dump(latency_list_of_pi2, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi2 latency list' + current_time + '.txt', 'w') as fp:
                pickle.dump(latency_list_of_pi2, fp)

            latency_list_of_pi2 *= 0

        def save_list_pi3():
            global latency_list_of_pi3
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_list_pi3).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi3 latency list' + current_time + '.txt', 'w')
            # simplejson.dump(latency_list_of_pi3, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi3 latency list' + current_time + '.txt', 'w') as fp:
                pickle.dump(latency_list_of_pi3, fp)

            latency_list_of_pi3 *= 0

        def save_list_pi4():
            global latency_list_of_pi4
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_list_pi4).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi4 latency list' + current_time + '.txt', 'w')
            # simplejson.dump(latency_list_of_pi4, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi4 latency list' + current_time + '.txt', 'w') as fp:
                pickle.dump(latency_list_of_pi4, fp)

            latency_list_of_pi4 *= 0

        def save_list_pi5():
            global latency_list_of_pi5
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_list_pi5).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi5 latency list' + current_time + '.txt', 'w')
            # simplejson.dump(latency_list_of_pi5, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi5 latency list' + current_time + '.txt', 'w') as fp:
                pickle.dump(latency_list_of_pi5, fp)

            latency_list_of_pi5 *= 0

        def save_list_pi6():
            global latency_list_of_pi6
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_list_pi6).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi6 latency list' + current_time + '.txt', 'w')
            # simplejson.dump(latency_list_of_pi6, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi6 latency list' + current_time + '.txt', 'w') as fp:
                pickle.dump(latency_list_of_pi6, fp)

            latency_list_of_pi6 *= 0

        def save_loss_list_pi1():
            global image_list_pi1
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            # threading.Timer(300.0, save_loss_list_pi1).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi1 image list ' + current_time + '.txt', 'w')
            # simplejson.dump(image_list_pi1, f)
            # f.close()

            threading.Timer(300.0, save_loss_list_pi1).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi1 image list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(image_list_pi1, fp)

            image_list_pi1 *= 0

        def save_loss_list_pi2():
            global image_list_pi2
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_loss_list_pi2).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi2 image list ' + current_time + '.txt', 'w')
            # simplejson.dump(image_list_pi2, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi2 image list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(image_list_pi2, fp)

            image_list_pi2 *= 0

        def save_loss_list_pi3():
            global image_list_pi3
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_loss_list_pi3).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi3 image list ' + current_time + '.txt', 'w')
            # simplejson.dump(image_list_pi3, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi3 image list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(image_list_pi3, fp)

            image_list_pi3 *= 0

        def save_loss_list_pi4():
            global image_list_pi4
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_loss_list_pi4).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi4 image list ' + current_time + '.txt', 'w')
            # simplejson.dump(image_list_pi4, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi4 image list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(image_list_pi4, fp)

            image_list_pi4 *= 0

        def save_loss_list_pi5():
            global image_list_pi5
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_loss_list_pi5).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi5 image list ' + current_time + '.txt', 'w')
            # simplejson.dump(image_list_pi5, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi5 image list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(image_list_pi5, fp)

            image_list_pi5 *= 0

        def save_loss_list_pi6():
            global image_list_pi6
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_loss_list_pi6).start()
            # f = open('/home/gateway2/Downloads/lab-based_testing_result/testing_result/pi6 image list ' + current_time + '.txt', 'w')
            # simplejson.dump(image_list_pi6, f)
            # f.close()

            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi6 image list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(image_list_pi6, fp)

            image_list_pi6 *= 0


        def save_send_time_list_pi1():
            global unix_timestamp_of_pi1
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_send_time_list_pi1).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi1 send time list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(unix_timestamp_of_pi1, fp)

            unix_timestamp_of_pi1 *= 0

        def save_send_time_list_pi2():
            global unix_timestamp_of_pi2
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_send_time_list_pi2).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi6 send time list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(unix_timestamp_of_pi2, fp)

            unix_timestamp_of_pi2 *= 0

        def save_send_time_list_pi3():
            global unix_timestamp_of_pi3
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_send_time_list_pi3).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi3 send time list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(unix_timestamp_of_pi3, fp)

            unix_timestamp_of_pi3 *= 0

        def save_send_time_list_pi4():
            global unix_timestamp_of_pi4
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_send_time_list_pi4).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi4 send time list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(unix_timestamp_of_pi4, fp)

            unix_timestamp_of_pi4 *= 0

        def save_send_time_list_pi5():
            global unix_timestamp_of_pi5
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_send_time_list_pi5).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi5 send time list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(unix_timestamp_of_pi5, fp)

            unix_timestamp_of_pi5 *= 0

        def save_send_time_list_pi6():
            global unix_timestamp_of_pi6
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_" + "%H:%M:%S.%f")
            threading.Timer(300.0, save_send_time_list_pi6).start()
            with open('/home/controller/Downloads/lab-based_testing_result/testing_result/pi6 send time list ' + current_time + '.txt', 'w') as fp:
                pickle.dump(unix_timestamp_of_pi6, fp)

            unix_timestamp_of_pi6 *= 0


        save_list_pi1()
        save_list_pi2()
        save_list_pi3()
        save_list_pi4()
        save_list_pi5()
        save_list_pi6()

        save_loss_list_pi1()
        save_loss_list_pi2()
        save_loss_list_pi3()
        save_loss_list_pi4()
        save_loss_list_pi5()
        save_loss_list_pi6()

        save_send_time_list_pi1()
        save_send_time_list_pi2()
        save_send_time_list_pi3()
        save_send_time_list_pi4()
        save_send_time_list_pi5()
        save_send_time_list_pi6()

    def update(self, event):
        """"""

        global local_consumer1
        global local_consumer2
        global local_consumer3
        global local_consumer4
        global local_consumer5
        global local_consumer6

        global my_queue1
        global my_queue2
        global my_queue3
        global my_queue4
        global my_queue5
        global my_queue6

        global latency_list_of_pi1
        global latency_list_of_pi2
        global latency_list_of_pi3
        global latency_list_of_pi4
        global latency_list_of_pi5
        global latency_list_of_pi6

        global unix_timestamp_of_pi1
        global unix_timestamp_of_pi2
        global unix_timestamp_of_pi3
        global unix_timestamp_of_pi4
        global unix_timestamp_of_pi5
        global unix_timestamp_of_pi6

        global image_list_pi1
        global image_list_pi2
        global image_list_pi3
        global image_list_pi4
        global image_list_pi5
        global image_list_pi6

        def kafka_image(consumer, out_queue, latency_list, timestamp, camera_name, image_list):
            msg = next(consumer)
            message = msg[6].split(' chula ')
            now = int(round(time.time() * 1000))
            sending_time = message[1]
            time_diff = abs(now - int(float(sending_time)))
            stream = cStringIO.StringIO(message[2])
            out_queue.put(stream)
            print('The latency of' + camera_name+ ' is ' + str(time_diff) + 'ms')
            latency_list.append(str(time_diff))
            timestamp.append(str(sending_time))
            frame = message[0]
            image_list.append(frame)

        def show_image(default_consumer, my_queue, camera_name, latency_list, timestamp, image_list):
            try:
                kafka_image(default_consumer, my_queue, latency_list, timestamp, camera_name, image_list)
                print('reading message from default '+ camera_name)
            except:
                # print('message is not found and showing previous image ' + camera_name)
                pass

        t1 = threading.Thread(target=show_image, args=(local_consumer1, my_queue1, 'PhayaThai-1',latency_list_of_pi1, unix_timestamp_of_pi1, image_list_pi1, ))
        t2 = threading.Thread(target=show_image, args=(local_consumer2, my_queue2, 'PhayaThai-2',latency_list_of_pi2, unix_timestamp_of_pi2, image_list_pi2, ))
#        t3 = threading.Thread(target=show_image, args=(local_consumer3, my_queue3, 'PhayaThai-3',latency_list_of_pi3, unix_timestamp_of_pi3, image_list_pi3, ))
        t4 = threading.Thread(target=show_image, args=(local_consumer4, my_queue4, 'PhayaThai-4',latency_list_of_pi4, unix_timestamp_of_pi4, image_list_pi4, ))
#        t5 = threading.Thread(target=show_image, args=(local_consumer5, my_queue5, 'PhayaThai-5',latency_list_of_pi5, unix_timestamp_of_pi5, image_list_pi5, ))
#        t6 = threading.Thread(target=show_image, args=(local_consumer6, my_queue6, 'PhayaThai-6',latency_list_of_pi6, unix_timestamp_of_pi6, image_list_pi6, ))

        t1.start()
        t2.start()
#        t3.start()
        t4.start()
#        t5.start()
#        t6.start()

        dc = wx.PaintDC(self)

        try:
            self.bmp1 = wx.BitmapFromImage(wx.ImageFromStream(my_queue1.get_nowait()))
            dc.DrawBitmap(self.bmp1, 450, 630)
        except:
            pass

        try:
            self.bmp2 = wx.BitmapFromImage(wx.ImageFromStream(my_queue2.get_nowait()))
            dc.DrawBitmap(self.bmp2, 860, 630)
        except:
            pass

#        try:
#            self.bmp3 = wx.BitmapFromImage(wx.ImageFromStream(my_queue3.get_nowait()))
#            dc.DrawBitmap(self.bmp3, 1270, 630)
#        except:
#            pass

        try:
            self.bmp4 = wx.BitmapFromImage(wx.ImageFromStream(my_queue4.get_nowait()))
            dc.DrawBitmap(self.bmp4, 450, 380)
        except:
            pass

#        try:
#            self.bmp5 = wx.BitmapFromImage(wx.ImageFromStream(my_queue5.get_nowait()))
#            dc.DrawBitmap(self.bmp5, 860, 380)
#        except:
#            pass

#        try:
#            self.bmp6 = wx.BitmapFromImage(wx.ImageFromStream(my_queue6.get_nowait()))
#            dc.DrawBitmap(self.bmp6, 1270, 380)
#        except:
#            pass

#######################################################################################
class MyFrame(wx.Frame):
    """"""

    # ---------------------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="An image on a panel", size=(1920, 1080))
        panel = MyPanel(self)
        self.Show()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
