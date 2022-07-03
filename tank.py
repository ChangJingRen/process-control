import numpy as np
from models.tank_model.disturbance import InflowDist


class Tank:
    "Conical tank"
    g = 9.81
    rho = 1000

    def __init__(
        self,
        max_height,
        max_radius,
	height,
	nom_height,
	nom_radius, 
        pipe_radius,
        max_level,
        min_level,
        init_level,
        dist,
        prev_tank=None,
    ):
        self.h = height
        self.r = nom_radius
	self.R = max_radius
	self.angel = atan(max_radius / max_height)
        self.A = nom_radius ** 2 * np.pi
	self.V = (np.pi * height ** 3 * nom_radius ** 2 * max_radius ** 2) / (3 *  max_height ** 2 )

        self.init_l = height * init_level
        self.level = self.init_l

        self.max = max_level * height
        self.min = min_level * height
        self.prev_q_out = 0

        self.A_pipe = pipe_radius ** 2 * np.pi
        self.add_dist = dist["add"]
        if dist["add"]:
            self.dist = InflowDist(
                nom_flow=dist["nom_flow"],
                var_flow=dist["var_flow"],
                max_flow=dist["max_flow"],
                min_flow=dist["min_flow"],
                add_step=dist["add_step"],
                step_flow=dist["step_flow"],
                step_time=dist["step_time"],
                pre_def_dist=dist["pre_def_dist"],
                max_time=dist["max_time"],
            )

    def change_level(self, dldt):
        self.level += dldt * self.h

    def get_dhdt(self, action, t, prev_q_out):
        "Calculates the change in water level"

        if self.add_dist:
            q_inn = self.dist.get_flow(t) + prev_q_out
        else:
            q_inn = prev_q_out

        f, A_pipe, g, l, delta_p, rho, r ,V ,A= self.get_params(action)
        q_out = f * A_pipe * np.sqrt(1 * g * l + delta_p / rho)

   	dq = q_inn - q_out
        new_level = dq * 3 / (A + 2 * np.pi * (R * h / H) ** 2)# Eq: 1
        return new_level, q_out

    def reset(self):
        "reset tank to initial liquid level"
        self.level = self.init_l

    def get_valve(self, action):
        "linear valve equation"
        return action

    def get_params(self, action):
        "collects the tanks parameters"
        f = self.get_valve(action)
        return f, self.A_pipe, Tank.g, self.level, 0, Tank.rho, self.r , self.V , self.A
