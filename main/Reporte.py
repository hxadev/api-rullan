import xlsxwriter
import abc 
from db import Connection
from abc import ABC,abstractmethod
import logging as logger


class Reporte:
    def __init__(self, titulo, mes, anio):
        logger.info("Nuevo reporte")
        self.titulo = titulo
        self.mes = mes
        self.anio = anio
        self.nombreReporte = "{}.xlsx".format(titulo)
        self.workbook = xlsxwriter.Workbook(self.nombreReporte)
        self.worksheet = self.workbook.add_worksheet()
        self.db = Connection.getConnection()
        self.dbCursor = self.db.cursor()

    @abstractmethod
    def crearEncabezado(self):
        pass

    @abstractmethod
    def crearCuerpo(self):
        pass

    @abstractmethod
    def generar(self):
        pass
