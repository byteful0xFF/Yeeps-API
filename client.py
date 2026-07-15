import requests
from datetime import datetime, timedelta


class API:
    def __init__(self, api_key, url="https://yeeps-proxy.onrender.com/yeeps"):
        self.url = url

        try:
            self.oculus_id, self.mobile_code = api_key.split("|", 1)
        except ValueError:
            raise ValueError(
                "API key must be in the format username|mobileCode"
            )

    def login(self):
        response = requests.post(
            self.url,
            json={
                "oculusID": self.oculus_id,
                "mobileCode": self.mobile_code
            },
            timeout=120
        )

        response.raise_for_status()

        return LoginResponse(response.json())


class LoginResponse:
    def __init__(self, data):
        self.raw = data
        self.userData = UserData(data)


class UserData:
    def __init__(self, data):
        self._data = data

    @property
    def username(self):
        return self._data.get("oculusID", "Unknown")

    @property
    def mobile_code(self):
        return self._data.get("mobileCode", "Unknown")

    @property
    def first_login(self):
        return self._data.get("firstLogin", "Unknown")

    @property
    def timesLoggedOn(self):
        return self._data.get("sessionCount", "Unknown")

    @property
    def cachedBanReason(self):
        return self._data.get("banReason", "Unknown")

    @property
    def cachedWarnReason(self):
        return self._data.get("warnReason", "Unknown")

    @property
    def banHoursLeft(self):
        return self._data.get("remainingBanHours", "Unknown")

    @property
    def isMuteBannedRaw(self):
        return self._data.get("isMutebanned", "Unknown")

    @property
    def banReason(self):
        if (self._data.get("remainingBanHours", "Unknown") == "0"):
            return f"{self.username} is not currently banned right now."

        if (self._data.get("remainingBanHours", "Unknown") == "Unknown"):
            return f"Failed to get ban status for {self.username}"

        return f"{self.username} is banned for {self.cachedBanReason} and has {self.banHoursLeft} hours left until they are unbanned."

    @property
    def warnReason(self):
        if (self._data.get("hasPendingWarning", "Unknown") == "0"):
            return f"{self.username} is not currently warned right now."

        if (self._data.get("hasPendingWarning", "Unknown") == "Unknown"):
            return f"Failed to get warning status for {self.username}"

        return f"{self.username} got warned for {self.cachedWarnReason}."

    @property
    def isMuteBanned(self):
        if (self._data.get("isMutebanned", "Unknown") == "0"):
            return f"{self.username} is not currently mute banned right now."

        return f"{self.username} is currently mute / mic banned."


    # -------------------------
    # Raw data helpers
    # -------------------------

    def getListRaw(self, key):
        """
        Returns the raw list from the API response.
        
        Example:
        userData.getListRaw("cw_admin")
        """
        return self._data.get(key, [])

    def getListText(self, key, displayName, errorDisplayName):
        """
        Returns a formatted version of a list.
        
        Example:
        userData.getListText("cw_admin", "CW admins")
        """
        items = self.getListRaw(key)

        if not items:
            return f"Player {self.username} {errorDisplayName}."

        return (
            f"Player {self.username} {displayName}:\n"
            + "\n".join(items)
        )

    # -------------------------
    # Pets
    # -------------------------

    @property
    def petsRaw(self):
        """
        Returns the raw pets JSON.
        """
        return self._data.get("pets", {})

    @property
    def pets(self):
        """
        Returns parsed Pet objects.
        """
        return [
            Pet(pet_id, pet_data)
            for pet_id, pet_data in self.petsRaw.items()
        ]

    # -------------------------
    # Other Lists
    # -------------------------

    @property
    def seenMessagesRaw(self):
        """
        Returns the raw cw_admin JSON list.
        """
        return self.getListRaw("seenMessages")

    @property
    def seenMessages(self):
        """
        Returns formatted CW owner (cw_admin) list.
        """
        return self.getListText("seenMessages", "has seen these one-time messages:", "has not seen any one-time messages.")

    @property
    def ownerInCwsRaw(self):
        """
        Returns the raw cw_admin JSON list.
        """
        return self.getListRaw("cw_admin")

    @property
    def ownerInCws(self):
        """
        Returns formatted CW owner (cw_admin) list.
        """
        return self.getListText("cw_admin", "is the owner of CWs:", "is not the owner of any CWs.")

    @property
    def staffInCwsRaw(self):
        """
        Returns the raw cw_staff JSON list.
        """
        return self.getListRaw("cw_staff")

    @property
    def staffInCws(self):
        """
        Returns formatted CW staff list.
        """
        return self.getListText("cw_staff", "is staff in CWs:", "is not staff in any CWs.")

    @property
    def vipInCwsRaw(self):
        """
        Returns the raw cw_aVIP JSON list.
        """
        return self.getListRaw("cw_vip")

    @property
    def vipInCws(self):
        """
        Returns formatted CW VIP list.
        """
        return self.getListText("cw_vip", "is VIP in CWs:", "is not VIP in any CWs.")

    @property
    def favoriteCwsRaw(self):
        """
        Returns the raw cw_admin JSON list.
        """
        return self.getListRaw("cw_favorite")

    @property
    def favoriteCws(self):
        """
        Returns formatted CW admin list.
        """
        return self.getListText("cw_favorite", "has favorited CWs:", "has not favorited any CWs.")

    @property
    def analyticEventKeys(self):
        """
        Returns the raw analyticEventKeys JSON list.
        """
        return self.getListRaw("analyticEventKeys")

    # -------------------------
    # Challenge Redeem Times
    # -------------------------

    @property
    def lastChallengeRedeemedTime_login(self):
        """
        Returns the last time the player redeemed the login Buttcoin reward.
        """
        return self._data.get("lastChallengeRedeemedTime_login", "")

    @property
    def lastChallengeRedeemedTime_easy(self):
        """
        Returns the last time the player completed the easy challenge.
        Easy challenges reward Buttcoins.
        """
        return self._data.get("lastChallengeRedeemedTime_easy", "")

    @property
    def lastChallengeRedeemedTime_hard(self):
        """
        Returns the last time the player completed the hard challenge.
        Hard challenges reward Buttcoins.
        """
        return self._data.get("lastChallengeRedeemedTime_hard", "")

    # -------------------------
    # Unlocks / Ownership
    # -------------------------

    @property
    def hasCreatorPack(self):
        """
        Returns whether the player owns the Creator Pack.

        1 = owns Creator Pack
        0 = does not own Creator Pack
        """
        return self._data.get("hasCreatorPack", 0) == 1

    @property
    def hasUnlockedPrivateRooms(self):
        """
        Returns whether the player has unlocked Private Rooms.

        1 = unlocked
        0 = locked
        """
        return self._data.get("hasUnlockedPrivateRooms", 0) == 1

    @property
    def hasPendingMobileLogin(self):
        """
        Returns whether the player has not accepted the Mobile Login prompt.

        1 = pending mobile login
        0 = no pending mobile login
        """
        return self._data.get("hasPendingMobileLogin", 0) == 1

    # -------------------------
    # Currency
    # -------------------------

    @property
    def buttcoinCount(self):
        """
        Returns the player's Buttcoin amount.
        """
        return self._data.get("currency", 0)

    @property
    def silverBeansCount(self):
        """
        Returns the player's Silver Bean amount.
        """
        return self._data.get("beans", 0)
