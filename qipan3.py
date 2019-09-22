import sys

import random

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication

from PyQt5.QtGui import QPainter, QPen

from PyQt5.QtCore import Qt

 

random.seed()  # 省略参数，意味着取当前系统时间

 

class MyQWidget(QWidget):

 

    def __init__(self):

        # 设置棋盘与棋子的间隔

        self.D = 56

        self.d = 54

 

        # 设置棋盘为二维数组

        self.Board = [[255]*15 for i in range(15)]

 

        # 设置出棋方

        self._Bool = False

 

        # 设置赢方

        self._over = 255

 

        super().__init__()

        self.initUI()

 

    def initUI(self):

        # 窗口绘制

 

        self.resize(16 * self.D, 16 * self.D)

        self.center()

        self.setWindowTitle('五子棋')

 

    def center(self):

        # 窗口归中

 

        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

 

    def paintEvent(self, QPaintEvent):

 

        if self._over == 255:

            # 绘制板块

            qpLine = QPainter()

            qpElip = QPainter()

 

            qpLine.begin(self)

            self.drawLines(qpLine)

            qpLine.end()

 

            qpElip.begin(self)

            self.drawEllipse(qpElip)

            qpElip.end()

 

        else:

            if self._over == 1:

                print('Black Win!')

            else:

                print('White Win!')

 

        self.update()

 

    def drawLines(self, qpLine):

        # 绘制棋盘

 

        for i in range(1, 16):

            if i == 1 or i == 15:

                pen = QPen(Qt.black, 2, Qt.SolidLine)

                qpLine.setPen(pen)

            else:

                pen = QPen(Qt.black, 1, Qt.SolidLine)

                qpLine.setPen(pen)

 

            qpLine.drawLine(self.D, i * self.D, 15 * self.D, i * self.D)

            qpLine.drawLine(i * self.D, self.D, i * self.D, 15 * self.D)

 

    def drawEllipse(self, qpElip):

        # 绘制棋子

 

        MinX, MaxX, MinY, MaxY = self.AlUpDnLfRt(15, 0, 15, 0)

        for i in range(MinX, MaxX):

            for j in range(MinY, MaxY):

                if self.Board[i][j] == 1:

                    qpElip.setPen(Qt.darkGray)

                    qpElip.setBrush(Qt.black)

                    qpElip.drawEllipse((j + 0.5) * self.D, (i + 0.5) * self.D, self.d, self.d)

                elif self.Board[i][j] == 0:

                    qpElip.setPen(Qt.darkGray)

                    qpElip.setBrush(Qt.white)

                    qpElip.drawEllipse((j + 0.5) * self.D, (i + 0.5) * self.D, self.d, self.d)

 

        self.update()

 

    def mousePressEvent(self, e):

 

        apos_x = e.pos().x()

        apos_y = e.pos().y()

 

        if apos_x >= 0.5 * self.D and apos_x <= 15.5 * self.D and apos_y >= 0.5 * self.D and apos_y <= 15.5 * self.D:

            apos_x, apos_y = self.aimPoint(apos_x, apos_y)

            apos_x, apos_y = self._Scope(apos_x, apos_y)

 

            if apos_x != -1:

                if self.Board[apos_y][apos_x] == 255:

 

                    if self._Bool == 0:

                        self.Board[apos_y][apos_x] = 0

 

                    else:

                        self.Board[apos_y][apos_x] = 0

 

                    self._Bool = not self._Bool

                    self.Traverse()

                    self.AlRobotGo()

                    self.Traverse()

                    print('Player to:')

 

    @staticmethod

    def _Scope(apos_x, apos_y):

 

        if apos_x >= 0 and apos_x <= 14 and apos_y >= 0 and apos_y <= 14:

            return apos_x, apos_y

        else:

            return -1

 

    def aimPoint(self, apos_x, apos_y):

        # 计算棋坐标

 

        sur_x = int(apos_x / self.D)

        sur_y = int(apos_y / self.D)

 

        apos_x %= self.D

        apos_y %= self.D

 

        if apos_x >= (self.D / 2):

            sur_x += 1

        if apos_y >= (self.D / 2):

            sur_y += 1

 

        sur_x, sur_y = self._Scope(sur_x - 1, sur_y - 1)

        return sur_x, sur_y

 

    def Traverse(self):

 

        MinX, MaxX, MinY, MaxY = self.AlUpDnLfRt(15, 0, 15, 0)

        for i in range(MinX, MaxX):

            for j in range(MinY, MaxY):

                if self.Board[i][j] != 255:

                    b_Up = _Right = b_Down = _Scp = 1

                    _Color = self.Board[i][j]

 

                    # 判断该点前点

                    _Uold = self.oldCompare(i + 1, j - 1, _Color)

                    _Rold = self.oldCompare(i, j - 1, _Color)

                    b_Dold = self.oldCompare(i - 1, j - 1, _Color)

                    _Sold = self.oldCompare(i - 1, j, _Color)

 

                    # 判断该点范围

                    if i - 4 < MinX and i + 4 > MaxX and j - 4 < MinY and j + 4 > MaxY:

                        break

 

                    # 进行遍历该点附近点

                    if _Uold != 0:

                        b_Up = self.Up_RangeDirct(i, j, _Color, b_Up)

 

                    if _Rold != 0:

                        _Right = self.Rt_RangeDirct(i, j, _Color, _Right)

 

                    if b_Dold != 0:

                        b_Down = self.Dn_RangeDirct(i, j, _Color, b_Down)

 

                    if _Sold != 0:

                        _Scp = self.Sp_RangeDirct(i, j, _Color, _Scp)

 

                    # 进行胜负判断

                    self.Game_over(b_Up, b_Down, _Right, _Scp, _Color)

 

    def oldCompare(self, x, y, n_color):

        if -1 != self._Scope(x, y):

            if self.Board[x][y] == n_color:

                return 0

            elif self.Board[x][y] == 255:

                return 255

            else:

                return 1

        else:

            return 2

 

    def Up_RangeDirct(self, x, y, n_color, now):

        for k in range(1, 5):

            if -1 != self._Scope(x - k, y + k):

                if self.Board[x - k][y + k] == n_color:

                    now += 1

                else:

                    return 0

            else:

                return 0

        return now

 

    def Rt_RangeDirct(self, x, y, n_color, now):

        for k in range(1, 5):

            if -1 != self._Scope(x, y + k):

                if self.Board[x][y + k] == n_color:

                    now += 1

                else:

                    return 0

            else:

                return 0

        return now

 

    def Dn_RangeDirct(self, x, y, n_color, now):

        for k in range(1, 5):

            if -1 != self._Scope(x + k, y + k):

                if self.Board[x + k][y + k] == n_color:

                    now += 1

                else:

                    return 0

            else:

                return 0

        return now

 

    def Sp_RangeDirct(self, x, y, n_color, now):

        for k in range(1, 5):

            if -1 != self._Scope(x + k, y):

                if self.Board[x + k][y] == n_color:

                    now += 1

                else:

                    return 0

            else:

                return 0

        return now

 

    def AlRobotGo(self):

        # 人机下棋

        if self._Bool:

 

            TrueScore = -10000

            MaxMinMaxScore = 10000

            TrueX = MaxMinMaxX = x = 0

            TrueY = MaxMinMaxY = y = 0

 

            MinX, MaxX, MinY, MaxY = self.AlUpDnLfRt(15, 0, 15, 0)

            for i in range(MinX, MaxX):

                for j in range(MinY, MaxY):

                    if self.Board[i][j] == 255:

                        self.Board[i][j] = 1

 

                        MinMaxScore_Flag = 1

                        MinMaxScore_Ok_Flag = 2

 

                        MMinX, MMaxX, MMinY, MMaxY = self.AlUpDnLfRt(MaxX, MinX, MaxY, MinY)

                        for ii in range(MMinX, MMaxX):

                            for jj in range(MMinY, MMaxY):

                                if ii != i or jj != j:

                                    if self.Board[ii][jj] == 255:

                                        self.Board[i][j] = 1

                                        self.Board[ii][jj] = 0

 

                                        NewScore = -100000

                                        NewScore_Flag = 1

                                        MinMaxScore_Ok_Flag -= 1

                                        if MinMaxScore_Ok_Flag == 0:

                                            MinMaxScore_Flag = 0

 

                                        MMMinX, MMMaxX, MMMinY, MMMaxY = self.AlUpDnLfRt(MMaxX, MMinX, MMaxY, MMinY)

                                        for iii in range(MMMinX, MMMaxX):

                                            for jjj in range(MMMinY, MMMaxY):

                                                if iii != i or jjj != j:

                                                    if iii != ii or jjj != jj:

                                                        if self.Board[iii][jjj] == 255:

                                                            self.Board[i][j] = 1

                                                            self.Board[ii][jj] = 0

                                                            self.Board[iii][jjj] = 1

                                                            _Score = self.AlTraverse()

                                                            self.Board[i][j] = 255

                                                            self.Board[ii][jj] = 255

                                                            self.Board[iii][jjj] = 255

 

                                                            if _Score > NewScore:

                                                                NewScore = _Score

                                                                x = i

                                                                y = j

                                                                if MinMaxScore_Flag == 1:

                                                                    MaxMinMaxScore = NewScore

                                                                    MaxMinMaxX = x

                                                                    MaxMinMaxY = y

 

                                                            if _Score >= MaxMinMaxScore and MinMaxScore_Flag == 0:

                                                                NewScore_Flag = 0

                                                                break

 

                                            if NewScore_Flag == 0:

                                                break

 

                                        if NewScore < MaxMinMaxScore and MinMaxScore_Flag == 0:

                                            MaxMinMaxScore = NewScore

                                            MaxMinMaxX = x

                                            MaxMinMaxY = y

 

                        if MaxMinMaxScore > TrueScore:

                            TrueScore = MaxMinMaxScore

                            TrueX = MaxMinMaxX

                            TrueY = MaxMinMaxY

 

                        if MaxMinMaxScore == TrueScore:

                            if random.randint(0,1):

                                TrueScore = MaxMinMaxScore

                                TrueX = MaxMinMaxX

                                TrueY = MaxMinMaxY

 

 

            self.Board[TrueX][TrueY] = 1

            print('Alrbot to........')

            self._Bool = 0

 

    def AlTraverse(self):

        # 人机遍历

        W_Score = B_Score = 10000

 

        MinX, MaxX, MinY, MaxY = self.AlUpDnLfRt(15, 0, 15, 0)

        for i in range(MinX, MaxX):

            for j in range(MinY, MaxY):

                if self.Board[i][j] != 255:

                    b_Up = _Right = b_Down = _Scp = 1

                    _UpF = _RiF = _DnF = _ScF = 0

                    N_Color = self.Board[i][j]

 

                    # 判断该点前点

                    _Uold = self.oldCompare(i + 1, i - 1, N_Color)

                    _Rold = self.oldCompare(i, j - 1, N_Color)

                    _Dold = self.oldCompare(i - 1, j - 1, N_Color)

                    _Sold = self.oldCompare(i - 1, j, N_Color)

 

                    # 进行遍历该点附近点

                    if _Uold != 0:

                        _UpF, b_Up = self.Al_Up_RangeDirct(i, j, N_Color, b_Up)

 

                    if _Rold != 0:

                        _RiF, _Right = self.Al_Rt_RangeDirct(i, j, N_Color, _Right)

 

                    if _Dold != 0:

                        _DnF, b_Down = self.Al_Dn_RangeDirct(i, j, N_Color, b_Down)

 

                    if _Sold != 0:

                        _ScF, _Scp = self.Al_Sp_RangeDirct(i, j, N_Color, _Scp)

 

                    New_Score = self.Now_Score(_Uold, b_Up, _UpF) + self.Now_Score(_Rold, _Right, _RiF) + self.Now_Score(_Dold, b_Down, _DnF) + self.Now_Score(_Sold, _Scp, _ScF)

                    if N_Color == 1:

                        B_Score += New_Score

                    else:

                        W_Score += New_Score

 

        return (B_Score - W_Score)

 

    def Al_Up_RangeDirct(self, x, y, n_color, now):

 

        for k in range(1, 5):

            if -1 != self._Scope(x - k, y + k):

                if self.Board[x - k][y + k] == n_color:

                    now += 1

 

                elif self.Board[x - k][y + k] == 255:

                    return 255, now

 

                else:

                    return 1, now

            else:

                return 2, now

        return 0, now

 

    def Al_Rt_RangeDirct(self, x, y, n_color, now):

 

        for k in range(1, 5):

            if -1 != self._Scope(x, y + k):

                if self.Board[x][y + k] == n_color:

                    now += 1

 

                elif self.Board[x][y + k] == 255:

                    return 255, now

 

                else:

                    return 1, now

            else:

                return 2, now

        return 0, now

 

    def Al_Dn_RangeDirct(self, x, y, n_color, now):

 

        for k in range(1, 5):

            if -1 != self._Scope(x + k, y + k):

                if self.Board[x + k][y + k] == n_color:

                    now += 1

 

                elif self.Board[x + k][y + k] == 255:

                    return 255, now

 

                else:

                    return 1, now

            else:

                return 2, now

        return 0, now

 

    def Al_Sp_RangeDirct(self, x, y, n_color, now):

 

        for k in range(1, 5):

            if -1 != self._Scope(x + k, y):

                if self.Board[x + k][y] == n_color:

                    now += 1

 

                elif self.Board[x + k][y] == 255:

                    return 255, now

 

                else:

                    return 1, now

            else:

                return 2, now

        return 0, now

 

    @staticmethod

    def Now_Score(O_lD, N_oW, N_wF):

 

        if N_oW < 5:

            if O_lD == 255:

                if N_wF == 255:

                    if N_oW == 1:

                        return 0

                    elif N_oW == 2:

                        return 100

                    elif N_oW == 3:

                        return 1000

                    else:

                        return 5000

                elif N_wF == 1 or N_wF == 2:

                    if N_oW == 1:

                        return 0

                    elif N_oW == 2:

                        return 20

                    elif N_oW == 3:

                        return 500

                    else:

                        return 1500

 

            elif O_lD == 1 or O_lD == 2:

                if N_wF == 255:

                    if N_oW == 1:

                        return 0

                    elif N_oW == 2:

                        return 20

                    elif N_oW == 3:

                        return 500

                    else:

                        return 1500

                else:

                    return 0

 

            else:

                return 0

        else:

            return 12345

 

    def AlUpDnLfRt(self, x1, x2, y1, y2):

 

        MinX = x1

        MaxX = x2

        MinY = y1

        MaxY = y2

 

        for i in range(x2, x1):

            for j in range(y2, y1):

                if self.Board[i][j] != 255:

                    if i > MaxX:

                        MaxX = i

                    if i < MinX:

                        MinX = i

                    if j > MaxY:

                        MaxY = j

                    if j < MinY:

                        MinY = j

 

        if MinX >= 2:

            MinX -= 2

        else:

            MinX = 0

        if MaxX <= 12:

            MaxX += 2

        else:

            MaxX = 15

        if MinY >= 2:

            MinY -= 2

        else:

            MinY = 0

        if MaxY <= 12:

            MaxY += 2

        else:

            MaxY = 15

 

        return MinX, MaxX, MinY, MaxY

 

    def Game_over(self, _up, _dowm, _right, _scp, _ncolor):

        if _up == 5 or _dowm == 5 or _right == 5 or _scp == 5:

            if _ncolor == 1:

                self._over = 1

            elif _ncolor == 0:

                self._over = 0

 

 

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = MyQWidget()

    ex.show()

    app.exec_()
