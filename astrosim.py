
import json
import os


# ==========================================
# 1. BASE CLASS: SPACECRAFT
# ==========================================

class Spacecraft:

    def __init__(self, spacecraft_id, name, fuel_capacity,
                 payload_capacity, max_gravity):

        self.__spacecraft_id = spacecraft_id
        self.__name = name
        self.__fuel_capacity = fuel_capacity
        self.__payload_capacity = payload_capacity
        self.__max_gravity = max_gravity

    # Encapsulation: getter methods

    def get_id(self):
        return self.__spacecraft_id

    def get_name(self):
        return self.__name

    def get_fuel_capacity(self):
        return self.__fuel_capacity

    def get_payload_capacity(self):
        return self.__payload_capacity

    def get_max_gravity(self):
        return self.__max_gravity

    # These methods will be overridden by child classes

    def get_type(self):
        return "Generic Spacecraft"

    def get_fuel_rate(self):
        return 0.0

    def get_speed(self):
        return 0.0

    def calculate_fuel(self, distance, gravity, payload):

        gravity_factor = 1 + gravity / 50
        payload_factor = 1 + payload / 1000

        return (distance * self.get_fuel_rate()
                * gravity_factor * payload_factor)

    def to_dict(self):

        return {
            "id": self.__spacecraft_id,
            "name": self.__name,
            "fuel_capacity": self.__fuel_capacity,
            "payload_capacity": self.__payload_capacity,
            "max_gravity": self.__max_gravity,
            "type": self.get_type()
        }


# ==========================================
# 2. CHILD CLASS: CHEMICAL ROCKET
# ==========================================

class ChemicalRocket(Spacecraft):

    def get_type(self):
        return "Chemical Rocket"

    def get_fuel_rate(self):
        return 0.18

    def get_speed(self):
        return 5.0


# ==========================================
# 3. CHILD CLASS: ION DRIVE
# ==========================================

class IonDrive(Spacecraft):

    def get_type(self):
        return "Ion Drive"

    def get_fuel_rate(self):
        return 0.07

    def get_speed(self):
        return 2.0


# ==========================================
# 4. CHILD CLASS: NUCLEAR SPACECRAFT
# ==========================================

class NuclearSpacecraft(Spacecraft):

    def get_type(self):
        return "Nuclear Thermal"

    def get_fuel_rate(self):
        return 0.12

    def get_speed(self):
        return 4.0


# ==========================================
# 5. PLANET CLASS
# ==========================================

class Planet:

    def __init__(self, name, distance, gravity):

        self.__name = name
        self.__distance = distance
        self.__gravity = gravity

    def get_name(self):
        return self.__name

    def get_distance(self):
        return self.__distance

    def get_gravity(self):
        return self.__gravity

    def display(self):

        print("\nDestination:", self.__name)
        print("Distance:", self.__distance, "million km")
        print("Gravity:", self.__gravity, "m/s^2")


# ==========================================
# 6. MISSION CLASS
# ==========================================

class Mission:

    def __init__(self, mission_id, spacecraft, planet, payload):

        self.__mission_id = mission_id
        self.__spacecraft = spacecraft
        self.__planet = planet
        self.__payload = payload
        self.__status = "NOT STARTED"
        self.__fuel_required = 0
        self.__travel_time = 0

    def simulate(self):

        self.__fuel_required = self.__spacecraft.calculate_fuel(
            self.__planet.get_distance(),
            self.__planet.get_gravity(),
            self.__payload
        )

        self.__travel_time = (
            self.__planet.get_distance()
            / self.__spacecraft.get_speed()
        )

        # Check mission requirements

        fuel_ok = (
            self.__fuel_required
            <= self.__spacecraft.get_fuel_capacity()
        )

        payload_ok = (
            self.__payload
            <= self.__spacecraft.get_payload_capacity()
        )

        gravity_ok = (
            self.__planet.get_gravity()
            <= self.__spacecraft.get_max_gravity()
        )

        if fuel_ok and payload_ok and gravity_ok:
            self.__status = "SUCCESS"
        else:
            self.__status = "ABORTED"

        return self.__status

    def get_id(self):
        return self.__mission_id

    def get_status(self):
        return self.__status

    def display_result(self):

        print("\n========== MISSION REPORT ==========")

        print("Mission ID:", self.__mission_id)
        print("Spacecraft:", self.__spacecraft.get_name())
        print("Spacecraft Type:", self.__spacecraft.get_type())
        print("Destination:", self.__planet.get_name())

        print("Payload:", self.__payload, "kg")

        print("Fuel Required:",
              round(self.__fuel_required, 2), "units")

        print("Available Fuel:",
              self.__spacecraft.get_fuel_capacity(), "units")

        print("Estimated Travel Time:",
              round(self.__travel_time, 2), "days")

        print("Mission Status:", self.__status)

        if self.__status == "ABORTED":

            print("Reason(s):")

            if self.__fuel_required > self.__spacecraft.get_fuel_capacity():
                print("- Insufficient fuel capacity")

            if self.__payload > self.__spacecraft.get_payload_capacity():
                print("- Payload exceeds spacecraft capacity")

            if self.__planet.get_gravity() > self.__spacecraft.get_max_gravity():
                print("- Destination gravity exceeds spacecraft limit")

        print("====================================")

    def to_dict(self):

        return {
            "mission_id": self.__mission_id,
            "spacecraft_id": self.__spacecraft.get_id(),
            "spacecraft_name": self.__spacecraft.get_name(),
            "spacecraft_type": self.__spacecraft.get_type(),
            "planet": self.__planet.get_name(),
            "payload": self.__payload,
            "fuel_required": self.__fuel_required,
            "travel_time": self.__travel_time,
            "status": self.__status
        }


