from functions import loginUser, registerUser, guideUser, clearScreen, app

# Interface
exitText = '''
 _______  __   __  _______  __   __  
|  _    ||  | |  ||       ||  | |  | 
| |_|   ||  |_|  ||    ___||  | |  | 
|       ||       ||   |___ |  | |  | 
|  _   | |_     _||    ___||__| |__| 
| |_|   |  |   |  |   |___  __   __  
|_______|  |___|  |_______||__| |__| 
'''

front = '''
__________                                               ._______   _________   ____ ___.____  ___________
\______   \_____    ______ ________  _  _____________  __| _/\   \ /   /  _  \ |    |   \    | \__    ___/
 |     ___/\__  \  /  ___//  ___/\ \/ \/ /  _ \_  __ \/ __ |  \   Y   /  /_\  \|    |   /    |   |    |   
 |    |     / __ \_\___ \ \___ \  \     (  <_> )  | \/ /_/ |   \     /    |    \    |  /|    |___|    |   
 |____|    (____  /____  >____  >  \/\_/ \____/|__|  \____ |    \___/\____|__  /______/ |_______ \____|   
                \/     \/     \/                          \/                 \/                 \/        

                                by github.com/prakharsaxena1

'''

menu = '( 1 ) ==> LOGIN\n( 2 ) ==> REGISTER\n( 3 ) ==> GUIDE / How to use\n( 4 ) ==> EXIT\n$OPTION: '
option = int(input(front+menu))

# Login
if option == 1:
    clearScreen()
    print("< === Login === >")
    loginUser()

# Register
elif option == 2:
    clearScreen()
    print("< === Register === >")
    registerUser()

# Guide
elif option == 3:
    clearScreen()
    print("< === Guide === >")
    guideUser()

# Exit
elif option == 4:
    print(exitText)

# Else for fools
else:
    print("INVALID INPUT")