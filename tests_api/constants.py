BASE_URL = "http://0.0.0.0:8080"

# Challenge paths
REACTOR_PATH = "api/challenge/reactor"

# Messages
INFORMATION_MESSAGE = "You are the Tech Commander of RBMK reactor power plant. " \
                      "Your task is to perform the reactor test. " \
                      "Bring the power level above 1000 but below 1500 and keep the reactor Operational. " \
                      "Use /{key}/control_room/analysis to peek at reactor core. " \
                      "Use /{key}/control_room to see full info about the reactor. " \
                      "Check in at the /desk to get your key to control room. " \
                      "Put in fuel rods or pull out control rods to raise the power. " \
                      "Put in control rods or pull out fuel rods to decrease the power. " \
                      "There are 11 flags to find. Good luck Commander. "
CHECK_IN_MESSAGE = "Take the key to your control room. Keep it safe. " \
                   "use it as resource path to check on your RMBK-100 reactor! " \
                   "Use following: /{key}/control_room to gain knowledge how to operate reactor. " \
                   "You may see if the core is intact here: /{key}/reactor_core . " \
                   "If anything goes wrong push AZ-5 safety button to put all control rods in place!" \
                   "Good luck Commander."
CONTROL_ROOM_MESSAGE = f"Hello, Comrade .*? What would you like to see?"
DELETE_CONTROL_ROD_MESSAGE = "Right, .*?, Removing control rod at .*?!."
PLACE_CONTROL_ROD_MESSAGE = "Right, .*?, Adding control rod at .*?!."
MANIPULATE_AZ_5_MESSAGE = "Right, Comrade .*?, Reactor State is: .*?. Afraid of a meltdown, huh?"
LOOK_INTO_REACTOR_CORE_MESSAGE = ".*?, the core looks fine!"
ANALYSIS_MESSAGE = ".*?, the reactor is in state .*?! It's power is on level"
REMOVE_FUEL_ROD_MESSAGE = "Right, .*?, Removing fuel rod at .*?!."
PUT_FUEL_ROD_MESSAGE = "Right, .*?, Adding fuel rod at .*?!."
RESET_PROGRESS_MESSAGE = "Your reactor is good as new!"
CHECK_KEY_MESSAGE = "You can now proceed with the timeline reversal process."

# Flags
CHERENKOV_CHICKEN_FLAG = "{flag_cherenkov_chicken_.*?}"
CURIOUS_FLAG = "{flag_curious_arent_we_.*?}"
DIDNT_SEE_THE_GRAPHITE_FLAG = "${flag_you_didn't_see_the_graphite_because_it's_not_there}"
