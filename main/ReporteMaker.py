import xlsxwriter
from Reporte1 import Reporte1


class ReporteMaker:
    def __init__(self, idReporte):
        self.idReporte = idReporte

    def switcherReporte(self):
        reportes = {
            1: self.reporte_1,
            2: self.reporte_2,
            3: self.reporte_3,
            4: self.reporte_4
        }

        func_reporte = reportes.get(self.idReporte, lambda: "Reporte Invalido")
        return func_reporte()
    
    

    def generarReporte(self):
        return self.switcherReporte()

    def reporte_1(self):
        reporte=Reporte1("01","2019")
        return reporte.generar()

    def reporte_2(self):
        return self.nombreReporte

    def reporte_3(self):
        return self.nombreReporte

    def reporte_4(self):
        return self.nombreReporte
