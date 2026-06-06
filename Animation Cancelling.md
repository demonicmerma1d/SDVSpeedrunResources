# Animation Cancelling
This is the src moderator post on what Animation Cancelling is, and what is speedrun legal regarding it (thank you Underscore76 for providing this).


Animation canceling (AC) is a built-in key combo which stops a player's action and returns them to a neutral state. It was originally used as a debug tool on PC that was unintentionally left in by Concerned Ape (CA) and is used by speedrunners to more quickly use tools. As this was not its intended use (but was approved by CA to remain in the game), this mechanic is the defining difference between vanilla and **glitchless**. 
 
This technique is done by pressing `RightShift`+`R`+`Delete` (+`fn` if you are playing on a Mac). 
 
__**Rules for Animation Canceling:**__
・Automatic timers and macros are not allowed. 
・The player must manually input the animation cancel keys after the action key. 
・The action key (by default: LeftClick/C) and your animation cancel keys cannot be mapped to the same button. 
 
For speedrunning, we allow 1:1, 2:1, and 3:1 mappings of the animation canceling keys. Below are some approved AHK scripts (Windows) you can use, as well as resources for implementation on other operating systems. Note that the keys shown in these scripts are the most common ones used by runners. You are free to change to whichever keys you would like. Timing for the pulse duration can be changed as well (see the pulse script).

__**1:1 Rebind**__
Each button is individually mapped to one other button. For example, when you press Space, your computer instead receives the “Delete” input. Traditionally, R and RShift are mapped to mouse keys and Delete is mapped to Space. 
 
**How to Use**: Left-click and then press all three of your keys to cancel the animation. You must release these keys before you can click again for your next action. 
**Pros**: usually easier to natively implement than other remapping methods
**Cons**: much harder to execute and causes more wear on hands and peripherals
```autohotkey
; AutoHotKey v1 1:1 bind
; NOTE: This script works in regular Stardew Valley and SMAPI, the use of SMAPI is banned in speedruns
#IfWinActive ahk_exe Stardew Valley.exe
XButton1::r
XButton2::RShift
+Space::Delete
return
```

__**3:1 Rebind**__
All three buttons are mapped exactly to one other button. That is, when your AC key is down, the mapped keys are down. When it is up, the mapped keys are up. 
 
**How to Use**: Left-click and then press space to cancel the animation. You must release the spacebar before you can click again for your next action. 
**Pros**: forage pick-up and harvesting with scythe is quicker, movement is easier
**Cons**: timing is more precise so can be more difficult to execute
```autohotkey
; AutoHotKey v1 3:1 bind
; NOTE: This script works in regular Stardew Valley and SMAPI, the use of SMAPI is banned in speedruns
SetTitleMatchMode, RegEx
#IfWinActive ahk_exe Stardew Valley
    Space::
    SendInput {Del down}{RShift down}{r down}
    KeyWait, space
    SendInput {Del up}{RShift up}{r up}
    return
```
```autohotkey
; AutoHotKey v2 3:1 bind
; NOTE: This script works in regular Stardew Valley and SMAPI, the use of SMAPI is banned in speedruns
#Requires AutoHotkey v2.0
SetTitleMatchMode "RegEx"
#HotIf WinActive("ahk_exe Stardew Valley")
Space::{
    Send "{Del down}{RShift down}{r down}"
    KeyWait "space"
    Send "{Del up}{RShift up}{r up}"
    return
}
```

__**3:1 Pulse**__
All three buttons are mapped to one other button, but the release of the button is independent. That is, when you press your AC key, the mapped keys are pressed and then released without requiring you to release your AC key. *Only one pulse per input is allowed*. The duration of the pulse can be modified, but note that too short a pulse may not be recognized by your PC.
 
