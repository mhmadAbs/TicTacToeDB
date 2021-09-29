import random
from tkinter import *
import mysql.connector
import sys

'''
    build a Connection to xo_db Database..
'''
db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="xo_db",
    passwd="mkmk"
)

root = Tk()
root.title("TicTacToe")
root.configure(bg="grey")
root.geometry("420x500+500+200")


class NewPlayer:

    def __init__(self, window):
        # Content of Squares
        s11 = StringVar()
        s12 = StringVar()
        s13 = StringVar()
        s21 = StringVar()
        s22 = StringVar()
        s23 = StringVar()
        s31 = StringVar()
        s32 = StringVar()
        s33 = StringVar()
        squares_strings = [s11, s12, s13, s21, s22, s23, s31, s32, s33]
        player_wins = 0
        ai_wins = 0
        window.title("TicTacToe(Register)")

        player_sign = StringVar()
        player_sign.set("X")
        print(player_sign.get())
        sign_menu = OptionMenu(window, player_sign, "X", "O")
        sign_menu.place(x=170, y=110)

        def getAiSign():
            if player_sign.get() == "X":
                return "O"
            return "X"

        '''
            Used to highlight the positions that caused the win
        '''

        def highlight(fst, snd, thd):
            fst.config(bg="orange")
            snd.config(bg="orange")
            thd.config(bg="orange")

        '''
            checks if a win condition was fulfilled.
        '''

        def checkResult():
            if s11.get() == s12.get() and s12.get() == s13.get() and s11.get() != "":
                stopGame()
                highlight(r1c1, r1c2, r1c3)
                return True
            elif s21.get() == s22.get() and s22.get() == s23.get() and s21.get() != "":
                stopGame()
                highlight(r2c1, r2c2, r2c3)
                return True
            elif s31.get() == s32.get() and s32.get() == s33.get() and s31.get() != "":
                stopGame()
                highlight(r3c1, r3c2, r3c3)
                return True

            elif s11.get() == s21.get() and s21.get() == s31.get() and s11.get() != "":
                stopGame()
                highlight(r1c1, r2c1, r3c1)
                return True
            elif s12.get() == s22.get() and s22.get() == s32.get() and s12.get() != "":
                stopGame()
                highlight(r1c2, r2c2, r3c2)
                return True
            elif s13.get() == s23.get() and s23.get() == s33.get() and s13.get() != "":
                stopGame()
                highlight(r1c3, r2c3, r3c3)
                return True

            elif s11.get() == s22.get() and s22.get() == s33.get() and s11.get() != "":
                stopGame()
                highlight(r1c1, r2c2, r3c3)
                return True
            elif s13.get() == s22.get() and s22.get() == s31.get() and s13.get() != "":
                stopGame()
                highlight(r1c3, r2c2, r3c1)
                return True

        '''
            Defines what happens when a Player clicks on a position.
        '''

        def onSquare(num, btn):
            if sign_menu["state"] == "disabled" and len(squares_strings) > 0:
                btn.config(state="disabled")
                if num == 11:
                    s11.set(player_sign.get())
                    squares_strings.remove(s11)

                elif num == 12:
                    s12.set(player_sign.get())
                    squares_strings.remove(s12)
                elif num == 13:
                    s13.set(player_sign.get())
                    squares_strings.remove(s13)
                elif num == 21:
                    s21.set(player_sign.get())
                    squares_strings.remove(s21)
                elif num == 22:
                    s22.set(player_sign.get())
                    squares_strings.remove(s22)
                elif num == 23:
                    s23.set(player_sign.get())
                    squares_strings.remove(s23)
                elif num == 31:
                    s31.set(player_sign.get())
                    squares_strings.remove(s31)
                elif num == 32:
                    s32.set(player_sign.get())
                    squares_strings.remove(s32)
                elif num == 33:
                    s33.set(player_sign.get())
                    squares_strings.remove(s33)
                if checkResult():
                    feedback_lbl.config(text="{} won the game !".format(username_entry.get()))
                    nonlocal player_wins
                    player_wins += 1
                    player_score_lbl.config(text=str(getPlayerScore()))
                if not checkResult() and len(squares_strings) == 0:
                    feedback_lbl.config(text="Tide !")
                if len(squares_strings) > 0 and not checkResult():
                    feedback_lbl.config(text="AI's Turn", fg="blue")
                    feedback_lbl.after(500, playAi)  # Some delay as if AI is thinking

        def u_nameExists(username):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM results WHERE username='{}'".format(username))
            res_set = cursor.fetchall()  # returns a list contains all results(as tuples)
            return len(res_set) > 0

        # To check the Validity of name given by the player
        def checkUNameValid():
            u_name = username_entry.get()
            if len(u_name) > 0:
                if u_nameExists(u_name):
                    feedback_lbl.config(text="Given name is token")
                    return False
                else:
                    return True
            else:
                feedback_lbl.config(text="Enter your Name first !")
                return False

        def submit():
            if checkUNameValid():
                username_entry.config(state="disabled")
                sign_menu.config(state="disabled")
                feedback_lbl.config(text="Game Started", fg="green")
                submit_btn.config(state="disabled")
                player_score_lbl.config(text=int(getPlayerScore()))
                ai_score_lbl.config(text=int(getAiScore()))

            else:
                feedback_lbl.config(text="Enter your Name first !")

        header = Label(window, anchor="center", bg="grey", fg="orange", height=2, text="Welcome to TicTacToe",
                       font="none 15 bold")
        header.grid(row=0, column=0)

        empty_row = Label(window, text="", bg="grey")
        empty_row.grid(row=1, column=0)

        id_lbl = Label(window, anchor="w", bg="grey", fg="black", height=1, text="Username : ",
                       font="none 12 ")
        id_lbl.place(x=15, y=70)

        username_entry = Entry(window, bg="white", width=20)
        username_entry.place(x=170, y=70)

        submit_btn = Button(window, text="Submit", width=6, fg="orange", bg="grey", font="none 12 bold",
                            command=submit)
        submit_btn.place(x=310, y=110)

        empty_row2 = Label(window, text="", bg="grey")
        empty_row2.grid(row=3, column=0)

        sign_lbl = Label(window, anchor="w", bg="grey", fg="black", height=1, text="Sign : ", font="none 12 ")
        sign_lbl.place(x=15, y=110)

        Label(window, text="--------------------------------------------------------------------------------------",
              fg="black",
              bg="grey").place(x=0, y=150)

        r1c1 = Button(window, textvariable=s11, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(11, r1c1))
        r1c1.place(
            height=50, x=40, y=290)
        r1c2 = Button(window, textvariable=s12, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(12, r1c2))
        r1c2.place(
            height=50,
            x=145,
            y=290)
        r1c3 = Button(window, textvariable=s13, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(13, r1c3))
        r1c3.place(
            height=50,
            x=250,
            y=290)
        r2c1 = Button(window, textvariable=s21, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(21, r2c1))
        r2c1.place(height=50, x=40, y=340)

        r2c2 = Button(window, textvariable=s22, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(22, r2c2))
        r2c2.place(height=50, x=145, y=340)

        r2c3 = Button(window, textvariable=s23, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(23, r2c3))
        r2c3.place(height=50, x=250, y=340)

        r3c1 = Button(window, textvariable=s31, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(31, r3c1))
        r3c1.place(height=50, x=40, y=390)

        r3c2 = Button(window, textvariable=s32, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(32, r3c2))
        r3c2.place(height=50, x=145, y=390)

        r3c3 = Button(window, textvariable=s33, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(33, r3c3))
        r3c3.place(height=50, x=250, y=390)

        feedback_lbl = Label(window, text="Enter ID to and submit to start", fg="brown", bg="grey", font="none 13 ")
        feedback_lbl.place(x=40, y=170)

        def getPlayerScore():
            return player_wins

        def getAiScore():
            return ai_wins

        player_score_lbl = Label(window, text=player_wins, fg="black", bg="white", font="Arial 35 bold")
        player_score_lbl.place(x=80, y=210)

        two_points_lbl = Label(window, text=":", fg="black", bg="grey", font="Arial 35 bold")
        two_points_lbl.place(x=180, y=210)

        ai_score_lbl = Label(window, text=ai_wins, fg="black", bg="white", font="Arial 35 bold")
        ai_score_lbl.place(x=270, y=210)

        '''
            To prevent player from selecting a position that is full
        '''

        def disable_btns():
            btns = [r1c1, r1c2, r1c3, r2c1, r2c2, r2c3, r3c1, r3c2, r3c3]
            for btn in btns:  #
                if btn["text"] != "":
                    btn.config(state="disabled")

        def playAi():

            if len(squares_strings) > 0 and not checkResult():  # There is at least one free place
                choice = random.choice(squares_strings)
                choice.set(getAiSign())
                feedback_lbl.config(text="{}'s Turn".format(username_entry.get()), fg="blue")
                squares_strings.remove(choice)
                if checkResult():
                    feedback_lbl.config(text="You lost !")
                    nonlocal ai_wins
                    ai_wins += 1
                    ai_score_lbl.config(text=str(ai_wins))

                disable_btns()

        '''
            To update database with the match result (After game was closed)
        '''

        def updateResult(username):
            cursor = db.cursor()
            cursor.execute(
                f"INSERT INTO results(username, p_score, ai_score) VALUES('{username}',{player_wins},{ai_wins})")
            db.commit()

        def exit_f():
            updateResult(username_entry.get())
            sys.exit()

        exit_btn = Button(window, text="Exit", width=15, fg="red", font="none 12 bold", command=exit_f)
        exit_btn.place(x=40, y=450, height=30)

        '''
            To Restart the whole game
        '''

        def restart():
            btns = [r1c1, r1c2, r1c3, r2c1, r2c2, r2c3, r3c1, r3c2, r3c3]

            nonlocal squares_strings  # so that the outer list variable get updated
            squares_strings = [s11, s12, s13, s21, s22, s23, s31, s32, s33]
            for sqr in squares_strings:
                sqr.set("")
            for btn in btns:
                btn.config(state="active", bg="white")
            feedback_lbl.config(text="Game Restarted")

        restart_button = Button(window, text="Restart", width=15, fg="green", font="none 12 bold", command=restart)
        restart_button.place(x=200, y=450, height=30)

        '''
            To stop the game at the End of a round (When there is a winner or tide)
        '''

        def stopGame():
            btns = [r1c1, r1c2, r1c3, r2c1, r2c2, r2c3, r3c1, r3c2, r3c3]
            for btn in btns:
                btn.config(state="disabled")


