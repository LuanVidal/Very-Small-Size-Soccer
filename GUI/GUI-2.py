import tkinter
import tkinter.messagebox
import customtkinter
import subprocess
from PIL import Image, ImageTk
import PIL 
import cv2

customtkinter.set_appearance_mode("System")  # Modos: Dark e light
customtkinter.set_default_color_theme("blue")  # Temas: 


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("VSS - Futebol de robôs")
        #self.iconbitmap('./img/if1.ico')
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,width=180,corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ Lada Esquerdo ============

        # Configuração do Grid (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   
        self.frame_left.grid_rowconfigure(5, weight=1)  
        self.frame_left.grid_rowconfigure(8, minsize=20)   
        self.frame_left.grid_rowconfigure(11, minsize=10) 

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="VSS - Futebol de robôs", text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Start simulation",
                                                command=self.button_event)

        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Stop simulation",
                                                command=self.button_event_fim)

        self.button_2.grid(row=3, column=0, pady=10, padx=20)


        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Start Cam",
                                                command=self.open_camera)

        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="GUI Appearance:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)

        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ Lado Direito ============

        # Configuração Grid (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ Centro ============

        # Configuração Grid (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   height=100,
                                                   corner_radius=6,  
                                                   fg_color=("white"),  
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ Lado Direito ============

        self.radio_var = tkinter.IntVar(value=0)


        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=1,
                                                number_of_steps=1,
                                                command=self.progressbar.set)

        self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
                                                command=self.progressbar.set)
        self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=["Todos no ataque", "Moderado", "Recuado"])

        self.combobox_1.grid(row=0, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="lack")
        self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="penalty")
        self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Set V e W")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="set var",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")
        #self.button_3.configure(state="disabled", text="Disabled CTkButton")
        self.combobox_1.set("game style")
        self.slider_1.set(0.2)
        self.slider_2.set(0.7)
        self.progressbar.set(0.5)
        #self.radio_button_3.configure(state=tkinter.DISABLED)
        #self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        self.check_box_2.select()

    # Função inicia o ros e manda os paramentos pro carrinho
    def button_event(self):
        subprocess.run(["roscore"])
        subprocess.run(["rosrun" , "rosesp32", "test_rosesp32.py"])

    def button_event_fim(self):
        subprocess.run(["^C"])

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()
    
    def open_camera(self):
            # Capture the video frame by frame

            _, frame = vid.read()
        
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
            captured_image = Image.fromarray(opencv_image)
        
            photo_image = ImageTk.PhotoImage(image=captured_image)
        
            self.label_info_1.photo_image = photo_image
            self.label_info_1.configure(image=photo_image)
        
            self.label_info_1.after(10, self.open_camera)
    
    

if __name__ == "__main__":
    app = App()
    vid = cv2.VideoCapture(1)

    width, height = 800, 600
    
    # Set the width and height

    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    app.mainloop()
    