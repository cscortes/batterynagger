import time
from tkinter import *

from lib.cbatterynagger import NoticeLogic
from lib.PConfig import thePConfig
from lib.projlog import log


class GUI(object):
    root = None

    def __init__(self):
        self.idx = 0
        self.myfont = ("Helvetica", 16)
        self.background = "#B0C4DE"
        
        GUI.root = Tk()
        GUI.root.geometry("+%d+%d" % (10,10))
        self.setup()
        GUI.root.after(5000, self.minimize_app)
        self.run()

    def minimize_app(self):
        # to minimize on startup
        GUI.root.iconify()

    def window_background(self):
        GUI.root.title("Battery Nagger")
        GUI.root.configure(background=self.background)
        
    def setup(self):
        self.window_background()

        self.photo = PhotoImage(file="images/battery_nagger.png")
        label = Label(GUI.root, image=self.photo, fg=self.background, bg=self.background)
        label.grid(row=0,columnspan=3, pady=25, padx=20)

        self.labels()
        self.setup_flashing_light()
        self.setup_settings()
        self.warning()

    def setup_settings(self):
        self.settings_link = Label(GUI.root, text="Settings", font=self.myfont, fg="white", bg="gray" )
        self.settings_link.grid(row=4, column=0,ipadx=5, ipady=5, pady=10 )
        self.settings_link.bind("<Button-1>", self.popup_settings)

    def setup_light_frames(self):
        self.red_frames = [PhotoImage(file='images/light_red.gif',format = 'gif -index %i' %(i)) for i in range(2)]
        self.yellow_frames = [PhotoImage(file='images/light_yellow.gif',format = 'gif -index %i' %(i)) for i in range(2)]
        self.green_frames = [PhotoImage(file='images/light_green.gif') for i in range(2)]
        self.use_green_light()

    def use_green_light(self):
        self.frames = self.green_frames

    def use_red_light(self):
        self.frames = self.red_frames

    def use_yellow_light(self):
        self.frames = self.yellow_frames

    def update_flashing_light(self):
        self.idx = (self.idx + 1) % 2
        self.flashing_button.configure(image=self.frames[self.idx])
        GUI.root.after(300, self.update_flashing_light)

    def setup_flashing_light(self):
        self.setup_light_frames()
        self.flashing_button = Label(GUI.root,fg=self.background, bg=self.background)
        self.flashing_button.grid(row=1, column=0, rowspan=2 )
        GUI.root.after(300, self.update_flashing_light)

    def create_label_main(self, row, col,  text, side = E, padx=10, pady=10):
        lab = Label(GUI.root, text=text,   font=self.myfont )
        lab.grid(row=row, column=col, sticky=side, padx=padx, pady=pady)
        return lab

    def labels(self):
        self.create_label_main(1,1,"Current Time:")
        self.create_label_main(2,1,"Next Check:"  )
        self.create_label_main(3,1,"Batt State:" )
        self.create_label_main(4,1,"Percent:"     )

        self.val1 = self.create_label_main(1,2,"N/A", side=W )
        self.val2 = self.create_label_main(2,2,"N/A", side=W )
        self.val3 = self.create_label_main(3,2,"N/A", side=W )
        self.val4 = self.create_label_main(4,2,"N/A", side=W )

    def warning(self):
        self.bottomlab = Label(GUI.root, text="  Notification: UPDATING ...  ", pady=20, width=30, fg="white", bg="purple", font=("Helvetica", 20))
        self.bottomlab.grid(row=5, columnspan=3 )

    def run(self):
        GUI.root.after(2000, self.go_check_the_battery)
        GUI.root.mainloop()

    def go_check_the_battery(self):
        import datetime 
        now : datetime.datetime = datetime.datetime.now()
        
        # .strftime("%H:%M:%S")
        # ---------------------------------------------------
        self.val1["text"] = now.strftime("%H:%M:%S")
        self.val2["text"] = (now + datetime.timedelta(seconds = prog.get_delay())).strftime("%H:%M:%S")
        self.val3["text"] = prog.get_ischarging()
        self.val4["text"] = "{}%".format(prog.get_percent())
        self.bottomlab["text"] = "Notification: {}".format(prog.get_notification())

        notif = prog.get_notification().lower()
        log.debug(notif)

        if ("fatal" in notif):
            self.bottomlab["bg"] = "red"
            self.bottomlab["fg"] = "white"
            GUI.root.lift()
            self.use_red_light()
        elif ('critical' in notif):
            self.bottomlab["bg"] = "orange"
            self.bottomlab["fg"] = "white"
            self.use_yellow_light()
        elif ("warn" in notif):
            self.bottomlab["bg"] = "yellow"
            self.bottomlab["fg"] = "black"
            self.use_yellow_light()
        else :
            self.bottomlab["bg"] = "gray"
            self.bottomlab["fg"] = "white"
            self.use_green_light()

        # ---------------------------------------------------
        if (prog.should_sleep()):
            GUI.root.after(prog.get_delay() * 1000, self.go_check_the_battery)

    def create_label_settings(self, row, col,  text, side = E, padx=10, pady=10):
        lab = Label(self.setting_root, text = text,   font=self.myfont )
        lab.grid(row=row, column=col, sticky=side, padx=padx, pady=pady)
        return lab

    def create_entry(self, row, col, val, side=W, padx=10, pady=5):
        entry = Entry(self.setting_root, justify=RIGHT, width=7, font=self.myfont )
        entry.insert (0, str(val))
        entry.grid(row=row, column=col, sticky=side, padx=padx, pady=pady)
        return entry

    def popup_settings(self, event):
        self.setting_root = Toplevel()
        self.setting_root.geometry("+%d+%d" % (event.x_root + 5, event.y_root - 200))
        self.setting_root.configure(background=self.background)

        lab0 = Label(self.setting_root, text="Settings", pady=20, width=25, 
            fg="white", bg="darkgrey", font=("Helvetica", 24))
        lab0.grid(row=0, columnspan=5)

        self.create_label_settings(1, 2, "level (%)", side=W)
        self.create_label_settings(1, 3, "interval (s)", side=W)

        self.create_label_settings(2, 1, "Fatal:")
        self.create_label_settings(3, 1, "Critical:" )
        self.create_label_settings(4, 1, "Warning:")

        # Configure entry text boxes
        self.settings_fatal = self.create_entry(2,2, thePConfig.get_fatal_level())
        self.settings_crit = self.create_entry(3,2, thePConfig.get_critical_level())
        self.settings_warn = self.create_entry(4,2, thePConfig.get_warning_level())

        # Configure entry text boxes
        self.settings_fatal_interval = self.create_entry(2,3, thePConfig.get_fatal_timeout())
        self.settings_crit_interval  = self.create_entry(3,3, thePConfig.get_critical_timeout())
        self.settings_warn_interval  = self.create_entry(4,3, thePConfig.get_warning_timeout())

        self.okay_cancel_buttons()
        self.setting_root.focus_force()

    def okay_cancel_buttons(self):
        but1 = Button(self.setting_root, text="Cancel", fg="white", bg="black", padx=20, pady=5, font=self.myfont, command=self.cancel_settings )
        but2 = Button(self.setting_root, text="Okay", fg="white", bg="black", padx=20, pady=5, font=self.myfont , command=self.set_settings)
        but1.grid(row=5, column=1, columnspan=2, padx=10, pady=20 , sticky=E)
        but2.grid(row=5, column=3, columnspan=2, padx=10, pady=20, sticky=W )

    def cancel_settings(self):
        self.setting_root.destroy()

    def set_settings(self):
        thePConfig.set_warning_level(self.settings_warn.get())
        thePConfig.set_critical_level(self.settings_crit.get())
        thePConfig.set_fatal_level(self.settings_fatal.get())

        thePConfig.set_warning_timeout(self.settings_warn_interval.get())
        thePConfig.set_critical_timeout(self.settings_crit_interval.get())
        thePConfig.set_fatal_timeout(self.settings_fatal_interval.get())

        thePConfig.update()
        self.cancel_settings()

prog = NoticeLogic()
prog.should_sleep()
gui = GUI()
