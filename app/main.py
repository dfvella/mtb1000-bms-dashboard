from app import QtWidgets, QtCore, uic

from .decoder import Decoder


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('ui/dashboard.ui', self)

        self.connectionLabel: QtWidgets.QLabel
        self.stateLabel: QtWidgets.QLabel
        self.cpuLabel: QtWidgets.QLabel
        self.faultLabel: QtWidgets.QLabel
        self.socLabel: QtWidgets.QLabel
        self.capacityLabel: QtWidgets.QLabel
        self.packVoltageLabel: QtWidgets.QLabel
        self.packCurrentLabel: QtWidgets.QLabel
        self.packPowerLabel: QtWidgets.QLabel
        self.avgCellLabel: QtWidgets.QLabel
        self.maxCellLabel: QtWidgets.QLabel
        self.minCellLabel: QtWidgets.QLabel
        self.thermistor1Label: QtWidgets.QLabel
        self.thermistor2Label: QtWidgets.QLabel
        self.thermistor3Label: QtWidgets.QLabel
        self.prechargeFetLabel: QtWidgets.QLabel
        self.dischargeFetLabel: QtWidgets.QLabel
        self.chargeFetLabel: QtWidgets.QLabel
        self.vc1: QtWidgets.QLCDNumber
        self.vc2: QtWidgets.QLCDNumber
        self.vc3: QtWidgets.QLCDNumber
        self.vc4: QtWidgets.QLCDNumber
        self.vc5: QtWidgets.QLCDNumber
        self.vc6: QtWidgets.QLCDNumber
        self.vc7: QtWidgets.QLCDNumber
        self.vc8: QtWidgets.QLCDNumber
        self.vc9: QtWidgets.QLCDNumber
        self.vc10: QtWidgets.QLCDNumber
        self.vc11: QtWidgets.QLCDNumber
        self.vc12: QtWidgets.QLCDNumber
        self.vc13: QtWidgets.QLCDNumber
        self.cb1: QtWidgets.QLabel
        self.cb2: QtWidgets.QLabel
        self.cb3: QtWidgets.QLabel
        self.cb4: QtWidgets.QLabel
        self.cb5: QtWidgets.QLabel
        self.cb6: QtWidgets.QLabel
        self.cb7: QtWidgets.QLabel
        self.cb8: QtWidgets.QLabel
        self.cb9: QtWidgets.QLabel
        self.cb10: QtWidgets.QLabel
        self.cb11: QtWidgets.QLabel
        self.cb12: QtWidgets.QLabel
        self.cb13: QtWidgets.QLabel

        self.cellVoltageLabels = [
            self.vc1,
            self.vc2,
            self.vc3,
            self.vc4,
            self.vc5,
            self.vc6,
            self.vc7,
            self.vc8,
            self.vc9,
            self.vc10,
            self.vc11,
            self.vc12,
            self.vc13,
        ]

        self.cellBalanceLabels = [
            self.cb1,
            self.cb2,
            self.cb3,
            self.cb4,
            self.cb5,
            self.cb6,
            self.cb7,
            self.cb8,
            self.cb9,
            self.cb10,
            self.cb11,
            self.cb12,
            self.cb13,
        ]

        self.decoder = Decoder()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_task)
        self.timer.start()

    def update_task(self):
        self.connectionLabel.setText(" Connected " if self.decoder.connected else " Disconnected ")
        self.stateLabel.setText(self.decoder.state.name)
        self.cpuLabel.setText(f" {self.decoder.cpu}% ")
        
        activeFaults = []
        if self.decoder.fault_oc: activeFaults.append("OC")
        if self.decoder.fault_sc: activeFaults.append("SC")
        if self.decoder.fault_uv: activeFaults.append("UV")
        if self.decoder.fault_ov: activeFaults.append("OV")
        if self.decoder.fault_ot: activeFaults.append("OT")
        if self.decoder.fault_bq: activeFaults.append("BQ")
        if self.decoder.fault_cm: activeFaults.append("CM")

        self.faultLabel.setText(f" {', '.join(activeFaults)} " if len(activeFaults) else " None ")
        self.socLabel.setText(f" {self.decoder.soc}% ")
        self.capacityLabel.setText(f" {(self.decoder.capacity / 3600000):.3f}Ah ")
        self.packVoltageLabel.setText(f" {(self.decoder.pack_voltage / 1000):.3f}V ")
        self.packCurrentLabel.setText(f" {(self.decoder.pack_current / 1000):.3f}A ")
        self.packPowerLabel.setText(f" {((self.decoder.pack_current * self.decoder.pack_voltage) / 1000000):.3f}W ")
        self.avgCellLabel.setText(f" {((sum(self.decoder.volt) / len(self.decoder.volt) / 1000)):.3f}V ")
        self.maxCellLabel.setText(f" {(max(self.decoder.volt) / 1000):.3f}V ")
        self.minCellLabel.setText(f" {(min(self.decoder.volt) / 1000):.3f}V ")
        self.thermistor1Label.setText(f" {self.decoder.temp[0]}C ")
        self.thermistor2Label.setText(f" {self.decoder.temp[1]}C ")
        self.thermistor3Label.setText(f" {self.decoder.temp[2]}C ")
        self.prechargeFetLabel.setText(" FET_ON " if self.decoder.precharge else " FET_OFF ")
        self.dischargeFetLabel.setText(" FET_ON " if self.decoder.discharge else " FET_OFF ")
        self.chargeFetLabel.setText(" FET_ON " if self.decoder.charge else " FET_OFF ")
        for i in range(13):
            if self.decoder.volt[i] % 10 == 0:
                self.decoder.volt[i] += 1
            self.cellVoltageLabels[i].display(self.decoder.volt[i] / 1000)
            self.cellBalanceLabels[i].setText(" FET_ON " if self.decoder.balance[i] else " FET_OFF ")