**How to Use**: Left-click and then press space to cancel the animation. You can click for your next action before you release the spacebar. 
**Pros**: larger timing window for starting your next action, making it easier to learn and do well
**Cons**: movement while animation canceling is much more difficult
```autohotkey
; AutoHotKey v1 Pulse 3:1 (simple, may not work on certain systems)
; NOTE: This script works in regular Stardew Valley and SMAPI, the use of SMAPI is banned in speedruns
SetTitleMatchMode, RegEx
#IfWinActive ahk_exe Stardew Valley
Space::
Send {Del down}{RShift down}{r down}{Del up}{RShift up}{r up}
```
```autohotkey
; AutoHotKey v1 Pulse 3:1 (works on all systems, can customize delay)
; NOTE: This script works in regular Stardew Valley and SMAPI, the use of SMAPI is banned in speedruns
SetTitleMatchMode, RegEx
#IfWinActive ahk_exe Stardew Valley
Space::
    SendInput {Del down}{RShift down}{r down}
    sleep 25 ;this number can be changed depending on system
    SendInput {Del up}{RShift up}{r up}
    Return
```
```autohotkey
; AutoHotKey v2 Pulse 3:1 (works on all systems, can customize delay)
; NOTE: This script works in regular Stardew Valley and SMAPI, the use of SMAPI is banned in speedruns
#Requires AutoHotkey v2.0
SetTitleMatchMode "RegEx"
#HotIf WinActive("ahk_exe Stardew Valley")
Space::{
    Send "{Del down}{RShift down}{r down}"
    Sleep 25 ;this number can be changed depending on system
    Send "{Del up}{RShift up}{r up}"
    return
}
```

__**Combo AHK script**__

This script is designed to let you do both pulse and rebind with two separate binds.

```autohotkey
; AutoHotKey v1 Combo Script (works on all systems, more accurate timing)
; Allows using both 3:1 rebind (via Space key) and pulse (on right click when holding alt or side mouse button)
; NOTE: This script works in regular Stardew Valley and SMAPI, the use of SMAPI is banned in speedruns
#NoEnv
#MaxHotkeysPerInterval 99000000
#KeyHistory 0
ListLines Off
Process, Priority, , H
SetBatchLines, -1

;Only run if Stardew is active
SetTitleMatchMode, RegEx
;If this doesn't work in SMAPI, you can try removing Valley from the following line.
#IfWinActive ahk_exe Stardew Valley

;Bind Alt to side mouse button, you can hold Alt instead of using this rebind
XButton1::Alt

;3:1 AC on Space
Space::
    SendInput {Del down}{RShift down}{r down}
    KeyWait, Space
    SendInput {Del up}{RShift up}{r up}
    return

;Pulse AC on Alt + Right Click
!RButton::
    SendInput {Blind}{Del down}{RShift down}{r down}
    Sleep(1)
    SendInput {Blind}{Del up}{RShift up}{r up}
    return

;Use Dll sleep, which is orders of magnitude more accurate than AHK sleep function
Sleep(frames){
    DllCall("kernel32.dll\Sleep", "UInt", frames*17)
}
```

__**Mac Animation Cancel App**__

If you have a Mac running macOS 14.0 or later, we've built a standalone app that will run the 3:1 bind which you can find here: https://github.com/Underscore76/AnimationCancelApp/releases

Grab the correct version based on your mac (if you're not sure, click the Apple icon in the top left of your desktop and select `About This Mac` . Under Processor or Chip, it will say "Intel" or "Apple M#". For Intel, select the Intel zip file, for Apple M-series, grab the arm zip file.

The first time you are in game with the app running and press Space, you'll get a permissions prompt to allow the app to control your computer. After allowing it should start to cancel as expected.

__**Karabiner (Mac Only - not recommended)**__
Macs are complicated and the additional fn key messes with a lot of things, which restricts us to a maximum of a 2:1 mapping. The following below allows you to use Space+V for animation canceling, but you can use the webpage to craft your own 1:1 or 2:1 mappings. 
 
**Maps Space to Delete**: https://tinyurl.com/SDVAC-SpaceDelete 
**Maps RightShift+R to V**: https://tinyurl.com/SDVAC-VRShiftR 
 
__**Python Script (All Systems, not first choice)**__
As AutoHotKey is only consistently available on Windows machines and Karabiner can be an absolute pain to work with, a Python script has been written using PyAutoGUI which can be used to implement the aforementioned rebinds. You can find the repository here: https://github.com/Underscore76/MacAnimationCancel