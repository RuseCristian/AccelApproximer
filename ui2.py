import tkinter as tk


class INIEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INI Editor")

        # Create and set variables for each field
        self.torque_curve = {}
        self.engine_idle_rpm = tk.StringVar()
        self.engine_redline = tk.StringVar()
        self.drivetrain_gears = {}
        self.drivetrain_layout = tk.StringVar()
        self.drivetrain_loss = tk.StringVar()
        self.drivetrain_shifting_time = tk.StringVar()
        self.drivetrain_off_clutch = tk.StringVar()
        self.drivetrain_clutch_bite = tk.StringVar()
        self.drivetrain_gas_level = tk.StringVar()
        self.tire_width = tk.StringVar()
        self.tire_aspect = tk.StringVar()
        self.tire_radial = tk.StringVar()
        self.tire_mu = tk.StringVar()
        self.tire_roling_k = tk.StringVar()
        self.car_name = tk.StringVar()
        self.car_mass = tk.StringVar()
        self.car_front_weight_distribution = tk.StringVar()
        self.car_cd = tk.StringVar()
        self.car_frontal_area = tk.StringVar()
        self.car_air_density = tk.StringVar()
        self.car_lift_coeficient = tk.StringVar()
        self.car_downforce_total_area = tk.StringVar()

        # Create labels and entry widgets for each field
        self.create_torque_curve_section()
        self.create_engine_section()
        self.create_drivetrain_gears_section()
        self.create_drivetrain_section()
        self.create_tire_section()
        self.create_car_section()

        SVBar = tk.Scrollbar(self)
        SVBar.pack(side=tk.RIGHT,
                   fill="y")

        SHBar = tk.Scrollbar(self,
                             orient=tk.HORIZONTAL)
        SHBar.pack(side=tk.BOTTOM,
                   fill="x")

        # Create a button to save the data
        save_button = tk.Button(self, text="Save", command=self.save_data)
        save_button.pack()

    def create_torque_curve_section(self):
        torque_curve_frame = tk.LabelFrame(self, text="Torque Curve")
        torque_curve_frame.pack(padx=10, pady=10)

        tk.Label(torque_curve_frame, text="RPM").grid(row=0, column=0)
        tk.Label(torque_curve_frame, text="Torque (Nm)").grid(row=0, column=1)

        for i in range(1, 10):
            tk.Label(torque_curve_frame, text=1000 * i).grid(row=i, column=0)
            torque_entry = tk.Entry(torque_curve_frame)
            torque_entry.grid(row=i, column=1)
            self.torque_curve[1000 * i] = torque_entry

    def create_engine_section(self):
        engine_frame = tk.LabelFrame(self, text="Engine")
        engine_frame.pack(padx=10, pady=10)

        tk.Label(engine_frame, text="Idle RPM").grid(row=0, column=0)
        idle_rpm_entry = tk.Entry(engine_frame, textvariable=self.engine_idle_rpm)
        idle_rpm_entry.grid(row=0, column=1)

        tk.Label(engine_frame, text="Redline").grid(row=1, column=0)
        redline_entry = tk.Entry(engine_frame, textvariable=self.engine_redline)
        redline_entry.grid(row=1, column=1)

    def create_drivetrain_gears_section(self):
        drivetrain_gears_frame = tk.LabelFrame(self, text="Drivetrain Gears")
        drivetrain_gears_frame.pack(padx=10, pady=10)

        tk.Label(drivetrain_gears_frame, text="Gear Ratio").grid(row=0, column=0)
        tk.Label(drivetrain_gears_frame, text="Drivetrain Loss (%)").grid(row=0, column=1)

        for i in range(1, 6):
            tk.Label(drivetrain_gears_frame, text="Gear {}".format(i)).grid(row=i, column=0)
            gear_ratio_entry = tk.Entry(drivetrain_gears_frame)
            gear_ratio_entry.grid(row=i, column=1)
            self.drivetrain_gears[i] = gear_ratio_entry

    def create_drivetrain_section(self):
        drivetrain_frame = tk.LabelFrame(self, text="Drivetrain")
        drivetrain_frame.pack(padx=10, pady=10)

        tk.Label(drivetrain_frame, text="Layout").grid(row=0, column=0)
        layout_entry = tk.Entry(drivetrain_frame, textvariable=self.drivetrain_layout)
        layout_entry.grid(row=0, column=1)

        tk.Label(drivetrain_frame, text="Drivetrain Loss (%)").grid(row=1, column=0)
        drivetrain_loss_entry = tk.Entry(drivetrain_frame, textvariable=self.drivetrain_loss)
        drivetrain_loss_entry.grid(row=1, column=1)

        tk.Label(drivetrain_frame, text="Shifting Time (s)").grid(row=2, column=0)
        shifting_time_entry = tk.Entry(drivetrain_frame, textvariable=self.drivetrain_shifting_time)
        shifting_time_entry.grid(row=2, column=1)

        tk.Label(drivetrain_frame, text="Off Clutch RPM").grid(row=3, column=0)

        off_clutch_entry = tk.Entry(drivetrain_frame, textvariable=self.drivetrain_off_clutch)
        off_clutch_entry.grid(row=3, column=1)

        tk.Label(drivetrain_frame, text="Clutch Bite Point").grid(row=4, column=0)
        clutch_bite_entry = tk.Entry(drivetrain_frame, textvariable=self.drivetrain_clutch_bite)
        clutch_bite_entry.grid(row=4, column=1)

        tk.Label(drivetrain_frame, text="Gas Level").grid(row=5, column=0)
        gas_level_entry = tk.Entry(drivetrain_frame, textvariable=self.drivetrain_gas_level)
        gas_level_entry.grid(row=5, column=1)

    def create_tire_section(self):
        tire_frame = tk.LabelFrame(self, text="Tire")
        tire_frame.pack(padx=10, pady=10)

        tk.Label(tire_frame, text="Width (mm)").grid(row=0, column=0)
        tire_width_entry = tk.Entry(tire_frame, textvariable=self.tire_width)
        tire_width_entry.grid(row=0, column=1)

        tk.Label(tire_frame, text="Aspect Ratio").grid(row=1, column=0)
        tire_aspect_entry = tk.Entry(tire_frame, textvariable=self.tire_aspect)
        tire_aspect_entry.grid(row=1, column=1)

        tk.Label(tire_frame, text="Radius (inches)").grid(row=2, column=0)
        tire_radial_entry = tk.Entry(tire_frame, textvariable=self.tire_radial)
        tire_radial_entry.grid(row=2, column=1)

        tk.Label(tire_frame, text="Friction Coefficient (µ)").grid(row=3, column=0)
        tire_mu_entry = tk.Entry(tire_frame, textvariable=self.tire_mu)
        tire_mu_entry.grid(row=3, column=1)

        tk.Label(tire_frame, text="Rolling Resistance Coefficient (k)").grid(row=4, column=0)
        tire_roling_k_entry = tk.Entry(tire_frame, textvariable=self.tire_roling_k)
        tire_roling_k_entry.grid(row=4, column=1)

    def create_car_section(self):
        car_frame = tk.LabelFrame(self, text="Car")
        car_frame.pack(padx=10, pady=10)

        tk.Label(car_frame, text="Car Name").grid(row=0, column=0)
        car_name_entry = tk.Entry(car_frame, textvariable=self.car_name)
        car_name_entry.grid(row=0, column=1)

        tk.Label(car_frame, text="Car Mass (kg)").grid(row=1, column=0)
        car_mass_entry = tk.Entry(car_frame, textvariable=self.car_mass)
        car_mass_entry.grid(row=1, column=1)

        tk.Label(car_frame, text="Front Weight Distribution (%)").grid(row=2, column=0)
        front_weight_distribution_entry = tk.Entry(car_frame, textvariable=self.car_front_weight_distribution)
        front_weight_distribution_entry.grid(row=2, column=1)

        tk.Label(car_frame, text="Cd Value").grid(row=3, column=0)
        car_cd_entry = tk.Entry(car_frame, textvariable=self.car_cd)
        car_cd_entry.grid(row=3, column=1)

        tk.Label(car_frame, text="Frontal Area (m^2)").grid(row=4, column=0)
        car_frontal_area_entry = tk.Entry(car_frame, textvariable=self.car_frontal_area)
        car_frontal_area_entry.grid(row=4, column=1)

        tk.Label(car_frame, text="Air Density (kg/m^3)").grid(row=5, column=0)
        car_air_density_entry = tk.Entry(car_frame, textvariable=self.car_air_density)
        car_air_density_entry.grid(row=5, column=1)

        tk.Label(car_frame, text="Lift Coefficient").grid(row=6, column=0)
        car_lift_coeficient_entry = tk.Entry(car_frame, textvariable=self.car_lift_coeficient)
        car_lift_coeficient_entry.grid(row=6, column=1)

        tk.Label(car_frame, text="Downforce Total Area (m^2)").grid(row=7, column=0)
        car_downforce_total_area_entry = tk.Entry(car_frame, textvariable=self.car_downforce_total_area)
        car_downforce_total_area_entry.grid(row=7, column=1)

    def save_data(self):
        # You can use the .get() method of the StringVar objects to retrieve the data
        # entered by the user and write it to a file, or do whatever you need to do with it
        pass



app = INIEditor()
app.mainloop()
