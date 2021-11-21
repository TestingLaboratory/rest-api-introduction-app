from rest_introduction_app.api.challenges.challenge_6.model import Storage

STORAGE_TYPE = "backpack"
MAX_ITEMS = 3

not_full_backpacks = [
    Storage(STORAGE_TYPE, MAX_ITEMS, []),
    Storage(STORAGE_TYPE, MAX_ITEMS, ["tent", "knife"]),
]

full_backpacks = [
    Storage(STORAGE_TYPE, MAX_ITEMS, ["tent", "knife", "lighter"]),
    Storage(STORAGE_TYPE, MAX_ITEMS, ["tent", "knife", "lighter", "camera"])
]
