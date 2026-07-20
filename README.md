# Yeeps API
Yeeps API is an API for the hit VR game Yeeps: Hide and Seek. It is made using the yeeps-proxy backend. It is 100% developed by **Byteful** (aka carbon612 or 0xFF). Developed fully in python, it is the first Yeeps API to be coded in python.


---

# Yeeps Python SDK Documentation

## Installation

```text
pip install yeeps
```
---

# Getting Started

Create an API instance using your API key.

The API key format is:

```text
metaUsername|mobileCode
```
so for me, an example would be
```text
byteful|1234
```
This is your warning to ***NEVER*** share your mobile code. It allows people to login to your account on the mobile app, and buy stuff you didn&lsquo;t need! They can also donate to community worlds, so they can donate to their own community world, **GIVING THEM YOUR MONEY!**
The one I put here (1234) is a fake one. It is not a real code.

# Logging In

Call `.login()` to retrieve the player's data.

```python
login = api.login()

userData = login.userData
```

The raw JSON response is available through:

```python
login.raw
```

---

# Account Information

| Property                    | Description               |
| --------------------------- | ------------------------- |
| `userData.username`         | Oculus username           |
| `userData.mobile_code`      | Mobile login code         |
| `userData.first_login`      | First login date          |
| `userData.timesLoggedOn`    | Total login count (VR & Mobile [?])         |
| `userData.cachedBanReason`  | Raw cached ban reason     |
| `userData.cachedWarnReason` | Raw cached warning reason |

Example:

```python
print(userData.username)
print(userData.timesLoggedOn)
```

---

# Ban Information

| Property                     | Description               |
| ---------------------------- | ------------------------- |
| `userData.banReason`         | Formatted ban status      |
| `userData.warnReason`        | Formatted warning status  |
| `userData.isMuteBanned`      | Formatted mute ban status |
| `userData.banHoursLeft`    | Remaining ban hours       |
| `userData.isMuteBannedRaw` | Raw mute ban value        |

Example:

```python
print(userData.banReason)
print(userData.warnReason)
print(userData.isMuteBanned)
```

---

# Pets

## Raw JSON

```python
userData.petsRaw
```

Returns the original pets dictionary from the API.

---

## Parsed Pets

```python
userData.pets
```

Returns a list of `Pet` objects.

Example:

```python
for pet in userData.pets:
    print(pet)
```

Each pet includes:

* Name
* Pet Type
* Level
* Favorite Food
* Current Position
* Next Task Time
* Completed Task Times

---

# CW Lists

The SDK exposes several Community World (CW) lists.

## Owner
This outputs a list of community worlds a player is the owner of.
```python
userData.ownerInCws
```

Raw JSON:

```python
userData.ownerInCwsRaw
```

---

## Staff
This outputs a list of community worlds a player is staff in.
```python
userData.staffInCws
```

Raw JSON:

```python
userData.staffInCwsRaw
```

---

## VIP
This outputs a list of community worlds a player is VIP in.
```python
userData.vipInCws
```

Raw JSON:

```python
userData.vipInCwsRaw
```

---

## Favorites
This outputs a list of all the community worlds a player has favorited.
```python
userData.favoriteCws
```

Raw JSON:

```python
userData.favoriteCwsRaw
```

---

## Seen Messages
This outputs a list of one-time messages that the player has seen, some examples include your CW getting moved to another code after another player purchases it when there is no fuel, and the welcome back message.
```python
userData.seenMessages
```

Raw JSON:

```python
userData.seenMessagesRaw
```

---

# Analytics
analyticEventKeys are mysterious, i don't know a lot about them, but from what i can tell it's a list of what you have done.
```python
userData.analyticEventKeys
```

Returns the raw analytics event key list.

---

# Daily Challenge Rewards

Returns the last redeem time for each reward.

```python
userData.lastChallengeRedeemedTime_login
```

Last login reward.

```python
userData.lastChallengeRedeemedTime_easy
```

Last easy challenge reward.

```python
userData.lastChallengeRedeemedTime_hard
```

Last hard challenge reward.

---

# Purchases & Unlocks

Returns `True` or `False`.

```python
userData.hasCreatorPack
```

Whether the player owns the Creator Pack.

```python
userData.hasUnlockedPrivateRooms
```

Whether Private Rooms have been unlocked.

```python
userData.hasPendingMobileLogin
```

Whether a mobile login is awaiting confirmation.

Example:

```python
if userData.hasCreatorPack:
    print("Player owns the Creator Pack.")
```

---

# Currency

```python
userData.buttcoinCount
```

Current Buttcoin balance.

```python
userData.silverBeansCount
```

Current Silver Bean balance.

Example:

```python
print(f"Buttcoins: {userData.buttcoinCount}")
print(f"Silver Beans: {userData.silverBeansCount}")
```

---

# Raw Response

The complete API response can always be accessed through:

```python
login.raw
```

Example:

```python
import json

print(json.dumps(login.raw, indent=4))
```

---

# Complete Example

```python
from yeeps import API

api = API("Jeremy|1234")

login = api.login()

userData = login.userData

print(userData.username)
print(userData.timesLoggedOn)
print(userData.banReason)
print(userData.hasCreatorPack)
print(userData.buttcoinCount)

print(userData.ownerInCws)

for pet in userData.pets:
    print(pet)
```

This SDK is designed so that almost every value is available in two forms when appropriate:

* `SomethingRaw` - The original JSON returned by the API.
* `Something` - A processed, human-friendly version suitable for direct use.

And that is the end of the documentation! Thanks for reading, have a good night/day/afternoon!