# ==========================================
# 7. MAIN APPLICATION CLASS
# ==========================================

class AstroSim:

    SPACECRAFT_FILE = "spacecraft.json"
    MISSION_FILE = "missions.json"

    def __init__(self):

        self.spacecrafts = []
        self.missions = []

        self.planets = [
            Planet("Mercury", 91.7, 3.7),
            Planet("Venus", 41.4, 8.87),
            Planet("Mars", 78.3, 3.71),
            Planet("Jupiter", 628.7, 24.79),
            Planet("Saturn", 1275.0, 10.44)
        ]

        self.load_data()

    # --------------------------------------
    # FILE HANDLING
    # --------------------------------------

    def save_data(self):

        spacecraft_data = [
            spacecraft.to_dict()
            for spacecraft in self.spacecrafts
        ]

        mission_data = self.missions

        with open(self.SPACECRAFT_FILE, "w") as file:
            json.dump(spacecraft_data, file, indent=4)

        with open(self.MISSION_FILE, "w") as file:
            json.dump(mission_data, file, indent=4)

    def load_data(self):

        if os.path.exists(self.SPACECRAFT_FILE):

            try:
                with open(self.SPACECRAFT_FILE, "r") as file:
                    data = json.load(file)

                for record in data:

                    spacecraft_type = record["type"]

                    classes = {
                        "Chemical Rocket": ChemicalRocket,
                        "Ion Drive": IonDrive,
                        "Nuclear Thermal": NuclearSpacecraft
                    }

                    if spacecraft_type not in classes:
                        continue

                    spacecraft = classes[spacecraft_type](
                        record["id"],
                        record["name"],
                        record["fuel_capacity"],
                        record["payload_capacity"],
                        record["max_gravity"]
                    )

                    self.spacecrafts.append(spacecraft)

            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                print("Warning: Spacecraft data could not be loaded.")

        if os.path.exists(self.MISSION_FILE):

            try:
                with open(self.MISSION_FILE, "r") as file:
                    data = json.load(file)

                for record in data:
                    self.missions.append(record)

            except (json.JSONDecodeError, KeyError, TypeError):
                print("Warning: Mission data could not be loaded.")

    # --------------------------------------
    # ID GENERATION
    # --------------------------------------

    def generate_spacecraft_id(self):

        if not self.spacecrafts:
            return 101

        return max(
            spacecraft.get_id()
            for spacecraft in self.spacecrafts
        ) + 1

    def generate_mission_id(self):

        if not self.missions:
            return 1001

        return max(
            mission["mission_id"]
            for mission in self.missions
        ) + 1

    # --------------------------------------
    # REGISTER SPACECRAFT
    # --------------------------------------

    def register_spacecraft(self):

        print("\n====== REGISTER SPACECRAFT ======")

        name = input("Enter spacecraft name: ").strip()

        if not name:
            print("Spacecraft name cannot be empty.")
            return

        print("\nSelect spacecraft type:")
        print("1. Chemical Rocket")
        print("2. Ion Drive")
        print("3. Nuclear Thermal")

        choice = input("Enter choice: ").strip()

        spacecraft_types = {
            "1": (ChemicalRocket, 350, 500, 20),
            "2": (IonDrive, 180, 200, 15),
            "3": (NuclearSpacecraft, 280, 800, 30)
        }

        if choice not in spacecraft_types:
            print("Invalid spacecraft type.")
            return

        spacecraft_class, fuel, payload, gravity = spacecraft_types[choice]

        spacecraft = spacecraft_class(
            self.generate_spacecraft_id(),
            name,
            fuel,
            payload,
            gravity
        )

        self.spacecrafts.append(spacecraft)
        self.save_data()

        print("\nSpacecraft registered successfully!")
        print("Spacecraft ID:", spacecraft.get_id())

    # --------------------------------------
    # DISPLAY SPACECRAFT
    # --------------------------------------

    def view_spacecraft(self):

        if not self.spacecrafts:
            print("\nNo spacecraft registered.")
            return

        print("\n========== SPACECRAFT FLEET ==========")

        for spacecraft in self.spacecrafts:

            print("\nID:", spacecraft.get_id())
            print("Name:", spacecraft.get_name())
            print("Type:", spacecraft.get_type())

            print("Fuel Capacity:",
                  spacecraft.get_fuel_capacity())

            print("Payload Capacity:",
                  spacecraft.get_payload_capacity())

            print("Maximum Gravity:",
                  spacecraft.get_max_gravity())

    # --------------------------------------
    # DISPLAY PLANETS
    # --------------------------------------

    def view_planets(self):

        print("\n========== DESTINATIONS ==========")

        for i, planet in enumerate(self.planets, start=1):

            print("\n", i, ".", planet.get_name())
            print("Distance:", planet.get_distance(),
                  "million km")
            print("Gravity:", planet.get_gravity(), "m/s^2")

    # --------------------------------------
    # LAUNCH MISSION
    # --------------------------------------

    def launch_mission(self):

        if not self.spacecrafts:
            print("\nRegister a spacecraft first.")
            return

        print("\n========== LAUNCH MISSION ==========")

        self.view_spacecraft()

        try:
            spacecraft_id = int(
                input("\nEnter spacecraft ID: ")
            )

        except ValueError:
            print("Invalid spacecraft ID.")
            return

        spacecraft = None

        for item in self.spacecrafts:

            if item.get_id() == spacecraft_id:
                spacecraft = item
                break

        if spacecraft is None:
            print("Spacecraft not found.")
            return

        self.view_planets()

        try:
            planet_choice = int(
                input("\nSelect destination number: ")
            )

            if planet_choice < 1 or planet_choice > len(self.planets):
                print("Invalid destination.")
                return

            payload = float(
                input("Enter payload weight in kg: ")
            )

            if payload < 0:
                print("Payload cannot be negative.")
                return

        except ValueError:
            print("Please enter valid numeric values.")
            return

        destination = self.planets[planet_choice - 1]

        mission = Mission(
            self.generate_mission_id(),
            spacecraft,
            destination,
            payload
        )

        mission.simulate()
        mission.display_result()

        self.missions.append(mission.to_dict())
        self.save_data()

    # --------------------------------------
    # MISSION HISTORY
    # --------------------------------------

    def view_history(self):

        if not self.missions:
            print("\nNo mission history available.")
            return

        print("\n========== MISSION HISTORY ==========")

        for mission in self.missions:

            print("\nMission ID:", mission["mission_id"])
            print("Spacecraft:", mission["spacecraft_name"])
            print("Destination:", mission["planet"])

            print("Fuel Used:",
                  round(mission["fuel_required"], 2))

            print("Status:", mission["status"])

    # --------------------------------------
    # MAIN MENU
    # --------------------------------------

    def menu(self):

        while True:

            print("\n===================================")
            print("          ASTROSIM")
            print("     SPACE MISSION SIMULATOR")
            print("===================================")

            print("1. Register Spacecraft")
            print("2. View Spacecraft Fleet")
            print("3. View Available Planets")
            print("4. Launch Space Mission")
            print("5. View Mission History")
            print("6. Exit")

            choice = input("\nEnter your choice: ").strip()
            print("You entered:", repr(choice))

            if choice == "1":
                self.register_spacecraft()

            elif choice == "2":
                self.view_spacecraft()

            elif choice == "3":
                self.view_planets()

            elif choice == "4":
                self.launch_mission()

            elif choice == "5":
                self.view_history()

            elif choice == "6":
                self.save_data()
                print("\nAstroSim shutting down.")
                print("Mission records saved successfully.")
                break

            else:
                print("\nInvalid choice. Try again.")


# ==========================================
# 8. PROGRAM EXECUTION
# ==========================================

if __name__ == "__main__":

    application = AstroSim()
    application.menu()