class RegisteredPlayer:

    def __init__(self, window):
        # Content of Squares
        s11 = StringVar()
        s12 = StringVar()
        s13 = StringVar()
        s21 = StringVar()
        s22 = StringVar()
        s23 = StringVar()
        s31 = StringVar()
        s32 = StringVar()
        s33 = StringVar()
        squares_strings = [s11, s12, s13, s21, s22, s23, s31, s32, s33]
        window.title("TicTacToe(Login)")

        player_wins = 0
        ai_wins = 0

        def getPlayerScore():
            cursor = db.cursor()
            sql_stmt = f"SELECT p_score, ai_score FROM results WHERE username='{uname_entry.get()}'"
            cursor.execute(sql_stmt)
            result = cursor.fetchone()
            return result[0], result[1]

        def getAiSign():
            if player_sign.get() == "X":
                return "O"
            return "X"

        def highlight(fst, snd, thd):
            fst.config(bg="orange")
            snd.config(bg="orange")
            thd.config(bg="orange")

        def checkResult():
            if s11.get() == s12.get() and s12.get() == s13.get() and s11.get() != "":
                stopGame()
                highlight(r1c1, r1c2, r1c3)
                return True
            elif s21.get() == s22.get() and s22.get() == s23.get() and s21.get() != "":
                stopGame()
                highlight(r2c1, r2c2, r2c3)
                return True
            elif s31.get() == s32.get() and s32.get() == s33.get() and s31.get() != "":
                stopGame()
                highlight(r3c1, r3c2, r3c3)
                return True

            elif s11.get() == s21.get() and s21.get() == s31.get() and s11.get() != "":
                stopGame()
                highlight(r1c1, r2c1, r3c1)
                return True
            elif s12.get() == s22.get() and s22.get() == s32.get() and s12.get() != "":
                stopGame()
                highlight(r1c2, r2c2, r3c2)
                return True
            elif s13.get() == s23.get() and s23.get() == s33.get() and s13.get() != "":
                stopGame()
                highlight(r1c3, r2c3, r3c3)
                return True

            elif s11.get() == s22.get() and s22.get() == s33.get() and s11.get() != "":
                stopGame()
                highlight(r1c1, r2c2, r3c3)
                return True
            elif s13.get() == s22.get() and s22.get() == s31.get() and s13.get() != "":
                stopGame()
                highlight(r1c3, r2c2, r3c1)
                return True

        def onSquare(num, btn):
            nonlocal ai_wins, player_wins
            if sign_menu["state"] == "disabled" and len(squares_strings) > 0:
                btn.config(state="disabled")
                if num == 11:
                    s11.set(player_sign.get())
                    squares_strings.remove(s11)

                elif num == 12:
                    s12.set(player_sign.get())
                    squares_strings.remove(s12)
                elif num == 13:
                    s13.set(player_sign.get())
                    squares_strings.remove(s13)
                elif num == 21:
                    s21.set(player_sign.get())
                    squares_strings.remove(s21)
                elif num == 22:
                    s22.set(player_sign.get())
                    squares_strings.remove(s22)
                elif num == 23:
                    s23.set(player_sign.get())
                    squares_strings.remove(s23)
                elif num == 31:
                    s31.set(player_sign.get())
                    squares_strings.remove(s31)
                elif num == 32:
                    s32.set(player_sign.get())
                    squares_strings.remove(s32)
                elif num == 33:
                    s33.set(player_sign.get())
                    squares_strings.remove(s33)
                if checkResult():
                    feedback_lbl.config(text="{} won the game !".format(uname_entry.get()))
                    player_wins += 1
                    player_score_lbl.config(text=player_wins)
                    updateDB()
                if not checkResult() and len(squares_strings) == 0:
                    feedback_lbl.config(text="Tide !")
                    player_wins += 1
                    ai_wins += 1
                    updateDB()
                if len(squares_strings) > 0 and not checkResult():
                    feedback_lbl.config(text="AI's Turn", fg="blue")
                    feedback_lbl.after(500, playAi)  # Some delay as if AI is thinking

        def submit():
            p_id = uname_entry.get()
            if len(p_id) > 0:
                uname_entry.config(state="disabled")
                sign_menu.config(state="disabled")
                feedback_lbl.config(text="Game Started", fg="green")
                submit_btn.config(state="disabled")
                updateResult()
                player_score_lbl.config(text=int(player_wins))
                ai_score_lbl.config(text=int(ai_wins))

            else:
                feedback_lbl.config(text="Enter you Name first !")

        player_sign = StringVar()
        player_sign.set("X")
        sign_menu = OptionMenu(window, player_sign, "X", "O")
        sign_menu.place(x=170, y=110)

        header = Label(window, anchor="center", bg="grey", fg="orange", height=2, text="Welcome to TicTacToe",
                       font="none 15 bold")
        header.grid(row=0, column=0)

        empty_row = Label(window, text="", bg="grey")
        empty_row.grid(row=1, column=0)

        uname_lbl = Label(window, anchor="w", bg="grey", fg="black", height=1, text="Player ID : ",
                          font="none 12 ")
        uname_lbl.place(x=15, y=70)

        uname_entry = Entry(window, bg="white", width=20)
        uname_entry.place(x=170, y=70)

        submit_btn = Button(window, text="Submit", width=6, fg="orange", bg="grey", font="none 12 bold",
                            command=submit)
        submit_btn.place(x=310, y=110)

        empty_row2 = Label(window, text="", bg="grey")
        empty_row2.grid(row=3, column=0)

        sign_lbl = Label(window, anchor="w", bg="grey", fg="black", height=1, text="Sign : ", font="none 12 ")
        sign_lbl.place(x=15, y=110)

        Label(window, text="--------------------------------------------------------------------------------------",
              fg="black",
              bg="grey").place(x=0, y=150)

        r1c1 = Button(window, textvariable=s11, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(11, r1c1))
        r1c1.place(
            height=50, x=40, y=290)
        r1c2 = Button(window, textvariable=s12, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(12, r1c2))
        r1c2.place(
            height=50,
            x=145,
            y=290)
        r1c3 = Button(window, textvariable=s13, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(13, r1c3))
        r1c3.place(
            height=50,
            x=250,
            y=290)
        r2c1 = Button(window, textvariable=s21, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(21, r2c1))
        r2c1.place(height=50, x=40, y=340)

        r2c2 = Button(window, textvariable=s22, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(22, r2c2))
        r2c2.place(height=50, x=145, y=340)

        r2c3 = Button(window, textvariable=s23, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(23, r2c3))
        r2c3.place(height=50, x=250, y=340)

        r3c1 = Button(window, textvariable=s31, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(31, r3c1))
        r3c1.place(height=50, x=40, y=390)

        r3c2 = Button(window, textvariable=s32, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(32, r3c2))
        r3c2.place(height=50, x=145, y=390)

        r3c3 = Button(window, textvariable=s33, bg="white", fg="black", font="none 15 bold", width=8,
                      command=lambda: onSquare(33, r3c3))
        r3c3.place(height=50, x=250, y=390)

        feedback_lbl = Label(window, text="Enter ID to and submit to start", fg="brown", bg="grey", font="none 13 ")
        feedback_lbl.place(x=40, y=170)

        player_score_lbl = Label(window, text="0", fg="black", bg="white", font="Arial 35 bold")
        player_score_lbl.place(x=80, y=210)

        two_points_lbl = Label(window, text=":", fg="black", bg="grey", font="Arial 35 bold")
        two_points_lbl.place(x=180, y=210)

        ai_score_lbl = Label(window, text="0", fg="black", bg="white", font="Arial 35 bold")
        ai_score_lbl.place(x=270, y=210)

        def playAi():
            btns = [r1c1, r1c2, r1c3, r2c1, r2c2, r2c3, r3c1, r3c2, r3c3]

            if len(squares_strings) > 0 and not checkResult():  # There is at least one free place
                choice = random.choice(squares_strings)
                choice.set(getAiSign())
                feedback_lbl.config(text="{}'s Turn".format(uname_entry.get()), fg="blue")
                squares_strings.remove(choice)
                if checkResult():
                    feedback_lbl.config(text="You lost !")
                    nonlocal ai_wins
                    ai_wins += 1
                    ai_score_lbl.config(text=str(ai_wins))
                    updateDB()  # CHANGE TO ENUMS

            for btn in btns:  # To prevent player from selecting a position that is full
                if btn["text"] != "":
                    btn.config(state="disabled")

        def updateDB():
            username = uname_entry.get()
            new_score_a = ai_score_lbl["text"]
            new_score_p = player_score_lbl["text"]
            cursor = db.cursor()
            sql_stmt = f"UPDATE results SET p_score={new_score_p}, ai_score={new_score_a} WHERE username='{username}'"
            cursor.execute(sql_stmt)
            db.commit()

        def updateResult():
            nonlocal player_wins, ai_wins
            player_wins, ai_wins = getPlayerScore()

        def exit_f():
            sys.exit()

        exit_btn = Button(window, text="Exit", width=15, fg="red", font="none 12 bold", command=exit_f)
        exit_btn.place(x=40, y=450, height=30)

        def restart():
            btns = [r1c1, r1c2, r1c3, r2c1, r2c2, r2c3, r3c1, r3c2, r3c3]

            nonlocal squares_strings  # so that the outer list variable updated
            squares_strings = [s11, s12, s13, s21, s22, s23, s31, s32, s33]
            for sqr in squares_strings:
                sqr.set("")
            for btn in btns:
                btn.config(state="active", bg="white")
            feedback_lbl.config(text="Game Restarted")

        restart_button = Button(window, text="Restart", width=15, fg="green", font="none 12 bold", command=restart)
        restart_button.place(x=200, y=450, height=30)

        def stopGame():
            btns = [r1c1, r1c2, r1c3, r2c1, r2c2, r2c3, r3c1, r3c2, r3c3]
            for btn in btns:
                btn.config(state="disabled")


def startReg():
    top = Toplevel()  # so that it appears on the top.
    top.title("TicTacToe")
    top.configure(bg="grey")
    top.geometry("420x500+500+200")
    NewPlayer(top)


def startLogin():
    top = Toplevel()  # so that it appears on the top.
    top.title("TicTacToe")
    top.configure(bg="grey")
    top.geometry("420x500+500+200")
    RegisteredPlayer(top)


reg_btn = Button(root, text="Register", command=startReg, width=30, height=5, fg="Green", font="none 15 bold",
                 relief="solid").pack(pady=10)
login_btn = Button(root, text="Login", command=startLogin, width=30, height=5, fg="Green", font="none 15 bold",
                   relief="solid").pack(pady=10)
ext_btn = Button(root, text="Exit", command=sys.exit, width=30, height=5, fg="Red", font="none 15 bold",
                 relief="solid").pack(pady=10)
mainloop()
